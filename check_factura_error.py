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

# Get the full traceback around the crearFactura 500 error
out, err = run("echo 'c0i1uhIPrEpu' | sudo -S journalctl -u gunicorn --no-pager -n 300 2>/dev/null | grep -A 20 'crearFactura.*500'")
print("=== TRACEBACK crearFactura ===")
print(out[:3000] if out else "No se encontró traceback")

# Get all log lines around that time
out2, err2 = run("echo 'c0i1uhIPrEpu' | sudo -S journalctl -u gunicorn --no-pager --since '2026-04-09 20:33:00' --until '2026-04-09 20:36:00' 2>/dev/null")
print("\n=== LOGS EN ESE MOMENTO ===")
print(out2[:3000] if out2 else "No hay logs")
