import flask
import json

app = flask.Flask(__name__)

PANEL_DATA_JSON_FILE = "/tmp/kindle_panel_data.json"

@app.route('/')
def index():
    with open(PANEL_DATA_JSON_FILE, 'r') as f:
        panel_data = json.loads(f.read())
        return flask.render_template('index.html', status=panel_data["status"])

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
