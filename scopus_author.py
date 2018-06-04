"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import pprint


from rdflib import Graph, RDF, Namespace, Literal, URIRef
from rdflib import URIRef, BNode, Literal

# Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
# client.inst_token = config['insttoken']

## Author example
# Initialize author with uri
URI = "https://krr.cs.vu.nl/"

data = {"data" : "24.3"}
data_json = json.dumps(data)

headers = {'Accept': 'application/json'}

my_auth = ElsAuthor(
        uri = 'https://api.elsevier.com/content/author/author_id/7004322609')

#data from Elsevier
# resp = client.exec_request('https://api.elsevier.com/content/search/scopus?query=all(7004322609)&apiKey=ff61921fc97787106a446daa9dc3827b')

resp = client.exec_request('https://api.elsevier.com/content/search/author?query=authlast(Harmelen)&apiKey=7f59af901d2d86f78a1fd60c1bf9426a')

data = resp               #data from scopus


#data from JSON file
# with open('data_scopus_author.json') as json_file:
#     data_json_file = json.load(json_file)

# data = data_json_file       #data from JSON file

with open('data_scopus_author.json', 'w') as outfile:
    json.dump(resp, outfile)


pprint.pprint(data)


def replaceSpace(string):
    return string.replace(" ", "_") #replace the space into _

def transformToRDF(string):
    return URIRef(URI + string)




#=======================
#RDFLIB
#=======================


g = Graph()

EX = Namespace('http://example.com/KE4KE/')
g.bind('ex', EX)


#
# file = open("data.ttl", mode="w")
#
# def serialize(filename):
#     g.serialize(destination=filename, format='turtle')
#     print("File is saved")
#
# def save(filename):
#     with open(filename, 'w') as f:
#         g.serialize(f, format='turtle')
#
#
# def load(filename):
#     with open(filename, 'r') as f:
#         g.load(f, format='turtle')
#
#
# serialize('data.ttl')