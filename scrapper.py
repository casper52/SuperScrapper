import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    company_name = html.find("a",{"class":"s-link"}).string.strip()
    location = html.find("div",{"class":"flex--item fc-black-500 fs-body1"}).text.strip()
    link_id = company_name.lower().replace(" ","-")

    return {
        'title': company_name,
        'company':company_name,
        'location':location,
        'link': f"https://stackoverflow.com/jobs/companies/{link_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping S0: page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"-company"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs/companies?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs