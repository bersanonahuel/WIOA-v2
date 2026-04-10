import paramiko

def run_remote_command(host, port, username, password, command):
    print(f"[*] Running: {command[:80]}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        if out: print("STDOUT:\n" + out.strip())
        if err: print("STDERR:\n" + err.strip())
        print(f"[*] Exit Status: {exit_status}\n")
        return exit_status
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        client.close()

host = 'wioav2.nserver.space'
port = 2223
user = 'wioa'
password = 'c0i1uhIPrEpu'

run_remote_command(host, port, user, password, "echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn")
run_remote_command(host, port, user, password, "echo 'c0i1uhIPrEpu' | sudo -S systemctl status gunicorn --no-pager")
