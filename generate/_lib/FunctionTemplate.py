
#class dep-Template():
#    def __init__(self):
#        print(''hi)


class dep_FunctionTemplate(list):
    def __init__(self, api_name, method, apiConfiguration):
        # convert to Postgres API Script
        # definition is a single function definition
        self.api_name = api_name
        self.method = method
        #self.definition = apiDefinition
        self.apiConfig = apiConfiguration
        # self.parameterList = ['{} {}'.format(param,self.definition['par ameters'][param]) for param in self.definition['pa rameters']]
        self.parameterList = None
        self.privileges =None
        self.tokenClaims =None

        # formatting
        self.nameFunction()      # Create or Replace Function
        self.declareVariables()  # Declare abc TEXT; ...
        self.begin()             # Begin plus function description comments
        # self.switchToRole(self.definition['runAsRole'])
        self.switchToRole(self.apiConfig[self.api_name]['runAsRole'])

        self.validateParameters()
        # self.startDataAssembly()
        # self.assembleDataHashPassword()
        self.assembleData()
        self.function()
        self.end()
        self.grantFunction()

    def getApiDef(self):
        return self.apiConfig[self.api_name]

    def getMethods(self, _type):
        #return self.apiConfig[self.api_name][_type]
        return self.apiConfig.getMethods(self.api_name, _type)
    '''
    getApiDef().getMethods(self.api_name, "header")
    getApiDef().getMethods(self.api_name, "parameters")
    getApiDef().getMethods(self.api_name, "privileges")



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
    '''
    def getParameterList(self):
        #return self.apiConfig.getParameterList(self.api_name)
        return ['{} {}'.format(param, self.getMethods('parameters')[self.method][param])
                                    for param in self.getMethods('parameters')[self.method]]

    '''
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

    # def getTokenByRole(self):
    #    if not self.tokenClaims:
    #        self.tokenClaims = {r: self.definition['roles'][r]['token'] for r in self.definition['roles']}
    #    return self.tokenClaims

    def getPrivilegesByRole(self):
        if not self.privileges:
            self.privileges = {r: self.getApiDef()['roles'][r]['privileges'] for r in self.getApiDef()['roles']}
        return self.privileges

    def getKeys(self):
        # keys = self.getApiDef()['keys']
        c = self.getApiDef()['chelate']
        rc = '{"pk":"%p","sk":"%s","tk":"%t"}'
        if '#' not in c['pk']:
            rc = rc.replace('%p' ,c['pk'])
        else:
            rc = rc.replace('%p' ,'TBD')

        if 'const#' in c['sk']:
            rc = rc.replace('%s' ,c['sk'])
        else:
            rc = rc.replace('%s' ,'TBD')

        if 'guid' in c['tk']:
            rc = rc.replace('%t' ,'*')
        else:
            rc = rc.replace('%t' ,'TBD')
        return rc

    # def warning(self):
    #    filename = __file__.split('/')
    #    filename = filename[len(filename)-1]
    #    rc = '''
    #    -- This function was generated using {}
    #    '''.format(filename)
    #    #self.append(rc)
    #    return rc

    def nameFunction(self):
        # pprint(self.getApiDef())
        schema = self.getApiDef()['schema']
        # param eters = ['{} {}'.format(param,self.getApiDef()['par ameters'][param]) for param in self.getApiDef()['pa rameters']]
        name = self.getApiDef()['name']
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
        # titleComment = '-- [Function: {} {} given {}]'.format( self.getApiDef()['name'].title(), self.method, ','.join(self.parameterList))
        titleComment = '-- [Function: {} {}]'.format( self.getApiDef()['name'].title(), self.method)

        methodComment = ''


        if self.method == 'DELETE':
            methodComment = \
                '''-- [Description: Remove a {} from the table]
                -- [Parameters: {}]
                -- [Delete by primary key]
                -- [pk is <text-value> or guid#<value>''' \
                    .format(self.getApiDef()['name'] ,','.join(self.self.getParameterList()))
        elif self.method == 'PUT':
            methodComment = \
                '''-- [Description: Change the values of a {} chelate]
                -- [Parameters: {}]
                -- [Update by primary key]
                -- [pk is <text-value> or guid#<value>''' \
                    .format(self.getApiDef()['name'] ,','.join(self.self.getParameterList()))
        elif self.method == 'POST':
            methodComment = \
                '''-- [Description: Store the original values of a {} chelate]
                -- [Parameters: {}]
                -- [pk is <text-value> or guid#<value>''' \
                    .format(self.getApiDef()['name'] ,','.join(self.getParameterList()))
        elif self.method == 'GET':
            methodComment = \
                '''-- [Description: Find the values of a {} chelate]
                -- [Parameters: {}]''' \
                    .format(self.getApiDef()['name'] ,','.join(self.self.getParameterList()))

        rc = \
            '''BEGIN
              {}
              {}'''.format(titleComment ,methodComment)

        # print('linify',rc.split('\n'))
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def switchToRole(self, role):

        rc = '''
          -- [Switch to {} Role]
          set role {}; '''.format(role, role)
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def validateParameters(self):

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
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])


    def validateToken(self):
        tokenRole = self.getApiDef()['tokenRole']
        rc = '''
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format({},CURRENT_USER)::JSONB;
          end if;'''.format('\'{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}\'')

        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        scopeVerificationList = []
        keyVerificationList =[]

        scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in self.getApiDef()['roles']
                                 if self.method in self.getApiDef()['roles'][role]['execute']]

        rc = '''
          -- [Verify token has expected scope]
          if {} then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{}'::JSONB;
          end if; '''.format(' and '.join(scopeVerificationList), '{"status":"401","msg":"Unauthorized"}')

        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        if len(keyVerificationList):
            rc = '''
             -- [Verify token has expected key]
             if {} then
                  RESET ROLE;
                  -- [Fail 401 when unexpected key is detected]
                  return '{}'::JSONB;
             end if;'''.format(' and '.join(keyVerificationList), '{"status":"401","msg":"Unauthorized"}')
            # self.append(rc)
            # self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def validateForm(self):
        perm = 'C'

        if self.method == 'PUT':
            perm = 'U'
        form = self.getApiDef()['chelate']['form']
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
                end if;''' \
                    .format(
                    ' or '.join(required),
                    '\'{"status":"400","msg":"Bad Request"}\''
                )
            # self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        else:
            rc = \
                '''          -- [Validate Requred form fields]
                -- [No required {} form fields ]
                  '''.format(self.method)
            # self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
            rc = \
                '''          -- [Validate optional form fields]
                -- [No optional {} form fields]
                  '''.format(self.method)
            # self.extend(rc.split('\n'))
            self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        # self.append(rc)
        # self.extend(rc.split('\n'))

        return self

    def hashPassword(self):
        rc = '''
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB; 
        end if;  
        '''
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

    # def hashPassword(self):
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
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def validateCriteria(self):
        rc = '''
          -- Validate Criteria'''
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

    def startDataAssembly(self):
        rc = '''
          -- [Data Assembly]'''
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        return self

    def assembleDataHashPassword(self):
        rc = '''
          -- Hash Password is Off'''
        if self.method == 'POST' or self.method == 'PUT':
            rc = '''
              -- [Hash Password is On]'''
            # self.append(rc)
            # self.extend(rc.split('\n'))

        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def assembleData(self):
        rc = '''
          -- [Assemble Data] Overload Me'''
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def function(self):
        #method = self.getApiDef()['method']
        name = self.getApiDef()['name']

        rc = '''
          -- [API {} {} Function]
          TBD
          '''.format(self.method, name)

        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def end(self):
        rc = '''
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;'''
        # self.append(rc)
        # self.extend(rc.split('\n'))
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self

    def grantFunction(self):
        # provides a statement of permissions
        schema = self.getApiDef()['schema']
        runAsRole = self.getApiDef()['runAsRole']
        parameters = self.getApiDef()['funcPattern'][self.method]
        '''
        rc = 'grant EXECUTE on FUNCTION {}.{} to {};' \
            .format(schema, self.getApiDef()['funcPattern'][self.method], runAsRole)

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        '''
        rc = 'grant EXECUTE on FUNCTION {}.{} ' \
            .format(schema, self.getApiDef()['funcPattern'][self.method])

        # METHOD
        lst = ['{} to {}; '.format(rc, role) for role in self.getApiDef()['roles']
               if
               'execute' in self.getApiDef()['roles'][role] and self.method in self.getApiDef()['roles'][role]['execute']]

        if len(lst) > 0:
            # print('-- {}'.format(self.method))
            # print(lst)
            self.append('-- {}'.format(self.method))
            self.extend(lst)

        return self

    '''
        def grantFunction(self):
        # provides a statement of permissions
        schema=self.getApiDef()['schema']
        runAsRole=self.getApiDef()['runAsRole']

        rc = 'grant EXECUTE on FUNCTION {}.{} to {};' \
            .format(schema, self.getApiDef()['funcPattern'][self.method], runAsRole)

        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return self
    '''

    def toString(self):
        return '\n'.join(self)


def main():
    from pprint import pprint

    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest

    configurationSourceTest = ConfigurationSourceTest().update(ConfigurationTargetTest())

    functionTemplate = FunctionTemplate("user","POST",configurationSourceTest)
    pprint(functionTemplate)


if __name__ == "__main__":
    main()