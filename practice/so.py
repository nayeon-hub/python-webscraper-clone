import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"



def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text,"html.parser")
  pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page {page}")
    result = requests.get(f"{URL}&pg={page}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)

def extract_job(html):
  title = html.find("h2",{"class":"mb4"}).find("a")["title"]
  company, location= html.find("h3",{"class":"mb4"}).find_all("span",recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']
  return {"title":title,"company":company,"location": location,"job_id": f"https://stackoverflow.com/jobs/{job_id}"}
  #get_text는 none을 반환하지 않음 string과 다르게


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs