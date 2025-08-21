"""
GitHub operations for HTML pages
"""
import os
from github import Github

def get_html_files_from_repo():
    """
    Get list of HTML files from the GitHub repository
    """
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return []
        
        g = Github(github_token)
        repo = g.get_repo("barisMarathon/html-pages-storage")
        
        # Get all HTML files from the repository
        contents = repo.get_contents("")
        html_files = []
        
        for content in contents:
            if content.name.endswith('.html'):
                html_files.append({
                    'name': content.name,
                    'download_url': content.download_url,
                    'size': content.size,
                    'updated': content.last_modified if hasattr(content, 'last_modified') else 'Unknown'
                })
        
        # Sort by name (most recent first based on timestamp in filename)
        html_files.sort(key=lambda x: x['name'], reverse=True)
        return html_files
        
    except Exception as e:
        print(f"Error fetching HTML files: {e}")
        return []

def get_repo_clone_url():
    """
    Get the clone URL for the HTML pages repository
    """
    return "https://github.com/barisMarathon/html-pages-storage.git"