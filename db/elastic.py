import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch')
ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'webhook_data')



class ElasticsearchDatabase:
    def __init__(self) -> None:
        self.connection_is_active = False
        self.client = None

    def get_es_connection(self):
        if self.connection_is_active == False:
            try:
                self.client = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])
                self.connection_is_active = True
                return self.client
            except Exception as ex:
                print("Error connecting to Elasticsearch : ", ex)
        return self.client
    

def create_es_index(index_name: str):
    if es_client.indices.exists(index=index_name):
        print(f"Elasticsearch index '{index_name}' already exists.")
    else:
        try:
            es_client.indices.create(index=index_name)
            print(f"Elasticsearch index '{index_name}' created.")
        except Exception as e:
            print(f"Error creating Elasticsearch index '{index_name}': {e}")


if __name__ == "__main__":
    es_db = ElasticsearchDatabase()
    es_client = es_db.get_es_connection()
    print("Elasticsearch connected.")
    # Create Elasticsearch index
    create_es_index(ELASTICSEARCH_INDEX)