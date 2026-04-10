import paramiko
import io
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

with io.open('status_output.txt', 'w', encoding='utf-8') as f:
    stdin, stdout, stderr = client.exec_command('sudo -S -H systemctl status gunicorn')
    stdin.write('c0i1uhIPrEpu\n')
    stdin.flush()
    f.write('GUNICORN:\n' + stdout.read().decode('utf-8', 'ignore'))

    stdin, stdout, stderr = client.exec_command('sudo -S -H systemctl status nginx')
    stdin.write('c0i1uhIPrEpu\n')
    stdin.flush()
    f.write('\nNGINX:\n' + stdout.read().decode('utf-8', 'ignore'))

    stdin, stdout, stderr = client.exec_command('sudo -S -H journalctl -u gunicorn -n 20 --no-pager')
    stdin.write('c0i1uhIPrEpu\n')
    stdin.flush()
    f.write('\nJOURNAL:\n' + stdout.read().decode('utf-8', 'ignore'))

