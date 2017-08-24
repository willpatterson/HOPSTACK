import os
import paramiko
import urllib.request
from urllib.parse import urlparse
import json

def exec_ssh_command(ip, username, rsa_key):
    print(os.path.expanduser('~/.ssh'))
    ssh = paramiko.SSHClient()

    private_key = paramiko.RSAKey.from_private_key_file(os.path.expanduser('./id_rsa_hop_lab'))
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('127.0.0.1', username='will', pkey=private_key)

    return ssh.exec_command('say test')



"""
import pycurl
from io import BytesIO
buffer = BytesIO()
with open('out.html', 'wb') as f:
    c = pycurl.Curl()
    #c.setopt(c.URL, 'http://www.lipsum.com/')
    c.setopt(c.URL, 'https://docs.python.org/2/library/io.html')
    c.setopt(c.WRITEDATA, f)
    c.perform
    c.close()

#body = buffer.getvalue()

#print(body.decode('iso-8859-1'))

#READ website

page = urllib.request.urlopen('http://www.lipsum.com/')
page = urllib.request.urlopen('http://www.google.com/')
page = urllib.request.urlopen('https://docs.python.org/2/library/io.html')
print(page.read())


ssh = paramiko.SSHClient()

private_key = paramiko.RSAKey.from_private_key_file(os.path.expanduser('./id_rsa_hop_lab'))
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='will', pkey=private_key)

stdin, stdout, stderr = ssh.exec_command('say testy')


#TEST urt
"""

def parse_raw_urt(urt):
    """TAKES a URT as a string or a dictionary containing unparsed strings
    and returns a dictoinary with parsed urls
    """
    if isinstance(urt, str):
        urt = json.loads(urt)
    try:
        if isinstance(urt['src'], str) or not urt['src'].__iter__:
            urt['src'] = [urt['src'],]
        if (isinstance(urt['dest'], str)) or not urt['dest'].__iter__:
            urt['dest'] = [urt['dest'],]

        for count, i in enumerate(urt['src']):
            urt['src'][count] = urlparse(i)
        for count, i in enumerate(urt['dest']):
            urt['dest'][count] = urlparse(i)
    except TypeError:
        raise ValueError('URT must a dictionary or json object with a src and dest feilds')

    return urt

if __name__ == '__main__':
    urt = {'src': ['ssh://will@base.local:~/Documents/DevBench/HOPSTACK/hopstack/htd/transfer_test.txt'], 'translation': None, 'dest': ['ssh://will@satelite.local:~/Documents/DevBench/HOPSTACK/hopstack/hdt/transfer_test_result.txt']}
    urt_json_str = json.dumps(urt)
    print(parse_raw_urt(urt))
    urt2 = {'src': 'ssh://will@base.local:~/Documents/DevBench/HOPSTACK/hopstack/htd/transfer_test.txt', 'translation': None, 'dest': 'ssh://will@satelite.local:~/Documents/DevBench/HOPSTACK/hopstack/hdt/transfer_test_result.txt'}
    print(parse_raw_urt(urt2))
