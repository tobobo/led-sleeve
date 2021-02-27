export class Auth {
  constructor({ pathname }) {
    const provider = pathname.split('/')[3];
    switch (provider) {
      case 'spotify':
        console.log('spotify auth');
        break;
      default:
        throw new Error('unknown provider');
    }
  }
}
