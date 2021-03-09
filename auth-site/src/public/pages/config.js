export class Config {
  constructor(location, config) {
    const pathSections = location.pathname.split('/');
    this.deviceName = pathSections[1];
    this.localDomain = config.localDomain;
  }
  
  attach() {
    document.body.innerHTML = `<a href="http://${this.deviceName}.${this.localDomain}">Config</a>`;
  }
}
