export class Auth {
  constructor({ pathname }, config) {
    const provider = pathname.split('/')[3];
    switch (provider) {
      case 'spotify':
        console.log('spotify auth');
        const spotifyParams = new URLSearchParams();

        const redirectUri = new URL(window.location);
        redirectUri.pathname = '/authcb/spotify';

        spotifyParams.set('client_id', config.spotify.clientId);
        spotifyParams.set('redirect_uri', redirectUri.toString());
        spotifyParams.set('state', 'spotify');
        spotifyParams.set('scope', 'user-read-currently-playing');
        spotifyParams.set('response_type', 'code');
        
        const spotifyUri = new URL('https://accounts.spotify.com/authorize');
        spotifyUri.search = spotifyParams.toString();
        
        window.location.assign(spotifyUri);
      default:
        throw new Error('unknown provider');
    }
  }
}
