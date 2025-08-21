output "vm_public_ip" {
  value       = "http://${azurerm_public_ip.pip.ip_address}"
  description = "Public IP address of the Virtual Machine"
}

output "public_ip" {
  value       = azurerm_public_ip.pip.ip_address
  description = "Raw Public IP address of the Virtual Machine"
}
