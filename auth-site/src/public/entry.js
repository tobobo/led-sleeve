import { Router } from './router.js';
import { Config } from './pages/config.js';
import { Auth } from './pages/auth.js';
import { AuthCallback } from './pages/auth-callback.js';
import { FourOhFour } from './pages/404.js';

async function start() {
  const config = await (await (fetch('/config.json'))).json();
  const router = new Router(location, config, [
    (location) => location.pathname.match(/^\/authcb\/[^\/]+\/?$/) && AuthCallback,
    (location) => location.pathname.match(/^\/[^\/]+\/auth\/[^/]+\/?$/) && Auth,
    (location) => location.pathname.match(/^\/[^\/]+\/?$/) && Config,
    () => FourOhFour,
  ]);
}

start();
