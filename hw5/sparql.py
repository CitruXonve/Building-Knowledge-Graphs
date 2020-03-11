from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT STR(?name) AS ?_name, STR(?edu) AS ?_edu
    WHERE {{
        [] a dbo:Person ;
            rdfs:label ?name ;
            dbo:almaMater [ rdfs:label ?edu ] .
        FILTER(STR(?name) = "{'Donald Trump'}")
        # FILTER(STR(?edu) = "{'University of Pennsylvania'}")
    }}
    # LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    # print(result["label"]["value"])
    values = []
    for item in result.items():
        values.append(item[1]['value'])
    print('\t'.join(values))