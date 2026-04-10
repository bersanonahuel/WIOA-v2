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

# Get only logs AFTER the last deploy (after 21:20)
out, err = run("echo 'c0i1uhIPrEpu' | sudo -S journalctl -u gunicorn --no-pager --since '2026-04-09 21:20:00' 2>/dev/null | grep -E '(500|ERROR|Traceback|Exception)'")
print("=== ERRORES DESPUES DEL ULTIMO DEPLOY ===")
print(out.strip() if out.strip() else "SIN NINGUN ERROR 500 desde el ultimo deploy")
