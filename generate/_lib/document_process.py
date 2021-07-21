from lib.document import Document
from datetime import date

'''
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
'''


class DocumentProcess(Document):
    def __init__(self, folder, file_name):
        super().__init__(folder, file_name)
        self.input_extention = None

    def getClassName(self):
        return self.__class__.__name__

    def setInputExtention(self, extention):
        self.input_extention = extention
        return self

    '''
    def load(self, lst=None):
    #def load(self, lst=[]):

        self.clear()

        if not lst:
            lst=[]
            # [Read from file]
            with open('{}/{}'.format(self.folder, self.filename),'r') as f:
                data = f.readlines()
                for ln in data:
                    lst.append(ln)
                    #print(ln.strip())

        lst = [l.strip() for l in lst]
        # [Read from List]
        for ln in lst:
            ln = ln.strip()
            if ln.startswith('# [#'):
                self.append(' ')

            if ln.startswith('# ['):
                self.append(ln.replace('# [','').replace(']',''))

        self.append('')
        self.append('<hr/>')

        self.append('')
        self.append('Date: {}'.format(date.today()))
        self.append('Source: {}'.format(self.filename))

        return self
    '''

def main():
    from pprint import pprint
    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest
    from lib.help_functions import get_environment

    print(ConfigurationTargetTest())
    print(ConfigurationSourceTest())
    print(ConfigurationSourceTest().update(ConfigurationTargetTest()))

    apiConfiguration = ConfigurationSourceTest().update(ConfigurationTargetTest())

    print(type(apiConfiguration))
    sourceDev = None
    targetDev = None

    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = get_environment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [Configure output targets from GIT repositories]
            targetDev = get_environment(apiConfiguration[apiName])

    #print(apiConfiguration)

    #pprint(targetDev)
    print('in  scripts',sourceDev.getFolder('scripts'))
    print('out scripts', targetDev.getFolder('scripts'))

    DocumentProcess( targetDev.getFolder('scripts'), "00.test.sql")\
        .setSource(sourceDev)\
        .setTarget(targetDev)\
        .setInputExtention("")
if __name__ == "__main__":
    main()

