// Clarigital AI News helper: pure functions (no Cloudflare APIs), so they can
// be unit-tested with plain Node. See _build/AI-NEWS.md for the design.
//
// RULES (agreed with the owner, S132):
//  - AI news only. Headlines + short summaries + a link to the original. Never
//    copy articles.
//  - Every brief item must link to a page the AI actually found in its web
//    search during that run. Anything else is dropped (validateBrief).
//  - Companies without an official feed are labelled "Discussed on Hacker News",
//    never presented as the company's own announcement.

export const UA = 'ClarigitalNewsBot/1.0 (+https://www.clarigital.com/ai-news/)';

// Official feeds, each verified by hand on 22 Sep 2026 (S132).
export const OFFICIAL = [
  { id: 'openai', name: 'OpenAI', product: 'ChatGPT', feed: 'https://openai.com/news/rss.xml',
    home: 'https://openai.com/news/' },
  { id: 'google', name: 'Google', product: 'Gemini', feed: 'https://blog.google/rss/',
    home: 'https://blog.google/', filter: 'google' },
  { id: 'deepmind', name: 'Google DeepMind', product: 'Gemini models', feed: 'https://deepmind.google/blog/feed/basic/',
    home: 'https://deepmind.google/blog/' },
  { id: 'microsoft', name: 'Microsoft', product: 'Copilot', feed: 'https://news.microsoft.com/source/feed/',
    home: 'https://news.microsoft.com/source/topics/ai/', filter: 'microsoft' },
  { id: 'nvidia', name: 'NVIDIA', product: 'AI chips', feed: 'https://nvidianews.nvidia.com/releases.xml',
    home: 'https://nvidianews.nvidia.com/' },
  { id: 'huggingface', name: 'Hugging Face', product: 'Open models', feed: 'https://huggingface.co/blog/feed.xml',
    home: 'https://huggingface.co/blog' },
];

// No official feed published (checked S132). Shown as discussion, clearly labelled.
export const DISCUSSED = [
  { id: 'anthropic', name: 'Anthropic', product: 'Claude', queries: ['Anthropic', 'Claude AI'], home: 'https://www.anthropic.com/news' },
  { id: 'meta', name: 'Meta AI', product: 'Llama', queries: ['Meta AI', 'Llama'], home: 'https://ai.meta.com/blog/' },
  { id: 'xai', name: 'xAI', product: 'Grok', queries: ['xAI', 'Grok'], home: 'https://x.ai/news' },
  { id: 'mistral', name: 'Mistral', product: 'Le Chat', queries: ['Mistral AI', 'Mistral'], home: 'https://mistral.ai/news/' },
  { id: 'deepseek', name: 'DeepSeek', product: 'DeepSeek models', queries: ['DeepSeek'], home: 'https://www.deepseek.com' },
];

export const PRESS = [
  { id: 'techcrunch', name: 'TechCrunch', feed: 'https://techcrunch.com/category/artificial-intelligence/feed/' },
];

const AI_WORDS = /\b(AI|A\.I\.|artificial intelligence|LLMs?|GPT[-\w.]*|ChatGPT|OpenAI|Anthropic|Claude|Gemini|DeepMind|Copilot|Llama|Mistral|DeepSeek|Grok|xAI|Nvidia|GPUs?|TPUs?|machine learning|neural|chatbots?|agents?|agentic|inference|Hugging ?Face|transformer|diffusion|frontier model)\b/i;

export function isAI(text) { return AI_WORDS.test(text || ''); }

// ---- tiny XML helpers (Workers have no DOMParser) ------------------------
const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };
export function decode(s) {
  if (!s) return '';
  s = s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
  s = s.replace(/<[^>]+>/g, ' ');
  s = s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === '#') {
      const n = e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(n) ? String.fromCodePoint(n) : m;
    }
    return ENT[e.toLowerCase()] ?? m;
  });
  return s.replace(/\s+/g, ' ').trim();
}

function tag(block, name) {
  const m = block.match(new RegExp('<' + name + '(?:\\s[^>]*)?>([\\s\\S]*?)</' + name + '>', 'i'));
  return m ? m[1] : '';
}

export function parseFeed(xml) {
  const out = [];
  if (!xml || typeof xml !== 'string') return out;
  const blocks = xml.match(/<item\b[\s\S]*?<\/item>/gi) || xml.match(/<entry\b[\s\S]*?<\/entry>/gi) || [];
  for (const b of blocks) {
    const title = decode(tag(b, 'title'));
    let link = decode(tag(b, 'link'));
    if (!/^https?:\/\//.test(link)) {
      const alt = b.match(/<link\b[^>]*rel=["']alternate["'][^>]*href=["']([^"']+)["']/i)
               || b.match(/<link\b[^>]*href=["']([^"']+)["']/i);
      link = alt ? alt[1].replace(/&amp;/g, '&') : '';
    }
    const dateRaw = decode(tag(b, 'pubDate') || tag(b, 'published') || tag(b, 'updated') || tag(b, 'dc:date'));
    const t = Date.parse(dateRaw);
    const cats = [...b.matchAll(/<category\b[^>]*?(?:term=["']([^"']+)["'])?[^>]*?(?:\/>|>([\s\S]*?)<\/category>)/gi)]
      .map(m => decode(m[1] || m[2] || '')).filter(Boolean);
    if (!title || !/^https?:\/\//.test(link)) continue;
    out.push({ title, url: link, ts: Number.isFinite(t) ? t : null, cats });
  }
  return out;
}

export function applyFilter(kind, items) {
  if (kind === 'google') {
    return items.filter(i => /innovation-and-ai|\/ai\/|deepmind|gemini/i.test(i.url) || isAI(i.title));
  }
  if (kind === 'microsoft') {
    return items.filter(i => i.cats.some(c => /^AI$/i.test(c)) || isAI(i.title));
  }
  return items;
}

export function hnStories(json, { minPoints = 0, aiOnly = false } = {}) {
  const hits = (json && Array.isArray(json.hits)) ? json.hits : [];
  const out = [];
  for (const h of hits) {
    const title = decode(h.title || h.story_title || '');
    if (!title) continue;
    if (aiOnly && !isAI(title)) continue;
    if ((h.points || 0) < minPoints) continue;
    const discuss = 'https://news.ycombinator.com/item?id=' + encodeURIComponent(h.objectID);
    const url = /^https?:\/\//.test(h.url || '') ? h.url : discuss;
    out.push({ title, url, discuss, points: h.points || 0, comments: h.num_comments || 0,
      ts: h.created_at_i ? h.created_at_i * 1000 : null, source: hostOf(url) });
  }
  return out;
}

export function hostOf(u) {
  try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return ''; }
}

export function dedupe(items) {
  const seen = new Set(); const out = [];
  for (const i of items) {
    const k = normUrl(i.url) || i.title.toLowerCase();
    if (seen.has(k)) continue; seen.add(k); out.push(i);
  }
  return out;
}

// ---- time ----------------------------------------------------------------
export function ist(now = Date.now()) {
  const d = new Date(now + 5.5 * 3600e3);
  return { date: d.toISOString().slice(0, 10), hour: d.getUTCHours() };
}

// ---- URL normalisation (for the "must come from the search" rule) ---------
export function normUrl(u) {
  try {
    const x = new URL(u);
    if (!/^https?:$/.test(x.protocol)) return '';
    x.hash = '';
    for (const p of [...x.searchParams.keys()]) if (/^utm_|^ref$|^fbclid$|^gclid$/i.test(p)) x.searchParams.delete(p);
    let s = x.hostname.replace(/^www\./, '') + x.pathname.replace(/\/+$/, '') + (x.search || '');
    return s.toLowerCase();
  } catch { return ''; }
}

// ---- the brief -------------------------------------------------------------
export function briefPrompt(dateIST) {
  return `Today is ${dateIST} (India Standard Time). You are writing the daily AI news brief for Clarigital, a website whose promise is that every fact is verifiable.

Use web search to find the most important AI news from roughly the last 36 hours.
SCOPE: artificial intelligence only - AI models and products, AI companies, AI chips and computing, AI policy and regulation, AI research, AI funding and deals. Nothing else (no general tech, science, markets or politics unless the story is about AI).
PRIORITY: major breaking developments over minor updates or opinion.

Return exactly this JSON and nothing else:
{
  "usa":   [ITEM, ITEM],                      // exactly 2 of the biggest AI stories in the United States
  "india": [ITEM, ITEM, ITEM],                // exactly 3 AI stories about India
  "world": [ITEM + "country":"ISO 3166 alpha-2 code"],  // 4 to 8 AI stories from other countries, one per country
  "continents": [{"region": "...", "line": "..."}]      // one line each for North America, South America, Europe, Asia, Africa, Oceania
}
ITEM = {"headline": "...", "summary": "...", "why": "...", "published": "YYYY-MM-DD", "source": {"name": "publisher name", "url": "https://..."}, "more": [{"name": "...", "url": "https://..."}]}

WRITING RULES
- Plain English a 16-year-old understands. No hype, no jargon; explain any technical term in a few words.
- headline: up to 12 words. summary: up to 35 words, facts only. why: up to 30 words, why it matters.
- Never invent or guess. Numbers, names and dates must appear in the linked source.
- source.url MUST be a page you opened or saw in your web search results in this conversation. Prefer the company's or government's own page, then major news organisations (Reuters, AP, Bloomberg, Financial Times, The Economic Times, The Hindu, Mint, TechCrunch and similar). No blogs, forums, aggregators or social media.
- "more" is optional: up to 2 extra confirming sources, same rule.
- If you cannot find enough real stories for a slot, return fewer items rather than padding.
- continents: if nothing significant happened in a region, say "No major AI development today." Do not pad with old trends.
Output the JSON only, no commentary, no markdown fences.`;
}

export function extractSearchUrls(content) {
  const set = new Set();
  for (const b of content || []) {
    if (b && b.type === 'web_search_tool_result' && Array.isArray(b.content)) {
      for (const r of b.content) if (r && r.url) set.add(normUrl(r.url));
    }
    if (b && b.type === 'text' && Array.isArray(b.citations)) {
      for (const c of b.citations) if (c && c.url) set.add(normUrl(c.url));
    }
  }
  set.delete('');
  return set;
}

export function extractJson(content) {
  const text = (content || []).filter(b => b && b.type === 'text').map(b => b.text).join('');
  const a = text.indexOf('{'), z = text.lastIndexOf('}');
  if (a < 0 || z <= a) throw new Error('no JSON in model output');
  return JSON.parse(text.slice(a, z + 1));
}

const clip = (s, n) => { s = decode(String(s || '')); return s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s; };

function cleanSource(s, allowed) {
  if (!s || typeof s.url !== 'string') return null;
  const n = normUrl(s.url);
  if (!n || !allowed.has(n)) return null;
  return { name: clip(s.name || hostOf(s.url), 60), url: s.url };
}

export function validateBrief(raw, allowed, { now = Date.now(), maxAgeDays = 4 } = {}) {
  const dropped = [];
  const item = (it, extra = {}) => {
    if (!it || typeof it !== 'object') return null;
    const src = cleanSource(it.source, allowed);
    if (!src) { dropped.push({ headline: clip(it.headline, 80), reason: 'source not found in this run\'s search results' }); return null; }
    const pub = Date.parse(it.published || '');
    if (Number.isFinite(pub) && now - pub > maxAgeDays * 86400e3) { dropped.push({ headline: clip(it.headline, 80), reason: 'older than ' + maxAgeDays + ' days' }); return null; }
    const text = [it.headline, it.summary, it.why].join(' ');
    if (!isAI(text)) { dropped.push({ headline: clip(it.headline, 80), reason: 'not about AI' }); return null; }
    const more = (Array.isArray(it.more) ? it.more : []).map(m => cleanSource(m, allowed)).filter(Boolean).slice(0, 2);
    return { headline: clip(it.headline, 110), summary: clip(it.summary, 260), why: clip(it.why, 220),
      published: Number.isFinite(pub) ? new Date(pub).toISOString().slice(0, 10) : null, source: src, more, ...extra };
  };
  const list = (arr, max, fn) => (Array.isArray(arr) ? arr : []).map(fn).filter(Boolean).slice(0, max);
  const usa = list(raw.usa, 2, x => item(x));
  const india = list(raw.india, 3, x => item(x));
  const seenC = new Set();
  const world = list(raw.world, 8, x => {
    const cc = String(x && x.country || '').toUpperCase();
    if (!/^[A-Z]{2}$/.test(cc) || cc === 'US' || cc === 'IN' || seenC.has(cc)) {
      dropped.push({ headline: clip(x && x.headline, 80), reason: 'country missing, repeated, or US/India (covered above)' });
      return null;
    }
    const r = item(x, { country: cc }); if (r) seenC.add(cc); return r;
  });
  const REG = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania'];
  const continents = REG.map(region => {
    const c = (Array.isArray(raw.continents) ? raw.continents : []).find(x => x && String(x.region || '').toLowerCase().startsWith(region.toLowerCase().split(' ')[0]));
    return c && c.line ? { region, line: clip(c.line, 200) } : null;
  }).filter(Boolean);
  return { usa, india, world, continents, dropped };
}

// ---- tag stories with Clarigital pages -----------------------------------
export function tagItems(brief, tags) {
  if (!Array.isArray(tags)) return brief;
  const rx = tags.map(t => ({ ...t, re: t.k.map(k => new RegExp('(^|[^\\w])' + k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '($|[^\\w])', (t.cs || k.length <= 4) ? '' : 'i')) }));
  const tagOne = it => {
    const text = it.headline + ' ' + it.summary + ' ' + it.why;
    const hits = [];
    for (const t of rx) {
      if (hits.length >= 2) break;
      if (t.re.some(r => r.test(text)) && !hits.some(h => h.u === t.u)) hits.push({ u: t.u, t: t.t });
    }
    return { ...it, pages: hits };
  };
  for (const k of ['usa', 'india', 'world']) brief[k] = (brief[k] || []).map(tagOne);
  return brief;
}
