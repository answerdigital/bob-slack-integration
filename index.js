// TODO:
// validate Bob HMAC signature
// handle Bob ping test
// handle Bob change events (which?)
// https://apidocs.hibob.com/reference/employee-changes-events
// is everything in the event or do we need a separate info call?
// Get-Employee header field if needed

import Slack from './slack';

export default {
  async fetch(request, env, ctx) {
    const requestUrl = new URL(request.url);
    const slack = new Slack(env.SLACK_TOKEN);
    const userId = await slack.getUserId(requestUrl.searchParams.get('email'));

    return await slack.setUserProfile(userId, {
      capability: 'Architecture',
      contractedLocation: 'Leeds',
    });
  },
};
