import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')
commands = [
    'cd /var/www/wioa && git status',
    'cd /var/www/wioa && GIT_SSH_COMMAND=\'ssh -i /var/www/.ssh/id_ed25519 -o StrictHostKeyChecking=no\' git fetch origin main',
    'cd /var/www/wioa && git reset --hard origin/main',
    'echo \'c0i1uhIPrEpu\' | sudo -S systemctl restart gunicorn',
]
for cmd in commands:
    print('Running:', cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())
