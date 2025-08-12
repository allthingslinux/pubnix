provider "hcloud" {
  token = var.hcloud_token
}

variable "hcloud_token" {
  type = string
}

resource "hcloud_server" "pubnix" {
  name        = "atl-pubnix"
  image       = "ubuntu-24.04"
  server_type = "cpx21"
  location    = "nbg1"
  ssh_keys    = []
}
