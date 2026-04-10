import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')

def run_cmd(cmd):
    print("Running:", cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', 'ignore')
    err = stderr.read().decode('utf-8', 'ignore')
    with open('collect_out.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n[{cmd}]\nSTDOUT:\n{out}\nSTDERR:\n{err}\n")

with open('collect_out.txt', 'w', encoding='utf-8') as f:
    f.write("Log START\n")

run_cmd("cd /var/www/wioa && source venv/bin/activate && python manage.py migrate --noinput")
run_cmd("cd /var/www/wioa && source venv/bin/activate && python manage.py collectstatic --noinput")
run_cmd("echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn")
