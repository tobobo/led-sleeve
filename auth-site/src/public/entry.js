import { Router } from './router.js';
import { Config } from './pages/config.js';
import { Auth } from './pages/auth.js';
import { AuthCallback } from './pages/auth-callback.js';
import { FourOhFour } from './pages/404.js';

async function start() {
  const config = await (await (fetch('/config.json'))).json();
  new Router(location, config, null, [
    (location) => location.pathname.match(/^\/[^\/]+\/?$/) && Config,
    (location) => location.pathname.match(/^\/authcb\/[^\/]+\/?$/) && AuthCallback,
    (location) => location.pathname.match(/^\/[^\/]+\/auth\/[^/]+\/?$/) && Auth,
    () => FourOhFour,
  ]);
}

start();
