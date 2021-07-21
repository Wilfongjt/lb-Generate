from pprint import pprint
import os
#import json
from lib.util import Util

from lib.document import Document
from lib.document_environment import EnvironmentDocument
from lib.development_git import GitDevelopment
from lib.development_local import LocalDevelopment
from lib.development_home import HomeDevelopment

from lib.api_configuration import ApiConfiguration
import tkinter as tk
from tkinter import filedialog

from lib.help_functions import report
from lib.help_functions import get_environment
from lib.help_functions import open_api
from lib.help_functions import combine_documents
from datetime import datetime
from lib.template_test import TestTemplate

'''
def openApiTarget(config_folder):
    return {}


def openApiConfiguration(config_folder):
    # [Method: openApiConfiguration]
    # [Description: Load a Configuration File]
    # [Parameter: config_folder]
    root = tk.Tk()
    root.withdraw()
    # [Pick configuration file]
    file_path = filedialog.askopenfilename(initialdir=config_folder,
                                           filetypes=(("Text File", "*.config"), ("All Files", "*.*")),
                                           title="Choose a configuration file."
                                           )
    if len(file_path) == 0:
        print('* Stop')
        exit(0)

    config_filename = file_path.split('/')
    config_filename = config_filename[len(config_filename) - 1]
    #print('config_filename', config_filename)

    #print('file_path', file_path)
    # [Returns ApiConfiguration]

    return ApiConfiguration(config_folder, config_filename).load()
'''
'''
def getEnvironment(environ):
    if 'repo-source' == environ['kind'] or 'repo-target' == environ['kind']:
        # [Configure GIT folders]
        #pprint(environ)
        dev = GitDevelopment(environ['umbrella'],
                             environ['branch'],
                             environ['project'],
                             environ['folders']).setup()
    elif 'relative-source' == environ['kind']:
        # [Configure relative folder]
        #print('environment', environ['kind'])
        dev = HomeDevelopment(environ['app-name']).setup()
    else:
        print('Stop..UNKNOWN Source')
        exit(0)
    return dev
'''
'''
def openApi(config_folder, file_type='source'):
    # [Method: openApiConfiguration]
    # [Description: Load a Configuration File]
    # [Parameter: config_folder]
    _type = ''
    _title = ''
    # [Confirm file type is source or target]
    if file_type == 'source':
        _type = '*.source'
        _title = 'Choose a source file'
    elif file_type == 'target':
        _type = '*.target'
        _title = 'Choose a target file'
    else:
        return None

    root = tk.Tk()
    root.withdraw()
    # [Pick configuration file]
    file_path = filedialog.askopenfilename(initialdir=config_folder,
                                           filetypes=(("Text File", _type), ("All Files", "*.*")),
                                           title=_title
                                           )
    if len(file_path) == 0:
        print('* Cancel')
        return None

    config_filename = file_path.split('/')
    config_filename = config_filename[len(config_filename) - 1]

    # [Returns ApiConfiguration]

    return ApiConfiguration(config_folder, config_filename).load()
'''
def main():
    clause2method = {'insert':'POST', 'update':'PUT', 'query':'GET', 'delete':'DELETE'}
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
    print('=================')
    print('Base Tests Combined')
    print('=================')
    #fileList = Util().getFileList(sourceDev.getDbFolder('sql'),'static.sql')
    fileList = Util().getFileList(sourceDev.getFolder('scripts'),'base.test.sql')
    fileList.sort()
    # [Replace project specific values]
    replace_ = ['one_db', 'hapi-api']
    replace_with = [targetDev.getName('db'), targetDev.getName('db_api')]

    targetName = '90.base.test.sql'
    combinedDocument = Document(targetDev.getFolder('scripts'), targetName)


    # [Backup the target file]
    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), targetName)
    print('  - backup : {}'.format(backup))

    # [Move Static Files to Target Folder]
    for fileName in fileList:
        # [Combine base tests into one file]
        # [Copy from a source folder to a target folder]

        staticDocument = Document(sourceDev.getFolder('scripts'), fileName) \
            .load() \
            .replace(replace_, replace_with)

        combinedDocument.extend(staticDocument)

    combinedDocument.save()

    print('=================')
    print('API Tests')
    print('=================')

    apiNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'api-definition' or apiConfiguration[nm]['kind'] == 'api-static']

    # [Move Static Files to Target Folder]
    #targetNames = []
    #sourceNames = []
    names = []
    src_folder = sourceDev.getFolder('scripts')
    tmpl_folder = '../templates'
    trg_folder = targetDev.getFolder('scripts')
    clauses = ['insert','query','update','delete']
    for apiName in apiNameList:
        schema = apiConfiguration[apiName]['schema'].replace('_','.')
        prefix = apiConfiguration[apiName]['prefix-test']
        # make list of existing test files
        names = [{"source":'{}.test.{}.{}.{}.api.test.sql'.format(prefix,schema, apiName.upper(), clause),
                  "target":'{}.{}.{}.api.test.sql'.format(prefix,apiName.upper(), clause),
                  "template": '{}.test.sql.template'.format(clause),
                  "clause": '{}'.format(clause),
                  "method": '{}'.format(clause2method[clause])} for clause in clauses]
        names = [pair for pair in names if Util().file_exists(src_folder, pair['source'])]
        #
        for pair in names:
            backup = None
            #print('pair', pair, 'kind', apiConfiguration[apiName]['kind'])
            if apiConfiguration[apiName]['kind'] == 'api-definition':
                # handle backup
                if Util().file_exists(trg_folder, pair['target']):
                    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), pair['target'])

                # Use Template
                if Util().file_exists(tmpl_folder, pair['template']): # Use Template
                    # Use Template
                    print('    - generate test {} FROM {}'.format(pair['target'], pair['template']))
                    if backup: print('       -- backup ', backup)
                    templateDoc = TestTemplate(apiName, pair['method'], pair['template']) \
                        .apply(apiConfiguration)\
                        .saveAs(trg_folder, pair['target'])

                elif Util().file_exists(src_folder, pair['source']): # Copy from existing file
                    # Copy from source
                    print('    - copy test {} FROM {} '.format(pair['target'],pair['source']))
                    # load
                    # replace
                    # save
                    doc = Document(src_folder, pair['source']) \
                        .load() \
                        .replace(replace_, replace_with)\
                        .saveAs(trg_folder,pair['target'])

                else: # No test available
                    print('No Test Available for ', pair['source'])

            elif apiConfiguration[apiName]['kind'] == 'api-static':
                #print('template', tmpl_folder)
                print('    - copy test for api-static ', pair['source'])

        # [Backup the target file]

        #print('  - backup : {}'.format(fileName))

    apiNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'api-static']

    # [Move Static Files to Target Folder]
    '''
    for apiName in apiNameList:
        schema = apiConfiguration[apiName]['schema'].replace('_','.'),
        targetName = '94.test.api.{}.{}.delete.api.test.sql'.format(schema, apiName.upper())
        print('  - API', targetName)
        # [Backup the target file]
        #print('  - backup : {}'.format(fileName))
    '''
if __name__ == "__main__":
    main()