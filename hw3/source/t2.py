from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF
import dateutil.parser as parser
import json

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
MYNS = Namespace('http://inf558.org/myfakenamespace#')
SCHEMA = Namespace('http://schema.org/')

my_kg = Graph()
my_kg.bind('my_ns', MYNS)
my_kg.bind('foaf', FOAF)
my_kg.bind('schema', SCHEMA)

# node_uri = URIRef(MYNS['inf558_production_company'])
# my_kg.add((node_uri, RDF.type, MYNS['productionCompany']))
# my_kg.add((node_uri, FOAF['name'], Literal('INF 558 Production Company')))

imdb_file = 'imdb.jl'
afi_file = 'afi.jl'
result_file = 'Zongdi_Xu_hw03_imdb_afi_el.json'

r_imdb = {}
with open(imdb_file, 'r') as fin:
    for line in fin.readlines():
        item = json.loads(line)
        r_imdb[item['url']]=item
    fin.close()

r_afi = {}
with open(afi_file, 'r') as fin:
    for line in fin.readlines():
        item = json.loads(line)
        r_afi[item['url']]=item
    fin.close()

joint_movies = []
all_companies = set()
with open(result_file) as fin:
    for item in json.loads(fin.read()):
        if item['imdb_movie'] is not None:
            url = item['imdb_movie']
            if item['afi_movie'] is not None:
                new_item = r_afi.get(item['afi_movie'], {}).copy()
                new_item.update(r_imdb.get(item['imdb_movie'], {}))
            else:
                new_item = r_imdb.get(item['imdb_movie'], {}).copy()
            joint_movies.append(new_item)
            all_companies.add(new_item.get('production_company', ''))

URI_companies = {}

count = 0
for company in sorted(all_companies):
    if company == '':
        continue
    uri = 'company_%07d' % count
    URI_companies[company] = uri
    my_kg.add((MYNS.__getitem__(uri), RDF.type, MYNS['productionCompany']))
    my_kg.add((MYNS.__getitem__(uri), FOAF.name, Literal(company)))
    count += 1

for new_item in joint_movies:
    url = new_item['url']
    node_uri = URIRef(url)
    my_kg.add((node_uri, RDF.type, MYNS['Movie']))
    my_kg.add((node_uri, SCHEMA.headline, Literal(new_item.get('title'))))
    my_kg.add((node_uri, SCHEMA.datePublished, Literal(parser.parse(str(new_item.get('release_date', new_item.get('year')))).date(), datatype=XSD.date))) # release-date
    my_kg.add((node_uri, SCHEMA.contentRating, Literal(new_item.get('certificate')))) # certificate
    my_kg.add((node_uri, SCHEMA.duration, Literal(new_item.get('runtime'), datatype=XSD.time))) # runtime
    my_kg.add((node_uri, SCHEMA.genre, Literal(new_item.get('genre')))) # genre
    my_kg.add((node_uri, MYNS.imdbRating, Literal(new_item.get('rating')))) # imdb-rating
    my_kg.add((node_uri, MYNS.imdbMetascore, Literal(new_item.get('metascore')))) # imdb-metascore
    my_kg.add((node_uri, MYNS.imdbVotes, Literal(new_item.get('votes')))) # imdb-votes
    my_kg.add((node_uri, MYNS.grossIncome, Literal(new_item.get('gross')))) # gross-income
    my_kg.add((node_uri, SCHEMA.producer, Literal(new_item.get('producer')))) # producer
    my_kg.add((node_uri, SCHEMA.author, Literal(new_item.get('writer')))) # writer
    my_kg.add((node_uri, MYNS.cinematographer, Literal(new_item.get('cinematographer')))) # cinematographer

    if new_item.get('production_company') is not None:
        my_kg.add((node_uri, SCHEMA.productionCompany, MYNS[URI_companies[new_item.get('production_company')]])) # production-company
    else:
        my_kg.add((node_uri, SCHEMA.productionCompany, Literal(None))) # production-company

my_kg.serialize('Zongdi_Xu_hw03_movie_triples.ttl', format="turtle")