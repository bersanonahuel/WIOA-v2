import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

# Check if certbot is installed
cmd = "certbot --version || echo 'Not installed'"
stdin, stdout, stderr = client.exec_command(cmd)
print("CERTBOT:", stdout.read().decode('utf-8', errors='ignore'))
