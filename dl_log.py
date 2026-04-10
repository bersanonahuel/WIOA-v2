import paramiko
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space',2223,'wioa','c0i1uhIPrEpu')
sftp = client.open_sftp()
print(sftp.open('/var/www/wioa/django_error.log').read().decode())
sftp.close()
