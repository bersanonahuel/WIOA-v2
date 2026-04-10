import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')
stdin,stdout,stderr=client.exec_command('cat /var/www/wioa/WIOA/settings.py')
with open('remote_settings_now.txt', 'wb') as f:
    f.write(stdout.read())
