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

import shutil

from lib.help_functions import report
from lib.help_functions import get_environment
from lib.help_functions import open_api
from lib.help_functions import combine_documents
from datetime import datetime

##########
# [# Generate Nuxtjs Application]
# [* process kind = nuxtjs-app]
##########


def main():
    combined_sql_list = []  # eventually is written to a file
    # [* Generate Nuxtjs Application]
    print('Generate Nuxtjs Application')
    print('  - load app configuration, generate funcPattern key and values')

    # [* All configuration files are stored in a common folder]
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

    print('=================')
    report(homeDev, sourceDev, targetDev)
    print('=================')

    ##########
    # [## Nuxt Applications]
    # [* generate new nuxt app]
    # [* copy existing app]
    #####
    apiNuxtjsNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'nuxtjs-app']
    for appName in apiNuxtjsNameList:
        print('appName', appName)
        # [ * Dont overwrite scripts when they exist]
        # [* Create script to generate nuxt app]
        # [* Create Heroku deployment script]
        # [* Create Heroku undeployment script]

if __name__ == "__main__":
    main()