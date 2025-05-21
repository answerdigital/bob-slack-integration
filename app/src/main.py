from js import Response, fetch, Object
from pyodide.ffi import to_js as _to_js
import base64
import json
import datetime


def to_js(obj):
    return _to_js(obj, dict_converter=Object.fromEntries)


# gather_response returns both content-type & response body as a string
async def gather_response(response):
    headers = response.headers
    content_type = headers["content-type"] or ""

    if "application/json" in content_type:
        return (content_type, (await response.json()).to_py())
    return (content_type, await response.text())


def check_updates(request, env):
    for field in request.data.fieldUpdates:
        for search_field in env.bob_check_fields.split(","):
            if field.id == search_field:
                return True
    return False


async def on_fetch(request, env):
    request = await request.json()

    if not check_updates(request, env):
        return Response.new("No updates needed")

    if await env.BobToSlack.get("BobUser") is None:
        return Response.new("BobUser missing from KV not configured")

    if await env.BobToSlack.get("BobPassword") is None:
        return Response.new("BobPassword missing from KV not configured")

    if await env.BobToSlack.get("SlackToken") is None:
        return Response.new("SlackToken missing from KV not configured")

    bob_call = await call_bob(env, request.data.employeeId)
    level = bob_call["work"]["customColumns"][env.bob_custom_level_column_short]
    title = bob_call["work"]["title"]
    email = bob_call["email"]
    start_date = bob_call["work"]["startDate"]
    if start_date is not None:
        start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    disc_profile = bob_call["work"]["custom"][env.bob_custom_disc_column_short]
    capability = bob_call["work"]["department"]

    slack_user = await call_slack(env, email)
    slack = await call_slack_update(env, slack_user["user"]["id"], level, title, capability, start_date, disc_profile)

    return Response.new(str(slack))


async def call_bob(env, bob_employeeid):
    bob_user = await env.BobToSlack.get("BobUser")
    bob_password = await env.BobToSlack.get("BobPassword")
    bob_fields = env.fields
    bob_endpoint = env.bob_endpoint

    credentials = base64.b64encode(f"{bob_user}:{bob_password}".encode("utf-8")).decode(
        "utf-8"
    )

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
    }

    body = {"fields": bob_fields.split(","), "humanReadable": "REPLACE"}

    options = {"body": json.dumps(body), "headers": headers, "method": "POST"}

    url = f"{bob_endpoint}{bob_employeeid}"

    response = await fetch(url, to_js(options))
    _, result = await gather_response(response)
    return result


async def call_slack(env, email):
    slack_token = await env.BobToSlack.get("SlackToken")
    slack_lookupemail_endpoint = env.slack_lookupemail_endpoint

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }

    options = {"headers": headers, "method": "GET"}

    url = f"{slack_lookupemail_endpoint}?email={email}"

    response = await fetch(url, to_js(options))
    _, result = await gather_response(response)

    return result


async def call_slack_update(env, user_id, level, title, capability, start_date, disc_profile):
    slack_token = await env.BobToSlack.get("SlackToken")
    slack_setuser_endpoint = env.slack_setuser_endpoint
    slack_title_field_id = env.slack_title_field_id
    slack_level_field_id = env.slack_level_field_id
    slack_capability_field_id = env.slack_capability_field_id
    slack_start_date_field_id = env.slack_start_date_field_id
    slack_disc_profile_field_id = env.slack_disc_profile_field_id

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }

    profile = {
        "fields": {
            slack_title_field_id: {"value": title, "alt": ""},
            slack_level_field_id: {"value": level, "alt": ""},
            slack_capability_field_id: {"value": capability, "alt": ""},
            slack_start_date_field_id: {"value": start_date, "alt": ""},
            slack_disc_profile_field_id: {"value": disc_profile, "alt": ""},
        }
    }

    body = {"profile": profile, "user": user_id}

    options = {"headers": headers, "method": "POST", "body": json.dumps(body)}

    url = f"{slack_setuser_endpoint}"

    response = await fetch(url, to_js(options))
    _, result = await gather_response(response)

    return result
