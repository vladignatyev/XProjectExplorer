from workspaceparser import Parser as WorkspaceParser

p = WorkspaceParser()
with open('test/AFNetworking.xml', 'r') as f:
	p.parse(f.read())

print p.workspace.version  # should print '1.0'

print filter(lambda fileref: fileref.path.endswith('.xcodeproj'), p.workspace.filerefs)  # should print all xcodeprojects
for group in p.workspace.groups:
	print group
