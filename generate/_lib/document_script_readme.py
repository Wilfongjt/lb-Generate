from lib.document import Document
from datetime import date

class ScriptReadmeDocument(Document):
    def __init__(self, folder, file_name):
        super().__init__(folder, file_name)

    def getClassName(self):
        return self.__class__.__name__

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
