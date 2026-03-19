# stijn.md

A minimal static blog hosted on Cloudflare Pages with infrastructure managed by Terraform.

## How to set up your own

This guide walks you through hosting a static site on Cloudflare Pages using a ccTLD domain (like `.md`, `.io`, `.dev`).

### Prerequisites

- A domain registered at any registrar
- A [Cloudflare](https://cloudflare.com) account (free tier is fine)
- A GitHub account and repository with your static site
- [Terraform](https://developer.hashicorp.com/terraform/install) installed

### 1. Move your domain to Cloudflare DNS

At your domain registrar, change the nameservers to the ones Cloudflare assigns you:

1. Add your domain in the Cloudflare dashboard
2. Cloudflare will give you two nameservers (e.g. `anna.ns.cloudflare.com`, `bob.ns.cloudflare.com`)
3. Update the nameservers at your registrar
4. Wait for propagation (can take up to 24 hours, usually much faster)

### 2. Create a Cloudflare API token

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click **Create Token**
3. Use **Create Custom Token** with these permissions:
   - **Account → Cloudflare Pages → Edit**
   - **Zone → Zone → Edit**
   - **Zone → DNS → Edit**
4. Scope it to your account and zone
5. Export it: `export CLOUDFLARE_API_TOKEN=your_token_here`

### 3. Connect GitHub to Cloudflare Pages

This is a one-time manual step that can't be done via Terraform:

1. Go to **Workers & Pages → Create → Pages → Connect to Git**
2. Authorize the Cloudflare Pages GitHub App on your account
3. Grant it access to your repository
4. Cancel out — don't finish creating the project (Terraform will handle that)

### 4. Configure Terraform

Copy `terraform/variables.tf` and create a `terraform/terraform.tfvars`:

```hcl
cloudflare_account_id = "your-account-id"   # Dashboard → any domain → right sidebar
cloudflare_zone_id    = "your-zone-id"       # Dashboard → your domain → right sidebar
github_owner          = "your-github-username"
github_repo           = "your-repo-name"
```

### 5. Deploy

```sh
cd terraform
terraform init
terraform plan
terraform apply
```

This creates:
- A Cloudflare Pages project connected to your GitHub repo
- A custom domain pointing to the Pages project
- A CNAME DNS record

After applying, the custom domain may show "Initializing" while Cloudflare provisions the SSL certificate. This usually resolves within a few minutes.

### 6. Publish

Push any change to `main` and Cloudflare Pages will auto-deploy. No build step needed — it serves the static files directly.

## Project structure

```
index.html              # Homepage
style.css               # Shared stylesheet
posts/
  hello-world.html      # Blog posts as standalone HTML files
terraform/
  main.tf               # Cloudflare Pages project, domain, DNS record
  variables.tf          # Input variables
  outputs.tf            # Pages URL and custom domain outputs
```
