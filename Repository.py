import fnmatch
import os
import git
from xml.dom import minidom

__author__ = 'prozac631'

DEFAULT_REPO_PATH = "XProjExplorer"


class Repo(object):

    repo_url = ""
    repo_name = ""
    work_dir = ""
    workspaces = []

    def __init__(self, repo_url):
        self.repo_url = repo_url
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
        result = []
        for root, dirnames, filenames in os.walk(self.repo_path):
            for dirname in fnmatch.filter(dirnames, "*.xcworkspace"):
                self.workspaces.append(os.path.abspath(dirname))
        os.chdir(self.workspaces[0])
        for root, dirnames, filenames in os.walk(os.getcwd()):
            for filename in filenames:
                result.append(filename)

        xcodeproj = minidom.parse(result[0]).getElementsByTagName("FileRef")[0].attributes['location'].value

        return result
