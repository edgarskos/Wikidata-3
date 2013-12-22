# -*- coding: utf-8  -*-
import pywikibot
from rdflib import URIRef, Graph
from rdflib.namespace import FOAF

property = input("Saisissez une propriété : ")

site = pywikibot.getSite("fr", "wikipedia")

def toWikiID(uri):
    if "//fr." in uri:
        return uri.lstrip('http://fr.dbpedia.org/resource/')
    else:
        return uri.lstrip('http://dbpedia.org/resource/')
        
def propExists(prop,claims):
    for datatmp in claims:
        if datatmp['m'][1]==prop:
            #if type(datatmp['m'][3])==dict:
             #   if datatmp['m'][3].has_key('numeric-id'):
              #      if datatmp['m'][3]['numeric-id']==entity:
            return True
            break
    return False
    
def dataLoad(wikiId):
    page=pywikibot.Page(site, wikiId)
    data = pywikibot.DataPage(page)
    return data
    
def idClean(data):
    return  str(data).lstrip('[[wikidata:').rstrip(']]')
    
def idCleanPlus(data):
    return  int(str(data).lstrip('[[wikidata:Q').rstrip(']]'))

def createClaim(s,l):        
    try:
        dataS=dataLoad(s)
        dicoS=dataS.get()
        try:
            retour=propExists(property,dicoS['claims'])
            if retour==True:
                retour="La propriété P" + str(property).encode('utf-8') +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + l.encode('utf-8')
                return retour
            else:
                try:
                    return dataS.editclaim("p"+str(property), l ,refs={("p143","Q193563")})
                except pywikibot.EditConflict:
                    pywikibot.output(u'Skipping because of edit conflict')
            del dataL, dicoL
        except pywikibot.NoPage:
            pywikibot.output(u'Page does not exist?!') 
        del dataS, dicoS           
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')


g = Graph()
g.parse("RDF/dump_Wikipedia_Fr_exact_match.nt", format="nt")

for subj, pred, obj in g:
    print createClaim(obj.split("http://fr.wikipedia.org/wiki/",1)[1],subj.split("http://data.bnf.fr/ark:/12148/cb",1)[1]) 
