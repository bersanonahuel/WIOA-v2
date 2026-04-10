import paramiko

def run(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu', timeout=15)
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    client.close()
    return out, err

# Check gunicorn error logs
out, err = run("echo 'c0i1uhIPrEpu' | sudo -S journalctl -u gunicorn --no-pager -n 50")
print("=== GUNICORN LOGS ===")
print(out)
print(err)

# Also check the delete view in the actual deployed code
out2, err2 = run("grep -n 'EliminarRegistroDetalle\\|csrf_exempt\\|dispatch' /var/www/wioa/apps/registros/views.py | head -30")
print("=== DELETE VIEW CODE ===")
print(out2)
print(err2)
