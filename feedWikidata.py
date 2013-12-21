# -*- coding: utf-8  -*-
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

property = input("Saisissez une propriété : ")

fichier = open("query.rq", "r")

sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")

sparql.setQuery(fichier.read())

site = pywikibot.getSite("fr", "wikipedia")

def toWikiID(uri):
    if "//fr." in uri:
        return uri.lstrip('http://fr.dbpedia.org/resource/')
    else:
        return uri.lstrip('http://dbpedia.org/resource/')
        
def propExists(prop,claims):
    for datatmp in claims:
        if datatmp['m'][1]==prop:
            return True
            break
    return False
    
def dataLoad(wikiId):
    page=pywikibot.Page(site, wikiId)
    data = pywikibot.DataPage(page)
    return data
    
def idClean(data):
    return  str(data).lstrip('[[wikidata:').rstrip(']]')   

def createClaim(s,l):        
    dataS=dataLoad(s)
    dicoS=dataS.get()
    if dataS!="None":
        if propExists(property,dicoS['claims'])==True:
            retour="La propriété P" + str(property) +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS)
            return retour
        else:
            dataL=dataLoad(l)
            dicoL=dataL.get()
            if dataL!="None":
                dataS.editclaim("p"+str(property), idClean(dataL) ,refs={("p143","Q8447")})
            else:
                retour="La page correspondante à "+ l.encode('utf-8') + " n'existe pas."
                return retour
    else:
        retour="La page correspondante à "+ s.encode('utf-8') + " n'existe pas."
        return retour
    
# JSON example
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print createClaim(toWikiID(result["s"]["value"]),toWikiID(result["l"]["value"]))
        
        
