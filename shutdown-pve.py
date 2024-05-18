import paramiko


def shutdown_vm(hostname, port, username, key_filepath, connection_timeout=5, command_timeout=5):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        # Automatically add the server's host key (note: this is not recommended for production code)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Load the SSH key
        private_key = paramiko.Ed25519Key.from_private_key_file(key_filepath)
        # Connect to the server using the SSH key
        ssh.connect(hostname, port, username, pkey=private_key,
                    timeout=connection_timeout)
        # Execute the shutdown command
        stdin, stdout, stderr = ssh.exec_command(
            'shutdown -h now', timeout=command_timeout)
        # Print the command output (if any)
        print(stdout.read().decode())
        print(stderr.read().decode())
        # Close the connection
        ssh.close()
        print(f"Shutdown command sent to {hostname}")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error with {hostname}: {e}")
    except Exception as e:
        print(f"An error occurred with {hostname}: {e}")


# List of VM details
vms = [
    {'hostname': '192.168.1.253', 'port': 22,
        'username': 'root', 'key_filepath': '/Users/andrew/.ssh/id_ed25519'},   # Add more VMs as needed
]

# Loop through each VM and shut it down
for vm in vms:
    shutdown_vm(vm['hostname'], vm['port'], vm['username'], vm['key_filepath'])
