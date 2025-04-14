# MY_GitHub_AI

## Project Overview
MY_GitHub_AI is a Python-based project that integrates GitHub repository fetching, AI-powered chat, and webhook functionality. It allows users to fetch files from a GitHub repository, index them for AI-based querying, and respond to GitHub webhook events.

## Features
- Fetch files from a GitHub repository.
- Index repository files using RAG (Retrieval-Augmented Generation) Vectorization.
- AI-powered chat interface for querying indexed files.
- Webhook server to handle GitHub push events and re-index repository files.

## Prerequisites
1. Python 3.11 or higher.
2. Install the required Python packages listed in `requirement.txt`.
3. Set up the following environment variables:
   - `GITHUB_TOKEN`: Your GitHub personal access token.
   - `GEMINI_API_KEY`: Your Gemini AI API key.
   - `REPO_OWNER`: The owner of the GitHub repository (default: `Priyankkumawat`).
   - `REPO_NAME`: The name of the GitHub repository (default: `vaccination_management_system`).

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MY_GitHub_AI
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

## Usage
### 1. Start the Webhook Server
Run the webhook server to listen for GitHub push events:
```bash
python src/webhook_server.py
```
The server will start at `http://localhost:5000/webhook`.

### 2. Run the Main Application
Start the main application to fetch repository files and interact with the AI:
```bash
python src/main.py
```

### 3. Interact with the AI
Once the application is running, you can type queries in the console to interact with the AI. Type `exit` or `q` to quit.

## Webhook Setup
To use the webhook functionality, configure your GitHub repository to send push events to `http://localhost:5000/webhook`.

## Folder Structure
- `src/`: Contains the source code for the project.
- `chroma_db/`: Stores the indexed database files.
- `Lib/`, `Include/`, `Scripts/`, `share/`: Virtual environment folders (ignored by Git).

## Contributing
Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.