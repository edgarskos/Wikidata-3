# -*- coding: utf-8  -*-
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import re

property = input("Saisissez une propriété : ")

fichier = open("query-fr.rq", "r")

sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")

sparql.setQuery(fichier.read().decode('utf-8'))

site = pywikibot.getSite("fr", "wikipedia")

def toWikiID(uri):
    if "//fr." in uri:
        return uri.lstrip('http://fr.dbpedia.org/resource/')
    else:
        return uri.lstrip('http://dbpedia.org/resource/')
        
def commonsId(string):
    return string.lstrip('Category:')
    
def imageId(string):
    return string.rstrip('/')    
        
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
            dataL=dataLoad(l)
            dicoL=dataL.get()
            retour=propExists(property,dicoS['claims'])
            if retour==True:
                retour="La propriété P" + str(property).encode('utf-8') +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + idClean(dataL).encode('utf-8') + " = " + l.encode('utf-8')
                return retour
            else:
                try:
                    edit=dataS.editclaim("p"+str(property), idClean(dataL) ,refs={("p143","Q8447")})
                    return edit
                except pywikibot.EditConflict:
                    pywikibot.output(u'Skipping because of edit conflict')
                except pywikibot.Error:
                    pywikibot.output(u'Exception inconnue : on passe au suivant')
                except Exception as er:
                    pywikibot.output(u'Exception inconnue : %s'%str(er))                    
        except pywikibot.NoPage:
            pywikibot.output(u'Page does not exist?!') 
        except pywikibot.Error:
            pywikibot.output(u'Exception inconnue : on passe au suivant')
        except Exception as er:
            pywikibot.output(u'Exception inconnue : %s'%str(er))
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')
    except pywikibot.Error:
        pywikibot.output(u'Exception inconnue : on passe au suivant')
    except Exception as er:
        pywikibot.output(u'Exception inconnue : %s'%str(er))
        
def createClaimCommons(s,l):        
    try:
        dataS=dataLoad(s)
        dicoS=dataS.get()
        try:
            retour=propExists(property,dicoS['claims'])
            if retour==True:
                retour="La propriété P" + str(property).encode('utf-8') +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + commonsId(l).encode('utf-8')
                return retour
            else:
                try:
                    return dataS.editclaim("p"+str(property), commonsId(l) ,refs={("p143","Q8447")})
                except pywikibot.EditConflict:
                    pywikibot.output(u'Skipping because of edit conflict')
            del dataL, dicoL
        except pywikibot.NoPage:
            pywikibot.output(u'Page does not exist?!') 
        del dataS, dicoS           
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')
        
def createClaimImage(s,l):        
    try:
        dataS=dataLoad(s)
        dicoS=dataS.get()
        try:
            retour=propExists(property,dicoS['claims'])
            if retour==True:
                retour="La propriété P" + str(property).encode('utf-8') +" existe pour "+ s.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + commonsId(l).encode('utf-8')
                return retour
            else:
                try:
                    image=re.match(u'http:\/\/upload\.wikimedia\.org\/wikipedia\/\commons\/[0-9a-z]{1}\/[0-9a-z]{2}\/(.*\.[a-zA-Z]{0,4})', l)   
                    try:
                        pathImage=image.group(1)
                    except Exception as er:
                        pywikibot.output(u'Exception inconnue : %s'%str(er))    
                    commons = pywikibot.getSite(u'commons', u'commons')
                    dataMedia = pywikibot.ImagePage(commons, pathImage)
                    mediadicoS=dataMedia.get()
                    try:
                        if pathImage and "Defaut.svg" not in pathImage:
                            try:
                                edit=dataS.editclaim("p"+str(property), pathImage,refs={("p143","Q8447")})
                                return edit
                            except pywikibot.EditConflict:
                                pywikibot.output(u'Skipping because of edit conflict')
                            except pywikibot.Error:
                                pywikibot.output(u'Exception inconnue : on passe au suivant')
                        else:
                            retour="Le chemin vers l'image n'est pas valide"
                            return retour
                    except pywikibot.NoPage:
                        pywikibot.output(u'Page does not exist?!') 
                    except pywikibot.IsRedirectPage:
                        pywikibot.output(u'%s est une page de redirection' % pagename)
                    except pywikibot.Error:
                        pywikibot.output(u'Exception inconnue : on passe au suivant')
                    except Exception as er:
                        pywikibot.output(u'Exception inconnue : %s'%str(er))
                except pywikibot.EditConflict:
                    pywikibot.output(u'Skipping because of edit conflict')
                except pywikibot.Error:
                    pywikibot.output(u'Exception inconnue : on passe au suivant')
                except Exception as er:
                    pywikibot.output(u'Exception inconnue : %s'%str(er))
        except pywikibot.NoPage:
            pywikibot.output(u'Page does not exist?!') 
        except pywikibot.Error:
            pywikibot.output(u'Exception inconnue : on passe au suivant')    
        except Exception as er:
            pywikibot.output(u'Exception inconnue : %s'%str(er))
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')              
    except pywikibot.Error:
        pywikibot.output(u'Exception inconnue : on passe au suivant')              
    except Exception as er:
        pywikibot.output(u'Exception inconnue : %s'%str(er))
        
def createClaimTime(s,l):        
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
                    edit=dataS.editclaim("p"+str(property), "+0000000"+l.encode('utf-8')+"T00:00:00Z", data_type="time", refs={("p143","Q8447")})
                    return edit
                except pywikibot.EditConflict:
                    pywikibot.output(u'Skipping because of edit conflict')
                except pywikibot.Error:
                    pywikibot.output(u'Exception inconnue : on passe au suivant')
                except Exception as er:
                    pywikibot.output(u'Exception inconnue : %s'%str(er))                    
        except pywikibot.NoPage:
            pywikibot.output(u'Page does not exist?!') 
        except pywikibot.Error:
            pywikibot.output(u'Exception inconnue : on passe au suivant')
        except Exception as er:
            pywikibot.output(u'Exception inconnue : %s'%str(er))
    except pywikibot.NoPage:
        pywikibot.output(u'Page does not exist?!')
    except pywikibot.Error:
        pywikibot.output(u'Exception inconnue : on passe au suivant')
    except Exception as er:
        pywikibot.output(u'Exception inconnue : %s'%str(er))         
    
# JSON example
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print createClaim(toWikiID(result["s"]["value"]),toWikiID(result["l"]["value"]))
