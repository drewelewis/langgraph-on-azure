
from elasticsearch import Elasticsearch

doc_type = "python_log"
index = "contosobank-logs-2025.05.21"


def main():
    results = []
    query={
            "match": {
                "levelname": "Error"
            }
        }
        
    try:
        client = Elasticsearch("http://localhost:9200/")
        
        resp=client.search(index=index, query=query)
        for hit in resp["hits"]["hits"]:
            results.append(hit)
        return results
    except Exception as e:
        print(f"An error running query {query} Error {e}")
        return results
    finally:
        client.close() 

if __name__ == "__main__":
    results = main()
    for result in results:
        print(result)