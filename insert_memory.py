from openai import OpenAI
import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pymongo import MongoClient
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pinecone.Index("simsim-memory")
mongo_cluster = MongoClient(os.getenv("MONGO_CLUSTER_URI"))
mongo_memory_collection = mongo_cluster["simsim"]["memory"]

embedding_model = "text-embedding-ada-002"

with open("대화내용요약.json", "r", encoding="utf-8") as f:
    summaries_list = json.load(f)
    
mongo_memory_collection.delete_many({})

next_id = 1
for list_idx, summaries in enumerate(summaries_list):
    date = f"202601{list_idx+1:02}"
    for summary in summaries:
        # 벡터화
        vector = client.embeddings.create(
            input=summary["요약"],
            model=embedding_model
        ).data[0].embedding
        # PineconeDB에 저장
        metadata = {"date": date, "keyword": summary["주제"]}
        upsert_response = pinecone_index.upsert([(str(next_id), vector, metadata)])

        # mongoDB에 저장
        query = {"_id": next_id}
        newvalues = {"$set": {"date": date, "keyword": summary["주제"],  "summary" : summary["요약"]}} 
        mongo_memory_collection.update_one(query, newvalues, upsert=True)
        
        if (next_id) % 5 == 0:    
            print(f"id: {next_id}")
            
        next_id += 1
        
# >> python insert_memory.py