from bs4 import BeautifulSoup
import requests

def roles():
    jobKeywords = ["consultant",
                    "consultancy",
                    "officer",
                    "communications",
                    "management",
                    "program",
                    "project management",
                    "program management",
                    "crisis response",
                    "humanitarian",
                    "political affairs",
                    "sustainable development",
                    "international development",
                    "public health"]

    jobSeniority = ["p3",
                    "p2",
                    "mid",
                    "senior",
                    "iasc 09",
                    "iasc 10",
                    "iasc 11",
                    "ics 09",
                    "ics 10",
                    "ics 11",
                    "iasc-09",
                    "iasc-10",
                    "iasc-11",
                    "ics-09",
                    "ics-10",
                    "ics-11",
                    ]

    url = "https://www.impactpool.org/search?page=1&per_page=200"
    website = requests.get(url)
    soup = BeautifulSoup(website.content, "html.parser")

    information = []
    for card in soup.select("div.job"):
        h3 = card.find("h3")
        a = card.find("a", href=True)
        if not h3 or not a:
            continue

        link = a["href"]
        if not link.startswith("http"):
            link = "https://www.impactpool.org" + link

        row = card.find("div", attrs = {"wrap":"wrap"})
        company = location = seniority = None
        if row:
            company_div = row.find("div", class_ = "ip-typography", recursive=False)
            inner = row.find("div", class_ ="ip-layout", recursive=False)
            company = company_div.get_text(strip=True) if company_div else None
            if inner:
                parts = [d.get_text(strip=True) for d in inner.find_all("div", class_ = "ip-typography", recursive=False)]
                location = parts[0] if len(parts) > 0 else None
                seniority = parts[1] if len(parts) > 1 else None

        title_lower = h3.get_text(strip=True).lower()
        seniority_lower = (seniority or "").lower()

        title_ok = any(k in title_lower for k in jobKeywords)
        seniority_ok = any(s in seniority_lower for s in jobSeniority)

        if title_ok and seniority_ok:
            information.append({
                "title": h3.get_text(strip=True),
                "organization": company,
                "location": location,
                "seniority": seniority,
                "link":link
            })
    return information

if __name__ == "__main__":
    information = roles()

    for entry in information:
        print(entry["title"], "-", entry["location"])
        print("Organization:", entry["organization"], ",  Seniority:", entry["seniority"])
        print("Access Job on -->  " + entry["link"])
        print()

    print(f"{len(information)} jobs have matched the search!")