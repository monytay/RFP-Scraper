from bs4 import BeautifulSoup
import requests

information = []

for page in range(0,20):
    base = "https://reliefweb.int/jobs"
    url = f"{base}?page={page}"
    website = requests.get(url)
    soup = BeautifulSoup(website.content, "html.parser")


    job = soup.find_all("h3", attrs = {"class":"rw-river-article__title"})
    location = soup.find_all("p", attrs = {"class":"rw-entity-country-slug"})
    organization = soup.find_all("dd", attrs = {"class":"rw-entity-meta__tag-value rw-entity-meta__tag-value--source rw-entity-meta__tag-value--taglist"})
    posted = soup.find_all("dd", attrs = {"class":"rw-entity-meta__tag-value rw-entity-meta__tag-value--posted rw-entity-meta__tag-value--date"})
    closingDate = soup.find_all("dd", attrs = {"class":"rw-entity-meta__tag-value rw-entity-meta__tag-value--closing-date rw-entity-meta__tag-value--date rw-entity-meta__tag-value--last"})

    for job, loc, org, posted, closing in zip(job, location, organization, posted, closingDate):
        information.append({
                "title": job.get_text(strip=True),
                "location": loc.get_text(strip=True),
                "organization": org.get_text(strip=True),
                "posted": posted.get_text(strip=True),
                "closing date": closing.get_text(strip=True)
        })

for entry in information:
    print(entry["title"], "-", entry["location"])
    print("Organization:", entry["organization"], ",  Posted on: ", entry["posted"],",  Ending on: ", entry["closing date"])
    print()

