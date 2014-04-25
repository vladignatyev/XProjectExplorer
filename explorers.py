#!-*- coding: utf-8 -*-
import json

from plistlib import readPlistFromString
import subprocess
import datetime
from time import sleep
import fnmatch
import os
import re

PROJECT_EXPLORER_KEY_PREFIX = "com.macbuildserver.XCodeProjectExplorer"

LOCK_EXPIRE_TIMEOUT = 10 * 60 # in minutes
CACHE_EXPIRE_TIME = 60 * 60 # in minutes

cache_update_deltatime = datetime.timedelta(hours=1)


class XCodeProjectExplorer(object):
    UNABLE_TO_PARSE_PROJECT_FILE = 504
    UNABLE_TO_FIND_SUITABLE_TARGETS = 505

    def __init__(self, redisConnection):

        """
        self.cache.keyPrefix = PROJECT_EXPLORER_KEY_PREFIX
        self.cache.keyFunc = lambda project: project.cloneUrl
        self.cache.workFunc = lambda project: self.parseProjectTargets(project)
        self.cache.decodeFunc = lambda result: json.loads(result)
        self.cache.encodeFunc = lambda data: json.dumps(data)
        """

        self.cache.expireTime = CACHE_EXPIRE_TIME
        self.cache.lockExpireTime = LOCK_EXPIRE_TIMEOUT


    def _obtainXcodeProjectFiles(self, clonePath):
        projectFiles = []
        for root, dirnames, filenames in os.walk(clonePath):
            for dirname in fnmatch.filter(dirnames, '*.xcodeproj'):
                projectFiles.append(os.path.join(root, dirname))
        return projectFiles

    def parseProjectTargets(self, project):
        projectsTargets = self.findProjectTargets(project)
        return projectsTargets

    def findProjectTargets(self, project):
        def resolve_plist_object(plist, object_id):
            return plist['objects'].get(object_id, None)

        def resolve_plist_object_by_isa(plist, isa):
            for key in plist['objects'].keys():
                object = plist['objects'][key]
                if object['isa'] == isa:
                    return object

        def replace_dict(string, dict):
            s = string
            for k in dict.keys():
                s = s.replace(k, dict[k])
            return s

        projectsTargets = []
        projectFiles = self._obtainXcodeProjectFiles(project.getRepoClonePath())
        for projectFile in projectFiles:
            os.chdir(projectFile)
            os.chdir('..')

            xcProjectTargets = []
            cmd = ['plutil', '-convert', 'xml1', '-o', '-', projectFile + '/project.pbxproj']
            p = readPlistFromString(subprocess.check_output(cmd))
            pbxProject = resolve_plist_object_by_isa(p, 'PBXProject')

            for targetId in pbxProject['targets']:
                target = resolve_plist_object(p, targetId)
                if target.get('productType', None) != "com.apple.product-type.application":
                    continue

                target['buildConfigurationList'] = resolve_plist_object(p, target['buildConfigurationList'])
                l = len(target['buildConfigurationList']['buildConfigurations'])
                for i in range(0, l):
                    o = resolve_plist_object(p, target['buildConfigurationList']['buildConfigurations'][i])
                    target['buildConfigurationList']['buildConfigurations'][i] = o

                def to_rfc1034_string(s):
                    return re.sub(r'[^A-Za-z0-9\.]', '-', s)

                variables = {
                    '${PRODUCT_NAME}': target['productName'],
                    '${PRODUCT_NAME:rfc1034identifier}': to_rfc1034_string(target['productName']),
                    }

                for buildConfiguration in target['buildConfigurationList']['buildConfigurations']:
                    with open(buildConfiguration['buildSettings']['INFOPLIST_FILE'], 'r') as f:
                        plist = readPlistFromString(f.read())
                        buildConfiguration['plist'] = {
                            'bundleIdentifier': replace_dict(plist.get('CFBundleIdentifier', ''), variables),
                            'bundleDisplayName': replace_dict(plist.get('CFBundleDisplayName', '${PRODUCT_NAME}'),
                                                              variables),
                            'bundleIcons': plist.get('CFBundleIcons', None),
                            }

                        if buildConfiguration['plist']['bundleIcons']:
                            buildConfiguration['plist']['primaryIcon'] = buildConfiguration['plist']['bundleIcons'].get(
                                'CFBundlePrimaryIcon', None)
                xcProjectTargets.append(target)

            if not xcProjectTargets:
                continue
            else:
                clonePath = project.getRepoClonePath()
                projectsTargets.append({'project': os.path.relpath(projectFile, clonePath),
                                        'targets': xcProjectTargets})
        return projectsTargets
