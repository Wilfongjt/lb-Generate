import os
from lib.util import Util
import datetime

class Document(list):
    def __init__(self, folder, file_name):
        self.folder = folder
        self.filename=file_name

    def load(self, lst=[]):
        self.clear()
        if len(lst) == 0:
            #print('curr', os.getcwd())
            with open('{}/{}'.format(self.folder,self.filename)) as file:
                data = file.readlines()
                #print('data', data)
                for ln in data:
                    #self.append(ln.strip())
                    self.append(ln)

        else:
            self.extend(lst)
            #for ln in lst:
            #    self.append(ln)
        return self

    def backup(self):

        if self.folder == None:
            # [Skip backup when document is empty]
            raise Exception('Unspecified backup folder: {}'.format(self.folder))

        backupFolder = '{}/backup'.format(self.folder)

        dt = datetime.datetime.now()

        backupName = '{}.{}.backup'.format(self.filename, dt.strftime("%Y-%j-%f")) #self.backupName(self.file_name)

        Util().createFolder(backupFolder)
        print('backup', backupFolder, backupName)
        self.saveAs(backupFolder, backupName)

        return self

    def show(self):
        for ln in self:
            print('ln',ln)
        return self

    def isDifferent(self, document):
        sz = len(self)
        diff = False
        i=0
        A = [ln.strip() for ln in self if ln.strip() != '' and ln != "" and ln != '\t' and ln != '\n' and ln != '\r']
        B = [ln.strip() for ln in document if ln.strip() != '' and ln != "" and ln != '\t' and ln != '\n' and ln != '\r']
        for ln in A:
            #print('type',type(ln))
            #if i < len(A):
            #    print('A[{}] "{}"'.format(i, ln))
            #if i < len(B):
            #    print('B[{}] "{}"'.format(i, B[i]))

            if ln not in B:
            #    print('A[{}] "{}"'.format(i, ln))
                diff = True
            #    print('    ----> NOT FOUND IN B {}'.format(document.filename))
            if i < len(B) and B[i] not in A:
            #    print('B[{}] "{}"'.format(i, B[i]))
                diff = True
             #   print('        <---- NOT FOUND IN A {}'.format(self.filename))
            i += 1

        return diff

    def showDifferent(self, document):
        print('A is ', self.filename)
        print('B is ', document.filename, ' from ', document.folder )
        sz = len(self)
        diff = False
        AList = self.toString().split('\n')
        i=0
        A = [ln.strip() for ln in AList if ln.strip() != '' and ln != "" and ln != '\t' and ln != '\n' and ln != '\r']
        B = [ln.strip() for ln in document if ln.strip() != '' and ln != "" and ln != '\t' and ln != '\n' and ln != '\r']
        for ln in A:
            #print('type',type(ln))
            if i < len(A):
                print('A[{}] "{}"'.format(i, ln))
            if i < len(B):
                print('B[{}] "{}"'.format(i, B[i]))

            if ln not in B:
                print('A[{}] "{}"'.format(i, ln))
                diff = True
                print('    ====> NOT FOUND IN B {}'.format(document.filename))
            if i < len(B) and B[i] not in A:
                print('B[{}] "{}"'.format(i, B[i]))
                diff = True
                print('        <==== NOT FOUND IN A {}'.format(self.filename))
            i += 1

        return diff

    def delete(self):
        Util().deleteFile(self.folder,self.filename)
        return self

    def write(self):
        #print('write ','{}/{}'.format(self.folder, self.filename) )
        with open('{}/{}'.format(self.folder, self.filename), 'w') as f:
            if len(self) == 0:
                # raise Exception('Warning empty file: {} {}'.format(self.folder,self.filename))
                f.write('')
            else:
                f.write('\n'.join(self))

        return self

    def replace(self, repl, repl_with):
        i = 0
        if type(repl) == list:
            for ln in self:
                for i in range(len(repl)):
                    if repl_with[i]:
                        self.replace(repl[i], repl_with[i])
        else:
            for ln in self:
                self[i] = ln.replace(repl, repl_with)
                i += 1
        return self

    '''
    def replace(self, findStr, replStr):
        # [Replace a target string with a give string]
        i = 0
        for ln in self:
            self[i] = ln.replace(findStr, replStr)
            i += 1
        return self
    '''
    def rename(self, folder,filename):
        self.folder = folder
        self.filename = filename
        return self

    def save(self):
        self.write()
        return self

    def saveAs(self,folder, filename):
        with open('{}/{}'.format(folder, filename), 'w') as f:
            #f.write('\n'.join(self))
            f.write(self.toString())
        return self

    def toString(self, sep='\n'):
        return sep.join(self)

def main():
    from lib.util import Util
    from pprint import pprint

    lst = ['one','two','one_db']
    rc ='''
    ab
    AB
    one_db one_db
    replace A B
    '''
    lst = rc.split('\n')

    lst = [ln for ln in lst if ln.strip() != '']
    print(lst)

    doc4 = Document('.', 'junk.txt').load(lst)
    doc4.replace('one_db', 'ONE_DB')
    doc4.show()
    doc4.write() # write to disk
    print('folder {} filename {}'.format(doc4.folder, doc4.filename))
    assert(Util().file_exists(doc4.folder,doc4.filename))
    Util().deleteFile(doc4.folder, doc4.filename) # clean up
    assert(not Util().file_exists(doc4.folder,doc4.filename))

    doc4.replace('A','C')
    pprint(doc4)


    doc4.replace(['C','B'],['D','E'])
    pprint(doc4)

    # Backup
    print('====== backup =======')
    doc5 = Document(os.getcwd(),'document.py').load()
    print('backup', doc5.backup())
    print('====== load -=======')
    env = Document('../examples/files','.env').load()
    print(env)

    assert(len(env)==35)

    envUpd = Document('../examples/files','merge.env').load()
    print(envUpd)
    print('len(envUpd)',len(envUpd))
    assert(len(envUpd)==2)


if __name__ == "__main__":
    main()
