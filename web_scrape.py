from bs4 import BeautifulSoup
import requests

def scrape_job(pages=20):
    information = []
    keywords = ["rfp",
                "request for proposal", 
                "rfq", 
                "request for quote", "rfi", 
                "request for information", 
                "m&e", 
                "monitoring", 
                "evaluation", 
                "interest", 
                "expresion of interest", 
                "call for expressions of interest", 
                "eoi",
                "assessment",
                "data",
                "analysis",
                "analytics"
                    ]

    for page in range(0,pages):
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
            link_tag = job.find("a")
            link = link_tag["href"] if link_tag and link_tag.get("href") else None
            if link and not link.startswith("http"):
                link = "https://reliefweb.int" + link


            title_lower = job.get_text(strip=True).lower()
            
            if any(keyword in title_lower for keyword in keywords):
                information.append({
                        "title": job.get_text(strip=True),
                        "location": loc.get_text(strip=True),
                        "organization": org.get_text(strip=True),
                        "posted": posted.get_text(strip=True),
                        "closing date": closing.get_text(strip=True),
                        "link": link,
                })

    return information

if __name__ == "__main__":
    information = scrape_job()

    for entry in information:
        print(entry["title"], "-", entry["location"])
        print("Organization:", entry["organization"], ",  Posted on: ", entry["posted"],",  Ending on: ", entry["closing date"])
        print("Access Job on -->   " + entry["link"])
        print()

    print(f"{len(information)} jobs have matched the search!")
