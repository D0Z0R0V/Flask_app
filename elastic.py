from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(host="")

with open("cities.csv") as f:
    read = csv.DictReder(f)
    helpers.bulk(es, read, index="pulluphardgucci")

resp = es.search(
    index="pulluphardgucci", 
    query={
        "mathc":{
            "name":"Moscow",
            },
        },
 )

print(resp.body)
