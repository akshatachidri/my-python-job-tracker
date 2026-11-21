from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "jobs.json"

def load_jobs():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []

def save_jobs(jobs):
    with open(FILE, "w") as f:
        json.dump(jobs, f)

@app.route("/")
def home():
    jobs = load_jobs()
    total = len(jobs)
    interviews = len([j for j in jobs if j["status"] == "Interview"])
    offers = len([j for j in jobs if j["status"] == "Selected"])
    rejected = len([j for j in jobs if j["status"] == "Rejected"])
    return render_template("index.html", jobs=jobs, total=total, interviews=interviews, offers=offers, rejected=rejected)

@app.route("/add", methods=["POST"])
def add():
    jobs = load_jobs()
    jobs.append({
        "company": request.form["company"],
        "role": request.form["role"],
        "date": request.form["date"],
        "status": request.form["status"]
    })
    save_jobs(jobs)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    jobs = load_jobs()
    if 0 <= id < len(jobs):
        jobs.pop(id)
        save_jobs(jobs)
    return redirect("/")

if __name__ == "__main__":
    app.run()
