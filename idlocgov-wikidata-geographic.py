
# coding: utf-8

# In[ ]:

import requests
import pprint
import pandas as pd
import re
from xml.etree import ElementTree as ET


# In[ ]:

# From Wikidata, get everything that is a subclass* of geographic region (Q82794) 

url = 'https://query.wikidata.org/sparql'
query = """
SELECT ?item ?itemLabel WHERE {
  #?item wdt:P244 ?id.
  ?item wdt:P279* wd:Q82794.
        
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  }
"""
classes_raw = requests.get(url, params = {'format': 'json', 'query': query})
classes_json = classes_raw.json()


# In[ ]:

# From Wikidata, for each of those subclasses, get all records that 
# are an instance of that subclass AND that have an LC authority ID. 
# Commented out is a step to then grab the id.loc.gov records and its 
# MADS. This slowed the script down too much, so is separated to next step.

LCitems = []

classes = classes_json['results']['bindings']
for x in classes:
    uri = x['item']['value']
    QID = re.sub('http://www.wikidata.org/entity/','',uri)
    queryLC = """
    SELECT ?item ?itemLabel ?id WHERE {
      ?item wdt:P244 ?id.
      ?item wdt:P31/wdt:P279 wd:"""+QID+""" .

      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      }
    """
    LCitems_raw = requests.get(url, params = {'format': 'json', 'query': queryLC})
    LCitems_json = LCitems_raw.json()
    for y in LCitems_json['results']['bindings']:
        LCitems.append(y)
        LCID = y['id']['value']
        y['lcid'] = LCID
        if LCID.startswith('sh'):
            LCIDurl = 'http://id.loc.gov/authorities/subjects/'+LCID+'.rdf'
            y['lcidurl'] = LCIDurl
        elif LCID.startswith('n'):
            LCIDurl = 'http://id.loc.gov/authorities/names/'+LCID+'.rdf'
            y['lcidurl'] = LCIDurl
        else:
            print(LCID + ' What authority is this?')
        #LCrdf = requests.get(LCIDurl)
        
        #LCrdf = requests.get(LCIDurl)
        #tree = ET.fromstring(LCrdf.content)
        #for child in tree:
            #y['mads'] = (child.tag)       

df = pd.DataFrame(LCitems)
df


# In[ ]:

# Save result to a file named "Wikidata.csv"

df.to_csv('Wikidata.csv', encoding='utf-8')


# In[ ]:

# Retreive the RDF XML from id.loc.gov and add 
# a column of MADS values. Print the LCID handles 
# as each is completed. 
# If the process stops, check the index of the 
# last item, and begin again at that index
#e.g.:   for index,row in df.iloc[225292:].iterrows():


for index,row in df.iloc.iterrows():
    LCIDurl = row[5]
    print(LCIDurl)
    LCrdf = requests.get(LCIDurl)
    tree = ET.fromstring(LCrdf.content)
    for child in tree: # as far as i am aware, there is only ever 1 child. 
        print(child.tag)
        df.loc[index,'mads'] = child.tag


# In[ ]:

df.to_csv(r'LCItems_MADsfrom225292.csv', encoding='utf-8')

