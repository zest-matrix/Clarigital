// CLARIGITAL — Search
(function() {
  var INDEX = null;

  function loadIndex(cb) {
    if (INDEX) { cb(); return; }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/search-index.json');
    xhr.onload = function() {
      try { INDEX = JSON.parse(xhr.responseText); } catch(e) { INDEX = []; }
      cb();
    };
    xhr.onerror = function() { INDEX = []; cb(); };
    xhr.send();
  }

  function score(guide, query) {
    var words = query.toLowerCase().split(/\s+/).filter(Boolean);
    var title = guide.t.toLowerCase();
    var desc = guide.d.toLowerCase();
    var cat = guide.c.toLowerCase();
    var s = 0;
    words.forEach(function(w) {
      if (title.indexOf(w) === 0) s += 40;
      else if (title.indexOf(' ' + w) !== -1) s += 30;
      else if (title.indexOf(w) !== -1) s += 20;
      if (desc.indexOf(w) !== -1) s += 8;
      if (cat.indexOf(w) !== -1) s += 5;
    });
    return s;
  }

  function search(query) {
    if (!query || query.length < 2) return [];
    return INDEX.map(function(g) {
      return { guide: g, score: score(g, query) };
    }).filter(function(r) { return r.score > 0; })
      .sort(function(a, b) { return b.score - a.score; })
      .slice(0, 8)
      .map(function(r) { return r.guide; });
  }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function renderResults(results, query, container) {
    if (!query || query.length < 2) {
      container.innerHTML = '';
      container.style.display = 'none';
      return;
    }
    if (results.length === 0) {
      container.innerHTML = '<div style="padding:14px 16px;font-size:.85rem;color:rgba(241,245,249,.5)">No results for &ldquo;' + escHtml(query) + '&rdquo;</div>';
      container.style.display = 'block';
      return;
    }
    var html = results.map(function(g) {
      var badge = g.s === 'atlas'
        ? '<span style="font-size:.65rem;font-weight:700;text-transform:uppercase;padding:2px 7px;border-radius:100px;background:rgba(99,102,241,.15);color:#818CF8;margin-left:6px">' + escHtml(g.c) + '</span>'
        : '<span style="font-size:.65rem;font-weight:700;text-transform:uppercase;padding:2px 7px;border-radius:100px;background:rgba(96,165,250,.1);color:#60A5FA;margin-left:6px">' + escHtml(g.c) + '</span>';
      return '<a href="' + escHtml(g.u) + '" class="search-result-item">'
        + '<div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;margin-bottom:3px">'
        + '<span style="font-size:.88rem;font-weight:600;color:#F1F5F9">' + escHtml(g.t) + '</span>'
        + badge + '</div>'
        + (g.d ? '<div style="font-size:.77rem;color:rgba(241,245,249,.5);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">' + escHtml(g.d) + '</div>' : '')
        + '</a>';
    }).join('');
    container.innerHTML = html;
    container.style.display = 'block';
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Wire nav search inputs
    document.querySelectorAll('[data-search-input]').forEach(function(input) {
      var resultsEl = document.querySelector('[data-search-results]');
      if (!resultsEl) return;
      var debounce;
      input.addEventListener('input', function() {
        clearTimeout(debounce);
        var q = input.value.trim();
        debounce = setTimeout(function() {
          loadIndex(function() { renderResults(search(q), q, resultsEl); });
        }, 160);
      });
      input.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') { input.value = ''; resultsEl.style.display = 'none'; }
        if (e.key === 'Enter') { var first = resultsEl.querySelector('a'); if (first) window.location.href = first.href; }
      });
      document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !resultsEl.contains(e.target)) resultsEl.style.display = 'none';
      });
    });

    // Keyboard shortcut: / or Ctrl+K / Cmd+K
    document.addEventListener('keydown', function(e) {
      if ((e.key === '/' || (e.ctrlKey && e.key === 'k') || (e.metaKey && e.key === 'k'))
          && document.activeElement.tagName !== 'INPUT'
          && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        var inp = document.querySelector('[data-search-input]');
        if (inp) inp.focus();
      }
    });
  });

  // Expose for hero search
  window._cgSearch = search;
  window._cgLoadIndex = loadIndex;

})();
