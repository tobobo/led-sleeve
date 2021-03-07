export class Account {
  constructor(container, account) {
    this.container = container;
    this.account = account;
    this.template = document.getElementById('account');
    this.hasInitializedContent = false;
  }
  
  async fetchAndRender() {
    const accountData = await (await fetch(`/api/accounts/${this.account.provider}/${this.account.id}`)).json();
    const accountEl = this.hasInitializedContent ? this.container : this.template.content.cloneNode(true);
    accountEl.querySelector('.account-provider').innerHTML = this.account.provider;
    accountEl.querySelector('.account-id').innerHTML = this.account.id;
    const accountImageEl = accountEl.querySelector('.account-image');
    if (accountData.now_playing_state?.image_url) {
      accountImageEl.style.backgroundImage = `url("${accountData.now_playing_state.image_url}")`;
      accountEl.querySelector('.is-not-playing').innerHTML = '';
    } else {
      accountImageEl.style.backgroundImage = null;
      accountEl.querySelector('.is-not-playing').innerHTML = 'not playing';
    }
    if (!this.hasInitializedContent) {
      this.container.appendChild(accountEl);
      this.hasInitializedContent = true;
    }
  }
  
  async fetchLoop() {
    await this.fetchAndRender();
    setTimeout(() => this.fetchLoop(), 5000);
  }
  
  attach() {
    this.fetchLoop();
  }
}
