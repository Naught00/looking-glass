import os
import gitlab
import github

def main():
    gl_token = os.environ['GITLAB_TOKEN']
    gh_token = os.environ['GITHUB_TOKEN']

    gl = gitlab.Gitlab(private_token=gl_token)
    gl.auth()

    gh = github.Github(gh_token)
    gh_user_name = get_gh_user_name()

    slug = get_slug()
    project = create_project(gl, gh, slug)

    mirror(project, gh_user_name, slug, gh_token)

def create_project(gl, gh, slug):
    project = gl.projects.create({'name': slug, 'visibility':'public'})

    user = gh.get_user()
    user.create_repo(slug)

    return project

def mirror(project, gh_user_name, slug, token):
    gh_url = "https://" + token + "@github.com/" + gh_user_name + "/" + slug

    project.remote_mirrors.create({'url': gh_url,
                                        'enabled': True})

def get_gh_user_name():
    gh_user_name = input("Enter Github username: ")

    return gh_user_name 

def get_slug():
    slug = input("Enter slug of new project: ")
    
    return slug

main()
