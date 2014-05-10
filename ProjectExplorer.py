import os
import fnmatch
from Workspace import Workspace

NO_PROJECTS = "No projects in repo"

__author__ = 'prozac631'


class ProjectExplorer(object):

    class Error(Exception):
        pass

    workspaces = []
    projects = []

    def __init__(self):
        pass

    def explore(self, path):
        try:
            os.chdir(path)
        except IOError:
            print "There is no such directory"

        for root, dirnames, filenames in os.walk(os.getcwd()):
            for dirname in fnmatch.filter(dirnames, "*.xcworkspace"):
                os.chdir(dirname)
                path = os.path.abspath("contents.xcworkspacedata")
                w = Workspace(path)
                self.workspaces.append(w)

    @property
    def workspaces(self):
        return self.workspaces

    @property
    def projects(self):
        return self.projects