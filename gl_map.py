import json
import sys
import re

print("gl_map.py (c) Tom Wiesing 2014")

if len(sys.argv) < 3:
    print("Use: gl_map.py <input_file> <output_file> [<usermap> = usermap.json]")
    sys.exit(0)

# Load Input / Output
input_file = open(sys.argv[1]).read()
output_file = sys.argv[2]

# Load the usermap
try:
  usermap = open(sys.argv[3]).read()
except:
  usermap = open("usermap.json").read()

usermap = json.loads(usermap)

# This is the regexes we will be using
user_regex = re.compile(r"(?:(?<=(\W))|^)\@([a-zA-Z0-9_.][a-zA-Z0-9_\-\.]*)(?:(?=(\W))|$)")
discard_regex = re.compile(r"^_(.*)_$")

# Load the data and here we go.
data = json.loads(input_file)

def map_text(text):
    def replacer(match):
        if usermap.has_key(match.group(2)):
            return "@"+usermap[match.group(2)]
        else:
            return "@"+match.group(2)
    return user_regex.sub(replacer, text)

def map_issue(issue):
    return {
        "body": map_text(issue["body"]),
        "labels": issue["labels"],
        "closed": issue["closed"],
        "comments": [{"body": map_text(c["body"])} for c in issue["comments"] if not discard_regex.match(c["body"])]
    }

# Map everything
data = [map_issue(i) for i in data]


# Write everything back
with open(output_file, "w") as f:
    f.write(json.dumps(data, indent=2))

print("Wrote "+output_file)
