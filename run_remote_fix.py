import paramiko
import traceback

def run_remote_fix():
    print("Conectando al servidor ssh...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')
        sftp = client.open_sftp()
        print("Subiendo fix_duplicates.py...")
        sftp.put('fix_duplicates.py', '/var/www/wioa/fix_duplicates.py')
        sftp.close()
        
        print("Ejecutando script...")
        cmd = 'cd /var/www/wioa && ./venv/bin/python fix_duplicates.py'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("STDOUT:")
        for line in stdout:
            print(line, end="")
            
        print("STDERR:")
        for line in stderr:
            print(line, end="")
            
    except Exception as e:
        print("Error:")
        traceback.print_exc()
    finally:
        client.close()

if __name__ == '__main__':
    run_remote_fix()
