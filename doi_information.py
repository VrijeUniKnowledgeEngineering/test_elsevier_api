"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
# from elsapy.elsdoc import FullDoc, AbsDoc
# from elsapy.elssearch import ElsSearch
import json
import pprint
import csv

from rdflib.namespace import RDF, FOAF, OWL, RDFS

from rdflib import Graph, RDF, Namespace, Literal, URIRef
from rdflib import URIRef, BNode, Literal

# Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
# client.inst_token = config['insttoken']

# Initialize author with uri
URI = "https://krr.cs.vu.nl/"

data = {"data" : "24.3"}
data_json = json.dumps(data)

headers = {'Accept': 'application/json'}

my_auth = ElsAuthor(
        uri = 'https://api.elsevier.com/content/author/author_id/7004322609')

doi_list = []
with open('input_data/authors_1.1.csv') as csvfile:
    doireader = csv.DictReader(csvfile)
    for row in doireader:
        doi_list.append(row['doi'])


# def serialize(filename):
#     g.serialize(destination=filename, format='turtle')
#     print("File is saved")

def save(filename):
    with open(filename, 'a+') as f:
        g.serialize(destination=filename, format='turtle')
        print("File is saved")


def load(filename):
    with open(filename, 'r') as f:
        g.load(f, format='turtle')


def transformToRDF(strURI):

    if strURI[0:] == '_':
        strURI = strURI[0:].replace("_", "")  # delete     (does not work)

    strURI = strURI.replace(":", "") #delete :
    strURI = strURI.replace("/", "")  #delete /
    strURI = strURI.replace(" ", "_") #replace the space into
    strURI = strURI.replace(",", "") #delete ,
    strURI = strURI.replace("'", "") #delete single quote       (does not work)
    strURI = strURI.replace("''", "") #delete dubble quote      (does not work)
    strURI = strURI.replace("""""", "") #delete dubble quote    (does not work)
    strURI = strURI.replace("(", "") #delete (
    strURI = strURI.replace(")", "") #delete )
    strURI = strURI.replace("-", "_") #delete -
    strURI = strURI.replace("?", "") #delete ?
    strURI = strURI.replace(".", "_") #delete .
    strURI = strURI.replace(";", "") #delete ;
    strURI = strURI.replace("©", "") #delete ©
    strURI = strURI.replace("%", "") #delete %
    strURI = strURI.replace("=", "") #delete =
    strURI = strURI.replace("!", "") #delete !
    strURI = strURI.replace("[", "") #delete .
    strURI = strURI.replace("]", "") #delete .
    strURI = strURI.replace("é", "e") #delete .

    return URIRef(URI + strURI) #create URI


#=======================
# RDF Lib
#=======================
g = Graph()

EX = Namespace('https://krr.cs.vu.nl/')
g.bind('krr', EX)

is_author_of = transformToRDF('isAuthorOf')
is_coauthor_of = transformToRDF('isCoAuthorOf')
has_authors = transformToRDF('hasAuthors')
has_keyword = transformToRDF('hasKeyword')
has_scopus_id = transformToRDF('hasScopusID')
has_description = transformToRDF('hasDescription')
has_isbn = transformToRDF('hasISBN')
has_issn = transformToRDF('hasISSN')
has_publication_name = transformToRDF('hasPublicationName')
has_page_range = transformToRDF('hasPageRange')
has_publication_year = transformToRDF('hasPublicationYear')
has_doi = transformToRDF('hasDoi')



for doi in doi_list:
    print(doi)
    #data from Elsevier
    url = 'https://api.elsevier.com/content/abstract/doi/'+ doi +'?apiKey=ff61921fc97787106a446daa9dc3827b'
    resp = client.exec_request(url)
    data = resp

    #=======================
    # Publications
    #=======================

    #Title
    if 'dc:title' in data['abstracts-retrieval-response']['coredata']:
        title_pub = transformToRDF(data['abstracts-retrieval-response']['coredata']['dc:title'])
        titles = transformToRDF('Titles')
        g.add((titles, RDF.type, OWL.Class))
        g.add((titles, RDFS.label, title_pub))
        g.add((titles, RDFS.subClassOf, OWL.Thing))
        g.add((title_pub, RDF.type, FOAF.Document))


    #ScopusID
    if 'dc:description' in data['abstracts-retrieval-response']['coredata']:
        scopusID = transformToRDF(data['abstracts-retrieval-response']['coredata']['dc:identifier'])
        scopusIDs = transformToRDF('ScopusID')
        g.add((scopusIDs, RDF.type, OWL.Class))
        g.add((scopusIDs, RDFS.label, scopusID))
        g.add((scopusIDs, RDFS.subClassOf, OWL.Thing))

    #Authors
    if 'author' in data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']:

        authors = []
        for i in range(len(data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['author'])):
            author = data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['author'][i]['ce:indexed-name']
            author_ID = data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['author'][i]['@auid']

            authors.append({
                'author_name': transformToRDF(author),
                'author_ID': transformToRDF(author_ID),
            })

        #Author
        for author in authors:
            anode = BNode
            g.add((author['author_name'],RDF.type, FOAF.person))
            g.add((scopusID, RDFS.label, author['author_ID']))
            g.add((author['author_name'], is_author_of, title_pub))
            g.add((author['author_name'], has_scopus_id, author['author_ID']))
            g.add((title_pub, has_authors, BNode(title_pub)))
            for co_author in authors :
                if author['author_name'] != co_author['author_name']:
                    g.add((author['author_name'], is_coauthor_of, BNode(title_pub)))
                    g.add((BNode(title_pub), is_coauthor_of, co_author['author_name']))


    # Description
    if 'dc:description' in data['abstracts-retrieval-response']['coredata']:
        description = transformToRDF(data['abstracts-retrieval-response']['coredata']['dc:description'])
        descriptions = transformToRDF('Description')
        g.add((descriptions, RDF.type, OWL.Class))
        g.add((descriptions, RDFS.subClassOf, OWL.Thing))
        g.add((descriptions, RDFS.label, description))
        g.add((title_pub, has_description, description))

    #ISBN
    if 'prism:isbn' in data['abstracts-retrieval-response']['coredata']:
        isbns = transformToRDF('ISBN')
        g.add((isbns, RDFS.subClassOf, OWL.Thing))
        g.add((isbns, RDF.type, OWL.Class))

        isbn_list = []
        if '$' in data['abstracts-retrieval-response']['coredata']['prism:isbn'][0]:
            for i in range(len(data['abstracts-retrieval-response']['coredata']['prism:isbn'])):
                isbn = data['abstracts-retrieval-response']['coredata']['prism:isbn'][i]['$']
                isbn_list.append(transformToRDF(isbn))

            for isbn in isbn_list:
                g.add((isbns, RDFS.label, isbn))
                g.add((title_pub, has_isbn, isbn))
        else:
            isbn = transformToRDF(data['abstracts-retrieval-response']['coredata']['prism:isbn'])
            g.add((isbns, RDFS.label, isbn))
            g.add((title_pub, has_isbn, isbn))

    # #ISSN
    if 'prism:issn' in data['abstracts-retrieval-response']['coredata']:
        issn = transformToRDF(data['abstracts-retrieval-response']['coredata']['prism:issn'])
        issns = transformToRDF('ISSN')
        g.add((issns, RDFS.subClassOf, OWL.Thing))
        g.add((issn, RDF.type, OWL.Class))
        g.add((issn, RDFS.label, issn))
        g.add((title_pub, has_issn, issn))


    # #Publication Name
    if 'prism:publicationName' in data['abstracts-retrieval-response']['coredata']:
        publication_name = transformToRDF(data['abstracts-retrieval-response']['coredata']['prism:publicationName'])
        pub_names = transformToRDF('Names')
        g.add((pub_names, RDF.type, OWL.Class))
        g.add((pub_names, RDFS.subClassOf, OWL.Thing))
        g.add((pub_names, RDFS.label, publication_name))
        g.add((title_pub, has_publication_name, publication_name))


    #Publication Pages
    if 'prism:pageRange' in data['abstracts-retrieval-response']['coredata']:
        page_range = transformToRDF(data['abstracts-retrieval-response']['coredata']['prism:pageRange'])
        pub_ranges = transformToRDF('Pages')
        g.add((pub_ranges, RDF.type, OWL.Class))
        g.add((pub_ranges, RDFS.subClassOf, OWL.Thing))
        g.add((pub_ranges, RDFS.label, page_range))
        g.add((title_pub, has_page_range, page_range))

    #Publication Year
    if 'publicationyear' in data['abstracts-retrieval-response']['item']['bibrecord']['head']['source']:
        publication_year = transformToRDF(data['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['publicationyear']['@first'])
        pub_years = transformToRDF('Years')
        g.add((pub_years, RDF.type, OWL.Class))
        g.add((pub_years, RDFS.subClassOf, OWL.Thing))
        g.add((pub_years, FOAF.age, publication_year))
        g.add((title_pub, has_publication_year, publication_year))

    #DOI
    if 'prism:doi' in data['abstracts-retrieval-response']['coredata']:
        doi_number = transformToRDF(data['abstracts-retrieval-response']['coredata']['prism:doi'])
        doiNumbers = transformToRDF('DOI')
        g.add((doiNumbers, RDF.type, OWL.Class))
        g.add((doiNumbers, RDFS.subClassOf, OWL.Thing))
        g.add((doiNumbers, RDFS.label, doi_number))
        g.add((title_pub, has_doi, doi_number))


    #Keywords
    if 'idxterms' in data['abstracts-retrieval-response']:
        if data['abstracts-retrieval-response']['idxterms'] is not None:
            if 'mainterm' in data['abstracts-retrieval-response']['idxterms']:
                keywords = []
                if type(data['abstracts-retrieval-response']['idxterms']) is list:
                    for i in range(len(data['abstracts-retrieval-response']['idxterms']['mainterm'])):
                        keyword = data['abstracts-retrieval-response']['idxterms']['mainterm'][i]['$']
                        keywords.append(transformToRDF(keyword))

                    for keyword in keywords:
                        g.add((title_pub, has_keyword, keyword))
                # if '$' in data['abstracts-retrieval-response']['idxterms']['mainterm']:
                #     keyword = data['abstracts-retrieval-response']['idxterms']['mainterm']['$']
                #     g.add((title_pub, has_keyword, keyword))

    print(title_pub)

save("output_data/publications.ttl")
