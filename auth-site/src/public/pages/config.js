export class Config {
  constructor(location, config, container) {
    this.container = container;
    const pathSections = location.pathname.split('/');
    this.deviceName = pathSections[0];
    this.localDomain = config.localDomain;
    this.template = document.getElementById('wifi-instructions');
    const redirectParams = new URLSearchParams(location.search);
    this.deviceName = pathSections[1];
    debugger;
    this.psk = redirectParams.get('psk');
    this.configUrl = `http://${this.deviceName}.${this.localDomain}`
  }
  
  attach() {
    const el = this.template.content.cloneNode(true);
    el.querySelector('.network-ssid').innerHTML = this.deviceName;
    el.querySelector('.network-psk').innerHTML = this.psk;
    el.querySelector('.config-link').href = this.configUrl;
    el.querySelector('.config-link').innerHTML = this.configUrl;
    this.container.appendChild(el);
  }
}
