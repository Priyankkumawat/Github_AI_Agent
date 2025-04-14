import requests
import os
from typing import List, Optional

class github_fetcher_class:
    def __init__(self, file_extensions: Optional[List[str]] = None):
        if file_extensions is None:
            self.file_extensions = [
                '.py', '.js', '.jsx', '.ts', '.tsx',
                '.html', '.css', '.scss', '.less',
                '.md', '.txt', '.rst', '.readme'
                '.json', '.yaml', '.yml', '.toml',
                '.c', '.cpp', '.h', '.hpp', '.java',
                '.go', '.rs', '.rb', '.php'
            ]
        else:
            self.file_extensions = file_extensions
    
    def fetch_repo_files(self,owner, repo, token):
        headers = {'Authorization': f'token {token}'}
        contents_url = f'https://api.github.com/repos/{owner}/{repo}/contents'

        def fetch_dir(self,url):
            files = []
            res = requests.get(url, headers=headers)
            res.raise_for_status()

            # print(f"response from github {res.json()[0]}")
            for item in res.json():
                if item['type'] == 'file':
                    extension = os.path.splitext(item['name'])[1]
                    print(f"file extension of {item['name']} is {extension}")
                    if extension in self.file_extensions:
                        file_res = requests.get(item['download_url'])
                        file_res.raise_for_status()
                        files.append({'path': item['path'], 'content': file_res.text})
                elif item['type'] == 'dir':
                    files.extend(fetch_dir(self,item['url']))
            return files
        
        return fetch_dir(self,contents_url)
