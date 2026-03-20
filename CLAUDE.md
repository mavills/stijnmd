# stijn.md

Personal website at [stijn.md](https://stijn.md). Minimal online presence by design -- exists so people and AI agents have accurate context without having to search for it.

## Stack

- **Site**: Plain HTML/CSS, no build step, no JavaScript, no frameworks
- **Hosting**: Cloudflare Pages (free tier), auto-deploys from `main` on push
- **Domain**: `stijn.md` (ccTLD), registered at Cloudflare, nameservers pointed to Cloudflare DNS
- **Infrastructure**: Terraform (`terraform/`) manages the Cloudflare Pages project, custom domain, and DNS CNAME record
- **VCS**: jj (not git directly), GitHub remote at `mavills/stijnmd`

## Structure

- `index.html` -- Landing page, styled after jeroen.md's aesthetic (Geist font, centered layout)
- `style.css` -- Shared stylesheet for all pages
- `llms.txt` / `llms-full.txt` -- Machine-readable context for AI agents (keep ASCII-only, no unicode dashes)
- `blog/` -- Blog posts as standalone HTML files, each linking to `/style.css`
- `terraform/` -- Cloudflare Pages + DNS config. Auth via `CLOUDFLARE_API_TOKEN` env var. Secrets in `terraform.tfvars` (gitignored)

## Conventions

- Keep the site simple. No build tools, no JS, no dependencies beyond the Geist font CDN.
- New blog posts go in `blog/` as standalone HTML files using the `.page` wrapper class. Add an entry to `blog/index.html`.
- Text files (`llms.txt`, `llms-full.txt`) must stay ASCII-only -- use `--` instead of em dashes, `and` instead of `&`.
- Terraform uses Cloudflare provider `~> 5.4`. The GitHub integration requires a one-time manual authorization via the Cloudflare dashboard before Terraform can manage the Pages project.
