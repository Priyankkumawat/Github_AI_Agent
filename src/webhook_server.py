from flask import Flask, request, jsonify
from threading import Thread
from github_fetcher import github_fetcher_class
from RAGVectorization import RAGVectorization
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Priyankkumawat"
REPO_NAME = "vaccination_management_system"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.get_json()
    print("📬 Push received:", data.get("head_commit", {}).get("message", "No message"))

    github_fetcher = github_fetcher_class()
    files = github_fetcher.fetch_repo_files(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    print(f"Fetched {len(files)} files from repo")

    file_indexer = RAGVectorization()
    file_indexer.index_repo_files(files)

    return jsonify({"status": "Repo re-indexed"}), 200

def run_webhook_server():
    print("🚀 Starting webhook server on http://localhost:5000/webhook")
    app.run(port=5000, threaded=True)
    