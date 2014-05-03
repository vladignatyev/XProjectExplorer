import unittest
from workspaceparser import Parser as WorkspaceParser
from defusedxml.common import EntitiesForbidden

class WorkspaceParserTestCase(unittest.TestCase):
	def load(self, parser, path):
		with open(path, 'r') as f:
			parser.parse(f.read())
		return parser

	def test_fixture_GraphSketcher(self):
		p = self.load(WorkspaceParser(), 'tests/GraphSketcher.xml')
		self.assertIn(WorkspaceParser.FileRefItem('group:GraphSketcher/iPad/GraphSketcher-iPad.xcodeproj'),\
		p.workspace.filerefs)

		self.assertIn(WorkspaceParser.FileRefItem('group:OmniGroup/Tools/FixStringsFile/FixStringsFile.xcodeproj'),\
		p.workspace.group('Tools').filerefs)

		self.assertEquals(len(p.workspace.filerefs), 1)

	def test_fixture_AFNetworking(self):
		p = self.load(WorkspaceParser(), 'tests/AFNetworking.xml')
		self.assertIn(WorkspaceParser.FileRefItem('group:Tests/AFNetworking Tests.xcodeproj'),\
		p.workspace.filerefs)
		self.assertIn(WorkspaceParser.FileRefItem('group:Example/AFNetworking iOS Example.xcodeproj'),\
		p.workspace.filerefs)

		self.assertIn(WorkspaceParser.FileRefItem('group:AFNetworking.h'),\
		p.workspace.group('AFNetworking').filerefs)

		self.assertEquals(len(p.workspace.group('AFNetworking').groups), 6)


	def test_sec_BillionLaughs(self):
		with self.assertRaises(EntitiesForbidden):
			p = self.load(WorkspaceParser(), 'tests/sec_BillionLaughs.xml')

	def test_sec_ExternalEntity(self):
		with self.assertRaises(EntitiesForbidden):
			p = self.load(WorkspaceParser(), 'tests/sec_ExternalEntity.xml')
	

if __name__ == '__main__':
	unittest.main()