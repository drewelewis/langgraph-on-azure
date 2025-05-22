import os
from typing import List, Optional
from pydantic import BaseModel, Field

from elasticsearch import Elasticsearch
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

isconnected=False

class ElasticSearchOperations():
    def search(self, query: str) -> list[any]| None:
        results = []
        try:
            client = Elasticsearch("http://localhost:9200/")
            
            resp = client.search(index="contosobank-logs-2025.05.21", query=query)
            print("Got {} hits:".format(resp["hits"]["total"]["value"]))
            for hit in resp["hits"]["hits"]:
                results.append(hit)
            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            return results
        finally:
            client.close() 

class Client():
    def __init__(self):
        self.client = None
        self.isconnected = False

    def connect(self):
        if not self.client:
            self.client = self.client()
        if self.client:
            try:
                if self.client.ping():
                    print("Connected to Elasticsearch")
                    self.isconnected = True
                else:
                    print("Could not connect to Elasticsearch")
                    self.isconnected = False
            except Exception as e:
                print(f"An error occurred: {e}")
                self.isconnected = False
        return self.client

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
    
    def client():
        try:
            client = Elasticsearch("http://localhost:9200/")
            if client.ping():
                print("Connected to Elasticsearch")
            else:
                print("Could not connect to Elasticsearch")
            return client
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

