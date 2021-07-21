from lib.util import Util
import json
import os
from pprint import pprint
#import collections
from collections.abc import MutableMapping
#from collections import OrderedDict
class ShallowDictionary(dict):
    # create file in ./config
    # load from top keys only
    # load from dictionary or file

    def __init__(self, folder='', filename=''):
        self.folder = folder
        self.filename = filename

    def load(self,_dictionary={}):
        # print('dictionary ', _dictionary)
        if len(_dictionary) > 0:
            print('load dictionary {}'.format(len(_dictionary)))
        else:
            if Util().file_exists(self.folder,self.filename):
                #print('loading file')
                with open('{}/{}'.format(self.folder, self.filename)) as f:
                    _dictionary = json.load(f)
            else:
                print('file not found: ', self.folder, self.filename)
                print('current folder', os.getcwd())

        for key in _dictionary:
            #print('- dictionary key', key)
            self[key] = _dictionary[key]

        return self

    def show(self):
        for key in self:
            print('key', key, self[key])
        return self

    def save(self):
        if len(self) > 0:

            backup=Util().makeBackupFile(self.folder, self.filename)
            print('- backup ', backup)
            print('- save {}/{}'.format(self.folder, self.filename))

            with open('{}/{}'.format(self.folder,self.filename), 'w') as json_file:
                json.dump(self, json_file, indent = 4)
        return self

    #def saveAs(self, folder, filename):
    #    print('save as {}/{}'.format(folder,filename))
    #    return self

    def flatten(self, key_name=None, parent_key='data', sep='-'):
        # flatten out dictionary
        parent = None
        if key_name == None:
            parent = self
        else:
            parent = self[key_name]

        items = []

        for k, v in parent.items():
            new_key = parent_key + sep + k if parent_key else k
            #if isinstance(v, MutableMapping):
            if isinstance(v, dict):
                items.extend(self.constants(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if len(v)>0 and type(v[0]) is str:
                    items.append((new_key, v))
            else:
                if not isinstance(v, list):
                    items.append((new_key, v))

        return dict(items)

    def constants(self, parent=None,parent_key='data', sep='-'):
        # flatten out dictionary
        items = []
        if parent == None:
            parent = self

        for k, v in parent.items():
            new_key = parent_key + sep + k if parent_key else k
            #if isinstance(v, MutableMapping):
            if isinstance(v, dict):
                items.extend(self.constants(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if len(v)>0 and type(v[0]) is str:
                    items.append((new_key, v))
            else:
                if not isinstance(v, list):
                    items.append((new_key, v))

        return dict(items)

    '''
    def lists(self, parent=None, parent_key='data', sep='-'):
        items = []
        if parent == None:
            parent = self
        local_list = {}
        for key, value in parent.items():
            new_key = parent_key + sep + key if parent_key else key
            if isinstance(value,dict): # add dictionary
                local_list[new_key] = value
                local_list.update(self.lists(value,new_key))
            if isinstance(value,list): # add dictionary
                local_list[new_key] = value

        return local_list
    '''

    def template_keys(self, topKey=None):
        if topKey == None:
            rc = self.flatten(d=None,parent_key='description')
        else:
            rc = self.flatten(d=self[topKey],parent_key='description')
        rc = [k for k in rc]
        return rc
'''

[user: {}]                        
[user: {}, user-methods: {}]
[user: {}, user-methods: {}, user-methods-POST: {}]

'''


def main():
    print('Test')

    _dictionary = {
        "user": {
        "kind":"api-definition",
        "prefix":"24",
        "name": "user",
        "schema": "api_0_0_1",
        "chelate": {
            "pk": "username",
            "sk": "const#USER",
            "tk": "guid",
            "form": {
                "username": {
                    "name":"username",
                    "type": "email",
                    "operations":"CruD",
                    "input": "CruD",
                    "output": "R"
                },
                "password": {
                    "name":"password",
                    "type": "password",
                    "operations":"Cu",
                    "input": "Cu",
                    "output": False
                },
                "displayname": {
                    "name":"displayname",
                    "type": "TEXT",
                    "operations":"cRu",
                    "input": "cu",
                    "output": "R"
                }
            },
            "active": {
                "default": True
            },
            "created": {
                "default": "NOW()"
            },
            "updated": {
                "default": "NOW()"
            },
            "owner": {
                "default": "current_setting('request.jwt.claim.key')"
            }
        },
        "methods": {
            "POST": {

            "roles": {
                "api_admin": {
                    "template": ["_chelate := base_0_0_1.chelate('[[data-POST-api-admin-chelate-id]]'::JSONB, _form);",
                                 "tmp = set_config('request.jwt.claim.key', replace(_chelate ->> 'tk','guid#',''), true);"]
                },
                "api_guest":""
            },
                "headers": {
                    "authorization":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"TEXT"}
                },
                "parameters": {
                    "token":{"name":"token","type":"TEXT"},
                    "form":{"name":"testForm","type":"JSON"}
                }
            },
            "GET": {
                "headers": {
                   "authorization":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"TEXT"}
                },
                "parameters": {
                    "token":{"name":"token","type":"TEXT"},
                    "form":{"name":"criteria","type":"JSON"},
                    "options":{"name":"options","type":"JSON"}
                },
                "roles": {}
            },
            "PUT": {
                "headers": {
                    "authorization":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"TEXT"}
                },
                "parameters": {
                    "token":{"name":"token","type":"TEXT"},
                    "key": {"name":"pk","type":"TEXT"},
                    "form":{"name":"form","type":"JSON"}
                },
                "roles": {}
            },
            "DELETE": {
                "headers": {
                    "authorization":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"TEXT"}
                },
                "parameters": {
                    "token":{"name":"token","type":"TEXT"},
                    "key": {"name":"pk","type":"TEXT"}
                },
                "roles": {}
            }
        },
        "type": "const#USER",
        "dep-roles": {
            "api_guest": {
                "description":["Guest cannot POST new user",
                               "Guest cannot GET user(s)",
                               "Guest cannot PUT changes into user",
                               "Guest cannot DELETE a user"],
                "privileges": "C",
                "token": "Gk",
                "execute":[]
            },
            "api_user": {
                "description":["User cannot POST another user.",
                               "User can only GET their own user info.",
                               "User can only PUT changes into their own user info",
                               "User can only DELETE their own user info"],
                "privileges": "crud",
                "token": "UK",
                "execute":["GET","PUT","DELETE"]
            },
            "api_admin": {
                "description":["Admin can POST new user",
                               "Admin can GET user(s)",
                               "Admin can DELETE any user",
                               "Admin cannot PUT any changes in a user"],
                "privileges": "r",
                "token": "AK",
                "execute":["POST","GET","DELETE"]
            }
        },
        "runAsRole": "api_guest",
        "tokenRole": "api_user",
        "passwordHashOn": "password"
    }
    }
    print('A ===============================')
    shallowDictionary = ShallowDictionary(folder='../config', filename='user.source').load()
    shallowDictionaryTarget = ShallowDictionary(folder='../config', filename='local.lb-api.target').load()
    shallowDictionary.update(shallowDictionaryTarget)
    pprint(shallowDictionary)

    print('B ===============================')

    #shallowDictionary = ShallowDictionary('../_tasks/config','sample.json.config').load()
    #shallowDictionary = ShallowDictionary().load(_dictionary)

    pprint("ShallowDictionary")
    pprint(shallowDictionary.constants(_dictionary['user']))
    #pprint(shallowDictionary.lists(_dictionary['user']))
    print('C ===============================')
    pprint(shallowDictionary.flatten('database'))
    # start one key in from parent
    #print(' ')
    #pprint(shallowDictionary.flatten(d=shallowDictionary['user'],parent_key='definition'))
    #pprint(['[[{}]]:{}'.format(k) for k in shallowDictionary.flatten(d=shallowDictionary['user'],parent_key='definition')])

    #pprint(shallowDictionary.template_keys('user'))
    #shallowDictionary.save()
    #rc = ['[[{}]]'.format(k) for k in shallowDictionary.template_keys('user')]

    #print('zzz',shallowDictionary['user'])
    #rc = [k for k in shallowDictionary.listify(d=shallowDictionary['user'],parent_key='list')]
    #pprint(rc)

    #pprint(shallowDictionary.listify(d=shallowDictionary['user'],parent_key='list'))


if __name__ == "__main__":
    main()