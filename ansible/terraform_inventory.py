#!/usr/bin/env python3
import json
import os
import sys
import subprocess

def generate_inventory():
    try:
        # Build paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        terraform_dir = os.path.join(script_dir, '..', 'terraform')
        terraform_state_file = os.path.join(terraform_dir, 'terraform.tfstate')
        
        # Read the Terraform state file
        with open(terraform_state_file, 'r') as f:
            state = json.load(f)
        
        # Extract server IPs from the state
        outputs = state.get('outputs', {})
        server_1_ip = outputs.get('server_1_ip', {}).get('value')
        server_2_ip = outputs.get('server_2_ip', {}).get('value')
        
        if not server_1_ip or not server_2_ip:
            print("Error: Could not find server IPs in terraform state", file=sys.stderr)
            sys.exit(1)
        
        # Get the private key from Terraform state
        private_key = None
        for resource in state.get('resources', []):
            if resource.get('type') == 'tls_private_key' and resource.get('name') == 'my_key':
                private_key = resource.get('instances', [])[0].get('attributes', {}).get('private_key_openssh')
                break
        
        if not private_key:
            print("Warning: Could not find private key in terraform state", file=sys.stderr)
            print("Using default ~/.ssh/id_ed25519 key", file=sys.stderr)
            key_path = "~/.ssh/id_ed25519"
        else:
            # Write the private key to a file
            key_path = os.path.join(script_dir, 'terraform_private_key')
            with open(key_path, 'w') as f:
                f.write(private_key)
            # Set correct permissions for SSH key
            os.chmod(key_path, 0o600)
            print(f"Private key written to {key_path}")
        
        # Generate inventory file content with corrected group names
        inventory_content = f"""[postgresql_servers]
pg_master ansible_host={server_1_ip} ansible_user=ubuntu
pg_replica ansible_host={server_2_ip} ansible_user=ubuntu

[postgres_master]
pg_master

[postgres_replica]
pg_replica

[postgresql:children]
postgres_master
postgres_replica

[postgresql:vars]
ansible_ssh_private_key_file={key_path}
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
ansible_python_interpreter=/usr/bin/python3
"""
        
        # Write to inventory file
        inventory_path = os.path.join(script_dir, 'inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write(inventory_content)
        
        print(f"Inventory file generated successfully at {inventory_path}")
        print(f"Master IP: {server_1_ip}, Replica IP: {server_2_ip}")
        
    except Exception as e:
        print(f"Error generating inventory: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_inventory()