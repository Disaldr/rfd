import re
from dotenv import load_dotenv
import os
from github import Github
import inquirer
from tqdm import tqdm

load_dotenv(override=True)
token = os.environ["GITHUB_TOKEN"]
username = os.environ["GITHUB_USERNAME"]
g = Github(token)

repos_list = []
# get private repos
for repo in g.get_user().get_repos(visibility="private"):
	if repo.owner.login == username:
		repos_list.append(repo)
# get public repos
for repo in g.get_user(login=username).get_repos():
	repos_list.append(repo)
	
repos_names = [x.name for x in repos_list]

questions = [
  inquirer.Checkbox('repos_to_delete',
                    message="Chose repos that you want to delete",
                    choices=repos_names,
                    ),
]
answers = inquirer.prompt(questions)
chosen_repos = [x for x in repos_list if x.name in answers['repos_to_delete']]
for repo in tqdm(chosen_repos):
	repo.delete()