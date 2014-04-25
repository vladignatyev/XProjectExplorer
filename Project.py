from explorers import XCodeProjectExplorer
import os
import git

DEFAULT_PROJECTS_PATH = "/XProjExplorer"

__author__ = 'prozac631'


class Project(object):

    repo_name = ""
    repo_path = ""
    repo_url = ""
    main_folder = DEFAULT_PROJECTS_PATH

    def __init__(self, repo_url):

        self.repo_url = repo_url
        self.repo_name = self.repo_url.split("/")[-1]

        os.chdir(os.path.expanduser("~"))

        if not os.path.exists("XProjExplorer"):
            os.mkdir("XProjExplorer")
        os.chdir("XProjExplorer")

        git.Git().clone(self.repo_url)

        os.chdir(self.repo_name)
        self.repo_path = os.path.abspath(os.getcwd())

    def getProjectTargets(self):
        pass

    def getBuildConfiguration(self):
        pass

    def checkCocoapods(self):
        pass

    def getWorkspaces(self):
        pass

p = Project("https://github.com/1000Memories/TMQuiltView")