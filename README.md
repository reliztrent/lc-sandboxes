# sandboxes

Scripts and Jupyter notebooks for testing, learning, and experimentation

## Comparing geographic entities in Wikidata with their id.loc.gov equivalents

These files are for practicing the id.loc.gov and wikidata apis. The goal is to compare geographic entities in Wikidata that have LC authority IDs, in an attempt to find mis-matches (e.g., Kern River the river and Kern River the Emmylou Harris song). In Wikidata, look for all items that are instances of any subclass (or subclass of subclass, etc.) of "geographic region" (Q82794) AND which have an LC authority ID. Then, go grab the LC authority record and check if its MADS tag is "Geographic" or otherwise. 

- Total Wikidata geo items with LC IDS: 244,077
- Geographic: 230797
- CorporateName: 12443
- ComplexSubject: 436
- Topic: 213
- ConferenceName: 81
- FamilyName: 41
- PersonalName: 23
- Title: 17
- NameTitle: 9
- LC id doesn't resolve: 17

### idlocgov-wikidata-geographic.ipynb
Jupyter notebook file to get data. May take a few days to run.
### idlocgov-wikidata-geographic.py
Python export of Jupyter notebook, untested
### LCItems_MADs.csv
CSV export of results. 