terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.4"
    }
  }
}

provider "cloudflare" {}

resource "cloudflare_pages_project" "blog" {
  account_id = var.cloudflare_account_id
  name       = "stijnmd"

  production_branch = "main"

  source = {
    type = "github"
    config = {
      owner             = var.github_owner
      repo_name         = var.github_repo
      production_branch = "main"
    }
  }

  build_config = {
    build_command   = ""
    destination_dir = "/"
  }

  deployment_configs = {
    production = {}
  }
}

resource "cloudflare_pages_domain" "blog" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.blog.name
  domain       = "stijn.md"
}

resource "cloudflare_dns_record" "blog" {
  zone_id = var.cloudflare_zone_id
  name    = "stijn.md"
  type    = "CNAME"
  content = "stijnmd.pages.dev"
  proxied = true
}
