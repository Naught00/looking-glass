import os
import gitlab
import github

def main():
    gl_token = os.environ['GITLAB_TOKEN']
    gh_token = os.environ['GITHUB_TOKEN']

    gl = gitlab.Gitlab(private_token=gl_token)
    gl.auth()

    gh = github.Github(gh_token)

    gh_user_name = get_details()

    gl_project_details = create_project(gl, gh)

    mirror(gl_project_details[0], gh_user_name, gl_project_details[1], gh_token)

def create_project(gl, gh):
    slug = input("Enter slug: ")

    project = gl.projects.create({'name': slug, 'visibility':'public'})

    user = gh.get_user()
    repo = user.create_repo(slug)
    return (project, slug)

def mirror(project, gh_user_name, slug, token):
    gh_url = "https://" + token + "@github.com/" + gh_user_name + "/" + slug

    mirror = project.remote_mirrors.create({'url': gh_url,
                                        'enabled': True})

def get_details():
    gh_user_name = input("Enter Github username: ")

    return gh_user_name 

main()
 
