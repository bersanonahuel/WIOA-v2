import paramiko

def deploy():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname='wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu', timeout=10)
        
        print('[*] Uploading registro.js')
        sftp = client.open_sftp()
        sftp.put(r'c:\s\Sistema\wiao\wioa\static\js\registros\registro.js', '/var/www/wioa/static/js/registros/registro.js')
        sftp.close()
        
        print('[*] Collecting static files (if necessary) or just restarting...')
        # We might need to run python manage.py collectstatic if Django uses staticfiles,
        # but since developers often just map /static to the folder or run collectstatic manually,
        # maybe we should run it just to be safe.
        stdin, stdout, stderr = client.exec_command("cd /var/www/wioa && source venv/bin/activate && python manage.py collectstatic --noinput && echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
        print('Success!')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    deploy()
