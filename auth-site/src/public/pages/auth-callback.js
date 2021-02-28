export class AuthCallback {
  constructor(location) {
    const { protocol, host, pathname, search } = location;
    const { deviceName } = JSON.parse(window.localStorage.getItem('auth_state'));
    window.localStorage.removeItem('auth_state');
    const provider = pathname.split('/')[2];
    const redirectParams = new URLSearchParams(search);
    redirectParams.set('authcb', provider);
    
    const redirectUrl = new URL(`/${deviceName}`, `${protocol}//${host}`);
    redirectUrl.search = redirectParams.toString();

    location.assign(redirectUrl);
  }
}
