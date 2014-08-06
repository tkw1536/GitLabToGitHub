#!/usr/bin/env python

import sys

import gitlab
import getpass

print("Migrating issues from GitLab to GitHub. ")

# Read in all the information.
gitlab_host = raw_input("Please enter your gitlab host: ")
gitlab_user = raw_input("Please enter your gitlab username: ")
gitlab_pass = getpass.getpass()

try:
    gitl = gitlab.Gitlab(gitlab_host)
    gitl.login(gitlab_user, gitlab_pass)
except:
    sys.stderr.write("Unable to login to gitlab. ")
    sys.exit(1)

print("Logged in. ")
gitlab_repo = raw_input("Enter the group/name of the repository to access: ")


gitlab_id = -1

for p in gitl.getprojects():
    if p["path_with_namespace"] == gitlab_repo:
        gitlab_id = p["id"]
        break
if gitlab_id == -1:
    sys.stderr.write("Unable to find project. ")
    sys.exit(1)

print("Accessing project issues from "+str(gitlab_id))


issues = []
page = 1

while True:
    res = gitl.getprojectissues(gitlab_id, page=page, per_page=100)
    if len(res) > 0 and page < 1000:
        issues.extend(res)
        page = page + 1
    else:
        break

issues = sorted(issues, key=lambda k:k["iid"])
issues = [({
    "title": i["title"],
    "body": i["description"],
    "labels": i["labels"]
}, i["state"] == "closed") for i in issues]

for (i, c) in issues:
    continue
    issue = github.create_issue(i)["number"]
    if c:
        issue = github.edi_issue(i, {"state": "closed"})


print("Done. ")
