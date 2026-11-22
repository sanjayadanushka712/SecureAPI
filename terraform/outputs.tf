output "server_ip" {
  description = "Public IP address used to reach the server"
  value       = local.public_ip
}

output "droplet_id" {
  description = "DigitalOcean droplet identifier"
  value       = digitalocean_droplet.app.id
}

output "ssh_command" {
  description = "Command to connect to the server"
  value       = "ssh root@${local.public_ip}"
}

output "domain" {
  description = "Domain configured for the deployment"
  value       = var.domain
}
