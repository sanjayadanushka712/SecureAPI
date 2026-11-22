variable "do_token" {
  type        = string
  sensitive   = true
  description = "DigitalOcean API token used by the provider"
}

variable "ssh_key_id" {
  type        = string
  default     = null
  description = "Existing DigitalOcean SSH key ID; when null ssh_key_name is looked up"
}

variable "ssh_key_name" {
  type        = string
  default     = "secureapi-deploy"
  description = "SSH key name to look up when ssh_key_id is not provided"
}

variable "region" {
  type        = string
  default     = "nyc3"
  description = "DigitalOcean region for the droplet"
}

variable "size" {
  type        = string
  default     = "s-1vcpu-1gb"
  description = "DigitalOcean droplet size slug"
}

variable "image" {
  type        = string
  default     = "ubuntu-24-04-x64"
  description = "DigitalOcean image slug"
}

variable "droplet_name" {
  type        = string
  default     = "secureapi-prod"
  description = "Name of the DigitalOcean droplet"
}

variable "domain" {
  type        = string
  default     = "secureapi.example.com"
  description = "Domain used for the deployment"
}

variable "manage_dns" {
  type        = bool
  default     = false
  description = "Create the domain and A record in the provider when true"
}

variable "enable_floating_ip" {
  type        = bool
  default     = false
  description = "Whether to reserve and attach a floating IP"
}

variable "droplet_tags" {
  type        = list(string)
  default     = ["secureapi"]
  description = "Tags applied to the droplet"
}
