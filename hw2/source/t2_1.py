import spacy
import en_core_web_sm
import csv
nlp = en_core_web_sm.load()
sentence = nlp("He played the coach on TV's Mister Peepers")
from spacy import displacy
options = {"distance": 96}
displacy.render(sentence, style="dep", options=options)