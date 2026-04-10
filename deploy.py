import paramiko
import sys
import os

def deploy_fixes(host, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        
        sftp = client.open_sftp()
        
        files_to_sync = [
            (r'c:\s\Sistema\wiao\wioa\apps\registros\views.py', '/var/www/wioa/apps/registros/views.py'),
            (r'c:\s\Sistema\wiao\wioa\apps\registros\models.py', '/var/www/wioa/apps/registros/models.py'),
            (r'c:\s\Sistema\wiao\wioa\apps\registros\filters.py', '/var/www/wioa/apps/registros/filters.py'),
            (r'c:\s\Sistema\wiao\wioa\apps\proyecto\models.py', '/var/www/wioa/apps/proyecto/models.py')
        ]
        
        for local_p, remote_p in files_to_sync:
            print(f"[*] Uploading {os.path.basename(local_p)}...")
            sftp.put(local_p, remote_p)
            
        sftp.close()

        print("[*] Restarting Gunicorn...")
        commands = [
            f"echo '{password}' | sudo -S systemctl restart gunicorn"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        print("Deployment Success!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        client.close()

if __name__ == "__main__":
    deploy_fixes('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')
