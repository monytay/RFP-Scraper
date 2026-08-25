from bs4 import BeautifulSoup

with open("https://reliefweb.int/jobs", "r") as f:
    doc = BeautifulSoup(f, "html.parser")

print(doc)
