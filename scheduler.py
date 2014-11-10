"""
==================================================================================
Scheduler script to submit crawling jobs schedule
==================================================================================
"""

import sys, getopt, subprocess, json

__author__ = 'Hendro Wibowo (hendrothemail@gmail.com)'
__version__ = '1.0'

from os import listdir
from os.path import isfile, join, splitext

from the_crawler.settings import SITE_CONFIG_PATH

def main(argv):
    if len(sys.argv) == 1:
        raise getopt.GetoptError
    
    opts, args = getopt.getopt(argv, "c:")
    config_path = SITE_CONFIG_PATH
    for opt, channel in opts:
        full_config_path = config_path + channel
        for f in listdir(full_config_path):
            if isfile(join(full_config_path, f)):        
                cmd = "curl http://localhost:6800/schedule.json -d project=%s -d spider=%s -d domain=%s -d channel=%s" \
                        % ('the_crawler', 'TheCrawlerEngineV1', splitext(f)[0], channel)
                subprocess.call(cmd.split())     

def is_project_exists():
    cmd_list_project = "curl http://localhost:6800/listprojects.json"
    cmd_exec = subprocess.Popen(cmd_list_project.split(), stdout=subprocess.PIPE)
    output = json.loads(cmd_exec.stdout.read())

    return True if len(output['projects']) > 0 else False
    
if __name__ == "__main__":
    if(is_project_exists()):
        main(sys.argv[1:])
    else:
        print "No project is exists!"
    