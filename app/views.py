from flask import render_template, request, abort
from pymantic import sparql
from app import app
from app import configuration

nav = [{'label': 'Home', 'url': '/index'},
       {'label': 'SPARQL1', 'url': '/query/1'},
       {'label': 'SPARQL2', 'url': '/query/2'},
       {'label': 'SPARQL3', 'url': '/query/3'},
       {'label': 'Builder', 'url': '/querybuilder'}]

# сверстать на блоках? https://jinja.palletsprojects.com/en/3.1.x/templates/#blocks
@app.route('/')
@app.route('/index')
def index():
    data = {'nav': nav,
            'content': 'Navigate to one of the hardcoded requests or simple requests builder'}
    return render_template('index.html', data=data)


@app.route('/query', defaults={'id': 1})
@app.route('/query/<int:id>')
def query(id: int):
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


@app.post('/rawsparql')
def raw_sparql():
    """Query raw SPARQL requests.
    ---
    parameters:
        name: body
        in: body
    responses:
        200:
            description: Request completed
            schema:
                type: array
                items:
                    type: string
        500:
            description: Request failed
            schema:
                type: string
    """
    try:
        query = request.get_data(as_text=True)
        server = sparql.SPARQLServer(configuration.dbendpoint)
        result = server.query(query)
        return result['results']['bindings']
    except Exception as err:
        return abort(500, err)

@app.errorhandler(404)
def not_found(error: int):
    data = {'nav': nav,
            'content': '404! Page not found'}
    return render_template('index.html', data=data)

# TODO: а может так?
# current_app.response_class(
#            response=json.dumps(
#                {'error': 'Не передан параметр number'}
#            ),
#            status=400,
#            mimetype='application/json'
#        )