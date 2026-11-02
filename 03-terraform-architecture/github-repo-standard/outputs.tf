output "repository_name" {
  value       = github_repository.repo.name
  description = "Name of the provisioned repository."
}

output "html_url" {
  value       = github_repository.repo.html_url
  description = "Web URL of the repository."
}

output "ssh_clone_url" {
  value       = github_repository.repo.ssh_clone_url
  description = "SSH clone URL."
}

output "ruleset_id" {
  value       = github_repository_ruleset.default_branch_rules.ruleset_id
  description = "ID of the applied ruleset."
}

