## curl -X PUT "elasticsearch-elasticsearch-coordinating-only.elk:9200/basf_lm?pretty"
## curl -X GET "elasticsearch-elasticsearch-coordinating-only.elk:9200/_cat/indices?pretty"
## curl http://elasticsearch-elasticsearch-coordinating-only.elk:9200/basf_lm/_count

from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import logging
import uuid
logging.basicConfig(level=logging.INFO)
import glob

from elasticsearch import helpers, Elasticsearch
es = Elasticsearch(hosts=["elasticsearch-elasticsearch-coordinating-only.elk:9200"])
def index_es(docs):
    res = helpers.bulk(es, docs, chunk_size=1000, request_timeout=200)
    print(res)


def parse_doc(document_path):
    ## create document for extraction with configurations
    pdf_document = Document(
        document_path=document_path,
        language='eng'
        )
    pdf2text = PDF2Text(document=pdf_document)
    content = pdf2text.extract()
    return (content)

basf_documents = glob.glob("/opt/notebooks/shahrukh/basf_documents/download_center_docs/*")

for basf_document in basf_documents:
    try:
        content = parse_doc(f"{basf_document}")
        paragraphs = []
        for page in content:
            for paragraph in page['text'].split('\n\n'):
                if paragraph and len(paragraph.strip()):
                    paragraphs.append({
                    'paragraph':    paragraph,
                    '_index': 'basf_lm',
                    '_id': str(uuid.uuid4()),
                    '_type': '_doc',
                    'document_name': basf_document.split('/')[-1]                    
                    })
        if len(paragraphs):
            index_es(paragraphs)
    except Exception as e:
        print(e)


