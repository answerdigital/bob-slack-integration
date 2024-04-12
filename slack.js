export default class Slack {
  #token;

  constructor(token) {
    this.#token = token;
  }

  async #slackFetch(api, params, options) {
    if (!options) { options = {}; }
    if (!options.method) { options.method = 'GET'; }
    if (!options.headers) { options.headers = {}; }
    options.headers.authorization = `Bearer ${this.#token}`;
    let url = new URL(`https://slack.com/api/${api}`);

    if (options.method == 'GET') {
      Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, v));
    } else {
      options.headers['content-type'] = 'application/json;charset=utf-8';
      options.body = JSON.stringify(params);
    }

    return await fetch(url, options);
  }

  async getUserId(email) {
    const response = await this.#slackFetch('users.lookupByEmail', {email});
    const body = await response.json();
    return body?.user?.id;
  }

  async setUserProfile(user, fields) {
    const fieldMapping = {
      capability: 'Xf06TR53N5T8',
      contractedLocation: 'Xf06TR5K2PQE',
    };

    const profile = Object.keys(fields).reduce((acc, field) => {
      acc[fieldMapping[field] || field] = fields[field];
      return acc;
    }, {});

    return await this.#slackFetch('users.profile.set', {user, profile}, {method: 'POST'});
  }
}
