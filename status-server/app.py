import flask
import json
import html2image

app = flask.Flask(__name__)

PANEL_DATA_JSON_FILE = "/tmp/kindle_panel_data.json"

@app.route('/')
def index():
    with open(PANEL_DATA_JSON_FILE, 'r') as f:
        panel_data = json.loads(f.read())
        return flask.render_template('index.html', status=panel_data["status"])

@app.route('/get_status_screenshot')
def get_status_screenshot():
    hti = html2image.Html2Image()
    status=None
    panel_data = None
    with open(PANEL_DATA_JSON_FILE, 'r') as f:
        panel_data = json.loads(f.read())
    status = panel_data["status"]
    html_str = flask.render_template('index.html', status=status)
    print("Returning screnshot with status ", status)
    hti.screenshot(html_str=html_str, save_as='kindle_panel_screenshot.png', size=(600, 800))
    return flask.send_file('kindle_panel_screenshot.png', mimetype='image/png')

@app.route('/set_status')
def set_status():
    query_params = flask.request.args.to_dict()
    print(query_params["new_status"])
    updated_panel_data_json = json.dumps({ "status": query_params["new_status"] }, indent=4)
    with open(PANEL_DATA_JSON_FILE, 'w') as f:
        f.write(updated_panel_data_json)
    return flask.render_template('set_status.html', new_status=query_params["new_status"])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
