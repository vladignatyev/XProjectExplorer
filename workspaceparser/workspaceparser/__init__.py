from defusedxml.ElementTree import fromstring as parse_from_string

class Parser(object):
	CONTAINER = 'container'
	GROUP = 'group'


	class Error(Exception):
		pass


	class WorkspaceItem(object):
		TAG = 'Workspace'
		def __init__(self, version='1.0'):
			self.filerefs = []
			self.groups = []
			self.version = str(version)

		def group(self, name):
			groups = filter(lambda g: g.name == name, self.groups)
			if len(groups) == 1:
				return groups[0] 
			return groups or None


	class GroupItem(object):
		TAG = 'Group'
		def __init__(self, location, name, filerefs=(), groups=()):
			self.locationType, self.path = location.split(':')
			if not self.locationType or not name:
				raise Parser.Error("GroupItem Error. Passed parameters: %s", 
					{'location': location, 'name': name, 'filerefs': filerefs})

			self.name = str(name)
			self.filerefs = list(filerefs)
			self.groups = list(groups)

		def __eq__(self, other):
			return self.name == other.name and self.filerefs == other.filerefs



	class FileRefItem(object):
		TAG = 'FileRef'
		def __init__(self, location):
			self.location = location
			self.locationType, self.path = location.split(':')

		def __eq__(self, other):
			return other.locationType == self.locationType and self.path ==\
				other.path and self.location == other.location


	def _parse_fileref(self, fileRefTag):
		location = fileRefTag.attrib.get('location', None)
		if not location:
			raise Parser.Error('FileRef should have "location" attribute! %s' % fileRefTag.attrib)
		return Parser.FileRefItem(location)

	def _parse_group(self, groupTag):
		location = groupTag.attrib.get('location', None)
		name = groupTag.attrib.get('name', None)
		group = Parser.GroupItem(location=location, name=name)
		for child in groupTag:
			if child.tag == Parser.FileRefItem.TAG:
				group.filerefs.append(self._parse_fileref(child))
			if child.tag == Parser.GroupItem.TAG:
				group.filerefs.append(self._parse_group(child))
			else:
				raise Parser.Error('Unsupported tag %s' % child.tag)
		return group

	def parse(self, stream):
		workspaceTag = parse_from_string(stream)

		if workspaceTag.tag != Parser.WorkspaceItem.TAG:
			raise Parser.Error('Root tag should be <Workspace ...>')

		workspaceVersion = workspaceTag.attrib['version']
		if workspaceVersion != '1.0':
			raise Parser.Error('Supported only Workspace version 1.0. Provided: %s' % workspaceVersion)

		workspace = Parser.WorkspaceItem()

		for child in workspaceTag:
			if child.tag == Parser.FileRefItem.TAG:
				workspace.filerefs.append(self._parse_fileref(child))
			elif child.tag == Parser.GroupItem.TAG:
				workspace.groups.append(self._parse_group(child))
			else:
				raise Parser.Error('Unsupported tag %s' % child.tag)

		self.workspace = workspace
		return self.workspace
