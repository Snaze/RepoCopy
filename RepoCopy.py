from github3 import login
import json
from subprocess import call
import os
import shutil

current_dir = os.getcwd()


def get_connection_info():
    with open("Credentials.json", "r") as the_file:
        to_ret = json.load(the_file)

    return to_ret


def print_output(to_output, verbose=False):
    if verbose:
        print (to_output)


def copy_repository(dest_gh, name, repo, verbose=False):

    print_output("Moving Repo '{0}'".format(name), verbose)

    os.chdir(current_dir)

    r = dest_gh.create_repo(name,
                            description=repo.description,
                            homepage=repo.homepage,
                            private=repo.private,
                            has_issues=repo.has_issues,
                            has_wiki=repo.has_wiki,
                            has_downloads=repo.has_downloads)

    r_url = r.svn_url

    if os.path.exists("../RepoCopyTemp"):
        shutil.rmtree("../RepoCopyTemp")

    os.chdir(os.path.join(current_dir, ".."))

    return_code = call(["git", "clone", "--mirror", repo.svn_url, "RepoCopyTemp"])
    print_output("git clone --mirror {0} RepoCopyTemp".format(repo.svn_url), verbose)
    print_output("return_code = {0}".format(return_code), verbose)
    if return_code != 0:
        print ("Error")
        return False

    os.chdir(os.path.join(current_dir, "..", "RepoCopyTemp"))

    return_code = call(["git", "remote", "set-url", "origin", r_url])
    print_output("git remote set-url origin {0}".format(r_url), verbose)
    print_output("return_code = {0}".format(return_code), verbose)
    if return_code != 0:
        print ("Error")
        return False

    return_code = call(["git", "push", "-f", "origin"])
    print_output("git push -f origin", verbose)
    print_output("return_code = {0}".format(return_code), verbose)
    if return_code != 0:
        print ("Error")
        return False

    os.chdir(os.path.join(current_dir, ".."))

    if os.path.exists("./RepoCopyTemp"):
        shutil.rmtree("./RepoCopyTemp")

    print_output("Completed Moving Repo '{0}'".format(name), verbose)

    return True


if __name__ == "__main__":
    connection_info = get_connection_info()

    source_login = connection_info["from"]["login"]
    source_password = connection_info["from"]["password"]
    source_url = connection_info["from"]["url"]

    dest_login = connection_info["to"]["login"]
    dest_password = connection_info["to"]["password"]
    dest_url = connection_info["to"]["url"]

    destination = dest_url
    if destination == "":
        destination = "https://api.github.com/"

    print ("    RepoMover    ")
    print ("-----------------------------------")
    print ("Preparing to move all repositories from {0} to {1}".format(source_url, destination))
    print ("Source User = {0}, Destination User = {1}".format(source_login, dest_login))

    if source_url == "":
        source_gh = login(username=source_login, password=source_password)
    else:
        source_gh = login(username=source_login, password=source_password, url=source_url)

    if dest_url == "":
        dest_gh = login(username=dest_login, password=dest_password)
    else:
        dest_gh = login(username=dest_login, password=dest_password, url=dest_url)

    source_user = source_gh.user()
    dest_user = dest_gh.user()

    print ("Source User = {0}".format(source_user))
    print ("Dest User = {0}".format(dest_user))

    if source_user is None:
        print ("Connection failed to source")
        exit(1)

    if dest_user is None:
        print ("Connection failed to destination")
        exit(1)

    source_repo_dict = dict()
    dest_repo_dict = dict()

    for repo in source_gh.iter_repos():
        source_repo_dict[repo.name] = repo

    for repo in dest_gh.iter_repos():
        dest_repo_dict[repo.name] = repo

    num_source_repos = len(source_repo_dict)
    num_dest_repos = len(dest_repo_dict)

    print ("{0} Source Repositories Found".format(num_source_repos))
    print ("{0} Destination Repositories Found".format(num_dest_repos))

    to_copy_repo_dict = {key:source_repo_dict[key] for key in source_repo_dict if key not in dest_repo_dict}

    print ("{0} Repositories will be copied (which do not exist at the destination)".format(len(to_copy_repo_dict)))

    for repo_name in to_copy_repo_dict:
        ret_val = copy_repository(dest_gh, repo_name, to_copy_repo_dict[repo_name], verbose=True)
        if not ret_val:
            break

    print ("RepoMover Complete")
