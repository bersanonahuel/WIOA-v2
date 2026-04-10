import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')

# First upload the corrected views.py file directly
sftp = client.open_sftp()
sftp.put(r'c:\s\Sistema\wiao\wioa\apps\registros\views.py', '/var/www/wioa/apps/registros/views.py')
sftp.close()
print("Uploaded views.py with is_ajax fix")

def run_cmd(cmd):
    print(f"\nRUNNING: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', 'ignore')
    err = stderr.read().decode('utf-8', 'ignore')
    if out: print("OUT:", out.strip())
    if err: print("ERR:", err.strip())

run_cmd("echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn")

client.close()
print("\nDone!")
