from lib.util import Util
import os
'''
+ python-scripts
+ Portfolio (..LittleBit)
    + code
        + Development
            + Umbrella
                + Branch
                    + Application
                        + api
                        + db
                    
                
    + Projects
        + System (lb-_documents)
            + Application
                + api
                + db
Development < Environment

GitDevelopment < Development < Environement
DocDevelopment < Development < Environement

'''

class Environment(dict):
    # [Environment]
    # [Extends: dict]
    # []
    def __init__(self):
        # [Define portfolio_name]
        self['portfolio_name'] = '..LyttleBit'
        # [Imput portfolios_folder]
        self['portfolio_folder']='{}/{}'.format(Util().getHomeFolder(),self['portfolio_name'])

    def setup(self):
        # [Method: setup]
        # [Description: Creates folders that do not already exist]
        for ln in self:

            if '_folder' in ln:
                #print('create folder', ln, self[ln])
                if not Util().folder_exists(self[ln]):
                    Util().createFolder(self[ln])
                    print('  - create folder: ', ln, self[ln] )
        return self

    def getGitIndex(self, folder=None):
        # [Method: gitGitIndex]
        # [Description: Get the position of the git folder in given path]
        rc = -1
        current_folder = os.getcwd()
        #print('Environment current_folder',current_folder )
        if not folder:
            split = current_folder.split('/')
        else:
            split = folder

        # walk up the path looking for .git folder

        i = len(split)
        for i in range(len(split)):
            if Util().folder_exists('{}/.git'.format('/'.join(split[0:i+1]))):
                #print('i', i , split[i], '/'.join(split[0:i+1]), '.git', Util().folder_exists('{}/.git'.format('/'.join(split[0:i+1]))) )
                rc = i

        if i == -1:
            raise Exception('No .git found in path')
        return rc

    #def get(self, key):
    #    if key not in self:
    #        return None
    #    return self[key]
    def getName(self, key):
        # [Method: Get imputed folder for defined key]
        # [eg: getFolder(')
        if '{}_name'.format(key) not in self:
            # print('not found ','{}_name'.format(key))
            return None
        return self['{}_name'.format(key) ]


    def getFolder(self, key):
        # [Method: Get imputed folder for defined key]
        # [eg: getFolder(')
        if '{}_folder'.format(key) not in self:
            #print('not found ','{}_folder'.format(key))
            return None
        return self['{}_folder'.format(key) ]

    def getPortfolioFolder(self):
        return self['portfolio_folder']




def main():
    from pprint import pprint
    development = Development()
    print('development')
    pprint(development)
    development.getGitIndex()
    '''
    environment = Environment().setup()
    development = Development().setup()
    gitDevelopment = GitDevelopment('01-lb-api','#10.postres','lb-api',api='hapi-api',db='one_db').setup()

    print('portfolio folder: ', environment.getPortfolioFolder())
    print('development folder: ', development.getDevelopmentFolder())
    print('git app folder', gitDevelopment.getAppFolder())
    print('git api folder', gitDevelopment.getApiFolder())
    print('git db folder', gitDevelopment.getDbFolder())
    print('repo folder', gitDevelopment.getRepoFolder())

    assert(Util().folder_exists(environment.getPortfolioFolder()))
    assert(Util().folder_exists(development.getDevelopmentFolder()))

    assert(Util().folder_exists(gitDevelopment.getAppFolder()))
    assert (Util().folder_exists(gitDevelopment.getApiFolder()))
    assert (Util().folder_exists(gitDevelopment.getApiFolder('lib')))
    assert (Util().folder_exists(gitDevelopment.getDbFolder()))
    assert (Util().folder_exists(gitDevelopment.getDbFolder('sql')))
    '''
    '''
    system = System('lb-doc-test','some_app')
    print('System', system)
    system.setup()
    print('portfolio folder: ', system.getPortfolioFolder())
    print('project folder:   ', system.getProjectsFolder())
    print('system folder:    ', system.getSystemFolder() )
    print('app folder:       ', system.getAppFolder())
    print('db folder:        ', system.getDbFolder())
    assert(Util().folder_exists(system.getAppFolder()))
    assert(Util().folder_exists(system.getDbFolder()))
    '''
    #docDev = DocDevelopment('app', api='api', db='db').setup()

    #homeDev = HomeDevelopment()
    #pprint(homeDev)

    #print('Config',homeDev.getConfigFolder())

    # Users/<user>/<portfolio>/<system>/<environment>/<group>/<branch>/<repo>/<sub-app>/

    #print('Group',homeDev.getGroupFolder())
    #print('Branch',homeDev.getBranchFolder())
    #print('Repo',homeDev.getRepoFolder())
    #print('Home',homeDev.getHomeFolder())
    #print('App',homeDev.getAppFolder())
    #print('Api',homeDev.getApiFolder())
    #print('Db',homeDev.getDbFolder())

    #assert(homeDev.getConfigFolder().endswith('lb-Generate/config') )
    #assert(homeDev.getGroupFolder().endswith('01-Generate') )
    #assert('#' in homeDev.getBranchFolder())
    #assert(homeDev.getRepoFolder().endswith('lb-Generate') )
    #assert(homeDev.getHomeFolder().endswith('lb-Generate') )
    #assert(homeDev.getAppFolder().endswith('examples/sample') )
    #assert(homeDev.getApiFolder().endswith('examples/sample/api') )
    #assert(homeDev.getDbFolder().endswith('examples/sample/_tasks') )
    '''
    gitDev = GitDevelopment('group', 'branch', 'project', 'app', api='api', db='db')
    gitDev.setup()
    pprint(gitDev)
    '''

    #gitDev = GitDevelopment('group', 'branch', 'project', folders=None)
    #gitDev = GitDevelopment('group', 'branch', 'project', folders='hi')
    #gitDev = GitDevelopment('group', 'branch', 'project', folders={"name":"my-db", "type":"db"})

    #gitDev = GitDevelopment('group', 'branch', 'project', folders=[{"name":"my-db","type":"db"},
    #                                                            {"name":"my-api","type":"db_api"},
    #                                                            {"name":"sql","type":"scripts"}])

    #pprint(gitDev)

if __name__ == "__main__":
    main()