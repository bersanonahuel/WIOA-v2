import paramiko
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space',2223,'wioa','c0i1uhIPrEpu')
stdin,stdout,stderr=client.exec_command('cat /var/www/wioa/django_error.log')
with open('remote_error.log', 'w', encoding='utf-8') as f:
    f.write(stdout.read().decode('utf-8', 'ignore'))
