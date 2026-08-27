// Aura App - Service Worker for Background Notifications & PWA
const CACHE_NAME = 'aura-cache-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

// Handle incoming notification message from main page
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
        const { title, body, icon, tag } = event.data;
        self.registration.showNotification(title, {
            body: body,
            icon: icon || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="28" fill="%230e0d11"/><text x="50%25" y="68%25" font-family="serif" font-weight="900" font-style="italic" font-size="56" fill="%23fbbf24" text-anchor="middle">R</text></svg>',
            badge: icon || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="28" fill="%230e0d11"/><text x="50%25" y="68%25" font-family="serif" font-weight="900" font-style="italic" font-size="56" fill="%23fbbf24" text-anchor="middle">R</text></svg>',
            tag: tag || 'aura-notification',
            renotify: true,
            vibrate: [200, 100, 200],
            data: { url: self.registration.scope }
        });
    }
});

// Handle notification click to focus or open the app
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
            for (const client of clientList) {
                if (client.url && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow('/');
            }
        })
    );
});
