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

# Get the last 100 lines of gunicorn logs, filter for errors only
out, err = run("echo 'c0i1uhIPrEpu' | sudo -S journalctl -u gunicorn --no-pager -n 200 2>/dev/null | grep -E '(ERROR|500|Traceback|Exception|Error)' | tail -50")
print("=== ERRORES EN LOGS ===")
print(out if out.strip() else "SIN ERRORES 500 encontrados")
print(err[:500] if err else "")

# Check if gunicorn is running cleanly
out2, err2 = run("echo 'c0i1uhIPrEpu' | sudo -S systemctl is-active gunicorn 2>/dev/null")
print("\n=== ESTADO GUNICORN ===")
print(out2.strip())

# Check nginx status
out3, err3 = run("echo 'c0i1uhIPrEpu' | sudo -S systemctl is-active nginx 2>/dev/null")
print("\n=== ESTADO NGINX ===")
print(out3.strip())
