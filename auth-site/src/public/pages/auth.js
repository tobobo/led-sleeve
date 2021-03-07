export class Auth {
  constructor(location, config) {
    const pathSections = location.pathname.split('/');
    const deviceName = pathSections[1];
    const provider = pathSections[3];
    window.localStorage.setItem('auth_state', JSON.stringify({ deviceName }));
    switch (provider) {
      case 'spotify':
        const spotifyParams = new URLSearchParams();

        const redirectUri = new URL(window.location);
        redirectUri.pathname = '/authcb/spotify';

        spotifyParams.set('client_id', config.spotify.clientId);
        spotifyParams.set('redirect_uri', redirectUri.toString());
        spotifyParams.set('state', 'led-sleeve');
        spotifyParams.set('scope', 'user-read-playback-state user-read-currently-playing');
        spotifyParams.set('show_dialog', 'true');
        spotifyParams.set('response_type', 'code');
        
        const spotifyUri = new URL('https://accounts.spotify.com/authorize');
        spotifyUri.search = spotifyParams.toString();

        location.replace(spotifyUri);
      default:
        throw new Error('unknown provider');
    }
  }
}
