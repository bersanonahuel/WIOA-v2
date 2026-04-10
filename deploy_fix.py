import paramiko

def deploy():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname='wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu', timeout=10)
        
        print('[*] Uploading views.py')
        sftp = client.open_sftp()
        sftp.put(r'c:\s\Sistema\wiao\wioa\apps\registros\views.py', '/var/www/wioa/apps/registros/views.py')
        sftp.close()
        
        print('[*] Restarting gunicorn')
        stdin, stdout, stderr = client.exec_command("echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
        print('Success!')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    deploy()
