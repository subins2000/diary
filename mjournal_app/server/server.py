import os

from flask import Flask, request, render_template, send_from_directory, jsonify
from mjournal import Entries


root_loc = None
server_loc = os.path.dirname(os.path.abspath(__file__))

template_loc = os.path.join(server_loc, 'templates')
server = Flask('mjournal', template_folder=template_loc)

def get_template_content(filename):
    global server_loc

    path = os.path.join(server_loc, 'templates', filename)

    with open(path, 'r') as myfile:
        data = myfile.read().replace('\n', '')

    return data

@server.route('/')
@server.route('/write')
@server.route('/settings')
def index(path = None):
    return render_template('index.html',
        home_template=get_template_content('home.html'),
        write_template=get_template_content('write.html'),
        settings_template=get_template_content('settings.html')
    )

@server.route('/js/<path:path>')
def send_js(path):
    global server_loc

    js_loc = os.path.join(server_loc, 'static', 'js')

    return send_from_directory(js_loc, path)

@server.route('/css/<path:path>')
def send_css(path):
    global server_loc

    css_loc = os.path.join(server_loc, 'static', 'css')

    return send_from_directory(css_loc, path)

@server.route('/fonts/<path:path>')
def send_fonts(path):
    global server_loc

    fonts_loc = os.path.join(server_loc, 'static', 'fonts')

    return send_from_directory(fonts_loc, path)

'''
AJAX Routes
'''

@server.route('/ajax/save', methods=['POST'])
def ajax_save():
    global root_loc

    entry_id = request.form['id']
    entry_content = request.form['content']

    entries = Entries(root_loc)
    entries.save_entry(entry_id, entry_content)

    return 'saved'

@server.route('/ajax/getEntries', methods=['GET'])
def ajax_get_entries():
    global root_loc

    entries = Entries(root_loc)
    all_entries = entries.get_all_entries()

    return jsonify(all_entries)

def run_server(root_loc_passed):
    global server, root_loc

    root_loc = root_loc_passed

    '''
    UPDATE templates on change
    '''
    server.config['TEMPLATES_AUTO_RELOAD'] = 'true'

    server.run(port=8786)
