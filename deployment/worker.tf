import {
  to = cloudflare_workers_script.main
  id = var.account_id + "/bob-to-slack"
}

resource "cloudflare_workers_script" "main" {
  content             = file("${path.module}/../app/src/main.py")
  account_id          = var.account_id
  compatibility_flags = ["python_workers"]
  compatibility_date  = "2024-03-29"
  script_name         = "bob-to-slack"
  bindings = [
    {
      type         = "kv_namespace",
      name         = var.kv_name,
      namespace_id = cloudflare_workers_kv_namespace.main.id
    },
    {
      type = "plain_text",
      name = "bob_custom_level_column"
      text = local.bob_custom_level_column_full
    },
    {
      type = "plain_text",
      name = "bob_custom_level_column_short"
      text = var.bob_custom_level_column
    },
    {
      type = "plain_text",
      name = "bob_endpoint"
      text = "https://api.hibob.com/v1/people/"
    },
    {
      type = "plain_text",
      name = "fields"
      text = "root.id,root.email,root.displayName,/work/title,personal.pronouns,${local.bob_custom_level_column_full}"
    },
    {
      type = "plain_text",
      name = "slack_level_field_id"
      text = var.slack_level_field_id
    },
    {
      type = "plain_text",
      name = "slack_lookupemail_endpoint"
      text = "https://slack.com/api/users.lookupByEmail"
    },
    {
      type = "plain_text",
      name = "slack_setuser_endpoint"
      text = "https://slack.com/api/users.profile.set"
    },
    {
      type = "plain_text",
      name = "slack_title_field_id"
      text = var.slack_title_field_id
    }
  ]
}
