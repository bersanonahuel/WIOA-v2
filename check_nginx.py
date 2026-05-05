import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

cmd = "cat /etc/nginx/sites-available/wioa || cat /etc/nginx/sites-enabled/default"
stdin, stdout, stderr = client.exec_command(cmd)

out = stdout.read().decode('utf-8', errors='ignore')
with open('remote_nginx.txt', 'w', encoding='utf-8') as f:
    f.write(out)
