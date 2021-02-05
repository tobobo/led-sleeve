const form = document.getElementById('credentials');
const status = document.getElementById('status');

function wait(duration) {
  return new Promise(resolve => {
    setTimeout(resolve, duration);
  });
}

async function waitForApp(attempts) {
  for (let i = 0; i < attempts; i++) {
    try {
      const response = await fetch('/');
      if (response.status === 200) {
        window.location.reload();
      }
    } catch (e) {
      // try again
    }
    await wait(2000);
  }
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  
  const body = new FormData(e.target);

  try {
    await fetch('/set_credentials', {
      method: 'POST',
      body,
    });
    form.remove();
    status.innerHTML = `
      <p>Wifi config saved. Connect this device to the network "${body.get('ssid')}" if it doesn't reconnect automatically.</p>
      <p>If the connection was successful, this page should reload in 10-30 seconds with the next step.</p>
    `;
    await wait(3000);
    await waitForApp(15);
    status.innerHTML = `
      <p>Hmm... We weren't able to connect. Make sure you're connected to "${body.get('ssid')}". If the configuration network is available, reconnect to it and try again.</p>
    `;
    await waitForApp(Infinity)
  } catch (e) {
    // something bad happened
  }
});
