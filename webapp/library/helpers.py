import subprocess, json, re, codecs, requests

__author__ = 'hendro'

"""
Helper functions
"""
def send_request(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else {'projects': ['']}

def is_engine_activated(engine_name):
    cmd_string = "crontab -l"
    cmd_exec = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
    regex = re.compile("%s" % engine_name)
    return True if regex.search(str(cmd_exec.stdout.read())) else False

def load_engine_db(path):
    with codecs.open(path, 'r+', encoding='utf-8') as f:
        return json.load(f)