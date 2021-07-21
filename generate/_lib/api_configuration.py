from lib.shallow_dictionary import ShallowDictionary
from pprint import pprint


class ApiConfiguration(ShallowDictionary):
    def __init__(self, folder='', filename=''):
        super().__init__(folder, filename)
        self.api_kinds = 'api-definition api-static'
        self.database_kinds = 'postgres '
        self.source_kinds = 'repo-source '
        self.target_kinds = 'repo-target'

    def load(self,_definitions={}):
        super().load(_definitions)
        #self.makeGeneratedKeys()
        return self

    def update(self, dictionary):
        super().update(dictionary)
        #self.makeGeneratedKeys()
        return self

    def getMethods(self,apiDefKey, _type):
        '''
        {'DELETE': {} or "" or [],
          'GET': {} or "" or [],
          'POST': {} or "" or [],
          'PUT': {} or "" or []'
        }
        _type is headers, parameters, privileges, ...
        '''
        name = self[apiDefKey]['name']
        lst = {}
        for m in self[apiDefKey]['methods']:
            lst[m] = {}
            for p in self[apiDefKey]['methods'][m]:
                lst[m] = self[apiDefKey]['methods'][m][_type]

        return lst
    '''
    def flatten(self, key_name=None):
        if not key_name:
            super
        else:    
            flat = super().fself[key_name]
        return flat
    '''
    def getConstants(self, api_name):
        return self.constants(parent=self[api_name])

    #def getLists(self,api_name):
    #    return self.lists(parent=self[api_name])

        #def getFunctionPattern(self, apiDefKey):
        '''
        have
        user: {
          methods: {
            POST:{
                header:{
                    authorization:{"name":"token","type":"TEXT"},
                    test:{"name":"testForm","type":"TEXT"}
                },
                parameters:{
                    "token":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"JSON"}
                },
                privileges:[]
            }
          }
        }
        want
         {'DELETE': 'user(TEXT, TEXT)',
          'GET': 'user(TEXT, JSON, JSON)',
          'POST': 'user(TEXT, JSON)',
          'PUT': 'user(TEXT, TEXT, JSON)'}
        '''
    #   function_name = self[apiDefKey]['name']
    #   methods = {}
    #    key = 'parameters'
    #    for m in self[function_name]['methods']:
    #        params = ['{}'.format(y[1]['type']) for y in [x for x in self[function_name]['methods'][m][key].items()]]
    #        params = ','.join(params)
    #        methods[m] = '{}({})'.format(function_name, params)

    #    return methods

    #def getScopeVerificationConditions(self, def_key):

    #    # subsitution key [[data-POST-scope-verification-condition]]
    #    # subsitution key [[data-GET-scope-verification-condition]]
    #    # subsitution key [[data-PUT-scope-verification-condition]]
    #    # subsitution key [[data-DELETE-scope-verification-condition]]

    #    methods = {}
    #    function_name = self[def_key]['name']
    #    #key = 'privileges'
    #    key = 'roles'
    #    for m in self[function_name]['methods']:
    #        privileges = ['not(\'{}\')'.format(p) for p in [x for x in self[function_name]['methods'][m][key]]]

    #        privileges = ' or '.join(privileges)
    #        methods[m] = '{}'.format(privileges)

    #    return methods

    #def getFormRequiredFieldConditions(self,def_key):
    #    # subsitution key [[data-POST-form-required-field-conditions]]
    #    # subsitution key [[data-GET-form-required-field-conditions]]
    #    # subsitution key [[data-PUT-form-required-field-conditions]]
    #    # subsitution key [[data-DELETE-form-required-field-conditions]]
    #    # Fix
    #    methods = {}
    #    function_name = self[def_key]['name']

    #    o2m = {'C':"POST","R":"GET","U":"PUT","D":"DELETE"}
    #    for operation in ['C',"R","U","D"]:
    #        required = ['not(_form ? \'{}\')'.format(r) for r in[fld[0] for fld in self[function_name]['chelate']['form'].items() if operation in fld[1]['operations']]]
    #        methods[o2m[operation]] =  ' or '.join(required)
    #        if len(methods[o2m[operation]]) == 0:
    #            methods[o2m[operation]]='1=0'

    #    return methods

    def getDatabase(self, dbName='_tasks'):
        rc = None

        if dbName not in self:
            print('ERROR Database key "{}" is not found in configuration.'.format(dbName))
            return None
        if self[dbName]['kind'] not in self.database_kinds:
            print('ERROR Database "{}" Kind: "{}", is not a _tasks.'.format(dbName, self[dbName]['kind']))
            return None
        rc = self[dbName].items()
        return rc
    '''
    def injectDatabase(self, def_name):

        if '_tasks' not in self:
            print('ERROR Database key not found.')
            self[def_name]['_tasks'] = {}
            return self

        self[def_name]['_tasks'] = self['_tasks']

        return self
    '''
    '''
    def injectGrantExecute(self, def_name):
        #getMethods(self, apiDefKey, _type):
        function_name = def_name
        _type = 'grant'
        #methods = {}
        #function_name = 'user'
        # function_execute_name = 'user'
        key = 'roles'
        key2 = 'parameters'

        for m in self[function_name]['methods']:

            # param-type, param-type
            param_types = ['{}'.format(y[1]['type']) for y in
                           [x for x in self[function_name]['methods'][m][key2].items()]]
            param_types = ','.join(param_types)

            privileges = ['grant EXECUTE on FUNCTION {}({}) to {};'.format(function_name, param_types, p) for p in
                          [x for x in self[function_name]['methods'][m][key]]]
            privileges = '\n'.join(privileges)

            self[function_name]['methods'][m][_type] = '{}'.format(privileges)

        return self
    '''
    #def makeGeneratedKeys(self):
    #    # [Create a function name complete with parameters]
    #    #methods = ["POST", "GET", "PUT", "DELETE"]
    #    # evaluate each API definition
    #    for def_key in self:
    #        if 'kind' not in self[def_key]:
    #            raise Exception('{} is missing kind'.format(def_key))
    #            #exit(0)
    #        elif  self[def_key]['kind'] == 'api-definition':
    #            #self[def_key]['funcPattern'] = self.getFunctionPattern(def_key)
    #            # eg if not(result ->> 'scope' = 'api_admin') and not(result ->> 'scope' = 'api_guest') then
    #            #for svc in self.getScopeVerificationConditions(def_key):
    #            #    self[def_key]['{}-scope-verification-condition'.format(svc)] = self.getScopeVerificationConditions(def_key)[svc]
    #            # eg if not(_form ? 'username') or not(_form ? 'password') then
    #            #for svc in self.getFormRequiredFieldConditions(def_key):
    #            #    self[def_key]['{}-form-required-field-condition'.format(svc)] = self.getFormRequiredFieldConditions(def_key)[svc]

    #            #self.injectDatabase(def_key)

    #            #self.injectGrantExecute(def_key)

    #    return self



def main():
    from pprint import pprint
    '''
    absoluteSys = {
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
    '''
    print('Test')

    api_configuration = ApiConfiguration(folder='../config', filename='user.source').load()
    #api_target = ApiConfiguration(folder='../config', filename='local.lb-api.target').load()
    #api_configuration.update(api_target)



    print("ApiConfiguration")
    pprint(api_configuration.getConstants('user'))

    print('Methods by type')
    #pprint(api_configuration.getMethods("user","headers"))
    #pprint(api_configuration.getMethods("user","parameters"))
    #pprint(api_configuration.getMethods("user","roles"))

    #print('constants')
    #pprint(api_configuration.constants(parent=api_configuration['user']))

    #print('getFunctionPattern')
    #pprint(api_configuration.getFunctionPattern( 'user'))

    #print('makeGeneratedKeys')
    #pprint(api_configuration.makeGeneratedKeys())

    #print('getParameterList')
    #pprint(api_confg.getParameterList('user'))
    print('==== ApiConfiguration ===')
    #pprint(api_configuration.getLists('user'))
    pprint(api_configuration.flatten('user',parent_key='user'))
if __name__ == "__main__":
    main()