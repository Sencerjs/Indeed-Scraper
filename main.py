import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv


# Create url based position and location
def get_url(position, location):
    url = f"https://www.indeed.com/jobs?q={position}&l={location}"
    return url


# Exracting informations from results
def get_record(job):
    job_url = "https://www.indeed.com" + job.h2.a.get("href")
    job_title = job.h2.a.span.get("title")
    job_location = job.find("div", "companyLocation").text
    job_summary = job.find("div","job-snippet").text.strip()
    company = job.find("span", "companyName").text
    post_date = job.find("span", "date").text
    today = datetime.today().strftime("%Y-%m-%d")
    job_salary = ""
    try:
        job_salary = job.find("div", "attribute_snippet").text.strip()
    except:
        job_salary = "No Salary Info" 

    
    result = (job_title, job_location, company, job_summary, post_date, today, job_salary, job_url)
    
    return result

# Collect all data 
def program(position, location):
    results = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("div", "job_seen_beacon")
        
        for job in jobs:
            result = get_record(job)
            results.append(result)
        
        try:
            url = "https://www.indeed.com" + soup.find("a", {"aria-label": "Next"}).get("href")
        except AttributeError:
            break 


# Save results to csv
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Job Title", "Location", "Company", "Post Date", "Extract Date", "Summary", "Salary", "Url"])
        writer.writerows(results)
        

# Run program with your criteria
program("data engineer", "los angeles")