export class Config {
  constructor(location, config) {
    this.deviceName = location.pathname.split('/')[1];
    this.localDomain = config.localDomain;
  }
  
  attach() {
    const iframe = document.createElement('iframe');
    const iframeSrc = new URL(`http://${this.deviceName}.${this.localDomain}${location.search}`);
    iframe.src = iframeSrc.toString();
    document.body.appendChild(iframe);
  }
}
