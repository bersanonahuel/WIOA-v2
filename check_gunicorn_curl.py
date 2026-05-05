import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

# Make a request using the local dev server or just simple python to make a request locally to gunicorn
cmd = "curl -i http://unix:/run/gunicorn/gunicorn.sock:/"
stdin, stdout, stderr = client.exec_command(cmd)
print("OUT:", stdout.read().decode('utf-8', errors='ignore'))
print("ERR:", stderr.read().decode('utf-8', errors='ignore'))
