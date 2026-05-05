import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

cmd = "echo 'c0i1uhIPrEpu' | sudo -S certbot certonly --nginx -d wioav2.nserver.space --non-interactive --agree-tos -m admin@nserver.space --dry-run"
stdin, stdout, stderr = client.exec_command(cmd)

out = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("OUT:", out)
print("ERR:", err)
