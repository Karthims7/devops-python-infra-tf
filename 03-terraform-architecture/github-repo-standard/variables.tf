variable "repository_name" {
  type        = string
  description = "The name of the GitHub repository."
}

variable "description" {
  type        = string
  default     = "Managed via Terraform - Enterprise DevOps Standard"
  description = "Description of the repository."
}

variable "visibility" {
  type        = string
  default     = "private"
  description = "Repository visibility (public, private, or internal)."
  validation {
    condition     = contains(["public", "private", "internal"], var.visibility)
    error_message = "Visibility must be one of: public, private, internal."
  }
}

variable "required_approvals" {
  type        = number
  default     = 2
  description = "Minimum number of approving PR reviews."
}

variable "topics" {
  type        = list(string)
  default     = ["devops", "terraform", "woven-by-toyota"]
  description = "GitHub repository topics."
}

