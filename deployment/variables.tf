variable "zone" {
  type = string
}

variable "account_id" {
  type = string
}

variable "kv_name" {
  type    = string
  default = "BobToSlack"
}

variable "kv_secret_bob_password" {
  type      = string
  sensitive = true
}

variable "kv_secret_bob_user" {
  type      = string
  sensitive = true
}

variable "kv_secret_slack_token" {
  type      = string
  sensitive = true
}

variable "bob_custom_level_column" {
  type    = string
  default = "column_1693476959605"
}

variable "slack_level_field_id" {
  type    = string
  default = "Xf08DNL0T80G"
}

variable "slack_title_field_id" {
  type    = string
  default = "Xf08HU7HLVM1"
}
