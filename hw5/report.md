# INF 558: Building Knowledge Graphs
## Report of Homework5
## Information Extraction II
### Author: Zongdi Xu (USC ID 5900-5757-70)
### Date: Mar 11, 2020

### Task 1.1

(Refer to uploaded files)

### Task 1.2

#### 1.2.1 Labeling functions

  ```python
  from snorkel.lf_helpers import (
      get_left_tokens, get_right_tokens, get_between_tokens,
      get_text_between, get_tagged_text, contains_token
  )


  import random, sys

  # TODO: Define your LFs here, below is a very simple LF
  def LF_random(c):
      return round(random.random())

  def LF_distance(c):
      return 1 if len(list(get_between_tokens(c)))<7 else -1

  def LF_hash(c):
      return (hash(c.person.get_span())+hash(c.organization.get_span())+sys.maxsize) % 2 * 2 -1

  def LF_right_detect(c):
      return 1 if contains_token(c, 'school') or contains_token(c, 'college') \
          or contains_token(c, 'university') \
          else -1

  def LF_between_detect_refined(c):
      candidate_predicates = list(get_between_tokens(c))
      prepositions = {'at', 'from', 'to'}
      intransitive_predicates = {'graduated', 'studied', 'enrolled',  'went', 'returned', 'educated'}
      transitive_predicates = {'attended'}
      phrases = {'member', 'of'}
      if len(transitive_predicates.intersection(candidate_predicates))>0 or \
          len(prepositions.intersection(candidate_predicates))>0 and \
              len(intransitive_predicates.intersection(candidate_predicates))>0 \
          or len(phrases.intersection(candidate_predicates))>1:
          return 1 
      return -1

  def LF_combined(c):
      if LF_between_detect_refined(c)==1 and LF_right_detect(c)==1:
          return 1
      return -1

  def LF_combined_refined(c):
      taboo = {'later', 'here', 'there'}
      if LF_combined(c)==1 and not len(taboo.intersection(get_between_tokens(c)))>0:
          return 1
      return -1
  ```

#### 1.2.2 Performance

* Score of generative model
  
  ![](./task1.2.2-1.png)

* Detailed statistics about LFs learned by generative model 
  
  ![](./task1.2.2-2.png)
  
#### 1.2.3 Distribution of training marginals

  ![](./task1.2.3.png)

#### 1.2.4 Comment of marginal distribution

  It is rather good because it shows a clear differentiation between 0.0 and 1.0.

### Task 1.3

#### 1.3.1 Additional Labeling Function

```python
  from SPARQLWrapper import SPARQLWrapper, JSON


  def LF_distant_supervision(c):
      if not LF_right_detect(c)==1:
          return -1
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
              FILTER(REGEX(?_name, "{'|'.join(list(map(lambda name: f'({name})', c.person.get_span().split())))}", "i"))
              # FILTER(STR(?name) = "{c.person.get_span()}")
              FILTER(?_edu = "{c.organization.get_span()}")
          }}
          # LIMIT 10
      """)
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
      return 1 if len(results["results"]["bindings"])>0 else -1
```

#### 1.3.2 Performance

* Score of generative model
  
  ![](./task1.3.2-1.png)

* Detailed statistics about LFs learned by generative model 
  
  ![](./task1.3.2-2.png)

#### 1.3.3 Distribution of training marginals

  ![](./task1.3.3.png)

#### 1.3.4 Comment of marginal distribution

  It is even better because it maintains a clear differentiation between 0.0 and 1.0 like that in `Task 1.2`, while removes some ambiguity near 0.4 or 0.6.

### Task 1.4

* Best tuned parameters
  
  ```python
    train_kwargs = {
      'lr':            0.009, # learning rate of the model
      'embedding_dim': 70,   # size of the feature vector
      'hidden_dim':    60,   # number of nodes in each layer in the model
      'n_epochs':      11,   # number of training epochs
      'dropout':       0.2,  # dropout rate (during learning)
      'batch_size':    70,   # training batch size
      'seed':          281
    }
  ```

* Best F1 score: `0.483`
  
  ![](./task1.4.png)
