import requests
from bs4 import BeautifulSoup


LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_requests(i):
  indeed_result = requests.get(f"{URL}&start={i*LIMIT}")
  indeed_soup = BeautifulSoup(indeed_result.text,"html.parser")
  return indeed_soup
  

def get_last_page():
  #마지막 page 확인하는 함수
  i = 0
  while True:
    indeed_soup = get_requests(i)
    pagination = indeed_soup.find("ul",{"class":"pagination-list"})
    last_page = pagination.find_all("li")[-1].get_text()
    if last_page != "":
      break
    i += 1
  return int(last_page)

def extract_job(html):
  title = html.find("h2",{"class":"title"}).find("a")["title"]
  company = html.find("span",{"class":"company"})
  company_anchor = company.find("a")
  if company_anchor is None:
    company = company.string
  else : 
    company = company_anchor.string
  company = company.strip()
  location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {'title':title,"company":company,"location":location,"link":f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"}

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: Page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_indeed_jobs(last_page)
  return jobs