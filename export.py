import csv

def save_to_file(jobs):
    file = open("jobs.csv", encoding="utf-8-sig", mode="w") # mode: 쓰기
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return