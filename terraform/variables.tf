variable "location" {
  description = "Azure region"
  type        = string
  default     = "polandcentral"
}

variable "resource_group_name" {
  description = "Name of the Resource Group"
  type        = string
  default     = "sdx-rg"
}

variable "vnet_cidr" {
  description = "CIDR block for the Virtual Network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the Subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "vm_admin_username" {
  description = "Admin username for the virtual machine"
  type        = string
  default     = "sdxuser"
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key"
  type        = string
}

variable "my_sub_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}
variable "subscription_id" {}

