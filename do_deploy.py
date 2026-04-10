import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')
commands = [
    'cd /var/www/wioa && GIT_SSH_COMMAND=\'ssh -i /var/www/.ssh/id_ed25519 -o StrictHostKeyChecking=no\' git pull origin main',
    'echo \'c0i1uhIPrEpu\' | sudo -S systemctl restart gunicorn',
    'echo \'c0i1uhIPrEpu\' | sudo -S systemctl status gunicorn'
]
for cmd in commands:
    print('Running:', cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())
