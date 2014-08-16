# GitLabToGitHub

## What is it?

This is a script to export a repository (including issues + comments) from Gitlab and import it to Github.
The only thing lost in the process is who created issues and comments. May also cause a lot of Spam from github when there are a lot of mentions.

## Dependencies

```
pip install gitlab pygithub3
```

## How to use?
### The automatic way
```bash
  bash GitLabToGitHub.sh <gitlab_url_to_repository> <your_gitlab_username> <github_url_to_repo> <github_username> <usermap>
```
Make sure the github repository exists and is empty. 
### The manual way

#### 1: Mirror over the actual repository

Move over the repository from gitlab to github.
```
cd /some/empty/directory
git clone --bare <gitlab_url_to_repository>
git push --mirror <github_url_to_repo>
```

#### 2: Export data from Gitlab

```bash
python gl_export.py <gitlab_url_to_repository> <your_gitlab_username> export.json
```

This will prompt you for your password and then dump all the required data to a file "export.json".

#### 3: Apply a usermap

Create a file "usermap.json" in JSON format with the following content:
```json
{
  "gitlab_username": "github_username"
}
```

Then apply this data to the file export.json you created in the first step:

```bash
python gl_map.py export.json export_mapped.json usermap.json
```

This will create a file export_mapped.json which contains the mapped json data.

#### 4: Import into Github

```
python gh_import.py <github_url_to_repo> <github_username> <data_file>
```

## License

MIT License, see [License.md](License.md)
