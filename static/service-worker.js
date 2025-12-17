const CACHE_NAME = 'movie-watchlist-v1';

const urlsToCache = [

  '/',

  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',

  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',

  '/static/images/icon-192x192.png',

  '/static/images/icon-512x512.png'

];



self.addEventListener('install', (event) => {

  event.waitUntil(

    caches.open(CACHE_NAME)

      .then((cache) => cache.addAll(urlsToCache))

  );

});



self.addEventListener('fetch', (event) => {

  event.respondWith(

    caches.match(event.request)

      .then((response) => {

        if (response) {

          return response;

        }

        return fetch(event.request);

      })

  );

});