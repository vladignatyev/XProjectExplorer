from Repository import Repo

__author__ = 'prozac631'


class ProjectExplorer(object):

    path = ""
    urls = []
    repos = []

    def __init__(self, path):
        self.path = path
        try:
            f = open(self.path)
        except IOError:
            raise IOError("There is no such file")

        for line in f:
            url = line.split("\n")[0]
            self.urls.append(url)

    def get_repos(self):
        for url in self.urls:
            repo = Repo(url)
            self.repos.append(repo)
        return self.repos