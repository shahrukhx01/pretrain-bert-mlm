from elasticsearch import helpers, Elasticsearch
import json
es = Elasticsearch(hosts=["elasticsearch-elasticsearch-coordinating-only.elk:9200"])


def scroll(es, index, body, scroll, size, **kw):
    page = es.search(index=index, body=body, scroll=scroll, size=size, **kw)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    while len(hits):
        yield hits
        page = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

body = {"query": {"match_all": {}}}
import ast
docs = []
content = []
from tqdm import tqdm
i = 0
for hits in tqdm(scroll(es, 'basf_lm', body, '2m', 10000)):
    # Do something with hits here
    for data in ast.literal_eval(json.dumps(hits, indent=4)):
        docs.append(data['_source']['document_name'])
        content += list(set(data['_source']['paragraph'].split()))
        
doc_files = len(set(docs))
print("files ", doc_files)
res = es.count(index='basf_lm', doc_type='_doc', body=body)["count"]
print("es docs", res)

print('paragraphs/doc', res/doc_files)
print('unique tokens', len(set(content)))


import eland as ed
#df = ed.DataFrame(es, es_index_pattern="basf_lm")
#print(df.head())