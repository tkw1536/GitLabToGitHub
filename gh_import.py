import re
import sys
import json
from pygithub3 import Github
import getpass

print("gl_import.py (c) Tom Wiesing 2014")

if len(sys.argv) < 4:
    print("Use: gh_import.py <github_url_to_repo> <github_username> <input_file>")
    sys.exit(0)

# Parse repo
repo_source_regex = re.compile(r"^(?:git@github\.com:|https?:\/\/github\.com\/)([^\/]+)\/([^\/]+?)(?:\.git)?$")

repo_username = repo_source_regex.match(sys.argv[1]).group(1)
repo_name = repo_source_regex.match(sys.argv[1]).group(2)

print("Logging in to Github. ")
# Get username
github_username = sys.argv[2]

# Load the data
data = open(sys.argv[3]).read()
data = json.loads(data)

print("Logged in. ")

# OK, lets connect to github
gh = Github(login=github_username, password=getpass.getpass())

for issue in data:
  if(len(issue["labels"]) > 0):
    gh.issues.create(dict(title=issue["title"], body=issue["body"], labels=",".join(issue["labels"])), user=repo_username, repo=repo_name)
  else:
    gh.issues.create(dict(title=issue["title"], body=issue["body"]), user=repo_username, repo=repo_name)

for (id, issue) in enumerate(data):
  for c in issue["comments"]:
    gh.issues.comments.create(id+1, c["body"], user=repo_username, repo=repo_name)
  if issue["closed"]:
    gh.issues.update(id+1, dict(state="closed"), user=repo_username, repo=repo_name)


print("Done. ")
