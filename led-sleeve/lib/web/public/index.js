async function start() {
  const accounts = await (await fetch('/api/accounts')).json();
  const account = accounts[0];
  const state = accounts[0].now_playing_state?.[0] ? `<img src="${accounts[0].now_playing_state?.[0]}">` : '<p>nothin\'</p>';
  document.getElementById('app').innerHTML = `${state}<p>${account.service_name}</p>`;
}

start();
