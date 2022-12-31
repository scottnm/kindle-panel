import flask
import json
import html2image
import tempfile
import os
import subprocess

app = flask.Flask(__name__)

PANEL_DATA_JSON_FILE = os.path.join(tempfile.gettempdir(), "kindle_panel_data.json")
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))

def load_panel_data():
    try:
        with open(PANEL_DATA_JSON_FILE, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print("Panel data not found @ %s! Creating and returning default data" % PANEL_DATA_JSON_FILE)
        default_panel_data = { "status": "unset" }
        store_panel_data(default_panel_data)
        return default_panel_data

def store_panel_data(panel_data):
    with open(PANEL_DATA_JSON_FILE, 'w') as f:
        data_str = json.dumps(panel_data, indent=4)
        f.write(data_str)

def load_css_str(path):
    css_file = os.path.join(SCRIPT_DIR, 'static', 'css', 'stylesheet.css')
    with open(path, 'r') as f:
        return f.read()

@app.route('/')
def index():
    panel_data = load_panel_data()
    return flask.render_template('index.html', status=panel_data["status"])

@app.route('/get_status_screenshot')
def get_status_screenshot():
    hti = html2image.Html2Image(output_path=SCRIPT_DIR)
    panel_data = load_panel_data()
    status = panel_data["status"]
    html_str = flask.render_template('index.html', status=status)
    # N.B. for some reason, `screenshot` doesn't seem to work when I pass a css_file parameter. I suspect it's some path
    # problem but I don't want to dig into it now
    css = load_css_str(os.path.join(SCRIPT_DIR, 'static', 'css', 'stylesheet.css'))
    hti.screenshot(html_str=html_str, css_str=css, save_as='kindle_panel_screenshot.png', size=(600, 800))
    convert_result = subprocess.call(
        ["magick", os.path.join(SCRIPT_DIR, "kindle_panel_screenshot.png"),
         "-gravity", "center",
         "-extent", "600x800",
         "-colorspace", "gray",
         "-depth", "8",
         os.path.join(SCRIPT_DIR, "kindle_panel_screenshot_gray8.png")])
    if convert_result != 0:
        print("png gray8 conversion failed!", convert_result)
    return flask.send_file('kindle_panel_screenshot_gray8.png', mimetype='image/png', max_age=0)

@app.route('/set_status')
def set_status():
    query_params = flask.request.args.to_dict()
    status = query_params["status"]
    store_panel_data({ "status":  status })
    return flask.render_template('set_status.html', status=status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
