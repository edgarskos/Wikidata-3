# -*- coding: utf-8  -*-
import pywikibot
from rdflib import URIRef, Graph, Namespace
from rdflib.namespace import FOAF
import pwb
import json
import re
import datetime

def dataLoad(site,wikiId):
    page=pywikibot.Page(site, wikiId)
    data = pywikibot.ItemPage.fromPage(page)
    return data

def sparqlEndpoint(lang):
    if "en" in lang:
        return "http://dbpedia.org/sparql"
    else:
        return "http://"+lang+".dbpedia.org/sparql"
        
def toWikiID(uri):
    if "//"+configuration['lang']+"." in uri:
        return uri.lstrip('http://'+configuration['lang']+'.dbpedia.org/resource/')      
    else:
        return uri.lstrip('http://dbpedia.org/resource/')        


    
def commonsId(string):
    return string.lstrip('Category:')
    
def imageId(string):
    return string.rstrip('/')
    
def idClean(data):
    return  str(data).lstrip('[[wikidata:').rstrip(']]')
    
def idCleanPlus(data):
    return  int(str(data).lstrip('[[wikidata:Q').rstrip(']]')) 

def propExists(prop,claims,entity):
    if prop in claims:
        for claim in claims[prop]:
            if idClean(claim.getTarget())==idClean(entity):
                return True
                break
    else:
        return False

def addAssertion(type,repo,property,source,target):
    claim=pywikibot.Claim(repo, str(property))
    claim.setTarget(target)
    if type=="claim":
        source.addClaim(claim)
    elif type=="source":
        source.addSource(claim)
    elif type=="qualifier":
        source.addQualifier(claim)        
                 
def createClaim(site,subject,property,object,source=None,qualifiers=None):
    repo = site.data_repository()  
    try:
        dataS=dataLoad(site,subject)
        if dataS:
            dataS.get()
            try:
                dataL=dataLoad(site,object)
                if dataL:
                    property='P'+property
                    retour=propExists(property,dataS.claims,dataL)
                    if retour==True:
                        response="La propriété " + str(property).encode('utf-8') +" existe pour "+ subject.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + idClean(dataL).encode('utf-8') + " = " + object.encode('utf-8')
                        print response
                    else:
                        try:
                            #addAssertion("claim",repo,str(property),dataS,dataL)
                            claim=pywikibot.Claim(repo, str(property))
                            claim.setTarget(dataL)
                            dataS.addClaim(claim)
                            print "Création pour " + subject.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " de la propriété " + str(property).encode('utf-8') + " avec pour valeur " + idClean(dataL).encode('utf-8') + " = " + object.encode('utf-8')
                            if source:
                                try:
                                    #addAssertion("source",repo,"P143",claim,pywikibot.ItemPage(repo, source))
                                    claimSource=pywikibot.Claim(repo, "P143")
                                    claimSource.setTarget(pywikibot.ItemPage(repo, source))
                                    claim.addSource(claimSource)
                                    print "Ajout d'une source"
                                except pywikibot.EditConflict:
                                    pywikibot.output(u'Skipping because of edit conflict')
                                except pywikibot.Error:
                                    pywikibot.output(u'Exception inconnue : on passe au suivant')
                                except Exception as er:
                                    pywikibot.output(u'Exception inconnue : %s'%str(er))
                            if qualifiers:
                                for key,value in qualifiers.items():
                                    if "dbpedia" in str(value):
                                        try:
                                            dataQualifier=dataLoad(site,toWikiID(value))
                                            if dataQualifier:
                                                #addAssertion("qualifier",repo,str(key),claim,dataQualifier)
                                                claimQualifier=pywikibot.Claim(repo, str(key))
                                                claimQualifier.setTarget(dataQualifier)
                                                claim.addQualifier(claimQualifier)
                                                print "Ajout d'un qualificatif"
                                        except pywikibot.NoPage:
                                            pywikibot.output('The page doesn\'t have a wikidata item :(')
                                        except pywikibot.Error:
                                            pywikibot.output(u'Erreur... On continue')        
                                        except Exception as e:
                                            pywikibot.error(u'Exception inconnue : %s'%str(e))
                                    else:
                                        try:
                                            #addAssertion("qualifier",repo,str(key),claim,value)
                                            claimQualifier=pywikibot.Claim(repo, str(key))
                                            claimQualifier.setTarget(value)
                                            claim.addQualifier(claimQualifier)
                                            print "Ajout d'un qualificatif"
                                        except pywikibot.Error:
                                            pywikibot.output(u'Erreur... On continue')        
                                        except Exception as e:
                                            pywikibot.error(u'Exception inconnue : %s'%str(e))
                        except pywikibot.EditConflict:
                            pywikibot.output(u'Skipping because of edit conflict')
                        except pywikibot.Error:
                            pywikibot.output(u'Exception inconnue : on passe au suivant')
                        except Exception as er:
                            pywikibot.output(u'Exception inconnue : %s'%str(er))
            except pywikibot.NoPage:
                pywikibot.output('The page doesn\'t have a wikidata item :(')
            except pywikibot.Error:
                pywikibot.output(u'Erreur... On continue')        
            except Exception as e:
                pywikibot.error(u'Exception inconnue : %s'%str(e))
    except pywikibot.NoPage:
        pywikibot.output('The page doesn\'t have a wikidata item :(')
    except pywikibot.Error:
        pywikibot.output(u'Erreur... On continue')        
    except Exception as e:
        pywikibot.error(u'Exception inconnue : %s'%str(e))
        
def createClaimDirect(site,subject,property,object,source=None,qualifiers=None):
    repo = site.data_repository()  
    try:
        dataS=pywikibot.ItemPage(repo,subject)
        if dataS:
            dataS.get()
            try:
                dataL=pywikibot.ItemPage(repo,object)
                if dataL:
                    property='P'+property
                    retour=propExists(property,dataS.claims,dataL)
                    if retour==True:
                        response="La propriété " + str(property).encode('utf-8') +" existe pour "+ subject.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " avec pour valeur " + idClean(dataL).encode('utf-8') + " = " + object.encode('utf-8')
                        print response
                    else:
                        try:
                            #addAssertion("claim",repo,str(property),dataS,dataL)
                            claim=pywikibot.Claim(repo, str(property))
                            claim.setTarget(dataL)
                            dataS.addClaim(claim)
                            print "Création pour " + subject.encode('utf-8') + " = " + idClean(dataS).encode('utf-8') + " de la propriété " + str(property).encode('utf-8') + " avec pour valeur " + idClean(dataL).encode('utf-8') + " = " + object.encode('utf-8')
                            if source:
                                try:
                                    #addAssertion("source",repo,"P143",claim,pywikibot.ItemPage(repo, source))
                                    claimSource=pywikibot.Claim(repo, "P143")
                                    claimSource.setTarget(pywikibot.ItemPage(repo, source))
                                    claim.addSource(claimSource)
                                    print "Ajout d'une source"
                                except pywikibot.EditConflict:
                                    pywikibot.output(u'Skipping because of edit conflict')
                                except pywikibot.Error:
                                    pywikibot.output(u'Exception inconnue : on passe au suivant')
                                except Exception as er:
                                    pywikibot.output(u'Exception inconnue : %s'%str(er))
                            if qualifiers:
                                for key,value in qualifiers.items():
                                    if "dbpedia" in str(value):
                                        try:
                                            dataQualifier=dataLoad(site,toWikiID(value))
                                            if dataQualifier:
                                                #addAssertion("qualifier",repo,str(key),claim,dataQualifier)
                                                claimQualifier=pywikibot.Claim(repo, str(key))
                                                claimQualifier.setTarget(dataQualifier)
                                                claim.addQualifier(claimQualifier)
                                                print "Ajout d'un qualificatif"
                                        except pywikibot.NoPage:
                                            pywikibot.output('The page doesn\'t have a wikidata item :(')
                                        except pywikibot.Error:
                                            pywikibot.output(u'Erreur... On continue')        
                                        except Exception as e:
                                            pywikibot.error(u'Exception inconnue : %s'%str(e))
                                    else:
                                        try:
                                            #addAssertion("qualifier",repo,str(key),claim,value)
                                            claimQualifier=pywikibot.Claim(repo, str(key))
                                            claimQualifier.setTarget(value)
                                            claim.addQualifier(claimQualifier)
                                            print "Ajout d'un qualificatif"
                                        except pywikibot.Error:
                                            pywikibot.output(u'Erreur... On continue')        
                                        except Exception as e:
                                            pywikibot.error(u'Exception inconnue : %s'%str(e))
                        except pywikibot.EditConflict:
                            pywikibot.output(u'Skipping because of edit conflict')
                        except pywikibot.Error:
                            pywikibot.output(u'Exception inconnue : on passe au suivant')
                        except Exception as er:
                            pywikibot.output(u'Exception inconnue : %s'%str(er))
            except pywikibot.NoPage:
                pywikibot.output('The page doesn\'t have a wikidata item :(')
            except pywikibot.Error:
                pywikibot.output(u'Erreur... On continue')        
            except Exception as e:
                pywikibot.error(u'Exception inconnue : %s'%str(e))
    except pywikibot.NoPage:
        pywikibot.output('The page doesn\'t have a wikidata item :(')
    except pywikibot.Error:
        pywikibot.output(u'Erreur... On continue')        
    except Exception as e:
        pywikibot.error(u'Exception inconnue : %s'%str(e))          

def before(s, pat):
    #returns the substring before pat in s.
    #if pat is not in s, then return a null string!
    pos =s.find(pat)
    if pos != -1:
       return s[:pos]
    return ""

#configFile = raw_input("Chemin vers le fichier de config : ")
configFile = "configFile.json"
fichier = open(configFile, "r")
configuration = json.loads(fichier.read().decode('utf-8'))
site = pywikibot.getSite(configuration['lang'],configuration['site'])

afs = Namespace("urn:afs:identifier/")
dcterms = Namespace("http://purl.org/dc/terms/")
    
    
    
    
g = Graph()
g.parse("RDF/facebookmuseum.rdf")

g.bind('dcterms', 'http://purl.org/dc/terms/')
g.bind('afs', 'urn:afs:identifier/')

for subj in g.subjects(dcterms.identifier):
    
    wikidata=g.value(subj, dcterms.identifier)
    twitter=g.value(subj, afs["twitter"])
    facebook=g.value(subj, afs["essai"])
    
    
    if twitter:
        qualifiers=dict()
        qualifiers['P554']=twitter
        createClaimDirect(site,wikidata,"553","Q918",None,qualifiers)
        del qualifiers
    if facebook:
        qualifiers=dict()
        qualifiers['P554']=facebook.encode('utf-8')
        createClaimDirect(site,wikidata,"553","Q355",None,qualifiers)  
        
        
        
        
        
        
        
