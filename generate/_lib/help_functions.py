from lib.api_configuration import ApiConfiguration

from lib.development_home import HomeDevelopment
from lib.development_git import GitDevelopment
from lib.development_local import LocalDevelopment
#from lib.system import ExamplesDevelopment
import tkinter as tk
from tkinter import filedialog

def get_environment(environ):

    if 'repo-source' == environ['kind'] or 'repo-target' == environ['kind']:

        # [Configure GIT folders]
        #pprint(environ)
        dev = GitDevelopment(environ['umbrella'],
                             environ['branch'],
                             environ['project'],
                             environ['folders']).setup()
    elif 'local-source' == environ['kind'] or 'local-target' == environ['kind']:
        dev = LocalDevelopment(environ['umbrella'],
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

def report(homeDev, sourceDev, targetDev):

    print('db name', targetDev.getName('db'))  # ['target']['folders']

    print('  - home          : {}'.format(homeDev.getFolder('home')))
    print('Source')
    print('  - source [db]     : {}'.format(sourceDev.getFolder('db')))
    print('  - source [scripts]: {}'.format(sourceDev.getFolder('scripts')))
    print('  - source [db_api] : {}'.format(sourceDev.getFolder('db_api')))
    print('  - source [project]: {}'.format(sourceDev.getFolder('project')))
    print('  - source [db_api] : {}'.format(sourceDev.getName('db_api')))
    print('  - source [env])   : {}'.format(sourceDev.getFolder('env')))
    print('  - source templates)   : ../templates')

    print('Target')
    print('  - target [db]     : {}'.format(targetDev.getFolder('db')))
    print('  - target [scripts]: {}'.format(targetDev.getFolder('scripts')))
    print('  - target [db_api] : {}'.format(targetDev.getFolder('db_api')))
    print('  - target [project]: {}'.format(targetDev.getFolder('project')))
    print('  - target name [db]    : {}'.format(targetDev.getName('db')))
    print('  - target name [db_api]: {}'.format(targetDev.getName('db_api')))
    print('  - target [env])   : {}'.format(targetDev.getFolder('env')))

def open_api(config_folder, file_type='source'):
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

from lib.document import Document
from lib.util import Util
#def combine_documents(apiConfiguration,sourceDev, targetDev, extention, outfileName):

def process_documents_to(apiConfiguration,sourceDev, targetDev, extention, outfileName):
    print('apiConfiguration',apiConfiguration)
    print('sourceDev',sourceDev)
    print('targetDev',targetDev)
    print('extention',extention)
    print('outfileName',outfileName)
    print('source scripts', sourceDev.getFolder('scripts'))
    print('target scripts', targetDev.getFolder('scripts'))

    staticScriptDocument = Document(targetDev.getFolder('scripts'), outfileName)  # dont load

    #print('staticScriptDocument', staticScriptDocument)
    fileList = Util().getFileList(sourceDev.getFolder('scripts'), extention)
    fileList.sort()
    #print('fileList',fileList)
    for fileName in fileList:
        # [Load test files ending with .test.sql]
        print('- script: ', fileName)
        staticDocument = Document(sourceDev.getFolder('scripts'), fileName) \
            .load() \
            .replace('one_db', apiConfiguration['_tasks']['name'])
        staticScriptDocument.extend(staticDocument)
    # [Backup a target script before overwriting]
    #print('staticScriptDocument', staticScriptDocument)
    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), staticScriptDocument.filename)
    # [Save all DB scripts into one file]
    staticScriptDocument.save()
