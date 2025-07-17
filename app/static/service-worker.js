const CACHE_NAME = 'edgebot-mk2-cache-v1';
const urlsToCache = [
  '/',
  '/download',
  '/wiring-tutorial',
  '/pro-tips',
  '/docs',
  '/donate',
  '/control-station',
  '/static/style.css',
  '/static/logo/logo2.png',
  '/static/manifest.json',
  '/static/wiring_diagrams/psu.jpg',
  '/static/wiring_diagrams/motors.jpg',
  '/static/wiring_diagrams/esp32_diagram.jpg',
  '/static/wiring_diagrams/connecting_motors&power_supply_unit.jpg',
  '/static/wiring_diagrams/connecting_esp32_to_L298n.jpg',
  '/static/wiring_diagrams/chasis_example2.jpg',
  '/static/wiring_diagrams/chasis_example1.jpg',
  // Add more assets or pages as needed
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
}); 