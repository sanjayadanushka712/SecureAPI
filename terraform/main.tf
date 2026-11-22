data "digitalocean_ssh_key" "deploy" {
  count = var.ssh_key_id == null ? 1 : 0
  name  = var.ssh_key_name
}

locals {
  ssh_key_ids = var.ssh_key_id == null ? [data.digitalocean_ssh_key.deploy[0].id] : [var.ssh_key_id]
  public_ip   = var.enable_floating_ip ? digitalocean_floating_ip.app[0].ip_address : digitalocean_droplet.app.ipv4_address
}

resource "digitalocean_droplet" "app" {
  name       = var.droplet_name
  image      = var.image
  size       = var.size
  region     = var.region
  ssh_keys   = local.ssh_key_ids
  tags       = var.droplet_tags
  monitoring = true
  ipv6       = true
}

resource "digitalocean_firewall" "app" {
  name        = "${var.droplet_name}-firewall"
  droplet_ids = [digitalocean_droplet.app.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "icmp"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

resource "digitalocean_floating_ip" "app" {
  count      = var.enable_floating_ip ? 1 : 0
  region     = var.region
  droplet_id = digitalocean_droplet.app.id
}

resource "digitalocean_domain" "app" {
  count = var.manage_dns ? 1 : 0
  name  = var.domain
}

resource "digitalocean_record" "app" {
  count  = var.manage_dns ? 1 : 0
  domain = digitalocean_domain.app[0].name
  type   = "A"
  name   = "@"
  value  = local.public_ip
  ttl    = 60
}

resource "digitalocean_record" "www" {
  count  = var.manage_dns ? 1 : 0
  domain = digitalocean_domain.app[0].name
  type   = "CNAME"
  name   = "www"
  value  = "${var.domain}."
  ttl    = 60
}
