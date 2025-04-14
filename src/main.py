from github_fetcher import github_fetcher_class
from RAGVectorization import RAGVectorization
from gemini_ai import GenminiAI
from webhook_server import run_webhook_server
import os
from threading import Thread

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPO_OWNER = "Priyankkumawat"
REPO_NAME = "vaccination_management_system"

def main():

    if not os.path.exists("./chroma_db"):
        github_fetcher = github_fetcher_class()
        files = github_fetcher.fetch_repo_files(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
        print(f"Fetched {len(files)} files from repo")

        # print(f"file name is {files[0]}")

        file_indexer = RAGVectorization()
        file_indexer.index_repo_files(files)
    else:
        print("chroma_db already exists")

    # AI
    gemini_ai = GenminiAI()
    gemini_ai.setup_gemini("AIzaSyDFoM8LA4n3-WEIAiDEmV9dLF2rchG0jZM")
    print("\n🤖 AI Chat Started (type 'exit' to quit)")

    while True:
        query = input("You: ")
        if query.lower() == "exit" or query.lower() =="q":
            break
        response = gemini_ai.ask_gemini(query)
        print("AI: ", response)

if __name__ == "__main__":
    # webshook satrted in background
    webhook_thread = Thread(target=run_webhook_server, daemon=True)
    webhook_thread.start()

    print(GITHUB_TOKEN)

    main()

