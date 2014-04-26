from explorers import XCodeProjectExplorer
import os
import git
import fnmatch

__author__ = 'prozac631'


class Project(object):

    repo_name = ""
    repo_path = ""
    repo_url = ""

    def __init__(self, repo_url):
        pass

    def getProjectTargets(self):
        # from xcodeprojectexplorer
        pass

    def getBuildConfiguration(self):
        # from xcodeprojectexplorer
        pass

    def checkCocoapodsExisting(self):
        for root, dirnames, filenames in os.walk(self.repo_path):
            if len(fnmatch.filter(filenames, '*.podspec')) != 0:
                return True
            else:
                return False