from pprint import pprint
import os
from lib.util import Util
from lib.api_configuration import ApiConfiguration
from lib.development_git import GitDevelopment
from lib.development_local import LocalDevelopment
from lib.development_home import HomeDevelopment
import subprocess
import sys

from lib.help_functions import report
from lib.help_functions import get_environment
from lib.help_functions import open_api
from lib.help_functions import combine_documents
from datetime import datetime

class CleanUp(list):
    def __init__(self, folder):
        self.folder=folder

    def getOriginalName(self, filename):
        return filename.replace('.dep', '')

    def load(self):
        print('load 1')
        filelist = Util().getFileList(self.folder,".dep")
        for fn in filelist:
            #print('fn',fn, self.getOriginalName(fn))
            if Util().file_exists(self.folder, self.getOriginalName(fn)):
                print('found skip ', fn)
            else:
                #print('not found remove from git')
                self.append(fn)
        return self

    def run(self):

        # change folder

        #cmd = "git --version"

        #returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        #print('returned value:', returned_value)

        startFolder = os.getcwd()
        os.chdir(self.folder)
        print('target folder ', os.getcwd())
        for fn in self:
            print('git rm {}'.format(self.getOriginalName(fn)))
            cmd = 'git rm {}'.format(self.getOriginalName(fn))
            returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            print('returned value:', returned_value)
            #try:
            #    returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            #    print('returned value:', returned_value)
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])


        for fn in self:
            print('rm {}'.format(fn))
            cmd = 'rm {}'.format( fn )
            returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            print('returned value:', returned_value)

        os.chdir(startFolder)
        return self

def main():
    # set folder\
    trgtFolder=''
    # get *.dep list
    # skip .dep if already exists in folder
    # i.e. myfile.sql and myfile.sql.dep should be skipped
    # make the target file name by removing the .dep
    # format git command
    # i.e. git rm <filename>
    # [Select API Source ]

    # [Use a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('utils', 'config'))
    #config_filename = Util().getApiName(config_folder,file_type="source")
    # [Select API Source ]
    apiConfiguration = open_api(config_folder,file_type="source")
    if not apiConfiguration:
        print('cancel')
        exit(0)

    print('config_folder', config_folder)
    #sourceConfiguration = Util().openApi(config_folder,file_type="source")
    #sourceConfiguration = ApiConfiguration(config_folder, config_filename).load()
    #apiConfiguration = ApiConfiguration(config_folder, config_filename).load()

    #apiConfiguration[apiName]

    if not apiConfiguration:
        print('cancel')
        exit(0)

    # setup default environment
    homeDev = HomeDevelopment().setup()

    # [Create missing folders]
    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()

    # [Configure GIT folders]
    # pprint(environ)
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = get_environment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [Configure output targets from GIT repositories]
            targetDev = get_environment(apiConfiguration[apiName])

    print('apiName', apiName)
    print('  - home          : {}'.format(homeDev.getFolder('home')))
    print('Source')
    print('  - source [db]     : {}'.format(sourceDev.getFolder('db')))
    print('  - source [scripts]: {}'.format(sourceDev.getFolder('scripts')))
    print('  - source [db_api] : {}'.format(sourceDev.getFolder('db_api')))
    print('  - source [project]: {}'.format(sourceDev.getFolder('project')))
    print('  - source [db_api] : {}'.format(sourceDev.getName('db_api')))
    print('  - source [env])   : {}'.format(sourceDev.getFolder('env')))


    print('apiConfiguration', apiConfiguration)
    #pprint(sourceConfiguration)
    cleanUp = CleanUp(sourceDev.getFolder('scripts')).load().run()
    #pprint(cleanUp)

if __name__ == "__main__":
    main()
