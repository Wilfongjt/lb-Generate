from pprint import pprint
import os
import json
from lib.util import Util
from lib.document import Document
from lib.git_development import GitDevelopment
#from lib.system import ExamplesDevelopment
from lib.home_development import HomeDevelopment

from lib.api_configuration import ApiConfiguration

import tkinter as tk
from tkinter import filedialog

'''
    "parameters": {
            "POST": {
                "token": "TEXT",
                "form": "JSON"
            },
            "GET": {
                "token": "TEXT",
                "criteria": "JSON",
                "options": "JSON"
            },
            "PUT": {
                "token": "TEXT",
                "pk": "TEXT",
                "form": "JSON"
            },
            "DELETE": {
                "token": "TEXT",
                "pk": "TEXT"
            }
        },
'''
##########
# Generate User
##########

# c is optinal but validate when present
# C is required
# r is optinal but validate when present
# R is required
# u is optinal but validate when present
# U is required

# pksk
# sktk
'''
Define API
1. create definitions
'''
'''
Expand API Definition
1. augment definitions
2. inject functPattern
3. expand Chelate
4. expand Criteria
 
'''
'''
Script API
1. Validate Token and Set Role
2. Verify Expected Token Role(s)
3. Validate Parameters
4. User Specific Data Assembly
5. Execute Function

INSERT

QUERY
Criteria for query by user
* query by api_user by username
* query by api_admin by username or guid

'''
'''
-- required
if not(criteria ? 'username') or not(criteria ? 'password') then
-- validation
if criteria ? 'username' then
if criteria ? 'password' then  
if criteria ? 'displayname' then

    
'''

'''____        __ _       _ _   _                 
 |  __ \      / _(_)     (_) | (_)                
 | |  | | ___| |_ _ _ __  _| |_ _  ___  _ __  ___ 
 | |  | |/ _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
 | |__| |  __/ | | | | | | | |_| | (_) | | | \__ \
 |_____/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
                                                  
'''

#  "keys":'{"pk":"username","sk":"const#USER","tk":"*"}',
'''

moved to ./config/user.json

definitions = {
    "user_chelate": {
        "pk": "username",
        "sk": "const#USER",
        "tk": "guid",
        "form": {
            "username": {"type": "email", "input": "CruD", "output": "R"},
            "password": {"type": "password", "input": "Cu", "output": False},
            "displayname": {"type": "TEXT", "input": "cu", "output": "R"}
        },
        "active": {"default": True},
        "created": {"default": "NOW()"},
        "updated": {"default": "NOW()"},
        "owner": {"default": "current_setting('request.jwt.claim.key')"}
    },
    "user": {
        "name": "user",
        "schema": "api_0_0_1",
        "chelate": "user_chelate",
        "type": "const#USER",
        "dep-roles": "roles",
        "runAsRole": "api_guest",
        "tokenRole": "api_user",
        "param eters": {"POST": {"token": "TEXT", "form": "JSON"},
                       "GET": {"token": "TEXT", "criteria": "JSON", "options": "JSON"},
                       "PUT": {"token": "TEXT", "pk": "TEXT", "form": "JSON"},
                       "DELETE": {"token": "TEXT", "pk": "TEXT"}},
        "dep-roles": {"api_guest": {"privileges": "C", "token": "Gk"},
                  "api_user": {"privileges": "RUD", "token": "UK"},
                  "api_admin": {"privileges": "r", "token": "AK"}
                  },
        "passwordHashOn": "password"
    }
}
'''

#exit(0)
'''
           _____ _____ 
     /\   |  __ \_   _|
    /  \  | |__) || |  
   / /\ \ |  ___/ | |  
  / ____ \| |    _| |_ 
 /_/    \_\_|   |_____|

'''

#f = [fld for fld in d["form"]]
#print('f',f)
'''
class API_Configuration(ShallowDictionary):
    def __init__(self, folder='', filename=''):
        super().__init__(folder, filename)

    def load(self,_definitions={}):
        super().load(definitions)
        self.makeGeneratedKeys()

    def makeGeneratedKeys(self):
        methods = ["POST", "GET", "PUT", "DELETE"]
        for key in self:
            print('API key', key)
            if 'schema' in self:
                print('schema')
                for method in methods:
                    print('method', method)
        return self
'''
'''
class API(dict):
    def __init__(self, folder='.', filename='junk.json'):
        self.folder = folder
        self.filename = filename
        # transform

    def load(self,_definitions={}):
        methods = ["POST","GET","PUT","DELETE"]
        if _definitions == {}:
            print('Definitions empty')
        #    # [load definitions from file]
        #    print('hi')
        #    with open('path_to_file/person.json') as f:
        #        _definitions = json.load(f)
        # evaluate all top level keys
        # convert param eters to funcPattern by POST, GET, PUT, DELETE
        # overwrite the existing funcPatterns
        for key in _definitions:
            # Augment Definitions
            cpy_definition = _definitions[key].copy()
            # merge chelate with main api definition
            # find a definition
            if 'schema' in cpy_definition:
                print('chelate', cpy_definition['chelate'])
                chelate = _definitions[cpy_definition['chelate']]
                cpy_definition['chelate'] = chelate
                cpy_definition['funcPattern']={}
                # add
                for method in methods:
                    print('method', method)
                    self[key]=cpy_definition
                    # functPattern
                    name = cpy_definition['name']
                    # ""
                    # parame ters = ['{} {}'.format(param,definition['par ameters'][method][param]) for param in definition['par ameters'][method]]
                    parame ters = ['{}'.format(cpy_definition['pa rameters'][method][param]) for param in cpy_definition['paramet ers'][method]]
                    params = ', '.join(parame ters)
                    print('params ', params)

                    cpy_definition['funcPattern'][method] = '{}({})'.format(name, params)
                    #definition['funcPattern'][method]= 'xxx'#'{}({})'.format(name, params)
        return self
'''
class FunctionTemplate(list):
    def __init__(self, method, apiDefinition):
        # convert to Postgres API Script
        # definition is a single function definition
        self.method = method
        self.definition = apiDefinition
        #self.parameterList = ['{} {}'.format(param,self.definition['par ameters'][param]) for param in self.definition['pa rameters']]
        self.parameterList = None
        self.privileges=None
        self.tokenClaims=None
        # formatting
        #self.warning()
        self.nameFunction()
        self.declareVariables()
        self.begin()
        self.switchToRole(self.definition['runAsRole'])
        self.validateParameters()
        #self.startDataAssembly()
        #self.assembleDataHashPassword()
        self.assembleData()
        self.function()
        self.end()
        self.grantFunction()
    '''
    def getMethods(self, _type):
        
        {'DELETE': {} or "" or [],
          'GET': {} or "" or [],
          'POST': {} or "" or [],
          'PUT': {} or "" or []'
        }
     
        name = self.definition['name']
        lst = {}
        for m in self.definition['methods']:
            lst[m] = {}
            for p in self.definition['methods'][m]:
                lst[m] = self.definition['methods'][m][_type]

        return lst

    def getParameterList(self):
        # ["<value> <type>","<value> <type>",...]
        print('getMethods',self.getMethods('parameters'))
        print('getMethods ', self.getMethods('parameters')[self.method])

        if not self.parameterList:
            # ["<value> <type>","<value> <type>",...]


            self.parameterList = ['{} {}'.format(param, self.getMethods('parameters')[self.method][param])
                                    for param in self.getMethods('parameters')[self.method]]
        return self.parameterList
    '''
    '''
        def getParameterList(self):
        # ["<value> <type>","<value> <type>",...]
        if not self.parameterList:
            # ["<value> <type>","<value> <type>",...]

            self.parameterList = ['{} {}'.format(param, self.definition['parameters'][self.method][param])
                                    for param in self.definition['parameters'][self.method]]
        return self.parameterList
    
    '''
    #def getTokenByRole(self):
    #    if not self.tokenClaims:
    #        self.tokenClaims = {r: self.definition['roles'][r]['token'] for r in self.definition['roles']}
    #    return self.tokenClaims

    def getPrivilegesByRole(self):
        if not self.privileges:
            self.privileges = {r: self.definition['roles'][r]['privileges'] for r in self.definition['roles']}
        return self.privileges

    def getKeys(self):
        #keys = self.definition['keys']
        c = self.definition['chelate']
        rc = '{"pk":"%p","sk":"%s","tk":"%t"}'
        if '#' not in c['pk']:
            rc = rc.replace('%p',c['pk'])
        else:
            rc = rc.replace('%p','TBD')

        if 'const#' in c['sk']:
            rc = rc.replace('%s',c['sk'])
        else:
            rc = rc.replace('%s','TBD')

        if 'guid' in c['tk']:
            rc = rc.replace('%t','*')
        else:
            rc = rc.replace('%t','TBD')
        return rc

    #def warning(self):
    #    filename = __file__.split('/')
    #    filename = filename[len(filename)-1]
    #    rc = '''
    #    -- This function was generated using {}
    #    '''.format(filename)
    #    #self.append(rc)
    #    return rc

    def nameFunction(self):
        #pprint(self.definition)
        schema=self.definition['schema']
        # param eters = ['{} {}'.format(param,self.definition['par ameters'][param]) for param in self.definition['pa rameters']]
        name = self.definition['name']
        name = '{}({})'.format(name, ','.join(self.getParameterList()))
        result = 'CREATE OR REPLACE FUNCTION {}.{}  RETURNS JSONB AS $$'.format( schema, name)

        self.append(result)
        return self

    def declareVariables(self):
        rc = ''
        if 'POST' in self.method:
            rc = '    Declare _form JSONB; Declare result JSONB; Declare _chelate JSONB := \'{}\'::JSONB;Declare tmp TEXT;'
        if 'GET' in self.method:
            rc = '    Declare _criteria JSONB; Declare result JSONB;'
        if 'PUT' in self.method:
            rc = '    Declare _chelate JSONB := \'{}\'::JSONB; Declare _criteria JSONB := \'{}\'::JSONB; _form JSONB := \'{}\'::JSONB; Declare result JSONB;'
        if 'DELETE' in self.method:
            rc = '    Declare result JSONB; Declare _criteria JSONB := \'{}\'::JSONB;'

        self.append(rc)

        return self

    def begin(self):
        #titleComment = '-- [Function: {} {} given {}]'.format( self.definition['name'].title(), self.method, ','.join(self.parameterList))
        titleComment = '-- [Function: {} {}]'.format( self.definition['name'].title(), self.method)

        methodComment = ''


        if self.method == 'DELETE':
            methodComment = \
            '''-- [Description: Remove a {} from the table]
            -- [Parameters: {}]
            -- [Delete by primary key]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'PUT':
            methodComment = \
            '''-- [Description: Change the values of a {} chelate]
            -- [Parameters: {}]
            -- [Update by primary key]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'POST':
            methodComment = \
            '''-- [Description: Store the original values of a {} chelate]
            -- [Parameters: {}]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'GET':
            methodComment = \
            '''-- [Description: Find the values of a {} chelate]
            -- [Parameters: {}]'''\
                .format(self.definition['name'],','.join(self.parameterList))

        rc = \
        '''BEGIN
          {}
          {}'''.format(titleComment,methodComment)


        #print('linify',rc.split('\n'))
        # self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def switchToRole(self, role):

        rc = '''
          -- [Switch to {} Role]
          set role {}; '''.format(role, role)
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def validateParameters(self):
        #for param in self.definition['param eters']:

        #for param in self.definition['parameters'][self.method]:
        for param in self.getMethods('parameters')[self.method]:

            if param == 'token':
                self.validateToken()
            elif param == 'form':
                self.validateForm()
            elif param == 'options':
                self.validateOptions()
            elif param == 'criteria':
                self.validateCriteria()
            elif param == 'pk':
                self.validatePk()
            else:
                print('uk param', param)

        return self

    def validatePk(self):

        rc = '''
          -- [Validate pk parameter]
          if pk is NULL then
              RESET ROLE;
              -- [Fail 400 when pk is NULL]
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])


    def validateToken(self):
        tokenRole = self.definition['tokenRole']
        rc = '''
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format({},CURRENT_USER)::JSONB;
          end if;'''.format('\'{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}\'')

        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        scopeVerificationList = []
        keyVerificationList =[]
        #if self.method == 'POST':
            #scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
            #                         self.getPrivilegesByRole() if 'C' in self.getPrivilegesByRole()[role].upper() ]
            # make list of roles with permission to execute
            # e.g., if not(result ->> 'scope' = 'api_guest') and not(result ->> 'scope' = 'api_guest') then

        #elif self.method == 'GET':
            #scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
            #                         self.getPrivilegesByRole() if 'R' in self.getPrivilegesByRole()[role].upper()]
         #   scopeVerificationList = [ 'not(result ->> \'scope\' = \'{}\')'.format(role) for role in self.definition['roles'] if self.method in self.definition['roles'][role]['execute'] ]

        #elif self.method == 'PUT':
        #    scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
        #                             self.getPrivilegesByRole() if 'U' in self.getPrivilegesByRole()[role].upper()]

        #elif self.method == 'DELETE':
        #    scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
        #                             self.getPrivilegesByRole() if 'D' in self.getPrivilegesByRole()[role].upper()]

        scopeVerificationList = [ 'not(result ->> \'scope\' = \'{}\')'.format(role) for role in self.definition['roles'] if self.method in self.definition['roles'][role]['execute'] ]

        rc = '''
          -- [Verify token has expected scope]
          if {} then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{}'::JSONB;
          end if; '''.format(' and '.join(scopeVerificationList), '{"status":"401","msg":"Unauthorized"}')

        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        if len(keyVerificationList):
            rc = '''
             -- [Verify token has expected key]
             if {} then
                  RESET ROLE;
                  -- [Fail 401 when unexpected key is detected]
                  return '{}'::JSONB;
             end if;'''.format(' and '.join(keyVerificationList), '{"status":"401","msg":"Unauthorized"}')
            #self.append(rc)
            #self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self


    def validateForm(self):
        #method=self.definition['method']
        perm = 'C'

        if self.method == 'PUT':
            perm = 'U'
        form=self.definition['chelate']['form']
        required = ['not(_form ? \'{}\')'.format(nm) for nm in form if perm in form[nm]['input']]
        # optional = ['_form ? \'{}\' and not(\'{}\')'.format(nm, nm) for nm in form if 'c' in form[nm]['input']]

        rc = \
          '''
                    -- [Validate form parameter] 
          if form is NULL then
              -- [Fail 400 when form is NULL]
              RESET ROLE;
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;    
          
          _form := form::JSONB; 
          '''
        self.extend([ln for ln in rc.split('\n') if ln.strip() != ''])
        if len(required) > 0:

            rc = \
          '''          -- [Validate Requred form fields]
          if {} then  
              -- [Fail 400 when form is missing requrired field]
              RESET ROLE;
              return {}::JSONB;
          end if;'''\
            .format(
                   ' or '.join(required),
                   '\'{"status":"400","msg":"Bad Request"}\''
                   )
            #self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        else:
            rc = \
          '''          -- [Validate Requred form fields]
          -- [No required {} form fields ]
            '''.format(self.method)
            #self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
            rc = \
          '''          -- [Validate optional form fields]
          -- [No optional {} form fields]
            '''.format(self.method)
            #self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        #self.append(rc)
        #self.extend(rc.split('\n'))

        return self
    def hashPassword(self):
        rc = '''
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB; 
        end if;  
        '''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

    #def hashPassword(self):
    #    if self.method == 'POST' or self.method == 'PUT':
    #        rc = '''
    #    -- [Hash Password x]
    #    if (_chelate ->> 'form')::JSONB ? '%k' then
    #            _form := (_chelate ->> 'form')::JSONB;
    #            _form := _form || format('{"password": "%s"}',crypt(form ->> '%k', gen_salt('bf')) )::JSONB;
    #            _chelate := _chelate || format('{"form": %s}',_form)::JSONB;
    #    end if;'''
    #        self.append(rc)

    def validateOptions(self):
        rc = '''
          -- Validate Options'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def validateCriteria(self):
        rc = '''
          -- Validate Criteria'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])


    def startDataAssembly(self):
        rc = '''
          -- [Data Assembly]'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def assembleDataHashPassword(self):
        rc = '''
          -- Hash Password is Off'''
        if self.method == 'POST' or self.method == 'PUT':
            rc = '''
              -- [Hash Password is On]'''
            #self.append(rc)
            #self.extend(rc.split('\n'))

        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def assembleData(self):
        rc = '''
          -- [Assemble Data]'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def function(self):
        method=self.definition['method']
        name= self.definition['name']

        rc = '''
          -- [API {} {} Function]
          TBD
          '''.format(method, name)

        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def end(self):
        rc = '''
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;'''
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self


    def grantFunction(self):
        # provides a statement of permissions
        schema=self.definition['schema']
        runAsRole=self.definition['runAsRole']
        parameters = self.definition['funcPattern'][self.method]
        '''
        rc = 'grant EXECUTE on FUNCTION {}.{} to {};' \
            .format(schema, self.definition['funcPattern'][self.method], runAsRole)

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        '''
        rc = 'grant EXECUTE on FUNCTION {}.{} ' \
            .format(schema, self.definition['funcPattern'][self.method])


        # METHOD
        lst = ['{} to {}; '.format(rc, role) for role in self.definition['roles']
            if 'execute' in self.definition['roles'][role] and self.method in self.definition['roles'][role]['execute']]

        if len(lst) > 0:
            #print('-- {}'.format(self.method))
            #print(lst)
            self.append('-- {}'.format(self.method))
            self.extend(lst)





        return self
    '''
        def grantFunction(self):
        # provides a statement of permissions
        schema=self.definition['schema']
        runAsRole=self.definition['runAsRole']
        
        rc = 'grant EXECUTE on FUNCTION {}.{} to {};' \
            .format(schema, self.definition['funcPattern'][self.method], runAsRole)

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self
    '''

    def toString(self):
        return '\n'.join(self)
'''
  _____          _   
 |  __ \        | |  
 | |__) |__  ___| |_ 
 |  ___/ _ \/ __| __|
 | |  | (_) \__ \ |_ 
 |_|   \___/|___/\__|
                     
                     

'''
class PostTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('POST',definition)

    '''
    def getKeys(self):
        #keys = self.definition['keys']
        c = self.definition['chelate']
        rc = '{"pk":"%p","sk":"%s","tk":"%t"}'
        if '#' not in c['pk']:
            rc = rc.replace('%p',c['pk'])
        else:
            rc = rc.replace('%p','TBD')

        if 'const#' in c['sk']:
            rc = rc.replace('%s',c['sk'])
        else:
            rc = rc.replace('%s','TBD')

        if 'guid' in c['tk']:
            rc = rc.replace('%t','*')
        else:
            rc = rc.replace('%t','TBD')

        return rc
    '''
    def getInsert(self, role, privileges):
        rc = '''             
              -- [Chelate Data]
              _chelate := base_0_0_1.chelate(\'{}\'::JSONB, _form); -- chelate with keys on insert
              -- [Stash guid for insert]
              tmp = set_config('request.jwt.claim.key', replace(_chelate ->> 'tk','guid#',''), true); 
              -- If is_local is true, the new value will only apply for the current transaction.
              --raise notice 'tmp %', tmp;'''\
            .format(self.getKeys())
        return rc

    def assembleData(self):
        rc = '''
        -- [Assemble Data]'''

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        self.hashPassword()

        rc = '          '
        self.append('        -- user specific stuff')

        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                  .format(role, self.getInsert(role, self.getPrivilegesByRole()[role]))
                  for role in self.definition['roles']
                      if self.method in self.definition['roles'][role]['execute']]

        rc += '           els'.join(lst)
        rc += '\n          end if;'

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']

        rc = '''
    
          -- [Insert {} Chelate]
          result := base_0_0_1.insert(_chelate);'''.format(name)
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self
'''
   _____      _   
  / ____|    | |  
 | |  __  ___| |_ 
 | | |_ |/ _ \ __|
 | |__| |  __/ |_ 
  \_____|\___|\__|
                  
'''



class GetTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('GET',definition)


    def getKey(self, value):
        # all upper are constants made up of const#value eg const#USER
        # lowercase are field names
        if '#' in value:
            return value.split('#')[0]
        return value

    def getValue(self, value):
        s = value.split('#')
        if s[0] == 'guid':
            return s[1]
        elif s[0] == 'const':
            return '\'{}\''.format(s[1])
        return 'criteria ->> {}'.format(value)

    def getQuery(self):
        rc = '''
             
              if _criteria ? 'pk' and _criteria ? 'sk' then
                  -- [Primary query {pk,sk}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk',_criteria ->> 'sk')::JSONB;
              elsif _criteria ? 'pk' and not(_criteria ? 'sk') then
                   -- [Primary query {pk,sk:*}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk','*')::JSONB;
              elsif _criteria ? 'sk' and _criteria ? 'tk' then
                  -- [Secondary query {sk,tk}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk',_criteria ->> 'tk')::JSONB;
              elsif _criteria ? 'sk' and not(_criteria ? 'tk') then
                  -- [Secondary query {sk,tk:*}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk','*')::JSONB;
              elsif _criteria ? 'xk' and _criteria ? 'yk' then
                  -- [Teriary query {tk,sk} aka {xk, yk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk',_criteria ->> 'yk')::JSONB;
              elsif _criteria ? 'xk' and not(_criteria ? 'yk') then
                  -- [Teriary query {tk} aka {xk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk','*')::JSONB;
              elsif _criteria ? 'yk' and _criteria ? 'zk' then
                  -- [Quaternary query {sk,pk} akd {yk,zk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk',_criteria ->> 'zk')::JSONB;
              elsif _criteria ? 'yk' and not(_criteria ? 'zk') then
                  -- [Quaternary query {yk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk','*')::JSONB;                
              end if;
        '''

        return rc

    def assembleData(self):
        self.append('          -- [Assemble user specific data]')
        rc = '          _criteria=criteria::JSONB;\n'
        rc += '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getQuery()) for role in self.getPrivilegesByRole() if self.definition['method']=='GET' and 'R' in self.getPrivilegesByRole()[role].upper() ]
        #lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getQuery()) for role in self.getPrivilegesByRole() if 'R' in self.getPrivilegesByRole()[role].upper() ]

        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                  .format(role, self.getQuery())
                  for role in self.definition['roles']
                      if self.method in self.definition['roles'][role]['execute']]

        rc += '           els'.join(lst)
        rc += '\n          end if;'
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.query(_criteria);'''.format(self.method, name)
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self



'''
  _____       _      _       
 |  __ \     | |    | |      
 | |  | | ___| | ___| |_ ___ 
 | |  | |/ _ \ |/ _ \ __/ _ \
 | |__| |  __/ |  __/ ||  __/
 |_____/ \___|_|\___|\__\___|
                             
'''

class DeleteTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('DELETE',definition)



    def getDelete(self):

        d = self.definition

        rc = '''
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:{} when undefined prefix]                
                _criteria := format('{}',pk)::JSONB;'''\
        .format(
            d['type'],
            '{"pk":"%s", "sk":"%k"}'.replace('%k', d['type']),
        )
        rc += '''
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:{}#<value> and sk:{} when <key># is not present]
                _criteria := format('{}',pk)::JSONB;              
              end if;
        '''.format(
                  d['chelate']['pk'],
                  d['type'],
                  '{"pk":"%k#%s", "sk":"%c"}'.replace('%k', d['chelate']['pk']).replace('%c', d['type'])
        )

        return rc

    def assembleData(self): #Delete
        self.append('          -- [Assemble user specific data]')
        #rc = '          _criteria=criteria::JSONB;\n'
        rc = '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete(role,self.definition['privileges'][role])) for role in self.definition['privileges'] if self.definition['method']=='DELETE' and self.definition['privileges'][role] ]

        #lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete())
        #       for role in self.getPrivilegesByRole()
        #       if 'D' in self.getPrivilegesByRole()[role].upper() ]

        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                  .format(role, self.getDelete())
                  for role in self.definition['roles']
                      if self.method in self.definition['roles'][role]['execute']]

        rc += '           els'.join(lst)
        rc += '\n          end if;'
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.delete(_criteria);'''.format(self.method, name)
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

'''
  _    _           _       _       
 | |  | |         | |     | |      
 | |  | |_ __   __| | __ _| |_ ___ 
 | |  | | '_ \ / _` |/ _` | __/ _ \
 | |__| | |_) | (_| | (_| | ||  __/
  \____/| .__/ \__,_|\__,_|\__\___|
        | |                        
        |_|                        

'''
class PutTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('PUT',definition)


    def getUpdate(self, role, privileges):
        d = self.definition

        rc = '''
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:{} when undefined prefix]      
                          
                _criteria := format('{}',pk)::JSONB;''' \
            .format(
            d['type'],
            '{"pk":"%s", "sk":"%k"}'.replace('%k', d['type']),
        )
        rc += '''
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:{}#<value> and sk:{} when <key># is not present]
                _criteria := format('{}',pk)::JSONB;              
              end if;
        '''.format(
            d['chelate']['pk'],
            d['type'],
            '{"pk":"%k#%s", "sk":"%c"}'.replace('%k', d['chelate']['pk']).replace('%c', d['type'])
        )
        rc += '''
              -- merget pk and sk
              _chelate := _chelate || _criteria;
              -- add the provided form
              _chelate := _chelate || format('{"form": %s}',_form)::JSONB; '''
        return rc
    def assebleDataByUser(self):
        self.append(' ')
        self.append('        -- [Assemble user specific data]')
        # rc = '          _criteria=criteria::JSONB;\n'
        rc = '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete(role,self.definition['privileges'][role])) for role in self.definition['privileges'] if self.definition['method']=='DELETE' and self.definition['privileges'][role] ]
        # privileges = self.getPrivilegesByRole()
        #lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,
        #                                                      self.getUpdate(role, self.getPrivilegesByRole()[role]))
        #       for role in self.getPrivilegesByRole()
        #       if 'U' in self.getPrivilegesByRole()[role].upper()]

        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                   .format(role, self.getUpdate(role, self.getPrivilegesByRole()[role]))
               for role in self.definition['roles']
               if self.method in self.definition['roles'][role]['execute']]

        rc += '           els'.join(lst)
        rc += '\n          end if;'
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])


    def assembleData(self):
        #rc = '''
        #_form := form::JSONB;
        #'''
        #self.append(rc)
        self.hashPassword()
        self.assebleDataByUser()

        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        #rc = ''''''
        if 'passwordHashOn' in self.definition and self.definition['passwordHashOn']:

            rc = '''
          -- [Hash password when found]
          if _form ? 'password' then
              --_form := (_chelate ->> 'form')::JSONB;
              _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB;
          end if;
            '''
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.update(_chelate);'''.format(self.method, name)
        #self.append(rc)
        #self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

'''
  _    _                 _ _           
 | |  | |               | | |          
 | |__| | __ _ _ __   __| | | ___ _ __ 
 |  __  |/ _` | '_ \ / _` | |/ _ \ '__|
 | |  | | (_| | | | | (_| | |  __/ |   
 |_|  |_|\__,_|_| |_|\__,_|_|\___|_|   
                                       
                                       
'''
'''
def warning():
    filename = __file__.split('/')
    filename = filename[len(filename)-1]
    rc = '-- This function was generated using {}'.format(filename)
    #self.append(rc)
    return rc
    #return rc.split('\n')
'''

def openApi(config_folder, file_type='source'):
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

    return ApiConfiguration(config_folder, config_filename).load()


'''
def openApiConfiguration(config_folder):
    # [Method: openApiConfiguration]
    # [Description: Load a Configuration File]
    # [Parameter: config_folder]
    root = tk.Tk()
    root.withdraw()
    # [Pick configuration file]
    file_path = filedialog.askopenfilename(initialdir=config_folder,
                                           filetypes=(("Text File", "*.config"), ("All Files", "*.*")),
                                           title="Choose a configuration file."
                                           )
    if len(file_path) == 0:
        print('* Stop')
        exit(0)

    config_filename = file_path.split('/')
    config_filename = config_filename[len(config_filename) - 1]
    #print('config_filename', config_filename)

    #print('file_path', file_path)
    # [Returns ApiConfiguration]

    return ApiConfiguration(config_folder, config_filename).load()
'''
def getEnvironment(environ):
    #if 'repo-source' == environ['kind']:
    if 'repo-source' == environ['kind'] or 'repo-target' == environ['kind']:

        # [Configure GIT folders]
        #pprint(environ)
        dev = GitDevelopment(environ['umbrella'],
                             environ['branch'],
                             environ['repo'],
                             environ['folders']).setup()
    elif 'relative-source' == environ['kind']:
        # [Configure relative folder]
        #print('environment', environ['kind'])
        dev = HomeDevelopment(environ['app-name']).setup()
    else:
        print('Stop..UNKNOWN Source')
        exit(0)
    return dev

def report(apiConfiguration, apiScriptFilename, homeDev, sourceDev, targetDev, backup={"original":None,"backup":None,"folder":None}):
    print('* Configuration')
    print('  - file   : {}'.format(apiScriptFilename))
    print('  - folder : {}'.format(homeDev.getFolder('config')))

    print('* Source')
    print('  - Repository folder: {}'.format(sourceDev.getFolder('repo')))
    print('  - Script file: {}'.format(apiScriptFilename))
    #print('  - Script folder: {}'.format(sourceDev.getDbFolder('sql')))
    print('  - Script folder: {}'.format(sourceDev.getFolder('scripts')))

    print('* Target')
    print('  - Repository folder: {}'.format(targetDev.getFolder('repo')))
    print('  - Script file: {}'.format(apiScriptFilename))
    print('  - Script backup  : {}'.format(backup['backup']))
    print('  - Script folder: {}'.format(targetDev.getFolder('scripts')))
    #print('  - Script folder: {}'.format(targetDev.getFolder('scripts')))

    # print('* Get Filename: {}'.format(apiScriptFilename))
    print('* Database')
    print('  - kind: {}'.format(apiConfiguration['database']['kind']))
    # print('  - target file: {}'.format(apiScriptFilename))
    print('  - sql folder: {}'.format(targetDev.getFolder('scripts')))
    #print('  - sql folder: {}'.format(targetDev.getFolder('scripts')))

    # print('* Backup ')

    print('  - original: {}'.format(backup['original']))
    print('  - backup  : {}'.format(backup['backup']))
    print('  - folder  : {}'.format(backup['folder']))


def process_to_one(apiConfiguration,sourceDev, targetDev, extention, outfileName):
    staticScriptDocument = Document(targetDev.getFolder('scripts'), outfileName)  # dont load
    fileList = Util().getFileList(sourceDev.getFolder('scripts'), extention)
    fileList.sort()
    for fileName in fileList:
        # [Load test files ending with .test.sql]
        print('- script: ', fileName)
        staticDocument = Document(sourceDev.getFolder('scripts'), fileName) \
            .load() \
            .replace('one_db', apiConfiguration['database']['name'])
        staticScriptDocument.extend(staticDocument)
    # [Backup a target script before overwriting]
    print('staticScriptDocument', staticScriptDocument)
    backup = Util().makeBackupFile(targetDev.getFolder('scripts'), staticScriptDocument.filename)
    # [Save all DB scripts into one file]
    staticScriptDocument.save()


def main():
    # [Generate API sql file]
    print('Generate API')
    print('  - load api configuration, generate funcPattern key and values')
    # get configuration file name {folder: "", name: ""}
    # get list of files of type .json in folder ./config

    # [Use a configuration file]
    config_folder = '{}'.format(os.getcwd().replace('database','config'))

    print('config_folder', config_folder)
    #apiConfiguration = openApiConfiguration(config_folder)
    # [Select API Source ]
    sourceConfiguration = openApi(config_folder,file_type="source")
    if not sourceConfiguration:
        print('cancel')
        exit(0)

    # [Select API Target ]
    targetConfiguration = openApi(config_folder,file_type="target")
    if not targetConfiguration:
        print('cancel')
        exit(0)
    # [Merge Source and Target]
    sourceConfiguration.update(targetConfiguration)
    apiConfiguration = sourceConfiguration
    #pprint(apiConfiguration)

    pageList = []

    pageList.append('\c {}'.format(apiConfiguration['database']['name']))
    pageList.append('SET search_path TO {};'.format(', '.join(apiConfiguration['database']['schema'])))

    # setup default environment
    homeDev = HomeDevelopment().setup()

    print('Home Development')
    print(homeDev.getFolder('config'))
    #pprint(homeDev)

    sourceDev = HomeDevelopment().setup()
    targetDev = HomeDevelopment().setup()

    # [Scan configuration for home, source, and target environment configurations]
    for apiName in apiConfiguration:
        if apiName == 'source':
            # [Configure input sources from GIT repositories]
            sourceDev = getEnvironment(apiConfiguration[apiName])

        elif apiName == 'target':
            # [Configure output targets from GIT repositories]
            targetDev = getEnvironment(apiConfiguration[apiName])


    print('  - home          : {}'.format(homeDev.getFolder('home')))
    #pprint(sourceDev)
    print('  - source [db]     : {}'.format(sourceDev.getFolder('db')))
    print('  - source [scripts]: {}'.format(sourceDev.getFolder('scripts')))
    print('  - target [db]     : {}'.format(targetDev.getFolder('db')))

    #pprint(targetDev)
    print('  - source [db]    : {}'.format(sourceDev.getFolder('db')))
    print('  - source [db_api]: {}'.format(sourceDev.getFolder('db_api')))
    print('  - target [db_api]: {}'.format(targetDev.getFolder('db_api')))
    #############
    # [Process multiple API Definitions]
    # skip api-static, database, source and target
    #############
    apiNameList = [nm for nm in apiConfiguration if apiConfiguration[nm]['kind'] == 'api-definition']

    for apiName in apiNameList:
        # avoid any non-api items

        apiScriptFilename = '{}.{}.{}.api.sql'.format(
            apiConfiguration[apiName]['prefix'],
            apiConfiguration[apiName]['schema'],
            apiConfiguration[apiName]['name'])

        # [Generate API Script]
        pageList.append('-- POST')
        # [Generate POST Function]
        pageList.extend(PostTemplate(apiConfiguration[apiName]))
        pageList.append('-- GET')
        # [Generate GET Function]
        pprint(apiConfiguration[apiName])
        pageList.extend(GetTemplate(apiConfiguration[apiName]))
        pageList.append('-- DELETE')
        # [Generate DELETE Function]
        pageList.extend(DeleteTemplate(apiConfiguration[apiName]))
        pageList.append('-- PUT')
        # [Generate PUT Function]
        pageList.extend(PutTemplate(apiConfiguration[apiName]))

        # [Assemble API (POST, GET, PUT, and Delete) Functions into single script]
        newDoc = Document(targetDev.getFolder('scripts'), apiScriptFilename).load(pageList)

        changed = True
        # [Dont overwrite exiting scripts]
        if Util().file_exists(targetDev.getFolder('scripts'),apiScriptFilename):
            # [Compare New Script to Old Script]
            oldDoc = Document(targetDev.getFolder('scripts'), apiScriptFilename).load()
            changed = newDoc.isDifferent(oldDoc)

        #report(apiConfiguration, apiScriptFilename, homeDev, sourceDev, targetDev)

        if changed :
            # [Write/Overwrite API script when new or when changes are detected]
            print('* Saving changes')
            print('   - Saving changes: {} API to {}/{}'.format(apiName.upper(), targetDev.getFolder('scripts'), apiScriptFilename))
            # [Backup script before overwriting]
            backup = Util().makeBackupFile(targetDev.getFolder('scripts'), apiScriptFilename)
            newDoc.write()
            report(apiConfiguration, apiScriptFilename, homeDev, sourceDev, targetDev, backup)

        else:
            # [Skip writing API script when NO changes detected]
            print('* No changes ... skipping {}'.format(apiScriptFilename))

    #############
    # [Process Static Scripts]
    #############
    # [Static scripts end with .static.sql]

    if not Util().confirm('* Install/Overwrite static scripts?','N'):
        print("writing static scripts")

        #############
        # [Process Static Database Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'db.sql','00.db.sql')

        #############
        # [Process Static Database Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'table.sql','10.base.table.sql')

        #############
        # [Process Base Function Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'base.function.sql','12.base.function.sql')

        #############
        # [Process Api Function Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'api.function.sql','20.api.function.sql')

        #############
        # [Process Static Data Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'data.sql','80.data.sql')

        #############
        # [Process Static Test Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'test.sql','90.test.sql')

        #############
        # [Process Static Cleaup Scripts]
        #############
        process_to_one(apiConfiguration, sourceDev, targetDev, 'cleanup.sql','98.test.cleanup.sql')

    ##############
    # [Process Postgres Extentions]
    ##############
    if not Util().confirm('* Install/Overwrite postgres configuration and extentions?','N'):
        print("  Overwriting postgres configuration and extentions")
        print('  - source ', sourceDev.getFolder('db'))
        print('  - target ', targetDev.getFolder('db'))
        # [Copy all files in extention/db folder]
        for fn in Util().getFileList(sourceDev.getFolder('db')):
            if Util().file_exists(targetDev.getFolder('db'),fn):
                #print('file exits')
                if not Util().confirm('  -- Overwrite {}?'.format(fn), 'N'):
                    #print('overwrite {}'.format(fn))
                    Util().copy(
                        '{}/{}'.format(sourceDev.getFolder('db'), fn),
                        '{}/{}'.format(targetDev.getFolder('db'), fn)
                    )
            else:
                print('  - copy', fn)
                Util().copy(
                    '{}/{}'.format(sourceDev.getFolder('db'),fn),
                    '{}/{}'.format(targetDev.getFolder('db'),fn)
                )

    ############
    # .env
    ###########
if __name__ == "__main__":
    main()
