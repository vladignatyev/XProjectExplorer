import os
import git

__author__ = 'prozac631'

DEFAULT_REPO_PATH = "XProjExplorer"


class Repo(object):

    repo_url = ""
    repo_name = ""
    work_dir = ""
    workspaces = []
    xcodeproj = []

    def __init__(self, url):
        self.repo_url = url

        self.repo_name = self.repo_url.split("/")[-1].split(".git")[0]
        self.work_dir = DEFAULT_REPO_PATH

        os.chdir(os.path.expanduser("~"))

        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
        os.chdir(self.work_dir)

        if not os.path.exists(self.repo_name):
            git.Git().clone(self.repo_url)

        os.chdir(self.repo_name)

        self.repo_path = os.path.abspath(os.getcwd())

    def getWorkspaces(self):
        pass