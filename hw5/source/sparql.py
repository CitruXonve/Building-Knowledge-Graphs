from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(f"""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?_name ?_edu
    WHERE {{
        [] a dbo:Person ;
            foaf:name ?name ;
            dbo:almaMater [ foaf:name ?edu ] .
        BIND(STR(?name) AS ?_name)
        BIND(STR(?edu) AS ?_edu)
        FILTER(REGEX(?_edu, "(school)|(university)|(college)|(academy)", "i"))
        FILTER(REGEX(?_name, "{'|'.join(list(map(lambda name: f'({name})', 'John Singleton'.split())))}", "i"))
        # FILTER(STR(?name) = "{'Donald Trump'}")
        # FILTER(?_edu = "{'DePaul University'}")
    }}
    # LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

fout = open('sparql_cache.txt', 'w')
cnt = 0
for result in results["results"]["bindings"]:
    # print(result["label"]["value"])
    values = []
    for item in result.items():
        values.append(item[1]['value'])
    # print('\t'.join(values))
    fout.write(str(values)+'\n')
    cnt += 1
print(len(results["results"]["bindings"]))
fout.close()