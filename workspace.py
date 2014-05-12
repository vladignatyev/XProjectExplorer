from workspaceparser import Parser as WorkspaceParser

__author__ = 'prozac631'


class Workspace(object):

	path = ""
	projects = []

	def __init__(self, path):
		self.path = path
		p = WorkspaceParser()
		with open(self.path, 'r') as f:
			p.parse(f.read())
			self.filerefs = p.workspace.filerefs
			self.projects = filter(lambda fileref: fileref.endswith('.xcodeproj'), p.workspace.filerefs)

	@property
	def projects(self):
		return self.projects