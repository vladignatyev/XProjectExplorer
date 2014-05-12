from explorer import ProjectExplorer
from explorer import NO_PROJECTS
import sys

__author__ = 'prozac631'

p = ProjectExplorer()
try:
	result = p.explore("/home/prozac631/XProjExplorer/TMQuiltView")
	if result == NO_PROJECTS:
		print "No projects found. Exiting now."
		sys.exit()
except ProjectExplorer.Error as e:
	print "Some explorer error occured: %s" % e