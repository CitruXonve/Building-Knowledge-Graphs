from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
MYNS = Namespace('http://inf558.org/myfakenamespace#')

my_kg = Graph()
my_kg.bind('myns', MYNS)
my_kg.bind('foaf', FOAF)

node_uri = URIRef(MYNS['inf558_production_company'])
my_kg.add((node_uri, RDF.type, MYNS['productionCompany']))

my_kg.add((node_uri, FOAF['name'], Literal('INF 558 Production Company')))

my_kg.serialize('sample_graph.ttl', format="turtle")