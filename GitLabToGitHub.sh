#!/bin/bash

gitlab="$1"
gitlab_user="$2"
github="$3"
github_user="$4"

echo "Copying repository data ..."
git clone --bare "$gitlab" tmp
cd tmp
git push --mirror "$github"
cd ..
echo "Exporting issue data from gitlab ..."
python gl_export.py "$gitlab" "$gitlab_user" data_0.json
echo "Mapping usernames ..."
python gl_map.py data_0.json data_1.json "$5"
echo "Importing issue data to github ..."
python gh_import.py "$github" "$github_user" data_1.json
echo "Cleaning up temporary files ..."
rm data_0.json data_1.json
rm -rf tmp
