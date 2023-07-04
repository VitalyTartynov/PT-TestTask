_sparql1 = {'value': 'SELECT ?class WHERE {?class a <http://www.w3.org/2002/07/owl#Class>}',
            'columns': ['class']}
_sparql2 = {'value': '''prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?individual_iri ?individual_label WHERE {
            ?individual_iri a owl:NamedIndividual;
                                rdfs:label ?individual_label
            }''', 'columns': ['individual_iri', 'individual_label']}
_sparql3 = {'value': 'SELECT ?subject ?predicate ?object WHERE {?subject ?predicate ?object}',
            'columns': ['subject', 'predicate', 'object']}

dbendpoint = 'http://192.168.1.20:9999/blazegraph/namespace/kb/sparql'
requests = [_sparql1, _sparql2, _sparql3]
