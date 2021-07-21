from lib.shallow_dictionary import ShallowDictionary
from pprint import pprint

class dep_SystemConfiguration(ShallowDictionary):
    def __init__(self, folder='', filename=''):
        super().__init__(folder, filename)
        self.api_kinds = 'api-definition api-static'
        self.database_kinds = 'postgres '
        self.source_kinds = 'repo-source '
        self.target_kinds = 'repo-target'

    def load(self, _dictionary={}):
        super().load(_dictionary)
        self.makeGeneratedKeys()
        return self

    def update(self, dictionary):
        super().update(dictionary)
        # merge dictionaries
        self.makeGeneratedKeys()
        return self

    def injectDatabase(self, def_name):
        for dbName in self:
            if self[dbName] in self.database_kinds:
                print('inject ', dbName, ' into ', def_name)
        return self

    def makeGeneratedKeys(self):
        # [Create a function name complete with parameters]
        methods = ["POST", "GET", "PUT", "DELETE"]
        # evaluate each API definition
        for def_key in self:
            if 'kind' not in self[def_key]:
                raise Exception('{} is missing kind'.format(def_key))
                #exit(0)
            elif  self[def_key]['kind'] == 'api-definition':
                self[def_key]['funcPattern'] = self.getFunctionPattern(def_key)
                # eg if not(result ->> 'scope' = 'api_admin') and not(result ->> 'scope' = 'api_guest') then
                for svc in self.getScopeVerificationConditions(def_key):
                    self[def_key]['{}-scope-verification-condition'.format(svc)] = self.getScopeVerificationConditions(def_key)[svc]
                # eg if not(_form ? 'username') or not(_form ? 'password') then
                for svc in self.getFormRequiredFieldConditions(def_key):
                    self[def_key]['{}-form-required-field-condition'.format(svc)] = self.getFormRequiredFieldConditions(def_key)[svc]

                self.injectDictionaries(def_key)

        return self

    def getApi(self, apiName):
        rc = None
        if apiName not in self:
            print('API key "{}" is not found in configuration.'.format(apiName))
            return None

        if self[apiName]['kind'] not in self.api_kinds:
            print('API {} Kind: "{}", is not an API.'.format(apiName, self[apiName]['kind']))
            return None
        return self[apiName]

    def getDatabase(self, dbName='_tasks'):
        rc = None

        if dbName not in self:
            print('Database key "{}" is not found in configuration.'.format(dbName))
            return None
        if self[dbName]['kind'] not in self.database_kinds:
            print('Database "{}" Kind: "{}", is not a _tasks.'.format(dbName, self[dbName]['kind']))
            return None
        rc = self[dbName]
        return rc

    def getSource(self,srcName = 'source'):
        rc = None

        if srcName not in self:
            print('Source key "{}" is not found in configuration.'.format(srcName))
            return None
        if self[srcName]['kind'] not in self.source_kinds:
            print('Source "{}" Kind: "{}", is not a source.'.format(srcName, self[srcName]['kind']))
            return None
        rc = self[srcName]
        return rc

    def getTarget(self,targetName = 'target'):
        rc = None
        if targetName not in self:
            print('Target key ({}) is not found in configuration.'.format(targetName))
            return None
        if self[targetName]['kind'] not in self.target_kinds:
            print('Target {} Kind: {}, is not a Target.'.format(targetName, self[targetName]['kind']))
            return None
        rc = self[targetName]
        return rc



#class UnitTest(unittest.TestCase):
#    def test1(self):
#        self.assertRaises(Exception, passing_function)

def main():
    from pprint import pprint
    target = {
        "target":{
                "kind":"repo-target",
                "umbrella":"01-Generate",
                "branch":"#01.init",
                "project":"lb-Generate",
                "folders": [{"name":"lb-api/one_db", "type":"db"},
                        {"name":"lb-api/hapi-api","type":"db_api"},
                        {"name":"sql","type":"scripts"}]
        },
        "_tasks": {
            "kind":"postgres",
            "name":"one_db",
            "schema":["api_0_0_1","base_0_0_1","public"],
            "table":{"name":"one"},
            "env": [
                {"key": "POSTGRES_DB","value": "aad_db"},
                {"key": "POSTGRES_USER","value": "postgres"},
                {"key": "POSTGRES_PASSWORD","value": "mysecretdatabasepassword"},
                {"key": "POSTGRES_JWT_SECRET","value": "PASSWORDmustBEATLEAST32CHARSLONGLONG"},
                {"key": "POSTGRES_API_PASSWORD","value": "guestauthenticatorsecretdatabasepassword"},
                {"key": "POSTGRES_JWT_CLAIMS","value": {"aud":"lyttlebit-api", "iss":"lyttlebit", "sub":"client-api", "user":"guest", "scope":"api_guest", "key":"0"}}
            ]
        }
    }

    source = {
        "source": {
                "kind":"repo-source",
                "umbrella":"01-Generate",
                "branch":"#01.init",
                "project":"lb-Generate",
                "folders": [{"name":"lb-api/one_db", "type":"db"},
                        {"name":"lb-api/hapi-api","type":"db_api"},
                        {"name":"sql","type":"scripts"}]
        },
        "user": {
            "kind": "api-definition",
            "prefix": "24",
            "name": "user",
            "schema": "api_0_0_1",
            "chelate": {
                "pk": "username",
                "sk": "const#USER",
                "tk": "guid",
                "form": {
                    "username": {
                        "name": "username",
                        "type": "email",
                        "operations": "CruD",
                        "input": "CruD",
                        "output": "R"
                    },
                    "password": {
                        "name": "password",
                        "type": "password",
                        "operations": "Cu",
                        "input": "Cu",
                        "output": False
                    },
                    "displayname": {
                        "name": "displayname",
                        "type": "TEXT",
                        "operations": "cRu",
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
                    "headers": {
                        "authorization": {"name": "token", "type": "TEXT"},
                        "test": {"name": "testForm", "type": "TEXT"}
                    },
                    "parameters": {
                        "token": {"name": "token", "type": "TEXT"},
                        "form": {"name": "testForm", "type": "JSON"}
                    },

                    "roles": {
                        "api_admin": {
                            "template": [
                                "_chelate := base_0_0_1.chelate('[[data-POST-api-admin-chelate-id]]'::JSONB, _form);",
                                "tmp = set_config('request.jwt.claim.key', replace(_chelate ->> 'tk','guid#',''), true);"]
                        }
                    }
                },
                "GET": {
                    "headers": {
                        "authorization": {"name": "token", "type": "TEXT"},
                        "test": {"name": "testForm", "type": "TEXT"}
                    },
                    "parameters": {
                        "token": {"name": "token", "type": "TEXT"},
                        "form": {"name": "criteria", "type": "JSON"},
                        "options": {"name": "options", "type": "JSON"}
                    },
                    "roles": {
                        "api_admin": {
                            "template": ["-- api_admin GET code"]
                        },
                        "api_user": {
                            "template": ["-- api_user GET code"]
                        }
                    }
                },
                "PUT": {
                    "headers": {
                        "authorization": {"name": "token", "type": "TEXT"},
                        "test": {"name": "testForm", "type": "TEXT"}
                    },
                    "parameters": {
                        "token": {"name": "token", "type": "TEXT"},
                        "key": {"name": "pk", "type": "TEXT"},
                        "form": {"name": "form", "type": "JSON"}
                    },
                    "roles": {
                        "api_admin":{
                            "template":["-- api_admin PUT code"]
                        },
                        "api_user":{
                            "template":["-- api_user PUT code"]
                        }
                    }
                },
                "DELETE": {
                    "headers": {
                        "authorization": {"name": "token", "type": "TEXT"},
                        "test": {"name": "testForm", "type": "TEXT"}
                    },
                    "parameters": {
                        "token": {"name": "token", "type": "TEXT"},
                        "key": {"name": "pk", "type": "TEXT"}
                    },
                    "roles": {
                        "api_user":{
                            "template":["-- api_user DELETE code"]
                        }
                    }
                }
            },
            "type": "const#USER",
            "dep-roles": {
                "api_guest": {
                    "description": ["Guest cannot POST new user",
                                    "Guest cannot GET user(s)",
                                    "Guest cannot PUT changes into user",
                                    "Guest cannot DELETE a user"],
                    "privileges": "C",
                    "token": "Gk",
                    "execute": []
                },
                "api_user": {
                    "description": ["User cannot POST another user.",
                                    "User can only GET their own user info.",
                                    "User can only PUT changes into their own user info",
                                    "User can only DELETE their own user info"],
                    "privileges": "crud",
                    "token": "UK",
                    "execute": ["GET", "PUT", "DELETE"]
                },
                "api_admin": {
                    "description": ["Admin can POST new user",
                                    "Admin can GET user(s)",
                                    "Admin can DELETE any user",
                                    "Admin cannot PUT any changes in a user"],
                    "privileges": "r",
                    "token": "AK",
                    "execute": ["POST", "GET", "DELETE"]
                }
            },
            "runAsRole": "api_guest",
            "tokenRole": "api_user",
            "passwordHashOn": "password"
        }
    }

    print('Test')
    systemConfig = SystemConfiguration()\
        .load(source)\
        .update(target)
    assert('user' in systemConfig )
    assert('_tasks' in systemConfig )
    assert('source' in systemConfig )
    assert('target' in systemConfig )



    assert(systemConfig.getApi('no_api') == None)
    assert(systemConfig.getApi('user') != None)
    assert(systemConfig.getApi('_tasks') == None)
    assert(systemConfig.getApi('source') == None)
    assert(systemConfig.getApi('target') == None)
    
    assert(systemConfig.getDatabase('no_database') == None)
    assert(systemConfig.getDatabase('user') == None)
    assert(systemConfig.getDatabase('_tasks') != None)
    assert(systemConfig.getDatabase('source') == None)
    assert(systemConfig.getDatabase('target') == None)

    assert (systemConfig.getSource('no_source') == None)
    assert (systemConfig.getSource('user') == None)
    assert (systemConfig.getSource('_tasks') == None)
    assert (systemConfig.getSource('source') != None)
    assert (systemConfig.getSource('target') == None)

    assert (systemConfig.getTarget('no_target') == None)
    assert (systemConfig.getTarget('user') == None)
    assert (systemConfig.getTarget('_tasks') == None)
    assert (systemConfig.getTarget('source') == None)
    assert (systemConfig.getTarget('target') != None)


if __name__ == "__main__":
    main()