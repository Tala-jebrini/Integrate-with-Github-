import json
import requests

USER_NAME = "Mohammad-Zaben/"
TOKEN = "ghp_Tq7Xx8XW481lD9ycZovKKwvHiXQ1XAMHe"
HEADERS = {
    "Authorization": f"token {TOKEN}"
}


def array_search(key_list, original_list):
    final_dict = {}
    for key in key_list:
        final_dict[key] = original_list[key]
    return final_dict


def get_branches(url, repo_name):
    key_list = ["name", "commit"]
    branch_list = []
    branch_url = url + repo_name + "/branches"
    response = requests.get(branch_url, headers=HEADERS)
    # Checking if the request was successful
    if response.status_code == 200:
        # Printing the retrieved data
        branchs = response.json()
        for i in range(len(branchs)):
            branch = json.dumps(branchs[i])
            branch_dict = json.loads(branch)
            final_branch_dict = array_search(key_list, branch_dict)
            branch_list.append(final_branch_dict)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return branch_list


def get_repository(user_name):
    url = "https://api.github.com/users/" + user_name + "repos"
    # Your personal access token
    response = requests.get(url, headers=HEADERS)
    repository_list = []
    # Checking if the request was successful
    if response.status_code == 200:
        # Printing the retrieved data
        j = response.json()

        for i in range(len(j)):
            repo = json.dumps(j[i])
            repo_dict = json.loads(repo)
            repository_list.append(repo_dict)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return repository_list


def get_commits(url, repo_name):
    key_list = ["url", "comments_url", "commit"]
    commits_url = url + repo_name + "/commits"
    response = requests.get(commits_url, headers=HEADERS)
    commit_list = []
    if response.status_code == 200:
        # Printing the retrieved data
        json_response = response.json()

        for i in range(len(json_response)):
            commits = json.dumps(json_response[i])
            commits_dict = json.loads(commits)
            final_commits_dict = array_search(key_list, commits_dict)
            final_commits_dict["commit"] = get_commit(final_commits_dict["commit"])
            commit_list.append(final_commits_dict)

    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return commit_list


def get_commit(commit_dict):
    key_list = ["url", "author", "committer", "message", "comment_count"]
    final_commit = array_search(key_list, commit_dict)
    return final_commit


def get_commit_comment(url, repo_name):
    commit_comment_url = url + repo_name + "/comments"
    key_list = ["commit_id", "body", "user"]
    response = requests.get(commit_comment_url, headers=HEADERS)
    Commit_comment_list = []

    if response.status_code == 200:
        # Printing the retrieved data
        json_response = response.json()

        for i in range(len(json_response)):
            comments = json.dumps(json_response[i])
            comments_dict = json.loads(comments)
            final_comments_dict = array_search(key_list, comments_dict)
            Commit_comment_list.append(final_comments_dict)

    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return Commit_comment_list


def get_collaborators(url, repo_name):
    collaborators_url = url + repo_name + "/collaborators"
    key_list = ["login", "role_name"]

    response = requests.get(collaborators_url, headers=HEADERS)
    collaborators_list = []

    if response.status_code == 200:
        # Printing the retrieved data
        json_response = response.json()

        for i in range(len(json_response)):
            collaborator = json.dumps(json_response[i])
            collaborator_dict = json.loads(collaborator)
            final_collaborator_dict = array_search(key_list, collaborator_dict)
            collaborators_list.append(final_collaborator_dict)

    else:
        print(f"Failed to retrieve data: {response.status_code}")

    return collaborators_list


def create_repository_list(url, repo_list):
    repository_list = []
    for i in range(len(repo_list)):
        repo_list[i]["Branches"] = get_branches(url, repo_list[i]["name"])
        repo_list[i]["Commits"] = get_commits(url, repo_list[i]["name"])
        repo_list[i]["Commit comment"] = get_commit_comment(url, repo_list[i]["name"])
        repo_list[i]["Collaborators"] = get_collaborators(url, repo_list[i]["name"])
        keys_to_keep = ["Branches", "Commits", "Commit comment", "Collaborators"]
        # Create a new dictionary with only the desired keys
        final_repo_dict = {key: repo_list[i][key] for key in keys_to_keep}
        repository_list.append(final_repo_dict)

    print(json.dumps(repository_list[0], indent=3))

if __name__ == '__main__':
    url = "https://api.github.com/repos/" + USER_NAME
    repo_list = get_repository(USER_NAME)
    create_repository_list(url, repo_list)
