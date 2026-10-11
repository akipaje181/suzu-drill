/* すずドリル service worker — offline cache */
const VERSION = 'suzu-drill-v41';
const CORE = ['./', './index.html', './manifest.webmanifest',
  './icon-192.png', './icon-512.png', './icon-180.png', './icon-maskable-512.png',
  './img/splash.webp', './img/room-bg.webp', './img/cheer-frame.webp',
  './img/win-morning.webp', './img/win-day.webp', './img/win-evening.webp', './img/win-night.webp',
  './img/omi-clover.webp', './img/omi-star.webp', './img/omi-rainbow.webp',
  './img/omi-hanamaru.webp', './img/omi-music.webp', './img/omi-cake.webp',
  './img/suzu-stand.webp', './img/suzu-cheer.webp', './img/suzu-write.webp',
  './img/suzu-think.webp', './img/suzu-rest.webp', './img/suzu-morning.webp',
  './img/suzu-medal.webp', './img/suzu-sleep.webp', './img/suzu-face.webp',
  './img/medal-first.webp', './img/medal-perfect1.webp', './img/medal-streak3.webp', './img/medal-streak7.webp',
  './img/medal-streak30.webp', './img/medal-card1.webp', './img/medal-card2.webp', './img/medal-card3.webp',
  './img/medal-s10.webp', './img/medal-s50.webp', './img/medal-s100.webp', './img/medal-goal7.webp',
  './img/medal-week1.webp'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const isFont = (url) => url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com' || url.hostname === 'cdn.jsdelivr.net';

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // The page itself: newest version when online, cached copy when not.
  if (req.mode === 'navigate' || url.pathname.endsWith('/index.html')) {
    e.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(VERSION).then((c) => c.put('./index.html', copy));
        return res;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Fonts and same-origin assets: cache first, fill the cache from the network.
  if (isFont(url) || url.origin === self.location.origin) {
    e.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); }
        return res;
      }))
    );
  }
});
