async function renderAccounts() {
  const accounts = await (await fetch('/api/accounts')).json();
  const account = accounts[0];
  if (!account) return;
  const state = accounts[0].now_playing_state?.[0] ? `<img src="${accounts[0].now_playing_state?.[0]}">` : '<p>nothin\'</p>';
  document.getElementById('app').innerHTML = `${state}<p>${account.provider}</p>`;
}

async function checkAuthCredentials() {
  const query = new URLSearchParams(window.location.search);
  debugger;
  const provider = query.get('authcb');
  if (!provider) return;
  if (provider === 'spotify') {
    await fetch('/api/accounts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        provider: 'spotify',
        code: query.get('code'),
      }),
    });
    renderAccounts();
  }
}

async function start() {
  renderAccounts();
  checkAuthCredentials();
}

start();
