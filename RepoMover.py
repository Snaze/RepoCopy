from github3 import login
import json


def get_connection_info():
    with open("Credentials.json", "r") as the_file:
        to_ret = json.load(the_file)

    return to_ret

if __name__ == "__main__":
    print get_connection_info()

    # gh = login(username='sigmavirus24', password='<password>', url="")
    #
    # sigmavirus24 = gh.user()
    # # <User [sigmavirus24:Ian Cordasco]>
    #
    # print(sigmavirus24.name)
    # # Ian Cordasco
    # print(sigmavirus24.login)
    # # sigmavirus24
    # print(sigmavirus24.followers)
    # # 4
    #
    # for f in gh.iter_followers():
    #     print(str(f))
    #
    # kennethreitz = gh.user('kennethreitz')
    # # <User [kennethreitz:Kenneth Reitz]>
    #
    # print(kennethreitz.name)
    # print(kennethreitz.login)
    # print(kennethreitz.followers)
    #
    # followers = [str(f) for f in gh.iter_followers('kennethreitz')]