from pprint import pprint
import os
#import json
from lib.util import Util
#from lib.document import Document
from lib.system import GitDevelopment
#from lib.system import ExamplesDevelopment
from lib.home_development import HomeDevelopment
from lib.document import Document
from lib.api_configuration import ApiConfiguration
import tkinter as tk
from tkinter import filedialog



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
def getEnvironment(environ):
    if 'repo-source' == environ['kind'] or 'repo-target' == environ['kind']:
        # [Configure GIT folders]
        #pprint(environ)
        dev = GitDevelopment(environ['umbrella'],
                             environ['branch'],
                             environ['repo'],
                             environ['folders']).setup()
    elif 'relative-source' == environ['kind']:
        # [Configure relative folder]
        #print('environment', environ['kind'])
        dev = HomeDevelopment(environ['app-name']).setup()
    else:
        print('Stop..UNKNOWN Source')
        exit(0)
    return dev

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

def main():
    # [Initialize Database in a Repo]
    # [Description: Move Static Database Scripts to a Repo]

    print('current folder', os.getcwd())

    homeDev = HomeDevelopment()
    assert(homeDev.getFolder('group').endswith('01-Generate'))
    assert(homeDev.getFolder('branch').endswith('01-Generate/#01.init'))
    assert(homeDev.getFolder('repo').endswith('01-Generate/#01.init/lb-Generate'))
    assert(homeDev.getFolder('config').endswith('01-Generate/#01.init/lb-Generate/generate/config'))
    assert(homeDev.getFolder('examples').endswith('lb-Generate/generate/examples'))

    '''
    print('  - load api configuration, generate funcPattern key and values')

    # [Interactively open a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('database','config'))
    apiConfiguration = openApiConfiguration(config_folder)

    # [Build a custom API sql script]

    pageList = []
    pageList.append('\c {}'.format(apiConfiguration['database']['name']))
    pageList.append('SET search_path TO {};'.format(', '.join(apiConfiguration['database']['schema'])))

    # pageList.append('-- This function was generated using {}'.format(filename))

    # setup default environment
    homeDev = HomeDevelopment().setup()
    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()
    #staticDev = HomeDevelopment().setup()
    # [Scan configuration for home, source, and target environment configurations]
    # [ ]

    print('* Copy')
    print('  - Static Source folder: {}'.format(sourceDev.getDbFolder('sql')))
    print('  - Target folder       : {}'.format(targetDev.getDbFolder('sql')))

    # [Move Static Files to Target Folder]
    for fileName in Util().getFileList(sourceDev.getDbFolder('sql'),'static.sql'):

        # [Backup the target file]
        backup = Util().makeBackupFile(targetDev.getDbFolder('sql'), fileName)
        # [Copy from a source folder to a target folder]
        staticDocument = Document(sourceDev.getDbFolder('sql'), fileName)\
            .load()\
            .replace('one_db', apiConfiguration['database']['name'])
        # [Copy Static files (.static.sql) from Source]
        staticDocument.saveAs(targetDev.getDbFolder('sql'), fileName)

        print('  - backup : {}'.format(fileName))
    '''
if __name__ == "__main__":
    main()