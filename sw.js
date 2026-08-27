// Aura App - Service Worker for Background Notifications & PWA
const CACHE_NAME = 'aura-cache-v4';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    return caches.delete(key);
                }
            }));
        }).then(() => clients.claim())
    );
});

// Handle incoming notification message from main page
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
        const { title, body, icon, tag } = event.data;
        const iconUrl = icon || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="28" fill="%230e0d11"/><text x="50%25" y="68%25" font-family="serif" font-weight="900" font-style="italic" font-size="56" fill="%23fbbf24" text-anchor="middle">R</text></svg>';
        
        self.registration.showNotification(title, {
            body: body,
            icon: iconUrl,
            badge: iconUrl,
            tag: tag || 'aura-msg-' + Date.now(),
            renotify: true,
            vibrate: [200, 100, 200],
            data: { url: self.registration.scope },
            actions: [
                { action: 'reply', title: 'Responder', type: 'text', placeholder: 'Escribe tu respuesta...' },
                { action: 'open_chat', title: 'Abrir Chat' }
            ]
        });
    }
});

// Handle notification click and interactive quick replies
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    // 1. If user replied directly from the notification (Android inline reply)
    if (event.action === 'reply' && event.reply) {
        const replyText = event.reply;
        event.waitUntil(
            clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
                for (const client of clientList) {
                    client.postMessage({ type: 'NOTIFICATION_REPLY', text: replyText });
                    if ('focus' in client) return client.focus();
                }
                if (clients.openWindow) {
                    return clients.openWindow('/?reply=' + encodeURIComponent(replyText));
                }
            })
        );
        return;
    }

    // 2. Default click: focus window and switch to chat tab
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
            for (const client of clientList) {
                client.postMessage({ type: 'SWITCH_TAB', tab: 'chat' });
                if ('focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow('/?tab=chat');
            }
        })
    );
});
