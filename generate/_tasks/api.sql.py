from pprint import pprint
import os
import json
from lib.util import Util
from lib.document import Document
from lib.document_environment import EnvironmentDocument
from lib.development_git import GitDevelopment
from lib.development_local import LocalDevelopment
#from lib.system import ExamplesDevelopment
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
from lib.help_functions import process_documents_to
from datetime import datetime

##########
# Generate API
##########


'''____        __ _       _ _   _                 
 |  __ \      / _(_)     (_) | (_)                
 | |  | | ___| |_ _ _ __  _| |_ _  ___  _ __  ___ 
 | |  | |/ _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
 | |__| |  __/ | | | | | | | |_| | (_) | | | \__ \
 |_____/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
                                                  
'''



'''
           _____ _____ 
     /\   |  __ \_   _|
    /  \  | |__) || |  
   / /\ \ |  ___/ | |  
  / ____ \| |    _| |_ 
 /_/    \_\_|   |_____|

'''


'''
  _____          _   
 |  __ \        | |  
 | |__) |__  ___| |_ 
 |  ___/ _ \/ __| __|
 | |  | (_) \__ \ |_ 
 |_|   \___/|___/\__|
                     
                     

'''

'''
   _____      _   
  / ____|    | |  
 | |  __  ___| |_ 
 | | |_ |/ _ \ __|
 | |__| |  __/ |_ 
  \_____|\___|\__|
                  
'''


'''
  _____       _      _       
 |  __ \     | |    | |      
 | |  | | ___| | ___| |_ ___ 
 | |  | |/ _ \ |/ _ \ __/ _ \
 | |__| |  __/ |  __/ ||  __/
 |_____/ \___|_|\___|\__\___|
                             
'''


'''
  _    _           _       _       
 | |  | |         | |     | |      
 | |  | |_ __   __| | __ _| |_ ___ 
 | |  | | '_ \ / _` |/ _` | __/ _ \
 | |__| | |_) | (_| | (_| | ||  __/
  \____/| .__/ \__,_|\__,_|\__\___|
        | |                        
        |_|                        

'''

'''
  _    _                 _ _           
 | |  | |               | | |          
 | |__| | __ _ _ __   __| | | ___ _ __ 
 |  __  |/ _` | '_ \ / _` | |/ _ \ '__|
 | |  | | (_| | | | | (_| | |  __/ |   
 |_|  |_|\__,_|_| |_|\__,_|_|\___|_|   
                                       
                                       
'''

'''

Source                          Target                          Generated 
API                                                             File                                Function
----------------------------    ----------------------------    -----------------                   -----------------
<app-name>.<api-name>.source    <app-name>.<api-name>.target    40.<api-name>.api.function.sql      --> POST function
                                                                                                    --> GET function
                                                                                                    --> PUT function
                                                                                                    --> DELETE function

                                                                24.<schema>.<api-name>.query.api.function.sql
                                                                24.<schema>.<api-name>.insert.api.function.sql
                                                                24.<schema>.<api-name>.update.api.function.sql
                                                                24.<schema>.<api-name>.delete.api.function.sql

                                                                42.<api-name>.api.function.sql      --> POST function
                                                                                                    --> GET function
                                                                                                    --> PUT function
                                                                                                    --> DELETE function
                                                                                                    
                                                                
                                                                .env                            --> <datbase>...
                                                                                                --> <api>...
                                                                
                                                                docker-compose.text.yml         --> db
                                                                                                --> api
                                                                                                --> web
                                                                
                                                                <project>.up.sh                 --> docker-compose up
                                                                <project>.down.sh               --> docker-compose down
                                                                <project>.test.sh               --> npm test 



Process  
------------
Generate
Copy 
Integrate
Test

'''
def main():
    combined_sql_list = [] # eventually is written to a file
    # [Generate API sql file]
    print('Generate API')
    print('  - load api configuration, generate funcPattern key and values')
    # get configuration file name {folder: "", name: ""}
    # get list of files of type .json in folder ./config

    # [Use a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('_tasks','config'))

    # [Select API Source ]
    sourceConfiguration = open_api(config_folder,file_type="source")
    if not sourceConfiguration:
        print('cancel')
        exit(0)

    # [Select API Target ]
    targetConfiguration = open_api(config_folder,file_type="target")
    if not targetConfiguration:
        print('cancel')
        exit(0)

    # [Merge Source and Target]
    sourceConfiguration.update(targetConfiguration)
    apiConfiguration = sourceConfiguration

    # setup default environment
    homeDev = HomeDevelopment().setup()

    # [Create missing folders]
    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()

    # [Scan configuration for home, source, and target environment configurations]
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = get_environment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [Configure output targets from GIT repositories]
            targetDev = get_environment(apiConfiguration[apiName])

    print('=================')
    report(homeDev, sourceDev, targetDev)
    print('=================')



    ##############
    # [Process Postgres Extentions]
    ##############
    if targetDev.getFolder('db'):
        if not Util().folder_exists(sourceDev.getFolder('db')):

            # [Copy first set of _tasks code and config files]
            Util().copyFolder(sourceDev.getFolder('db'),
                              targetDev.getFolder('db'))

        else:
            if not Util().confirm('* Install/Overwrite postgres code and extentions?','N'):
                print("  Overwriting postgres configuration and extentions")
                print('  - source ', sourceDev.getFolder('db'))
                print('  - target ', targetDev.getFolder('db'))
                # [Copy all files in extention/db folder]
                for fn in Util().getFileList(sourceDev.getFolder('db')):
                    if Util().file_exists(targetDev.getFolder('db'),fn):
                        if not Util().confirm('  -- Overwrite {}?'.format(fn), 'N'):
                            Util().copy(
                                '{}/{}'.format(sourceDev.getFolder('db'), fn),
                                '{}/{}'.format(targetDev.getFolder('db'), fn)
                            )
                    else:
                        print('  - copy', fn)
                        Util().copy(
                            '{}/{}'.format(sourceDev.getFolder('db'),fn),
                            '{}/{}'.format(targetDev.getFolder('db'),fn)
                        )

    #############
    # [## Initalize docker-component]
    #############
    # [Define list of words to replace in docker-compose file]
    replace_ = ['one_db','hapi-api']
    replace_with =[targetDev.getName('db'), targetDev.getName('db_api')]
    if not Util().file_exists(targetDev.getFolder('project'), 'docker-compose.test.yml'):
        # [Copy docker-compose.yml to target when it doesnt exist]
        #print('Create new docker-compose.yml')
        dcDoc = Document(sourceDev.getFolder('project'),'docker-compose.yml').load()
        dcDoc.replace(replace_, replace_with)
        dcDoc.saveAs(targetDev.getFolder('project'),'docker-compose.test.yml')

    else:
        # [Ask to overwrite when docker-compose exists]
        if not Util().confirm('* Overwrite docker-compose.test.yml?', 'N'):

            dcDoc = Document(sourceDev.getFolder('project'), 'docker-compose.yml').load()

            backup = Util().makeBackupFile(targetDev.getFolder('project'), 'docker-compose.test.yml')

            print('backup', backup)
            dcDoc = Document(sourceDev.getFolder('project'), 'docker-compose.yml').load()

            dcDoc.replace(replace_, replace_with)
            dcDoc.saveAs(targetDev.getFolder('project'), 'docker-compose.test.yml')


    ##############
    # [## .env         # if .env doesnt exist then create one]
    #############
    srcDoc = EnvironmentDocument(sourceDev.getFolder('env'), '.env').load()
    srcDoc.replace(replace_, replace_with)
    if not Util().file_exists(targetDev.getFolder('env'), '.env'):
        # [Copy .env to target when it doesnt exist]
        print('Create .env')
        srcDoc.saveAs(targetDev.getFolder('env'),'.env')
    else:          # [if .env exists then update and add new variables]
        if not Util().confirm('* Update .env?', 'N'):
            # [Ask to update when .e nv exists]
            print('Update .env')
            trgtDoc = EnvironmentDocument(targetDev.getFolder('env'), '.env').load()
            #pprint(trgtDoc)
            #print('--------')
            trgtDoc.backup()
            trgtDoc.update(srcDoc)
            trgtDoc.save()
            #trgtDoc.saveAs(targetDev.getFolder('env'), '.env')
            #pprint(trgtDoc)

    #############
    # [## Process Static Scripts]
    #############
    # [Static scripts end with .static.sql]
    if targetDev.getFolder('db'):
        if not Util().confirm('* Install/Overwrite static scripts?', 'N'):
            print("writing static scripts")

            #############
            # [Process Static Db-Api]
            #############

            process_documents_to(apiConfiguration, sourceDev, targetDev, 'db.sql', '00.db.sql')

            #############
            # [Process Static Database Scripts]
            #############
            process_documents_to(apiConfiguration, sourceDev, targetDev, 'table.sql', '10.base.table.sql')

            #############
            # [Process Base Function Scripts]
            #############
            # process_to_one(apiConfiguration, sourceDev, targetDev, 'base.function.sql','12.base.function.sql')
            process_documents_to(apiConfiguration, sourceDev, targetDev, 'base.function.sql', '20.base.function.sql')

            #############
            # [Process Api Function Scripts]
            #############
            # process_to_one(apiConfiguration, sourceDev, targetDev, 'api.function.sql','20.api.function.sql')
            # combine_documents(apiConfiguration, sourceDev, targetDev, 'api.function.sql', '30.api.function.sql')
            process_documents_to(apiConfiguration, sourceDev, targetDev, 'api.usage.sql', '30.api.usage.sql')

            #############
            # [Process Static Test Scripts]
            #############
            #combine_documents(apiConfiguration, sourceDev, targetDev, 'base.test.sql', '90.base.test.sql')
            #combine_documents(apiConfiguration, sourceDev, targetDev, 'api.test.sql', '92.api.test.sql')

            #############
            # [Process Static Data Scripts]
            # retired the data scripts. data is now encpsulated in tests
            #############
            # process_to_one(apiConfiguration, sourceDev, targetDev, 'data.sql','80.data.sql')

            #############
            # [Process Static Cleaup Scripts]
            # retired the data scripts. data is now encpsulated in tests
            #############
            # process_to_one(apiConfiguration, sourceDev, targetDev, 'cleanup.sql','98.test.cleanup.sql')

    #############
    # [Process DbApi]
    #############

    #Util().copyFolder(sourceDev.getFolder('db_api'), targetDev.getFolder('db_api'),ignore=shutil.ignore_patterns('node_modules'))

    #
    #############
    # [## Process multiple API SQL Definitions]
    # skip api-static, _tasks, source and target
    #############
    # [Set target _tasks name]
    if targetDev.getFolder('db'):
        apiNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'api-definition']

        for apiName in apiNameList:

            apiScriptFilename = '{}.{}.api.function.sql'.format(
                apiConfiguration[apiName]['prefix'],
                apiConfiguration[apiName]['name'].upper())

            # [Combine all API functions into one script]
            combined_sql_list = []
            combined_sql_list.append('-- api      : {}'.format(apiName.upper()))
            combined_sql_list.append('-- schema   : {}'.format(apiConfiguration[apiName]['schema']))
            combined_sql_list.append('-- generated on: {}'.format(datetime.now()))
            combined_sql_list.append('-- source project: {} '.format(sourceDev.getName('project')))

            #combined_sql_list.append('\c {}'.format(targetDev.getName('db')))
            #combined_sql_list.append('SET search_path TO {};'.format(', '.join(apiConfiguration['_tasks']['schema'])))

            # [Generate POST Function]
            combined_sql_list.append('-- POST')
            combined_sql_list.extend(PostTemplate(apiName, folder='../templates', filename='post.sql.template') \
                                     .validate(apiConfiguration)\
                                     .apply(apiConfiguration))

            # [Generate GET Function]
            combined_sql_list.append('-- GET')
            combined_sql_list.extend(GetTemplate(apiName, folder='../templates', filename='get.sql.template') \
                                     .validate(apiConfiguration) \
                                     .apply(apiConfiguration))

            # [Generate DELETE Function]
            combined_sql_list.append('-- DELETE')
            combined_sql_list.extend(DeleteTemplate(apiName, folder='../templates', filename='delete.sql.template') \
                                     .validate(apiConfiguration) \
                                     .apply(apiConfiguration))

            # [Generate PUT Function]
            combined_sql_list.append('-- PUT')
            combined_sql_list.extend(PutTemplate(apiName, folder='../templates', filename='put.sql.template') \
                                     .validate(apiConfiguration) \
                                     .apply(apiConfiguration))

            # [Assemble API (POST, GET, PUT, and Delete) Functions into single script]
            newDoc = Document(targetDev.getFolder('scripts'), apiScriptFilename).load(combined_sql_list)

            # [Confirm overwrite of existing API files]
            if not Util().file_exists(targetDev.getFolder('scripts'),apiScriptFilename):
                print('    - Writing API {} script'.format(apiScriptFilename))
                # [Create Api when Api doesnt exist]
                newDoc.write()
            else:
                if not Util().confirm('* Overwrite API {} script?'.format(apiScriptFilename), 'N'):
                    # [Confirm the overwrite of existing Api script]
                    # [Backup Api script before overwriting]
                    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), apiScriptFilename)
                    print("    - Overwriting API {} script".format(apiScriptFilename))
                    newDoc.write()


        apiStaticNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'api-static']
        #############
        # [## Process static API scripts]
        # Static scripts are copied, combined and renamed to the target folder
        #############
    if targetDev.getFolder('db'):

        for apiName in apiStaticNameList:

            sourceFilename = '{}.{}.{}.api.function.sql'.format(
                '24',
                apiConfiguration[apiName]['schema'].replace('_','.'),
                apiConfiguration[apiName]['name']
            )
            targetFilename = '{}.{}.api.function.sql'.format(
                apiConfiguration[apiName]['prefix'],
                apiConfiguration[apiName]['name'].upper())

            combined_sql_list = []
            combined_sql_list.append('-- api      : {}'.format(apiName.upper()))
            combined_sql_list.append('-- schema   : {}'.format(apiConfiguration[apiName]['schema']))
            combined_sql_list.append('-- copied on: {}'.format(datetime.now()))
            combined_sql_list.append('-- source project: {}'.format(sourceDev.getName('project')))

            combined_sql_list.append('\c {}'.format(targetDev.getName('db')))
            combined_sql_list.append('SET search_path TO {};'.format(', '.join(apiConfiguration['_tasks']['schema'])))

            # [Define list of words to replace in docker-compose file]
            replace_ = ['one_db','hapi-api']
            replace_with =[targetDev.getName('db'), targetDev.getName('db_api')]

            if not Util().file_exists(targetDev.getFolder('scripts'), targetFilename):

                # [Copy docker-compose.yml to target when it doesnt exist]

                print('* Create new {}'.format(targetFilename))
                print('    -- load {}'.format(apiName))
                print('    -- swap out values ')
                print('    -- write api to target ')
                dcDoc = Document(sourceDev.getFolder('scripts'),sourceFilename).load()
                dcDoc.replace(replace_, replace_with)
                dcDoc.saveAs(targetDev.getFolder('scripts'),targetFilename)

            else:
                # [Ask to overwrite when docker-compose exists]

                if not Util().confirm('* Overwrite {}?'.format(targetFilename), 'N'):
                    #print('* Overwrite api-static')
                    print('    -- load {}'.format(apiName))
                    print('    -- replace values ')
                    print('    -- save api to target ')
                    dcDoc = Document(sourceDev.getFolder('scripts'), sourceFilename).load()

                    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), targetFilename)

                    print('    -- backup', backup)
                    dcDoc = Document(sourceDev.getFolder('scripts'), sourceFilename).load()
                    dcDoc.replace(replace_, replace_with)
                    dcDoc.saveAs(targetDev.getFolder('scripts'), targetFilename)

    ###################
    # [Write API tests]
    ##################
    '''
    if targetDev.getFolder('db'):

        for apiName in apiNameList:
    
            apiTESTFilename = '95.{}.{}.api.test.sql'.format(
                apiConfiguration[apiName]['schema'],
                apiConfiguration[apiName]['name'])
    
            print('    - Overwrite TEST {}'.format(apiTESTFilename))
    
            # [Combine all API functions into one script]
            combined_test_list = []
            #combined_test_list.append('\c {}'.format(targetDev.getName('db')))
    
            combined_test_list.append('-- DELETE')
            combined_test_list.extend(DeleteTestTemplate(apiName, folder='../templates', filename='delete.test.sql.template') \
                                     .apply(apiConfiguration))
    
            # [Assemble API (POST, GET, PUT, and Delete) Functions into single script]
            testDoc = Document(targetDev.getFolder('scripts'), apiTESTFilename).load(combined_test_list)
            
            print('testDoc')
            pprint(testDoc)
            
            # [Confirm overwrite of existing API files]
            if not Util().file_exists(targetDev.getFolder('scripts'),apiTESTFilename):
                print('    - Writing API {} TEST script'.format(apiTESTFilename))
                # [Create Api when Api doesnt exist]
                #testDoc.write()
            else:
                if not Util().confirm('* Overwrite API {} TEST script?'.format(apiTESTFilename), 'N'):
                    # [Confirm the overwrite of existing Api script]
                    # [Backup Api script before overwriting]
                    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), apiTESTFilename)
                    print("    - Overwriting API {} script".format(apiTESTFilename))
                    #testDoc.delete()
                    #testDoc.write()
        
    '''


if __name__ == "__main__":
    main()
