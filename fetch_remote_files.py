import paramiko, os

def fetch():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu', timeout=10)
    sftp = client.open_sftp()

    files = [
        '/var/www/wioa/staticfiles/js/app.js',
        '/var/www/wioa/staticfiles/js/registros/registro.js',
    ]

    out_dir = r'c:\s\Sistema\wiao\remote_static'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'registros'), exist_ok=True)

    for f in files:
        local = os.path.join(out_dir, os.path.basename(f))
        if 'registros' in f:
            local = os.path.join(out_dir, 'registros', os.path.basename(f))
        print(f'Downloading {f} -> {local}')
        sftp.get(f, local)

    sftp.close()
    client.close()
    print('Done!')

if __name__ == '__main__':
    fetch()
