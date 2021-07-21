from lib.util import Util
#from lib.system import GitDevelopment
#import re
import os
from lib.help_functions import open_api
from lib.development_home import HomeDevelopment
from lib.help_functions import get_environment
from lib.document_script_readme import ScriptReadmeDocument
from pprint import pprint

def main():
    combined_sql_list = [] # eventually is written to a file
    # [Generate API sql file]
    print('Generate README.md')
    print('  - load api configuration, generate funcPattern key and values')
    # get configuration file name {folder: "", name: ""}
    # get list of files of type .json in folder ./config

    # [Use a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('_documents','config'))
    print('config_folder',config_folder)
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
    pprint(apiConfiguration)
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = get_environment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [Configure output targets from GIT repositories]
            targetDev = get_environment(apiConfiguration[apiName])

    print('=================')
    #report(homeDev, sourceDev, targetDev)
    print('=================')
    pprint(sourceDev)
    print(sourceDev.getFolder('group'))
    script_list = [{"source":fn,"target":"README.{}.md".format(fn)} for fn in Util().getFileList(sourceDev.getFolder('group'), ext='.sh')]
    print('script_list',script_list)
    for fn in script_list:
        print('script', sourceDev.getFolder('group'), fn['source'] )
        print('script', targetDev.getFolder('group'), fn['target'] )

        scriptDoc = ScriptReadmeDocument(sourceDev.getFolder('group'), fn['source']).load()
        pprint(scriptDoc)
        scriptDoc.saveAs(targetDev.getFolder('group'), fn['target'])
    '''
    if not Util().file_exists(sourceDev.getFolder('umbrella')):
        # [Copy first set of _tasks code and config files]
        #Util().copyFolder(sourceDev.getFolder('db'),
        #                  targetDev.getFolder('db'))
        print('')
    else:
        if not Util().confirm('* Install/Overwrite postgres code and extentions?','N'):
    '''

if __name__ == "__main__":
    main()
