from pymantic import sparql

server = sparql.SPARQLServer('http://192.168.1.20:9999/blazegraph/namespace/kb/sparql')

query = 'SELECT ?class WHERE {?class a <http://www.w3.org/2002/07/owl#Class>}'
#query = '''prefix owl: <http://www.w3.org/2002/07/owl#>
#            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#            SELECT ?individual_iri ?individual_label WHERE {
#            ?individual_iri a owl:NamedIndividual;
#                                rdfs:label ?individual_label
#            }'''
#query = 'SELECT ?subject ?predicate ?object WHERE {?subject ?predicate ?object}'
result = server.query(query)
for b in result['results']['bindings']:
    print(b['subject']['value'], b['predicate']['value'], b['object']['value'])