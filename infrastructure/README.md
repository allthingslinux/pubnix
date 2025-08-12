# ATL Pubnix Infrastructure

- Terraform (Hetzner Cloud) under `infrastructure/terraform/hetzner`
- Ansible roles under `infrastructure/ansible`

Usage:

Terraform (provision server):

```bash
cd infrastructure/terraform/hetzner
export HCLOUD_TOKEN=...  # set token
terraform init
terraform apply -var hcloud_token=$HCLOUD_TOKEN
```

Ansible (configure server):

```bash
cd infrastructure/ansible
ansible-playbook -i inventory.ini site.yml
```
