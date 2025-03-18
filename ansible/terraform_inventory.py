#!/usr/bin/env python3
import json
import os
import sys

def generate_inventory():
    try:
        # Read the Terraform state file
        with open('terraform.tfstate', 'r') as f:
            state = json.load(f)
        
        # Extract server IPs from the state
        outputs = state.get('outputs', {})
        server_1_ip = outputs.get('server_1_ip', {}).get('value')
        server_2_ip = outputs.get('server_2_ip', {}).get('value')
        
        if not server_1_ip or not server_2_ip:
            print("Error: Could not find server IPs in terraform state", file=sys.stderr)
            sys.exit(1)
        
        # Generate inventory file content
        inventory_content = f"""[postgres_servers]
pg_master ansible_host={server_1_ip} ansible_user=ubuntu
pg_replica ansible_host={server_2_ip} ansible_user=ubuntu

[postgres_master]
pg_master

[postgres_replica]
pg_replica

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_ed25519
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
"""
        
        # Write to inventory file
        with open('inventory.ini', 'w') as f:
            f.write(inventory_content)
        
        print(f"Inventory file generated successfully with master: {server_1_ip}, replica: {server_2_ip}")
        
    except Exception as e:
        print(f"Error generating inventory: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_inventory()