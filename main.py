import os
import base64
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, make_response, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from Stats import Stats
from werkzeug.utils import secure_filename

# Class Flask
app = Flask(__name__)
CORS(app, expose_headers='Authorization', resources={r"/get/stats": {"origins": "*"},
                                                     r"/get/top-n": {"origins": "*"},
                                                     r"/upload": {"origins": "*"},
                                                     r"/filter/data": {"origins": "*"},
                                                     r"/filter/matches": {"origins": "*"},
                                                     r"/filter/matches-data": {"origins": "*"},
                                                     r"/filter/by-name": {"origins": "*"},
                                                     r"/filter/by-id": {"origins": "*"}
                                                     })
app.route('/')


def base():
    return (
        "<h1 style='color:blue'>This is the home page. Redirect to https://mcmakler-challenge.ey.r.appspot.com/swagger/ for testing the API.</h1>")


@app.route('/static/<path:path>', methods=['POST'])
@cross_origin()
def openSwagger(path):
    return redirect("/swagger", code=200)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app-name': "Technical Challenge - Data Engineer - McMakler"
    })

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/get/stats', methods=['POST'])
@cross_origin()
def get_stats():
    #
    if verify_auth(request.headers) is True:
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'column' in payload_received and 'method' in payload_received:
            column_name = payload_received['column']
            return_method = payload_received['method']
            result = stats_obj.get_result(column_name, return_method)
            if isinstance(result, int) or isinstance(result, list):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            # {
            #     "column":"MSZoning",
            #     "method":"common"
            # } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/get/top-n', methods=['POST'])
@cross_origin()
def get_top_n():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'filters' in payload_received:
            filters = payload_received['filters']
            result = stats_obj.get_sorted_n(filters)
            if isinstance(result, list):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            #     {
            #         "filters":
            #         {"column":["OverallQual", "MSZoning"], "order":[true, false], "limit":7},
            #
            #     } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_data():
    if verify_auth(request.headers):
        return_msg = dict()
        stats_obj = create_object()

        if 'data' in request.files:
            file_content = request.files['data']
            filename = secure_filename(file_content.filename)
            result = stats_obj.store_data(file_content, filename)
            if result:
                return_msg['result'] = "File saved"
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/filter/data', methods=['POST'])
@cross_origin()
def filter_data():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'filters' in payload_received:
            filters = payload_received['filters']
            result = stats_obj.filter_data(filters, 'id')
            if isinstance(result, list):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            #     {
            #         "filters":[
            #         {"column":"OverallQual", "operator":"geq", "value":7},
            #         {"column":"OverallCond", "operator":"geq", "value":8},
            #         ]
            #     } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/filter/matches', methods=['POST'])
@cross_origin()
def filter_matches():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'filters' in payload_received:
            filters = payload_received['filters']
            result = stats_obj.filter_data(filters, 'count')
            if isinstance(result, int):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            #         {
            #             "filters":[
            #             {"column":"OverallQual", "operator":"geq", "value":7},
            #             {"column":"OverallCond", "operator":"geq", "value":8}
            #             ]
            #         } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/filter/matches-data', methods=['POST'])
@cross_origin()
def filter_matches_data():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'filters' in payload_received:
            filters = payload_received['filters']
            result = stats_obj.filter_data(filters)
            if isinstance(result, dict):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            #     {
            #         "filters":[
            #         {"column":"OverallQual", "operator":"geq", "value":7},
            #         {"column":"OverallCond", "operator":"geq", "value":8}
            #         ]
            #     } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


@app.route('/filter/by-name', methods=['POST'])
@cross_origin()
def filter_by_name():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'filters' in payload_received:
            filters = payload_received['filters']
            result = stats_obj.filter_by_string(filters)
            if isinstance(result, int):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204
        else:
            # return_msg['result'] = """Missing values in the received payload. See the below give example payload.\n
            #         {
            #             "filters":[
            #             {"column":"ExterQual","value":"Ex"}
            #             ]
            #         } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401

    return make_response(jsonify(return_msg), status_message)


@app.route('/filter/by-id', methods=['POST'])
@cross_origin()
def filter_by_id():
    if verify_auth(request.headers):
        payload_received = request.get_json()
        return_msg = dict()
        stats_obj = create_object(payload_received)

        if 'ids' in payload_received:
            ids = payload_received['ids']
            result = stats_obj.filter_ids(ids)

            if isinstance(result, dict):
                return_msg['result'] = result
                status_message = 200
            else:
                return_msg = None
                status_message = 204

        else:
            # return_msg['result'] = """Missing ids in the received payload. See the below give example payload.\n
            #         {
            #             "ids":[1, 4, 5, 1000, 1460]
            #         } """
            return_msg = None
            status_message = 400
    else:
        return_msg = None
        status_message = 401
    return make_response(jsonify(return_msg), status_message)


def create_object(payload=dict()):
    return_data = None
    if 'filename' in payload:
        filename = payload['filename']
        if filename == 'data.csv':
            filepath = filename
        else:
            filepath = os.path.join('/tmp', filename)

        if os.path.exists(filepath):
            return_data = Stats(filepath)
        else:
            return_data = Stats()
    else:
        return_data = Stats()
    return return_data


def verify_auth(data):
    # method verifies the header information for authentication
    # extracts username & password from the headers 
    # and validates against ENV variables
    # Receives: header information from request
    # Returns: True or False based on validation
    return_data = None
    if "Authorization" in data:
        credentials = data["Authorization"]
        credentials = credentials.split()[-1]
        env_credentials = os.environ.get('USERNAME') + ":" + os.environ.get('PASSWORD')
        env_credentials_bytes = env_credentials.encode('ascii')
        env_credentials_base64_bytes = base64.b64encode(env_credentials_bytes)
        env_credentials_base64 = env_credentials_base64_bytes.decode('ascii')

        if credentials == env_credentials_base64:
            return_data = True
        else:
            return_data = False
    else:
        return_data = False

    return return_data


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", use_reloader=False)
