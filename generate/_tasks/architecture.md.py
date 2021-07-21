from pprint import pprint
import os
import json
from lib.util import Util
from lib.document import Document
from lib.document_architecture import ArchitectureDocument
from lib.development_git import GitDevelopment
#from lib.system import ExamplesDevelopment
from lib.development_home import HomeDevelopment

from lib.api_configuration import ApiConfiguration

import tkinter as tk
from tkinter import filedialog
import datetime



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

def main():
    # [Generate Architecture Document]
    print('Generate API')
    print('  - load api configuration, generate funcPattern key and values')
    # get configuration file name {folder: "", name: ""}
    # get list of files of type .json in folder ./config

    # [Use a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('_tasks','config'))

    print('config_folder', config_folder)
    #apiConfiguration = openApiConfiguration(config_folder)
    # [Select API Source ]
    sourceConfiguration = openApi(config_folder,file_type="source")
    if not sourceConfiguration:
        print('cancel')
        exit(0)

    # [Select API Target ]
    targetConfiguration = openApi(config_folder,file_type="target")
    if not targetConfiguration:
        print('cancel')
        exit(0)


    # [Generate API Architecture Document]
    # [Merge Source and Target]
    sourceConfiguration.update(targetConfiguration)
    apiConfiguration = sourceConfiguration
    #pprint(apiConfiguration)


    #pageList = []

    #pageList.append('\c {}'.format(apiConfiguration['_tasks']['name']))
    #pageList.append('SET search_path TO {};'.format(', '.join(apiConfiguration['_tasks']['schema'])))

    # setup default environment
    homeDev = HomeDevelopment().setup()

    print('Home Development')
    print(homeDev.getFolder('config'))
    #pprint(homeDev)

    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()

    # [Make an Architecture table for each API Configuration]

    # [Scan configuration for home, source, and target environment configurations]
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = getEnvironment(apiConfiguration[apiName])

        elif apiName == 'target':
            print('get target environment')
            # [Configure output targets from GIT repositories]
            targetDev = getEnvironment(apiConfiguration[apiName])
            pprint(targetDev)

    print('  - home          : {}'.format(homeDev.getFolder('home')))
    #pprint(sourceDev)
    print('  - source [db]     : {}'.format(sourceDev.getFolder('db')))
    print('  - source [scripts]: {}'.format(sourceDev.getFolder('scripts')))
    print('  - target [db]     : {}'.format(targetDev.getFolder('db')))
    print('  - target [repo]     : {}'.format(targetDev.getFolder('project')))

    print(' ')
    #pprint(targetDev)
    print('  - source [db]    : {}'.format(sourceDev.getFolder('db')))
    print('  - source [db_api]: {}'.format(sourceDev.getFolder('db_api')))
    print('  - target [db_api]: {}'.format(targetDev.getFolder('db_api')))
    print('  - target [repo]: {}'.format(targetDev.getFolder('project')))

    #############
    # [Process multiple API Definitions]
    #############
    apiNameList = [nm for nm in apiConfiguration
                      if apiConfiguration[nm]['kind'] == 'api-definition'
                      or apiConfiguration[nm]['kind'] == 'api-static']

    database = apiConfiguration['_tasks']

    architectureDocument = ArchitectureDocument(apiConfiguration,
                                                folder=targetDev.getFolder('project'),
                                                filename='dev.Architecture.md')
    architectureDocument.build()\
        .save()

    exit(0)

    # [Give document a Title]
    #architectureDocument.append('# API Architectures')
    #architectureDocument.append('Date: {}'.format(datetime.datetime.now()))
    # [Provide a Date]
    #architectureDocument.append('Sources:')
    #for s in title_sources:
    #    architectureDocument.append('* {}'.format(s))
    '''
    for apiName in apiNameList:
        #apiMdFilename = '{}.{}.{}.api.architecture.md'.format(
        #    apiConfiguration[apiName]['prefix'],
        #    apiConfiguration[apiName]['schema'],
        #    apiConfiguration[apiName]['name'])
        #print('apiScriptFilename ', apiMdFilename)
        architectureDocument.append(' ')

        architectureDocument.append('## {}'.format(apiName))
        arch =[]
        arch.append('| {} |'.format(' | '.join(['', '', '', '', ''])))
        arch.append('| {} |'.format(' | '.join([' - ', ' - ', ' - ', ' - ', ' - '])))

        uiList = ['UI']

        uiList.extend(['{}'.format(getUI(m)) for m in apiConfiguration.getMethods(apiName,'parameters')])

        arch.append('| {} |'.format(' | '.join(uiList)))

        httpList =['HTTP']

        httpList.extend(['{}'.format(m) for m in apiConfiguration.getMethods(apiName,'parameters') ])

        arch.append('| {} |'.format(' | '.join(httpList)))
        # [ROUTES Line]
        routeList = ['Routes']
        routeList.extend(['/{}'.format(apiName) for m in apiConfiguration.getMethods(apiName,'parameters') ])
        arch.append('| {} |'.format(' | '.join(routeList)))
        # [DB CLIENT Line]
        dbClientList = ['Db Client']
        dbClientList.extend(['pg.query( {}({}) )'.format(apiName, getParameterNames( apiConfiguration.getMethods(apiName,'parameters'), m)) for m in apiConfiguration.getMethods(apiName,'parameters')])

        arch.append('| {} |'.format(' | '.join(dbClientList)))
        schema = apiConfiguration[apiName]['schema']

        # [API SQL FUNCTION Line]
        apiSqlList = ['API SQL Function']
        apiSqlList.extend(['{}.{}({})'.format(schema,apiName,getParameterTypes( apiConfiguration.getMethods(apiName,'parameters'), m)) for m in apiConfiguration.getMethods(apiName,'parameters') ])
        arch.append('| {} |'.format(' | '.join(apiSqlList)))

        # [STATIC BASE FUNCTION Line]
        staticBaseList = ['Static Base Function']
        staticBaseList.extend(['{}.{}'.format('base_0_0_1',getBaseFunction(m)) for m in apiConfiguration.getMethods(apiName,'parameters') ])
        arch.append('| {} |'.format(' | '.join(staticBaseList)))

        # [Table Line]
        tableList = ['Table']
        tableList.extend(['{}'.format( getTable(_tasks,m)) for m in apiConfiguration.getMethods(apiName,'parameters') ])
        arch.append('| {} |'.format(' | '.join(tableList)))

        pprint(arch)
        architectureDocument.append(" ")
        architectureDocument.extend(arch)

    pprint(architectureDocument)
    architectureDocument.save()
    '''

if __name__ == "__main__":
    main()
