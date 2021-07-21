from pprint import pprint
from lib.document import Document

class EnvironmentDocument(Document):
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
            if ln.startswith('#'):
                self.append(ln)
            elif '=' in ln:
                p = ln.split('=')
                self.append('{}={}'.format(p[0].strip(),p[1].strip()))
            else:
                self.append('# {}'.format(ln))

        return self

    def set(self,key,value):
        i = 0
        for i in range(len(self)):
            #if key in self[i]:
            if self[i].strip().startswith(key):
                self[i]='{}={}'.format(key.strip(),value.strip())
                print('   - updated ', key.strip(), ' to ', value.strip())
                return self

        print('   - insert  ', key.strip(), ' to ', value.strip())
        self.append('{}={}'.format(key.strip(),value.strip()))
        return self

    def has(self, key):
        for ln in self:
            if ln.strip().startswith(key):
                return True
        return False

    #def insert(self,key,value):
    #    i = 0
    #    for i in range(len(self)):
    #        if self[i].strip().startswith(key):
    #            break
    #    self.append('{}={}'.format(key.strip(), value.strip()))
    #    return self

    def get(self,key):
        value=None
        for nv in self:
            if nv.strip().startswith(key):
                value = nv.split('=')
                if len(value)==2:
                    value = value[1].strip()
                    break
        return value

    def update(self,envDoc):
        if envDoc.getClassName() != 'EnvironmentDocument':
            # [Ignore update when document is not a env file.]
            return self

        for ln in envDoc:
            # [Skip update on all comments]
            if not ln.strip().startswith('#'):
                value = ln.split('=')
                if len(value) == 2:
                    # [Skip anything that doesnt have an equal sign]
                    self.set(value[0], value[1])

    def insert(self, envDoc):
        if envDoc.getClassName() != 'EnvironmentDocument':
            # [Ignore update when document is not a env file.]
            return self
        for ln in envDoc:
            if not ln.strip().startswith('#'):
                item = ln.strip().split('=')
                #print('insert has', item, self.has(item[0]))
                if not self.has(item[0]):
                    #print('insert new')
                    self.append('{}={}'.format(item[0].strip(), item[1].strip()))

        return self

def main():
    env = EnvironmentDocument('../examples/files','.env').load()
    assert(len(env)==35)
    #print('-------')

    envUpd = EnvironmentDocument('../examples/files','merge.env').load()
    assert(len(envUpd)==2)
    #print('-------')
    print('==== Update ====')
    env.update(envUpd)
    assert(len(env)==36)
    #pprint(env)
    '''
    env_list = [
        '#########################',
        ' NODE_ENV = development ',
        '  # Postgres specific variables  ',
        'Not a comment comment',
        '#########################',
        'POSTGRES_DB = one_db',
        '#########################',
        'API_HOST = 0.0.0.0'
    ]



    folder = ''
    file_name = ''
    print('=========Start======')

    env = EnvironmentDocument(folder, file_name).load(env_list)

    env.set('ANY','SomeValue')

    #print('NODE_ENV', env.get('NODE_ENV'))
    assert env.get('NODE_ENV') == 'development'
    assert env.get('ANY') == 'SomeValue'

    assert env.has('NODE_ENV') == True
    assert env.has('POSTGRES_DB') == True
    assert env.has('API_HOST') == True
    assert env.has('JUNK') == False

    print(env)


    print('=========Update======')
    env_update = [
        ' NODE_ENV = DEVELOPMENT',
        ' # Postgres specific variables',
        '  API_HOST = 1.1.1.1',
        '   VERYNEW=MYNEWSTUFF'
    ]
    envUpd =  EnvironmentDocument(folder, file_name).load(env_update)
    env.update(envUpd)
    print(env)

    assert env.get('NODE_ENV') == 'DEVELOPMENT'
    assert env.get('API_HOST') == '1.1.1.1'
    assert env.get('VERYNEW') == 'MYNEWSTUFF'


    print('=======Insert======')
    # insert will add items when key dont exist
    # insert will not update when key exists
    env_insert = [
        ' NODE_ENV = NO',
        ' # Postgres specific variables',
        '  API_HOST = NO ',
        ' VERYNEW=NO ',
        'MORE=INSERT '
    ]
    envIns = EnvironmentDocument(folder, file_name).load(env_insert)
    env.insert(envIns)
    pprint(env)
    assert env.get('NODE_ENV') == 'DEVELOPMENT'
    assert env.get('API_HOST') == '1.1.1.1'
    assert env.get('VERYNEW') == 'MYNEWSTUFF'
    assert env.get('MORE') =='INSERT'


    print(env.toString('\n'))
    '''

if __name__ == "__main__":
    main()
