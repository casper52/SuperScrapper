from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from export import save_to_file

app = Flask("Casper Job Scrapper")

db = {}

@app.route("/")
def home():
    return render_template("casper.html") #templates 폴더에 저장한 html 호출

@app.route("/report")
def report():
    word = request.args.get('word') #검색어 추출
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else: #word가 존재하지 않을 경우 리다이렉트
        return redirect("/")
    return render_template("report.html", #렌더링, html에 데이터를 넘겨준다
                           searchingBy = word,
                           resultsNumber = len(jobs),
                           jobs = jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word: #검색어에 해당하는 결과가 없으면 홈으로 리다이렉트
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv") #export 한 csv파일 다운로드
    except:
        return redirect("/")

app.run()
