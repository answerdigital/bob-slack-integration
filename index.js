// TODO:
// validate Bob HMAC signature
// handle Bob ping test
// handle Bob change events (which?)
// https://apidocs.hibob.com/reference/employee-changes-events
// is everything in the event or do we need a separate info call?
// Get-Employee header field if needed

import { Buffer } from 'node:buffer';
import Slack from './slack';

function authorize(request, env) {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) { return false; }

  const [scheme, auth] = authHeader.split(' ');
  if (scheme != 'Basic' || !auth) { return false; }

  return (env.BASIC_AUTH == Buffer.from(auth, 'base64').toString());
}

export default {
  async fetch(request, env, ctx) {
    const requestUrl = new URL(request.url);
    const slack = new Slack(env.SLACK_TOKEN);

    if (!authorize(request, env)) {
      return new Response('Not authed', {
        status: 401,
        headers: {'www-authenticate': 'Basic realm="bob-slack-integration", charset="utf-8"'},
      });
    }

    const userId = await slack.getUserId(requestUrl.searchParams.get('email'));

    if (!userId) {
      return new Response('User not found', {status: 404});
    }

    return await slack.setUserProfile(userId, {
      capability: 'Architecture',
      contractedLocation: 'Leeds',
    });
  },
};
