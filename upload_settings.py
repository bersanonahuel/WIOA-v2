import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')
sftp = client.open_sftp()
sftp.put(r'c:\s\Sistema\wiao\wioa\WIOA\settings.py', '/var/www/wioa/WIOA/settings.py')
sftp.close()
def run_cmd(cmd):
    print('Running:', cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode('utf-8','ignore'))
    print(stderr.read().decode('utf-8','ignore'))
run_cmd('cd /var/www/wioa && source venv/bin/activate && python manage.py collectstatic --noinput')
run_cmd('echo \'c0i1uhIPrEpu\' | sudo -S systemctl restart gunicorn')
