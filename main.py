import os
import csv
import pyperclip
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from weasyprint import HTML
import re
import shutil
from pathlib import Path
import time

#configuration
USER_NAME = "Your_Name_Here" 
BASE_DIR = os.path.expanduser("~/JobApplications")
RESUME_KEYWORDS = ["FlowCV", "Resume"]
COVER_KEYWORDS = ["FlowCV", "Cover"]
RESUME_FILENAME = f"{USER_NAME}_Resume.pdf"
COVER_FILENAME = f"{USER_NAME}_Cover_Letter.pdf"

DOWNLOADS_DIR = Path.home() / "Downloads"
os.makedirs(BASE_DIR, exist_ok=True)

LOG_FILE = os.path.join(BASE_DIR, "applications_log.csv")

# Get copied job URL from clipboard
job_url = pyperclip.paste().strip() 
if not job_url.startswith("http"):
    print("No job URL found. Please copy a valid link.")
    exit()

print(f"\n Fetching URL: {job_url}")

try:
    response = requests.get(job_url, timeout=10)
    response.raise_for_status()
    html = response.text
except Exception as e:
    print(f"Failed to fetch URL: {e}")
    exit()

# Parse and extract job title
soup = BeautifulSoup(html, "html.parser")
title = soup.title.string if soup.title else "Unknown_Job_Title"
print(f"Page title: '{title}'")

# Create a clean folder name
job_folder_name = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:100]
if not job_folder_name or len(job_folder_name) < 2:
    job_folder_name = f"Job_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
print(f"Final folder name: '{job_folder_name}'")

job_folder = os.path.join(BASE_DIR, job_folder_name)
os.makedirs(job_folder, exist_ok=True)

# Save as PDF
pdf_path = os.path.join(job_folder, "job_posting.pdf")
try:
    HTML(string=html, base_url=job_url).write_pdf(pdf_path)
    print(f"Saved job posting to: {pdf_path}")
except Exception as e:
    print("Failed to save PDF:", e)
    exit()

#automatically move the resume and cover letter
def get_latest_pdf(*keywords):
    pdfs = list(DOWNLOADS_DIR.glob("*.pdf"))
    filtered = [
        f for f in pdfs
        if all(k.lower() in f.name.lower() for k in keywords)
    ]
    if not filtered:
        return None
    latest_file = max(filtered, key=lambda f: f.stat().st_mtime)
    if time.time() - latest_file.stat().st_mtime < 3600:
        return latest_file
    return None

def confirm_and_move(latest_file, dest_filename, folder):
    if latest_file:
        answer = input(f"\nUse latest '{latest_file.name}' as {dest_filename}? [Y/n]: ").strip().lower()
        if answer in ["", "y", "yes"]:
            dest_path = os.path.join(folder, dest_filename)
            shutil.move(latest_file, dest_path)
            print(f"{dest_filename} moved to job folder.")
            return dest_path
    else:
        print(f"No recent '{dest_filename}' found in Downloads.")
    return ""

resume_file = get_latest_pdf(*RESUME_KEYWORDS)
resume_path = confirm_and_move(resume_file, RESUME_FILENAME, job_folder)

cover_file = get_latest_pdf(*COVER_KEYWORDS)
cover_letter_path = confirm_and_move(cover_file, COVER_FILENAME, job_folder)

#log to csv
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    if job_url in df["URL"].values:
        print("\nJob already logged. Skipping duplicate entry.")
        exit()

status = input("\nEnter application status [applied]: ").strip() or "applied"

log_entry = {
    "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "JOB_TITLE": title,
    "STATUS": status,
    "URL": job_url,
}

fieldnames = ["TIMESTAMP", "JOB_TITLE", "STATUS", "URL"]
file_exists = os.path.exists(LOG_FILE)

with open(LOG_FILE, mode="a", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerow(log_entry)

print("Logged application in CSV.\n")
