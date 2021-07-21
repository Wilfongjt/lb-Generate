from pprint import pprint
import os
import json
from lib.util import Util
from lib.document import Document
from lib.document_environment import EnvironmentDocument
from lib.development_git import GitDevelopment
from lib.development_local import LocalDevelopment
# from lib.system import ExamplesDevelopment
from lib.development_home import HomeDevelopment

from lib.api_configuration import ApiConfiguration

import tkinter as tk
from tkinter import filedialog

from lib.template import Template
from lib.template_post import PostTemplate
from lib.template_get import GetTemplate
from lib.template_put import PutTemplate
from lib.template_delete import DeleteTemplate
from lib.template_delete_test import DeleteTestTemplate
from lib.template_script import ScriptTemplate

import shutil

from lib.help_functions import report
from lib.help_functions import get_environment
from lib.help_functions import open_api
from lib.help_functions import combine_documents
from datetime import datetime
import subprocess

##########
# [# Generate Nuxtjs Application]
# [* process kind = nuxtjs-app]
##########


def main():
    combined_sql_list = []  # eventually is written to a file
    # [* Generate Heroku Scripts]
    print('Generate Heroku Scripts')
    print('  - Scripts to load, restart, and drop heroku applicatons')

    # [* All configuration files are stored in /config folder]
    config_folder = '{}'.format(os.getcwd().replace('_tasks', 'config'))

    # [1. Select APP Source ]
    sourceConfiguration = open_api(config_folder, file_type="source")
    if not sourceConfiguration:
        print('cancel')
        exit(0)

    # [2. Select APP Target ]
    targetConfiguration = open_api(config_folder, file_type="target")
    if not targetConfiguration:
        print('cancel')
        exit(0)

    # [* Merge Source and Target]
    sourceConfiguration.update(targetConfiguration)
    apiConfiguration = sourceConfiguration

    # setup default environment
    homeDev = HomeDevelopment().setup()

    # [* Create missing folders]
    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()

    # [* Scan configuration for home, source, and target environment configurations]
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [* Find Source configuration]
            sourceDev = get_environment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [* Find Target configuration]
            targetDev = get_environment(apiConfiguration[apiName])

    pprint(targetDev)
    #exit(0)

    print('=================')
    report(homeDev, sourceDev, targetDev)
    print('=================')
    ##########
    # [## Heroku Scripts]
    # [* generate a deployment script]
    # [* generate a destroy script]
    # [* generate a restart script]
    #####
    # configuration eg {"lb-a": {"heroku": {"operations":"C"}}}
    apiNameList = [nm for nm in apiConfiguration
                        if 'heroku' in  apiConfiguration[nm]
                            and 'operations' in apiConfiguration[nm]['heroku']
                            and 'C' in apiConfiguration[nm]['heroku']['operations']]

    #apiNameList = [nm for nm in apiConfiguration
    #                    if 'operations' in  apiConfiguration[nm]['heroku']
    #                        and 'C' in apiConfiguration[nm]['heroku']['operations'] ]

    #apiNameList = [nm for nm in apiConfiguration if 'deploy' in  apiConfiguration and apiConfiguration[nm]['deploy']]

    print('apiNameList',apiNameList)
    for appName in apiNameList:
        print('=====',appName,'=====')
        #pprint(apiConfiguration.flatten())
        pprint(apiConfiguration.flatten(appName, parent_key='app'))

        # [* Deployment script]
        # [ * Dont overwrite scripts when they exist]

        scriptFolder = targetDev.getFolder('sh-scripts')
        # [* Create Heroku deployment script]
        #scriptName = '{}.CREATE.sh'.format(appName)
        scriptName = 'heroku.CREATE.sh'

        overwrite = False
        if Util().file_exists(scriptFolder, scriptName):
            if Util().confirm('Overwrite {}'.format(scriptName), default='N') != 'N':
                overwrite = True
        if overwrite or not Util().file_exists(scriptFolder, scriptName):
            #print('====Flatten=====')
            tmpl = ScriptTemplate(appName,folder='../templates', filename='heroku.create.app.template') \
                .apply(apiConfiguration.flatten()) \
                .apply(apiConfiguration.flatten(appName, parent_key='app'))

            tmpl.saveAs(scriptFolder, scriptName)
            cmd = 'chmod 755 {}/{}'.format(scriptFolder, scriptName)
            returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            print('returned value:', returned_value)
        overwrite = False

        # [* Create Heroku destroy script]
        #scriptName = '{}.DELETE.sh'.format(appName)
        scriptName = 'heroku.DELETE.sh'

        if Util().file_exists(scriptFolder, scriptName):
            if Util().confirm('Overwrite {}'.format(scriptName), default='N') != 'N':
                overwrite = True
        if overwrite or not Util().file_exists(scriptFolder, scriptName):
            #print('====Flatten=====')
            tmpl = ScriptTemplate(appName,folder='../templates', filename='heroku.delete.app.template') \
                .apply(apiConfiguration.flatten()) \
                .apply(apiConfiguration.flatten(appName, parent_key='app'))
            print('output to ', scriptFolder)
            tmpl.saveAs(scriptFolder, scriptName)
            cmd = 'chmod 755 {}/{}'.format(scriptFolder, scriptName)
            returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            print('returned value:', returned_value)
        overwrite = False

if __name__ == "__main__":
    main()