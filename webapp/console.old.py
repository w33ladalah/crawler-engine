from os import listdir, rename
from os.path import isfile, join, splitext
import subprocess
import json
import re
import codecs
import requests

from bottle import Bottle, run, request, response, static_file, template, redirect

from config import USERNAME, PASSWORD, SECRET, APP_NAME, CONSOLE_ROOT_DIR, DB_PATH, CONFIG_PATH
from webapp.library import AutoVivification


app = Bottle()
scrapyd_api_url = "http://engine.lintas.me:6800"

@app.route('/')
@app.route('/login')
def login():
    username = request.get_cookie("account", secret=SECRET)
    if username:
        redirect("/home")
    else:
        return template('page_login', title=APP_NAME)


@app.route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if check_login(username, password):
        response.set_cookie("account", username, secret=SECRET)

        redirect("/home")
    else:
        redirect("/login")


@app.route('/home')
def engine_list():
    username = request.get_cookie("account", secret=SECRET)

    if username:
        engine_config = load_engine_db(DB_PATH)
        engines = engine_config['engine']
        try:
            post_to_lintas = engine_config['post_to_lintas']
        except KeyError:
            post_to_lintas = "No"
        engine_count = len(engines)
        engine_list = AutoVivification()
        for engine in engines:
            engine_list[engine]['status'] = "ACTIVE" if is_engine_activated(engine.lower()) else "INACTIVE"
            engine_list[engine]['cmd'] = engines[engine]['cmd']
            engine_list[engine]['minute_run_at'] = engines[engine]['run_at'][0]
            engine_list[engine]['hour_run_at'] = engines[engine]['run_at'][1]
        try:
            running_project = "text-primary|" + send_request("%s/listprojects.json" % scrapyd_api_url)['projects'][0]
            running_spider = "text-primary|" + send_request("%s/listspiders.json?project=%s" % (scrapyd_api_url, running_project.split('|')[1]))['spiders'][0]
            project_version = "text-primary|" + send_request("%s/listversions.json?project=%s" % (scrapyd_api_url, running_project.split('|')[1]))['versions'][0]
        except requests.ConnectionError:
            running_project = "text-danger|CRAWLER SERVER IS DOWN"
            running_spider = "text-danger|CRAWLER SERVER IS DOWN"
            project_version = "text-danger|CRAWLER SERVER IS DOWN"
        except IndexError:
            running_project = "text-danger|NO CRAWLER PROJECT RUNNING"
            running_spider = "text-danger|NO CRAWLER PROJECT RUNNING"
            project_version = "text-danger|NO CRAWLER PROJECT RUNNING"

        return template('_layout/layout.html', title=APP_NAME, name=username, page='main', running_project=running_project, running_spider=running_spider, project_version=project_version, engine_count=engine_count, engines=engine_list, post_to_lintas=post_to_lintas)
    else:
        redirect("/login")


@app.route('/information')
def general_information():
    username = request.get_cookie("account", secret=SECRET)

    if username:
        engine_count = len(load_engine_db(DB_PATH)['engine'])
        try:
            running_project = "text-primary|" + send_request("%s/listprojects.json" % scrapyd_api_url)['projects'][0]
            running_spider = "text-primary|" + send_request("%s/listspiders.json?project=%s" % \
                                                            (scrapyd_api_url, running_project.split('|')[1]))[
                'spiders'][0]
            project_version = "text-primary|" + send_request("%s/listversions.json?project=%s" % \
                                                             (scrapyd_api_url, running_project.split('|')[1]))[
                'versions'][0]
        except requests.ConnectionError:
            running_project = "text-danger|CRAWLER SERVER IS DOWN"
            running_spider = "text-danger|CRAWLER SERVER IS DOWN"
            project_version = "text-danger|CRAWLER SERVER IS DOWN"
        except IndexError:
            running_project = "text-danger|NO CRAWLER PROJECT RUNNING"
            running_spider = "text-danger|NO CRAWLER PROJECT RUNNING"
            project_version = "text-danger|NO CRAWLER PROJECT RUNNING"
        return template('_layout/layout.html', title=APP_NAME, name=username, page='informations', \
                        running_project=running_project, running_spider=running_spider, project_version=project_version, \
                        engine_count=engine_count)
    else:
        redirect('/login')

"""
Activate or deactivate engine. If engine is activated then will submitted to crontab jobs.
"""
@app.route('/engine/<engine_name>/<minute>/<hour>/<cmd>')
def activate_deactivate_engine(engine_name, minute, hour, cmd):
    cmd_string = 'sh %s/shell/set_cron.sh %s %s %s %s' % \
                 (CONSOLE_ROOT_DIR, minute, '*/%s' % hour, engine_name, 'APPEND' if cmd == 'activate' else 'REMOVE')
    cmd_exec = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)

    if str(cmd_exec.stdout.read()) == "":
        redirect("/home")


@app.route('/new_engine')
def add_engine():
    username = request.get_cookie("account", secret=SECRET)

    if username:
        return template('_layout/layout.html', title=APP_NAME, name=username, page='add_engine')
    else:
        redirect('/login')


@app.route('/new_engine', method='POST')
def add_engine_action():
    username = request.get_cookie("account", secret=SECRET)

    if username:
        engine_name = request.forms.get('engine')
        cmd = request.forms.get('cmd')
        at_hour = request.forms.get('run_at').split(':')[0]
        at_minute = request.forms.get('run_at').split(':')[1]

        with codecs.open(DB_PATH, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['engine']["%s%s" % (engine_name[0].upper(), engine_name[1:])] = {
                'cmd': cmd,
                'run_at': [int(at_minute), int(at_hour)]
            }
            f.seek(0)
            json.dump(data, f, indent=4)
        redirect('/home')
    else:
        redirect('/login')


@app.route('/engine/<engine_name>/edit')
def update_engine(engine_name):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        engine = load_engine_db(DB_PATH)['engine']["%s%s" % (engine_name[0].upper(), engine_name[1:])]
        engine_name = "%s%s" % (engine_name[0].upper(), engine_name[1:])
        return template('_layout/layout.html', title=APP_NAME, name=username, page='update_engine', \
                        engine_name=engine_name, engine_data=engine)
    else:
        redirect('/login')


@app.route('/engine/<engine_name>/edit', method='POST')
def action_update_engine(engine_name):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        cmd = request.forms.get('cmd')
        at_hour = request.forms.get('run_at').split(':')[0]
        at_minute = request.forms.get('run_at').split(':')[1]

        with codecs.open(DB_PATH, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['engine']["%s%s" % (engine_name[0].upper(), engine_name[1:])] = {
                'cmd': cmd,
                'run_at': [int(at_minute), int(at_hour)]
            }
            f.seek(0)
            json.dump(data, f, indent=4)
        redirect('/home')
    else:
        redirect('/login')


@app.route('/engine/<engine_name>/delete')
def action_delete_engine(engine_name):
    username = request.get_cookie("account", secret=SECRET)
    if username:
        with open(DB_PATH) as f:
            data = json.load(f)
            for item in data['engine']:
                real_engine_name = "%s%s" % (engine_name[0].upper(), engine_name[1:])
                if item == real_engine_name:
                    data['engine'].pop(item)
                    break
        open(DB_PATH, "w").write(json.dumps(data, sort_keys=True, indent=4))
        redirect('/home')
    else:
        redirect('/login')


@app.route('/engine/rebuild', method='POST')
def recompile_and_upload():
    version = request.forms.get('version')
    run_engine_compiler(version)


@app.route('/site_config/<engine_name>')
def list_site_config(engine_name):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        cfg_path = "%s/site_config/%s" % (CONFIG_PATH, engine_name)
        domains = [splitext(f)[0] for f in listdir(cfg_path) if isfile(join(cfg_path, f))]
        return template('_layout/layout.html', title=APP_NAME, name=username, page='site_config', \
                        site_config_path=cfg_path, site_configs=domains, engine=engine_name)
    else:
        redirect('/login')


@app.route('/site_config/<engine_name>/add')
def add_site_config(engine_name):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        return template('_layout/layout.html', title=APP_NAME, name=username, page='add_site_config', \
                        engine_name=engine_name)
    else:
        redirect('/login')


@app.route('/site_config/<engine_name>/add', method='POST')
def action_add_site_config(engine_name):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        domain = request.forms.get('domain')
        configuration = request.forms.get('configuration')
        cfg_path = "%s/site_config/%s/%s.txt" % (CONFIG_PATH, engine_name, domain)
        file = open(cfg_path, "w")
        file.write(configuration)
        file.close()
        redirect('/site_config/%s' % engine_name)
    else:
        redirect('/login')


@app.route('/site_config/<engine_name>/<domain>/edit')
def update_site_config(engine_name, domain):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        domain = domain.replace('_', '.')
        cfg_path = "%s/site_config/%s/%s.txt" % (CONFIG_PATH, engine_name, domain)
        config_content = open(cfg_path).read()
        return template('_layout/layout.html', title=APP_NAME, name=username, page='update_site_config', \
                        engine_name=engine_name, domain=domain, configuration=config_content)
    else:
        redirect('/login')


@app.route('/site_config/<engine_name>/<domain>/edit', method='POST')
def action_update_site_config(engine_name, domain):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        cfg_path = "%s/site_config/%s/%s.txt" % (CONFIG_PATH, engine_name, domain.replace('_', '.'))
        file = open(cfg_path, "w")
        file.write(request.forms.get('configuration'))
        file.close()
        redirect('/site_config/%s' % engine_name)
    else:
        redirect('/login')


@app.route('/site_config/<engine_name>/<domain>/delete')
def soft_delete_site_config(engine_name, domain):
    username = request.get_cookie("account", secret=SECRET)

    if username:
        src_cfg_path = "%s/site_config/%s/%s.txt" % (CONFIG_PATH, engine_name, domain.replace('_', '.'))
        dst_cfg_path = "%s/site_config/others/%s.txt" % (CONFIG_PATH, domain.replace('_', '.'))
        rename(src_cfg_path, dst_cfg_path)
        redirect('/site_config/%s' % engine_name)
    else:
        redirect('/login')


@app.route('/logout')
def logout():
    response.delete_cookie("account")
    redirect("/login")


@app.route('/assets/<file_path:path>')
def server_static(file_path):
    return static_file('%s/theme/%s' % (CONSOLE_ROOT_DIR, file_path), root='/')


@app.error(404)
def error404(error):
    return '<center><img src="/assets/image/404.jpg" height="500" /><br><h1>Hollaaa...!!! hahahahaha...!!!</h1>' \
           '<p>404 not found...!!!</p></center>'


def send_request(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else {'projects': ['']}


def is_engine_activated(engine_name):
    cmd_string = "crontab -l"
    cmd_exec = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
    regex = re.compile("%s" % engine_name)
    return True if regex.search(str(cmd_exec.stdout.read())) else False


def run_engine_compiler(version):
    cmd_string = 'sh %s/shell/compiler.sh %s' % (CONSOLE_ROOT_DIR, version)
    cmd_exec = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
    print str(cmd_exec.stdout.read())


def check_login(username, password):
    return True if ( username == USERNAME and password == PASSWORD ) else False


def load_engine_db(path):
    with codecs.open(path, 'r+', encoding='utf-8') as f:
        return json.load(f)

# Run the application
run(app, host='0.0.0.0', port=1421, reloader=True)