import os

from flask import Flask, Request, request
from github import Github

token = os.environ.get('GH_TOKEN')
g = Github(token)
repo = g.get_repo('9CHWW0x/TRPO')
app = Flask(__name__)


def create_branch(repo, name):
    master = repo.get_git_ref('heads/master')
    master_sha = master.object.sha
    ref_name = 'refs/heads/{}'.format(name)
    repo.create_git_ref(ref_name, master_sha)


def issue_branch(num):
    return 'issue{}'.format(num)


def opened(repo, num):
    name = issue_branch(num)
    create_branch(repo, name)
    return 'Created'


def closed(repo, num):
    name = issue_branch(num)
    branch = repo.get_git_ref('heads/{}'.format(name))
    branch.delete()
    return 'Closed'

@app.route("/", methods=['GET', 'POST'])
def handler():
    json = request.json
    action = json['action']
    num = json['issue']['number']
    if action == 'opened':
        return opened(repo, num)
    elif action == 'closed':
        return closed(repo, num)
    else:
        return 'Nothing'
