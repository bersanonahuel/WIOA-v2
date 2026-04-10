import paramiko
import sys
import os

def upload_and_restart(host, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        
        print("[*] Uploading models.py via SFTP to /var/www/wioa/apps/registros/...")
        sftp = client.open_sftp()
        sftp.put(r'c:\s\Sistema\wiao\wioa\apps\registros\models.py', '/var/www/wioa/apps/registros/models.py')
        sftp.close()

        print("[*] Restarting Gunicorn...")
        commands = [
            f"echo '{password}' | sudo -S systemctl restart gunicorn"
        ]
        
        for cmd in commands:
            print(f"[*] Running: {cmd[:80]}...")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            if out: print("STDOUT: " + out.strip())
            if err: print("STDERR: " + err.strip())
                
        print("Success!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        client.close()

if __name__ == "__main__":
    host = 'wioav2.nserver.space'
    port = 2223
    user = 'wioa'
    password = 'c0i1uhIPrEpu'
    upload_and_restart(host, port, user, password)
