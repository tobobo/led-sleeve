import { Router } from './router.js';
import { Accounts } from './pages/accounts/accounts.js';

async function start() {
  const config = await (await (fetch('/config.json'))).json();
  new Router(location, config, document.getElementById('app'), [
    (location) => location.pathname.match(/^\/?$/) && Accounts,
  ]);
}

start();
