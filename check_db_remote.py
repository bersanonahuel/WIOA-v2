import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

cmd = "cd /var/www/wioa && echo 'c0i1uhIPrEpu' | sudo -S chown wioa:www-data db.sqlite3 && echo 'c0i1uhIPrEpu' | sudo -S chmod 664 db.sqlite3 && echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn && sleep 3 && curl -I http://localhost"
stdin, stdout, stderr = client.exec_command(cmd)

out = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("STDOUT:", out)
print("STDERR:", err)
