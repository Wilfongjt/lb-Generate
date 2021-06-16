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

from lib.template import Template
from lib.template_post import PostTemplate
from lib.template_get import GetTemplate
from lib.template_put import PutTemplate
from lib.template_delete import DeleteTemplate


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



'''
           _____ _____ 
     /\   |  __ \_   _|
    /  \  | |__) || |  
   / /\ \ |  ___/ | |  
  / ____ \| |    _| |_ 
 /_/    \_\_|   |_____|

'''


'''
  _____          _   
 |  __ \        | |  
 | |__) |__  ___| |_ 
 |  ___/ _ \/ __| __|
 | |  | (_) \__ \ |_ 
 |_|   \___/|___/\__|
                     
                     

'''
class dep_PostTemplate(Template):
    def __init__(self,definition):
        super().__init__('POST',definition)

    def getCustomCodeTemplate(self, method_code):
        lst = super().getCustomCodeTemplate()
        lst.extend(self.assembleData())

        return lst

    def getInsert_(self, role, privileges):
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
        -- [Assemble Data]
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB;
        end if;
        if CURRENT_USER = [[data-POST-role]] then
        end if;
        '''
        '''
        # skip blank lines
        self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
        self.hashPassword()
        rc = '          '
        self.append('        -- user specific stuff')
        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                  .format(role, self.getInsert_(role, self.getPrivilegesByRole()[role]))
                  for role in self.definition['roles']
                      if self.method in self.definition['roles'][role]['execute']]
        rc += '           els'.join(lst)
        rc += '\n          end if;'
        '''
        #self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])

        return rc.split('\n')

    #def function(self):
    #    name = self.definition['name']
    #    rc = '''
    
    #      -- [Insert {} Chelate]
    #      result := base_0_0_1.insert(_chelate);'''.format(name)

    #    self.extend([ln for ln in rc.split('\n') if ln.strip() not in ''])
    #    return self
'''
   _____      _   
  / ____|    | |  
 | |  __  ___| |_ 
 | | |_ |/ _ \ __|
 | |__| |  __/ |_ 
  \_____|\___|\__|
                  
'''



class dep_GetTemplate(Template):
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

class dep_DeleteTemplate(Template):
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
class dep_PutTemplate(Template):
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
        pageList.extend(PostTemplate(apiName, folder='../templates', filename='post.sql.template') \
            .apply(apiConfiguration))
        #pageList.extend(PostTemplate(apiName, apiConfiguration))
        #pageList.extend(PostTemplate(apiConfiguration[apiName]))

        pageList.append('-- GET')
        # [Generate GET Function]
        pprint(apiConfiguration[apiName])
        pageList.extend(GetTemplate(apiName, folder='../templates', filename='get.sql.template')\
            .apply(apiConfiguration))
        #pageList.extend(GetTemplate(apiConfiguration[apiName]))

        pageList.append('-- DELETE')
        # [Generate DELETE Function]
        pageList.extend(DeleteTemplate(apiName, folder='../templates', filename='delete.sql.template')\
            .apply(apiConfiguration))

        pageList.append('-- PUT')
        # [Generate PUT Function]
        pageList.extend(PutTemplate(apiName, folder='../templates', filename='put.sql.template')\
            .apply(apiConfiguration))

        # [Assemble API (POST, GET, PUT, and Delete) Functions into single script]
        newDoc = Document(targetDev.getFolder('scripts'), apiScriptFilename).load(pageList)
        #pprint(newDoc)

        changed = True
        # [Dont overwrite existing scripts]
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
