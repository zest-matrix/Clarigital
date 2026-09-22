// Clarigital Worker. Serves the static site exactly as before; adds three
// small endpoints for the AI News page (/ai-news/):
//   GET /api/feeds       live company + trending headlines (nothing stored; 10-min edge cache)
//   GET /api/brief       today's AI brief (written once a day at 06:00 IST)
//   GET /api/brief/run?token=...   manual re-run, only if BRIEF_RUN_TOKEN is set
// Static files are served first by Cloudflare, so this code only runs for
// paths that are not files. Every other path falls straight through to ASSETS.
import { DurableObject } from 'cloudflare:workers';
import {
  UA, OFFICIAL, DISCUSSED, PRESS, parseFeed, applyFilter, hnStories, dedupe, ist,
  briefPrompt, extractSearchUrls, extractJson, validateBrief, tagItems,
} from './lib.js';

const SEC = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Strict-Transport-Security': 'max-age=86400; includeSubDomains',
  'X-Frame-Options': 'SAMEORIGIN',
};
const json = (obj, status = 200, maxAge = 300) => new Response(JSON.stringify(obj), {
  status,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': `public, max-age=${maxAge}`, ...SEC },
});

async function getText(url, ms = 8000) {
  const r = await fetch(url, { headers: { 'User-Agent': UA, Accept: 'application/rss+xml, application/atom+xml, application/xml, text/xml, application/json, */*' },
    signal: AbortSignal.timeout(ms), cf: { cacheTtl: 300 } });
  if (!r.ok) throw new Error(url + ' -> HTTP ' + r.status);
  return r.text();
}

const WEEK = 7 * 86400e3;

async function buildFeeds() {
  const now = Date.now();
  const since = Math.floor((now - WEEK) / 1000);
  const official = OFFICIAL.map(async c => {
    const items = applyFilter(c.filter, parseFeed(await getText(c.feed)))
      .filter(i => !i.ts || now - i.ts < 30 * 86400e3)
      .sort((a, b) => (b.ts || 0) - (a.ts || 0)).slice(0, 4)
      .map(i => ({ title: i.title, url: i.url, ts: i.ts, source: c.name }));
    return { id: c.id, name: c.name, product: c.product, kind: 'official', home: c.home, items };
  });
  const discussed = DISCUSSED.map(async c => {
    const all = [];
    for (const q of c.queries) {
      const u = 'https://hn.algolia.com/api/v1/search?tags=story&restrictSearchableAttributes=title&hitsPerPage=10'
        + '&query=' + encodeURIComponent(q) + '&numericFilters=' + encodeURIComponent('created_at_i>' + since + ',points>15');
      all.push(...hnStories(JSON.parse(await getText(u))));
    }
    const items = dedupe(all).sort((a, b) => b.points - a.points).slice(0, 4);
    return { id: c.id, name: c.name, product: c.product, kind: 'discussed', home: c.home, items };
  });
  const hn = (async () => {
    const u = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=80';
    return hnStories(JSON.parse(await getText(u)), { aiOnly: true }).sort((a, b) => b.points - a.points).slice(0, 10);
  })();
  const press = PRESS.map(async p => parseFeed(await getText(p.feed)).slice(0, 8)
    .map(i => ({ title: i.title, url: i.url, ts: i.ts, source: p.name })));

  const settle = async ps => (await Promise.allSettled(ps)).map(r => r.status === 'fulfilled' ? r.value : null);
  const [o, d, h, pr] = await Promise.all([settle(official), settle(discussed), settle([hn]), settle(press)]);
  const fallback = (list, src) => list.map((v, i) => v || { id: src[i].id, name: src[i].name, product: src[i].product,
    kind: src === OFFICIAL ? 'official' : 'discussed', home: src[i].home, items: [], error: true });
  return {
    updated: new Date(now).toISOString(),
    companies: [...fallback(o, OFFICIAL), ...fallback(d, DISCUSSED)],
    trending: { hn: h[0] || [], press: pr.flat().filter(Boolean) },
  };
}

async function feeds(ctx) {
  const cache = caches.default;
  const key = new Request('https://www.clarigital.com/__cache/api-feeds-v1');
  const hit = await cache.match(key);
  if (hit) return hit;
  const res = json(await buildFeeds(), 200, 600);
  ctx.waitUntil(cache.put(key, res.clone()));
  return res;
}

// ---- the daily brief ---------------------------------------------------------
async function callClaude(env, messages) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({
      model: env.BRIEF_MODEL || 'claude-sonnet-5',
      max_tokens: 8000,
      tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: Number(env.BRIEF_MAX_SEARCHES || 15) }],
      messages,
    }),
    signal: AbortSignal.timeout(600000),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error('Claude API ' + r.status + ': ' + (body.error && body.error.message || '').slice(0, 200));
  return body;
}

export async function generateBrief(env, now = Date.now()) {
  if (!env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY is not set');
  const { date } = ist(now);
  const messages = [{ role: 'user', content: briefPrompt(date) }];
  const content = [];
  for (let turn = 0; turn < 4; turn++) {           // web search can pause a long turn; resume it
    const res = await callClaude(env, messages);
    content.push(...(res.content || []));
    if (res.stop_reason !== 'pause_turn') break;
    messages.push({ role: 'assistant', content: res.content });
  }
  const allowed = extractSearchUrls(content);
  const raw = extractJson(content);
  const v = validateBrief(raw, allowed, { now });
  let tags = null;
  try { tags = await (await env.ASSETS.fetch(new Request('https://www.clarigital.com/ai-news/tags.json'))).json(); } catch {}
  const brief = tagItems({ date, generated: new Date(now).toISOString(), model: env.BRIEF_MODEL || 'claude-sonnet-5',
    usa: v.usa, india: v.india, world: v.world, continents: v.continents }, tags);
  brief.checks = { searchResults: allowed.size, dropped: v.dropped };
  if (brief.usa.length + brief.india.length < 2) throw new Error('too few verified stories (' + (brief.usa.length + brief.india.length) + '); kept previous brief');
  return brief;
}

// One object, one place: holds the latest brief and the run state. Nothing about visitors is stored.
export class BriefStore extends DurableObject {
  async getBrief() { return (await this.ctx.storage.get('brief')) || null; }
  async getState() { return (await this.ctx.storage.get('state')) || {}; }

  async requestRun(reason, force = false) {
    const st = await this.getState();
    const now = Date.now();
    const today = ist(now).date;
    if (st.running && now - (st.runningSince || 0) < 20 * 60e3) return { queued: false, why: 'already running' };
    const count = st.day === today ? (st.count || 0) : 0;
    if (count >= (force ? 6 : 3)) return { queued: false, why: 'daily limit reached' };
    if (!force && st.lastAttempt && now - st.lastAttempt < 30 * 60e3) return { queued: false, why: 'tried recently' };
    await this.ctx.storage.put('state', { ...st, queued: reason, queuedAt: now });
    await this.ctx.storage.setAlarm(now + 500);
    return { queued: true };
  }

  async alarm() {
    const now = Date.now();
    const today = ist(now).date;
    let st = await this.getState();
    st = { ...st, running: true, runningSince: now, lastAttempt: now, day: today, count: (st.day === today ? (st.count || 0) : 0) + 1 };
    await this.ctx.storage.put('state', st);
    try {
      const brief = await generateBrief(this.env, now);
      await this.ctx.storage.put('brief', brief);
      st.lastError = null; st.lastSuccess = now;
    } catch (e) {
      st.lastError = String(e && e.message || e).slice(0, 300);
    } finally {
      st.running = false;
      await this.ctx.storage.put('state', st);
    }
  }
}

const store = env => env.BRIEF_STORE.get(env.BRIEF_STORE.idFromName('main'));

async function brief(env, url) {
  const s = store(env);
  const [b, st] = await Promise.all([s.getBrief(), s.getState()]);
  const { date, hour } = ist();
  const stale = !b || (b.date !== date && hour >= 6);
  let pending = !!st.running;
  if (stale && env.ANTHROPIC_API_KEY && !st.running) {
    const q = await s.requestRun('visit');
    pending = q.queued || pending;
  }
  const out = { brief: b, today: date, pending, configured: !!env.ANTHROPIC_API_KEY };
  if (env.BRIEF_RUN_TOKEN && url.searchParams.get('token') === env.BRIEF_RUN_TOKEN) out.state = st;
  return json(out, 200, pending || !b ? 30 : 300);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    try {
      if (url.pathname === '/api/feeds') return await feeds(ctx);
      if (url.pathname === '/api/brief') return await brief(env, url);
      if (url.pathname === '/api/brief/run') {
        if (!env.BRIEF_RUN_TOKEN || url.searchParams.get('token') !== env.BRIEF_RUN_TOKEN) return json({ error: 'not found' }, 404, 0);
        return json(await store(env).requestRun('manual', true), 200, 0);
      }
    } catch (e) {
      return json({ error: 'temporarily unavailable' }, 503, 30);
    }
    return env.ASSETS.fetch(request);
  },
  async scheduled(event, env, ctx) {
    ctx.waitUntil(store(env).requestRun('cron', true));
  },
};
