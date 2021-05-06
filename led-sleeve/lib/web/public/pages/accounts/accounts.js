import { Account } from './account.js';

export class Accounts {
  constructor(_location, config, container) {
    this.config = config;
    this.container = container;
    this.accountsTemplate = window.document.getElementById('accounts');
    this.accountTemplate = window.document.getElementById('account');
    this.addAccountTemplate = window.document.getElementById('add-account');
  }

  removeQueryParams() {
    history.replaceState({}, document.title, window.location.pathname);
  }
  
  getAuthCredentials() {
    const query = new URLSearchParams(window.location.search);
    const provider = query.get('authcb');
    if (!provider) return;
    this.removeQueryParams();
    return query;
  }

  async checkAuthCredentials(credentials) {
    if (credentials.get('authcb') === 'spotify') {
      await fetch('/api/accounts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: 'spotify',
          code: credentials.get('code'),
        }),
      });
    }
  }
  
  async renderAccounts() {
    const noAccountsLabel = this.container.querySelector('.no-accounts');
    const accounts = await (await fetch('/api/accounts')).json();
    if (accounts.length === 0) {
      noAccountsLabel.style.display = 'block';
    } else {
      noAccountsLabel.style.display = 'none';
    }
    this.accounts = accounts.map((account) => {
      const accountContainer = document.createElement('div');
      this.accountsList.appendChild(accountContainer);
      const accountChild = new Account(accountContainer, account);
      accountChild.attach();
      return accountChild;
    });
  }
  
  renderAddAccount() {
    if (this.accounts.length === 1) return;
    const addAccountChild = this.addAccountTemplate.content.cloneNode(true);
    [...addAccountChild.querySelectorAll('.account-link')].forEach(accountLink => {
      accountLink.href = accountLink.dataset.href
        .replace('__AUTH_SITE_BASE__', this.config.auth_site_base)
        .replace('__DEVICE_NAME__', this.config.device_name);
    })
    this.accountsList.appendChild(addAccountChild);
  }

  async attach() {
    this.accountsContainer = this.accountsTemplate.content.cloneNode(true);
    this.accountsList = this.accountsContainer.querySelector('.accounts-list');
    this.container.appendChild(this.accountsContainer);
    const credentials = this.getAuthCredentials();
    if (credentials) {
      await this.checkAuthCredentials(credentials);
    }
    await this.renderAccounts();
    this.renderAddAccount();
  }
}
