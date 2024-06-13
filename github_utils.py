import requests
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fetch_github_repo(repo_url):
    repo_name = repo_url.split('github.com/')[-1]
    api_url = f"https://api.github.com/repos/{repo_name}/contents"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def extract_repo_files(file_list, path="", file_contents=[]):
    for file_info in file_list:
        if file_info['type'] == 'file' and file_info['name'].endswith(('.py', '.txt', '.md')):
            file_contents.append(file_info['download_url'])
        elif file_info['type'] == 'dir':
            subdir_url = file_info['_links']['self']
            subdir_files = requests.get(subdir_url).json()
            extract_repo_files(subdir_files, path + file_info['name'] + "/", file_contents)
    return file_contents

def fetch_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def fetch_all_files(file_urls):
    text_list = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_file_content, file_urls)
        for text in results:
            if text:
                text_list.append(text)
    return text_list

def process_repo_texts(repo_url):
    repo_content = fetch_github_repo(repo_url)
    file_urls = extract_repo_files(repo_content)
    
    text_list = fetch_all_files(file_urls)
    
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""], chunk_size=1000, chunk_overlap=0)
    character_split_texts = character_splitter.split_text('\n\n'.join(text_list))
    return clean_text_list(character_split_texts)

def clean_text_list(text_list):
    cleaned_texts = []
    for text in text_list:
        text = text.replace('\t', ' ').replace('\n', ' ')
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        cleaned_texts.append(cleaned_text)
    return cleaned_texts
