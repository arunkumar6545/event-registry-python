from eventregistry import *
er = EventRegistry(apiKey = "6d8bee13-1ce4-4c0f-8af6-be6d6c5b2784")
file1 = open("amazon.csv","w") 
q = QueryArticlesIter(conceptUri = er.getConceptUri("Amazon"))
for art in q.execQuery(er, sortBy = "date"):
    file1.write(art['date'] + "," + art['url'] + "," + str(art['sentiment']) + "," + str(art['wgt'])+ "\n")
file1.close()