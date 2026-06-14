(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  }

  // Highlight the current section in the terminal nav.
  (function () {
    var here = location.pathname.replace(/\/index\.html$/, '/');
    var links = document.querySelectorAll('nav.term a');
    for (var i = 0; i < links.length; i++) {
      var lp = links[i].pathname.replace(/\/index\.html$/, '/');
      if (lp === here ||
        (lp === '/categories.html' && here.indexOf('/category/') === 0) ||
        (lp === '/tags.html' && here.indexOf('/tag/') === 0)) {
        links[i].setAttribute('aria-current', 'page');
      }
    }
  })();

  // Add a copy button to each code block.
  (function () {
    if (!navigator.clipboard) return;
    var blocks = document.querySelectorAll('.post-content div.highlight');
    for (var i = 0; i < blocks.length; i++) {
      (function (block) {
        var pre = block.querySelector('pre');
        if (!pre) return;
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'copy-btn';
        btn.textContent = 'copy';
        btn.setAttribute('aria-label', 'Copy code to clipboard');
        btn.addEventListener('click', function () {
          navigator.clipboard.writeText(pre.innerText).then(function () {
            btn.textContent = 'copied';
            btn.classList.add('copied');
            setTimeout(function () {
              btn.textContent = 'copy';
              btn.classList.remove('copied');
            }, 1400);
          });
        });
        var tools = document.createElement('div');
        tools.className = 'code-tools';
        var lang = block.getAttribute('data-lang');
        if (lang) {
          var label = document.createElement('span');
          label.className = 'code-lang';
          label.textContent = lang;
          tools.appendChild(label);
        }
        tools.appendChild(btn);
        block.appendChild(tools);
      })(blocks[i]);
    }
  })();

  // Client-side search (search page only).
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
