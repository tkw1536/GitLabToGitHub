# GitLabToGitHub

## What is it?

This is a script to export a repository (including issues + comments) from Gitlab and import it to Github.
The only thing lost in the process is who created issues and comments. May also cause a lot of Spam from github when there are a lot of mentions.

## How does it work?

### 1: Export data from Gitlab

```bash
python gl_export.py <gitlab_url_to_repository> <your_gitlab_username> export.json
```

This will prompt you for your password and then dump all the required data to a file "export.json".

### 2: Apply a usermap

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

### 3: Import into Github

(Not yet done)

## License

MIT License, see [License.md](License.md)
