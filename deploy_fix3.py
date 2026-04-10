import paramiko

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu', timeout=10)
    
    sftp = client.open_sftp()
    
    files_to_upload = [
        (r'c:\s\Sistema\wiao\wioa\static\js\registros\registro.js', '/var/www/wioa/static/js/registros/registro.js'),
        (r'c:\s\Sistema\wiao\wioa\static\js\app.js',                '/var/www/wioa/static/js/app.js'),
    ]
    
    for local, remote in files_to_upload:
        print(f'[*] Uploading {local} -> {remote}')
        sftp.put(local, remote)
    
    sftp.close()
    
    print('[*] Running collectstatic...')
    stdin, stdout, stderr = client.exec_command(
        'cd /var/www/wioa && source venv/bin/activate && python manage.py collectstatic --noinput 2>&1'
    )
    out = stdout.read().decode()
    print(out)
    
    print('[*] Restarting gunicorn...')
    stdin2, stdout2, stderr2 = client.exec_command(
        "echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn"
    )
    stdout2.read()
    
    client.close()
    print('[+] Deploy done!')

if __name__ == '__main__':
    deploy()
