import smtplib
import requests
from datetime import datetime, timedelta
import os
import ssl

time = (datetime.now() - timedelta(days=1)).isoformat()

repos = (
    "pittcsc/Summer2022-Internships",
    "quantprep/quantinternships2022",
    "ChrisDryden/Canadian-Tech-Internships-Summer-2022"
)


email = """From: "Bryce Wilson" <{email}>
To: "Bryce Wilson" <{email}>
Subject: New Internships!

Hi Bryce!

The following internship repos have been updated recently.
""".format(email="br"+"yce"+"@"+"bryce"+"mw"+"."+"ca")


count = 0
for repo in repos:
    for commit in requests.get(f"https://api.github.com/repos/{repo}/commits?since={time}", headers={"Accept": "application/vnd.github.v3+json"}).json():
        email += f"{commit['html_url']}\n"
        count += 1

if count:
    with smtplib.SMTP_SSL(os.environ['BRYCE_MAIL_SERVER'], os.environ['BRYCE_MAIL_PORT'], context=ssl.create_default_context()) as server:
        # server.set_debuglevel(2)
        server.login(os.environ['BRYCE_MAIL_USER'], os.environ['BRYCE_MAIL_PASS'])
        server.sendmail("br"+"yce"+"@"+"bryce"+"mw"+"."+"ca", ("br"+"yce"+"@"+"bryce"+"mw"+"."+"ca",), email)
        print(email)
