(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  }

  var input = document.getElementById('q');
  if (!input) return;

  var statusEl = document.getElementById('search-status');
  var resultsEl = document.getElementById('search-results');
  var index = [];

  fetch('search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; })
    .catch(function () { if (statusEl) statusEl.textContent = 'search index unavailable'; });

  function score(item, terms) {
    var hay = (item.title + ' ' + item.tags.join(' ') + ' ' + item.summary + ' ' + item.category).toLowerCase();
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      if (item.title.toLowerCase().indexOf(terms[i]) !== -1) s += 3;
      if (hay.indexOf(terms[i]) !== -1) s += 1; else return 0;
    }
    return s;
  }

  function render(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { resultsEl.innerHTML = ''; statusEl.textContent = 'type to search ' + index.length + ' posts'; return; }
    var hits = index.map(function (it) { return { it: it, s: score(it, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; });
    statusEl.textContent = hits.length + ' match' + (hits.length === 1 ? '' : 'es');
    resultsEl.innerHTML = hits.map(function (x) {
      var it = x.it;
      var chips = it.tags.map(function (t) { return '<span class="chip">' + t + '</span>'; }).join('');
      return '<article class="card"><div class="pmeta"><span class="ts">' + it.date + '</span>' +
        (it.category ? '<span class="cat">' + it.category + '</span>' : '') + '</div>' +
        '<h2 class="card-title"><a href="' + it.url + '">' + it.title + '</a></h2>' +
        '<p class="sum">' + it.summary + '</p><div class="chips">' + chips + '</div></article>';
    }).join('');
  }

  input.addEventListener('input', function () { render(input.value); });
})();
