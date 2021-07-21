import os
from os.path import isfile, join
from os import listdir
from pathlib import Path
from datetime import datetime
#from shutil import copytree, ignore_patterns
import shutil
#from distutils.dir_util import copy_tree
#from lib.api_configuration import ApiConfiguration

import tkinter as tk
from tkinter import filedialog

class Util():
    def toClassName(self, fileName):
        #parts = fileName.split('.')
        fileName = fileName.replace('-', '.')
        parts = [p.capitalize() for p in fileName.split('.')]
        return ''.join(parts)
    '''
    def harden(self, alist):
        for ln in alist:

            ln = ln.replace('\n','')
            print('            \'{}\','.format(ln))
        return self
    '''
    def getFileExtension(self, filename):
        lst = filename.split('.')[1:]
        ext = '.'.join(lst)
        return ext

    def folder_exists(self, folder):
        exists = os.path.isdir('{}'.format(folder))
        return exists

    def file_exists(self, folder, filename):
        exists = os.path.isfile('{}/{}'.format(folder, filename))
        return exists

    def fileExists(self,path_name):
        exists = os.path.isfile(path_name)
        return exists

    def createFolder(self, folder):
        # create all folders in a given path
        # No trailing / in folder
        #path = folder

        try:
            p=''
            for sub in folder.split('/'):
                if len(sub) > 0:
                    p += '/{}'.format( sub )
                    #print('check folder ', p)
                    if not os.path.exists(p):
                        #print('create folder ', p)
                        os.mkdir('{}/'.format(p))



            #if not self.folder_exists('{}/'.format(path)):
            #    os.mkdir('{}/'.format(path))

            #print("Successfully created the directory %s " % path)
        except OSError:
            path=None
            print("FAILURE: Creation of the directory %s failed" % path)

        return self

    '''
        def createFolder(self, folder):
        # No trailing / in folder
        path = folder

        try:
            
            if not self.folder_exists('{}/'.format(path)):
                os.mkdir('{}/'.format(path))

            #print("Successfully created the directory %s " % path)
        except OSError:
            path=None
            #print("Creation of the directory %s failed" % path)

        return self
    '''

    def deleteFolder(self, folder):
        # Note: You can only remove empty folders.
        if self.folder_exists(folder ):
            print('deleteFolder', folder)
            os.rmdir(folder)
        return self

    def deleteFile(self, folder, file_name):

        if self.file_exists(folder, file_name):
            os.remove("{}/{}".format( folder, file_name ))
        return self

    def getFileList(self, path, ext=None):
        onlyfiles=[]

        if len(listdir(path)) > 0:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f) )]
            if ext != None:
                onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

        #return onlyfiles
        return [fn for fn in onlyfiles if '.DS_Store' not in fn]

    def getFileListWalk(self, path, ext=None):
        pathAndFile=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                    #print(os.path.join(root, file))
                    pathAndFile.append(os.path.join(root,file))
        return pathAndFile

    def getFolderList(self, path):
        onlyfolders = []

        if len(listdir(path)) > 0:
            onlyfolders = ['{}/{}'.format(path,f) for f in listdir(path) if not isfile(join(path, f))]
            #if ext != None:
            #    onlyfolders = [f for f in onlyfolders if f.startswith(ext) or f.endswith(ext)]

        # return onlyfiles
        return [fn for fn in onlyfolders]

    def stringify(self, key_list):
        # convert integers in list to str
        if len(key_list) == 0:
            return []

        if not (type(key_list[0] is int)):
            return key_list

        return [ str(k) for k in key_list]

    def loadEnv(self, filepath):

        with open(filepath) as file:

            lines = file.readlines()
            for ln in lines:
                if not ln.startswith('#'):
                    #print('lb', ln)
                    #print('split', ln.split('='))
                    ln = ln.split('=')
                    if len(ln) > 2:
                        os.environ[ln[0]]=ln[1]

            #print('type', type(data))
        return self

    def getHomeFolder(self):
        return str(Path.home())

    def getWorkFolder(self, path):
        return '{}/{}'.format(self.getHomeFolder(),path)

    def getResourceProjectFolder(self, suffix=None):
        '''
        returns path to resource folder in the source code
        suffix can be a folder name or a file name
        '''
        rc = os.getcwd()

        #if not (rc.endswith('_app' or rc.endswith('_res'))):
        #    rc = '{}/_res'.format(rc)

        if rc.endswith('_app'):
            rc = rc.replace('/_app','')

        if suffix != None:
            rc ='{}/{}'.format(rc, suffix)

        return rc

    def getLines(self, folder, filename):
        rc = []
        with open('{}/{}'.format(folder, filename)) as f:
           rc = f.readlines()

        return rc

    def writeLines(self, folder, filename, lines):
        rc = []
        with open('{}/{}'.format(folder, filename),'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in lines])
        return self

    def copy(self, fromFile, toFile):
        # fromFile is the source file path/filename
        # toFile is the destination path/filename
        # doesnt overwrite existing file
        if self.fileExists(fromFile):
            shutil.copy(fromFile, toFile)
        return self
    '''
        def copy(self, fromFile, toFile ):
        # fromFile is the source file path/filename
        # toFile is the destination path/filename
        # doesnt overwrite existing file
        if self.fileExists(fromFile):
            shutil.copy(fromFile, toFile)
        return self
    '''

    def copyFolder(self,fromFolder, toFolder,ignore=None):
        # ignore is ignore_patterns('*.pyc', 'tmp*')
        if ignore:
            #print('ignore', ignore)
            shutil.copytree(fromFolder, toFolder, dirs_exist_ok=True,ignore=ignore)
        else:
            shutil.copytree(fromFolder, toFolder, dirs_exist_ok=True)

        #from shutil import copytree, ignore_patterns
        #copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))
        return self


    def backupName(self, currentName):
        # currentName eg some.sql
        # output: some.sql.<datetime>.backup
        # remember to exclude .backup from GIT Repo in target folder
        #now = datetime.now()
        #d4 = now.strftime("%Y.%m.%d.%H.%M.%S.%f")
        #datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f")
        #return '{}.{}.backup'.format(currentName,datetime.now().strftime("%Y%m%d%H%M%S%f"))
        return '{}.{}.backup'.format(currentName,datetime.now().strftime("%Y-%j-%f"))

    def makeBackupFile(self, folder, filename):
        # get backupName
        # copy filename to backupName,
        # copy backup to a backup folder
        #print('makeBackupFile 1 folder ', folder)
        #print('makeBackupFile', folder, filename)
        if folder == None:
            raise Exception('Unspecified backup folder: {}'.format(folder))
        backupFolder = '{}/backup'.format(folder)
        bkName = self.backupName(filename)

        self.createFolder(backupFolder)

        if Util().file_exists(folder, filename):
            self.copy('{}/{}'.format(folder, filename),
                      '{}/{}'.format(backupFolder,bkName))

            return {"folder":backupFolder,"original":filename,"backup":bkName}
        return {"folder":folder,"original":None,"backup":None}

    def confirm(self, question, default='Y'):
        val = input("{}: [{}]".format(question, default))
        if val == '':
            val = default
        rc = True
        if val != default.upper() and val != default.lower():
            rc = False
        #else:
        #    val = False
        return rc

    def collect(self,question, default ):
        val = input("{}: [{}]".format(question,default))
        if val == '':
            val = default
        elif val == 'q':
            val = None
        elif val == 'Q':
            val = None
        elif val == 'n':
            val = None
        elif val == 'N':
            val = None
        elif val == 'x':
            val = None
        elif val == 'X':
            val = None
        return val
    '''
    def getApiName(self, config_folder, file_type='source'):
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
        #return ApiConfiguration(config_folder, config_filename).load()
        return config_filename
    '''

def main():
    print('time', Util().backupName("Hi.sql"))
    print('backup',Util().makeBackupFile(os.getcwd(),'test.txt'))

    if Util().confirm('Continue?'):
        print('please continue')
    else:
        print('stop')

    if Util().confirm('Continue?', 'N'):
        print('stop')
    else:
        print('continue')
    #print('hi',Util().collect('Name','James'))
    #if Util().collect('Name', 'James')
    #print({
    #        'James': 'j',
    #        None: exit(0)
    #    }[Util().collect('Name','James')])
    val = Util().collect('Name','James')
    if val == None:
        print('stop')
        exit(0)
    else:
        print('do something with {}'.format(val))
    print('more')
    '''
    #from app_settings import AppSettingsTest
    from dotenv import load_dotenv
    import os

    os.environ['LB-TESTING'] = '1'
    load_dotenv()

    env_folder = Util().getResourceProjectFolder()
    Util().loadEnv('{}/.env'.format(env_folder))

    #appSettings = AppSettingsTest()
    test_folder = "{}/{}".format(str(Path.home()), "test-me" )# user folder
    assert(Util().createFolder(test_folder).folder_exists(test_folder))
    assert(Util().folder_exists(test_folder))
    #
    test_file='test.txt'
    with open('{}/{}'.format(test_folder, test_file), "w") as f:
        f.write("test line")
    assert(Util().file_exists(test_folder, test_file))
    assert(Util().getFileList(test_folder, 'txt') == [test_file])
    assert(not Util().deleteFile(test_folder, test_file).file_exists(test_folder, test_file))
    assert(not Util().deleteFolder(test_folder).folder_exists(test_folder))
    # get extension
    #c_file = 'credentials.db_api-table-table.pg.json._DEP'
    #print('Util().getFileExtension(c_file)',Util().getFileExtension(c_file))
    #assert(Util().getFileExtension(c_file)=='db_api-table-table.pg.json')
    # source folder
    #working_folder_name_default = 'example'
    folderlist = Util().getFolderList(env_folder)
    print('folderlist', folderlist)
    os.environ['LB-TESTING'] = '0'
    '''
if __name__ == "__main__":
    main()