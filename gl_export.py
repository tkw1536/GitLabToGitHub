#!/usr/bin/env python

import sys
import json
import re
import requests

import gitlab
import getpass

def gitlab_get(gilab_client, url, page=1, per_page=100):
    data = {'page': page, 'per_page': per_page}

    request = requests.get(gilab_client.api_url+url, params=data,
                           headers=gilab_client.headers, verify=gilab_client.verify_ssl)
    if request.status_code == 200:
        return json.loads(request.content.decode("utf-8"))
    else:
        return False

def gitlab_grab_issues(gitlab_client, project_id):
    issues = []

    # Grab all the issues
    page = 1
    while True:
        res = gitl.getprojectissues(gitlab_id, page=page, per_page=100)
        if len(res) > 0 and page < 1000:
            issues.extend(res)
            page = page + 1
        else:
            break

    return issues

def gitlab_grab_comments(gitlab_client, project_id, issue_id):
    comments = []

    # Grab all the issues
    page = 1
    while True:
        res = gitlab_get(gitlab_client, "/projects/"+str(project_id)+"/issues/"+str(issue_id)+"/notes", page=page, per_page=100)
        if len(res) > 0 and page < 1000:
            comments.extend(res)
            page = page + 1
        else:
            break

    return comments

def gitlab_build_comments(gitlab_client, project_id, issue_id):
    return [{"body": c["body"]} for c in gitlab_grab_comments(gitlab_client, project_id, issue_id)]

def build_gitlab_issues(gitlab_client, project_id):
    return [{
        "title": i["title"],
        "body": i["description"],
        "labels": i["labels"],
        "comments": gitlab_build_comments(gitlab_client, project_id, i["id"]),
        "closed": i["state"] == "closed"
    } for i in gitlab_grab_issues(gitlab_client, project_id)]

user_regex = r"@(.+?)\b"

print("Exporting issues from Gitlab")

if len(sys.argv) < 3:
    print("Usage: gl_export.py <gitlab_url> <gitlab_user> [<destination> = export.json]")
    sys.exit(0)



gitlab_user = sys.argv[2]

# extarct the gitlab host and repo from the first argument
url_regex = r'^http(?:s?)://(.*)/([^/]+/[^/]+)(?:/?)$|^git@(.*):([^/]+/[^/]+)\.git$'
gitlab_host = re.findall(url_regex, sys.argv[1])

# and save them in some variables
gitlab_repo = gitlab_host[0][1]
gitlab_host = "http://"+gitlab_host[0][0]

# and try the password.
gitlab_pass = getpass.getpass()

try:
    gitl = gitlab.Gitlab(gitlab_host)
    gitl.login(gitlab_user, gitlab_pass)
except:
    sys.stderr.write("Unable to login to gitlab. ")
    sys.exit(1)

print("Logged in. ")


gitlab_id = -1

for p in gitl.getprojects():
    if p["path_with_namespace"] == gitlab_repo:
        gitlab_id = p["id"]
        break
if gitlab_id == -1:
    sys.stderr.write("Unable to find project. ")
    sys.exit(1)

print("Accessing project issues from "+str(gitlab_id))

issues = build_gitlab_issues(gitl, gitlab_id)

fn = sys.argv[3] or "export.json"


with open(fn, "w") as text_file:
    text_file.write(json.dumps(issues))

print("Wrote "+fn)
