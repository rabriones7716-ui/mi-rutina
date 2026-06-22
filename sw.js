/* Service worker · cachea la app para uso sin internet */
var CACHE = "mirutina-v3";
var ASSETS = ["./", "./index.html", "./Mi_Rutina.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./icon-512-maskable.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (ks) {
      return Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(function (r) {
      return r || fetch(e.request).then(function (resp) {
        var cp = resp.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, cp); });
        return resp;
      }).catch(function () { return caches.match("./Mi_Rutina.html"); });
    })
  );
});
