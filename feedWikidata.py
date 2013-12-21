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
    try:
        dataS=dataLoad(s)
        dicoS=dataS.get()
        if propExists(property,dicoS['claims'])==True:
            retour="La propriété P" + str(property) +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS)
            return retour
        else:
            try:
                dataL=dataLoad(l)
                dicoL=dataL.get()
                dataS.editclaim("p"+str(property), idClean(dataL) ,refs={("p143","Q8447")})
            except pywikibot.NoPage:
                pywikibot.output(u'Page does not exist?!')            
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')
    
# JSON example
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print createClaim(toWikiID(result["s"]["value"]),toWikiID(result["l"]["value"]))
