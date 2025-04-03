resource "cloudflare_workers_kv_namespace" "main" {
  account_id = var.account_id
  title      = var.kv_name
}

resource "cloudflare_workers_kv" "bob_password" {
  account_id   = var.account_id
  namespace_id = cloudflare_workers_kv_namespace.main.id
  key_name     = "BobPassword"
  value        = var.kv_secret_bob_password
}

resource "cloudflare_workers_kv" "bob_user" {
  account_id   = var.account_id
  namespace_id = cloudflare_workers_kv_namespace.main.id
  key_name     = "BobUser"
  value        = var.kv_secret_bob_user
}

resource "cloudflare_workers_kv" "slack_token" {
  account_id   = var.account_id
  namespace_id = cloudflare_workers_kv_namespace.main.id
  key_name     = "SlackToken"
  value        = var.kv_secret_slack_token
}
