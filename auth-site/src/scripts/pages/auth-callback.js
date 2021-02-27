export class AuthCallback {
  constructor({ pathname }) {
    const provider = pathname.split('/')[2];
    switch (provider) {
      case 'spotify':
        console.log('spotify cb');
        break;
      default:
        throw new Error('unknown provider');
    }
  }
}
