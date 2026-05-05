import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

cmd = "echo 'c0i1uhIPrEpu' | sudo -S systemctl status gunicorn --no-pager; echo '---'; echo 'c0i1uhIPrEpu' | sudo -S systemctl status nginx --no-pager; echo '---'; journalctl -u gunicorn -n 50 --no-pager"
stdin, stdout, stderr = client.exec_command(cmd)

out = stdout.read().decode('utf-8', errors='ignore')
with open('remote_status.txt', 'w', encoding='utf-8') as f:
    f.write(out)
