from google.generativeai import GenerativeModel
import google.generativeai as genai
import requests
import chromadb

class GenminiAI:
    def __init__(self, chroma_db_path = "./chroma_db", collection_name: str = "repo_chunks"):
        self.model_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        self.client = chromadb.PersistentClient(chroma_db_path)

        try:
            self.collection = self.client.get_collection(
                name=collection_name
            )
            print(f"✅ Connected to ChromaDB collection '{collection_name}'")
        except Exception as e:
            raise ValueError(f"Could not find ChromaDB collection '{collection_name}'. "
                             f"Make sure you've run the repository vectorization first. Error: {e}")
    
            
    def setup_gemini(self, api_key):
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model = GenerativeModel('Gemini 2.0 Flash')
    
    def retrieve_context(self, query, k=20):
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        return "\n".join(results['documents'][0])
    
    def ask_gemini(self,query):
        context = self.retrieve_context(query)
        prompt = (
            "You are an AI assistant for a GitHub project.\n"
            "Use only the context below to answer the user's question.\n"
            "If you don't find relevant info, respond: 'Not found in repository.'\n\n"
            f"Context:\n{context}\n\n"
            f"User question: {query}"
        )

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(
            f"{self.model_url}?key={self.api_key}",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("❌ Error:", response.status_code, response.text)
            return "Failed to get response from Gemini."
            