import paramiko
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space',2223,'wioa','c0i1uhIPrEpu')

log_conf = """
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/www/wioa/django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
"""

commands = [
    "echo '" + log_conf.replace('\n', '\\n') + "' | sudo -S tee -a /var/www/wioa/WIOA/settings.py",
    "echo 'c0i1uhIPrEpu' | sudo -S touch /var/www/wioa/django_error.log",
    "echo 'c0i1uhIPrEpu' | sudo -S chmod 777 /var/www/wioa/django_error.log",
    "echo 'c0i1uhIPrEpu' | sudo -S systemctl restart gunicorn",
    "sleep 4",
    "curl -sS http://127.0.0.1/accounts/login/?next=/",
    "cat /var/www/wioa/django_error.log"
]

for cmd in commands:
    print('---', cmd[:80])
    if 'tee -a' in cmd:
        stdin,stdout,stderr=client.exec_command(cmd)
        stdin.write('c0i1uhIPrEpu\n')
        stdin.flush()
    else:
        stdin,stdout,stderr=client.exec_command(cmd)
    
    print(stdout.read().decode('utf-8','ignore'))
    print(stderr.read().decode('utf-8','ignore'))
