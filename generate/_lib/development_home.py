import os
from lib.development import Development

class HomeDevelopment(Development):
    def __init__(self):
        super().__init__()
        # for test, the cwd is in the /lib and for prod cwd will be the next folder up so remove /lib for consistancy
        # /Users/<user>/<portfolio>..LyttleBit/code/Development/<umbrella>/<branch>/<repo>
        # Users/<user>/<portfolio>/<system>/code/<environment>/<group>/<branch>/<repo>/<sub-app>/

        parts = os.getcwd().replace('/_documents','').replace('/_tasks','').replace('/lib','').split('/')
        #print('homeDev parts' , parts)
        git_index = self.getGitIndex()
        #print('parts', parts)
        self['config_name'] = 'config'
        self['group_name'] = parts[git_index-2]
        self['branch_name'] = parts[git_index-1]
        #self['group_name'] = parts[len(parts) - 4]
        #self['branch_name'] = parts[len(parts) - 3]

        self['examples_name']='examples'
        #self['repo_name'] = parts[len(parts)-2]
        #self['home_name'] = parts[len(parts)-2]
        self['repo_name'] = parts[git_index]
        self['home_name'] = parts[git_index]

        '''
        self['app_name'] = app_name
        self['api_name'] = 'api'
        self['db_name'] = '_tasks'
        '''
        self['group_folder']= '{}/{}'.format(self.getDevelopmentFolder(),self['group_name'])
        self['branch_folder']= '{}/{}'.format(self['group_folder'],self['branch_name'])
        self['repo_folder']= '{}/{}'.format(self['branch_folder'], self['repo_name'])
        self['env_folder']= '{}/{}'.format(self['branch_folder'], self['repo_name'])

        self['home_folder']= '{}/{}'.format(self['branch_folder'], self['home_name'])
        self['config_folder'] = '{}/generate/{}'.format(self['repo_folder'], self['config_name'])

        self['examples_folder']= '{}/generate/{}'.format(self['home_folder'],self['examples_name'])

        #for ap in [app for app in Util().getFolderList(self['repo_folder']) if '.git' not in app]:
        #    print('folder_naem', ap.replace('{}/'.format(self['repo_folder']),''))

        #for app in Util().getFolderList(self['repo_folder']):
        #    print('folder_naem', app.replace('{}/'.format(self['repo_folder']),''))



def main():
    from pprint import pprint
    # /Users/<user>/<portfolio>..LyttleBit/code/Development/<umbrella>/<branch>/<repo>
    # Users/<user>/<portfolio>/<system>/code/<environment>/<group>/<branch>/<repo>/<sub-app>/
    print('current folder', os.getcwd())
    homeDev = HomeDevelopment()
    # portfolia isnt testable accross multiple users

    assert(homeDev.getFolder('group').endswith('01-Generate'))
    assert(homeDev.getFolder('branch').endswith('#01.init'))
    assert(homeDev.getFolder('projecct').endswith('lb-Generate'))
    assert(homeDev.getFolder('config').endswith('lb-Generate/generate/config'))
    assert(homeDev.getFolder('examples').endswith('lb-Generate/generate/examples'))

if __name__ == "__main__":
    main()