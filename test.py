import requests
from bs4 import BeautifulSoup

url = "https://github.com/orgs/tensorflow/repositories"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

repo_names = []
for repo in soup.select(".lh-condensed a"):
    repo_names.append(repo.text.strip())

print(repo_names)