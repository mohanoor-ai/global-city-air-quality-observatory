# Local Setup Guide

This document explains how to set up the project locally for development.

---

## Python Environment

```bash
uv sync
```

---

## Terraform Setup

From the project root:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Edit `terraform/terraform.tfvars` with your real GCP values.

Then run:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

## Notes

- `terraform/terraform.tfvars` is ignored by git.
- `terraform/terraform.tfvars.example` is the committed template.
