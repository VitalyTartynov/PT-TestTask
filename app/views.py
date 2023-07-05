from flask import render_template, request, abort
from flask_restx import Resource, Namespace, fields
from flask_restx._http import HTTPStatus

from pymantic import sparql
from app import app, api
from app import configuration

nav = [{'label': 'Home', 'url': '/index'},
       {'label': 'SPARQL1', 'url': '/query/1'},
       {'label': 'SPARQL2', 'url': '/query/2'},
       {'label': 'SPARQL3', 'url': '/query/3'},
       {'label': 'Builder', 'url': '/querybuilder'},
       {'label': 'Swagger UI', 'url': '/api/v1'}]


@app.route('/')
@app.route('/index')
def index():
    """
    Main page without work with database.
    :return:
    """
    data = {'nav': nav,
            'content': 'Navigate to one of the hardcoded requests or simple requests builder'}
    return render_template('index.html', data=data)


@app.route('/query', defaults={'id': 1})
@app.route('/query/<int:id>')
def query(id: int):
    """
    Query pages for concrete requests from task.
    :param id: Request id.
    :return: Page with data from database.
    """
    data = {'nav': nav}
    try:
        server = sparql.SPARQLServer(app.dbendpoint)
        if id > 3:
            return abort(404)
        requestdata = configuration.requests[id-1]
        result = server.query(requestdata['value'])
        bindings = result['results']['bindings']
        data['query'] = requestdata['value']
        data['columnnames'] = requestdata['columns']
        data['result'] = bindings
    except Exception as err:
        data['errors'] = err
    return render_template('query.html', data=data)


@app.route('/querybuilder', methods = ['GET', 'POST'])
def querybuilder():
    """
    Additional page for executing input queries.
    :return: Page for input query and show results.
    """
    data = {'nav': nav,
            'query': configuration.requests[0]['value']}
    if request.method == 'POST':
        try:
            server = sparql.SPARQLServer(app.dbendpoint)
            newquery = request.form.get('query')
            result = server.query(newquery)
            data['query'] = newquery
            data['result'] = result['results']['bindings']
        except Exception as err:
            data['errors'] = err
    return render_template('querybuilder.html', data=data)


sparqlNsp = Namespace('api/v1')
execCommand = sparqlNsp.model('Exec SPARQL query', {'query': fields.String(required=True, description='Raw SPARQL')})
api.add_namespace(sparqlNsp)

@sparqlNsp.route('/rawsparql')
class RawRequests(Resource):
    """
    API for execute raw SPARQL queries
    """

    @sparqlNsp.expect(execCommand)
    @api.response(HTTPStatus.OK.value, "Request completed")
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, "Internal server error")
    def post(self):
        """
        Query raw SPARQL requests.
        """
        try:
            body = request.get_json()
            rawquery = body['query']
            server = sparql.SPARQLServer(configuration.dbendpoint)
            result = server.query(rawquery)
            return result['results']['bindings']
        except Exception as err:
            return abort(500, err)

@app.errorhandler(404)
def not_found(error: int):
    """
    Not found page.
    :param error: Error number.
    :return: Page with description.
    """
    data = {'nav': nav,
            'content': '404! Page not found'}
    return render_template('index.html', data=data)