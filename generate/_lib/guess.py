from lib.util import Util
from lib.shallow_dictionary import ShallowDictionary
import os

class Guess():
    def __init__(self):
        self.somethin=None

    def guess(self):

        return None

class BranchFolderGuess(Guess):
    def __init__(self):
        self.key = 'branch'
        self.repo_name = None
        self.parent_folder=os.getcwd()

    def setRepoName(self,repo_name):
        self.repo_name = repo_name
        return self

    def setParentFolder(self, parent_folder=None):
        if not parent_folder:
            self.parent_folder=os.getcwd()
        else:
            self.parent_folder=parent_folder

        return self

    def guess(self, default):
        # get list of potential folders
        folders = Util().getFolderList(self.parent_folder)
        rc = default
        # expect the last found with a .git/ subfolder is the correct one
        for folder in folders:
            if Util().folder_exists('{}/{}/{}'.format(folder,self.repo_name,'.git')):
                #print('yes ', folder)
                rc = folder.replace(self.parent_folder, '').replace('/','')

        return rc
'''
class Guessables(dict):
    def __init__(self):
        self.append(BranchFolderGuess())

    def append(self, guess):
        self[guess.key] = guess
        return self

    def get(self, key):
        return self[key]
'''

def main():
    parent_folder = '?'
    branch = BranchFolderGuess()\
        .setRepoName('lb-Generate')\
        .setParentFolder('../../../..')
    print('branch', branch.guess('babel'))
    #guessable = Guessables().append(branch)

    #print('branch folder guess', Guessables().get('branch').setParentFolder('../../../..').setRepoName('lb-Generate').guess())

    #print('branch folder guess',BranchFolderGuess('lb-Generate','../../../..').guess())

if __name__ == "__main__":
    main()