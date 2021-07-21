from lib.development import Development
from lib.guess import BranchFolderGuess

class GitDevelopment(Development):
    # [Git Development Repository]
    # [Description: Define and imput repository source folders]
    def __init__(self, group, branch, project, folders):
        super().__init__()
        # [Define repository path]
        self['group_name'] = group   # 01-app
        # [Impute group_folder]
        self['group_folder'] = '{}/{}'.format(self.getDevelopmentFolder(), self['group_name'])
        #self['branch_name'] = branch # #NN.desc
        self['branch_name'] = BranchFolderGuess()\
            .setParentFolder(self['group_folder'])\
            .setRepoName(project)\
            .guess(branch) # #NN.desc

        self['project_name'] = project # repo is same as home
        # [Define multiple folder configuration types]
        if type(folders) is str:
            print("unhandled string {}".format(folders))
        elif type(folders) is dict: # {}
            print("unhandled dict {}".format(folders))
        elif type(folders) is list: # {}
            # [Handle multiple repository folder types]
            for application in folders:
                if application['type'] == 'db':
                    # [Handle _tasks {type:db,name:<folder-name>}]
                    self['{}_name'.format(application['type'])] = application['name']
                elif application['type'] == 'db_api':
                    # [Handle _tasks API eg, {type:db_api, name:<folder-name>}]
                    self['{}_name'.format(application['type'])] = application['name']
                elif application['type'] == 'scripts':
                    # [Handle _tasks Scripts {type:scripts, name:<folder-name>}]
                    self['{}_name'.format(application['type'])] = application['name']
                elif application['type'] == 'sh-scripts':
                    # [Handle _tasks Scripts {type:sh-scripts, name:<folder-name>}]
                    self['{}_name'.format(application['type'])] = application['name']
                else:
                    # [Handle Undefined types]
                    print('Undefined app type {}', application['type'])
        # Impute group_folder]
        #self['group_folder'] = '{}/{}'.format(self.getDevelopmentFolder(), self['group_name'])
        # [Impute branch_folder from getDevelopmentFolder() and group_name]
        self['branch_folder'] = '{}/{}'.format(self['group_folder'], self['branch_name'])
        # [Impute group_folder from group_folder and branch_name]
        self['project_folder'] = '{}/{}'.format(self['branch_folder'], self['project_name'])
        # [Impute project_folder from branch_folder and repo_name]
        self['env_folder'] = '{}/{}'.format(self['branch_folder'], self['project_name'])
        if 'db_name' in self:
            # [Impute db_folder from repo_folder and db_name]
            self['db_folder']= '{}/{}'.format(self['project_folder'],self['db_name'])

        if 'scripts_name' in self:
            # [Impute scripts_folder from db_folder and scripts_name]
            self['scripts_folder'] = '{}/{}'.format(self['db_folder'],self['scripts_name'])

        if 'sh-scripts_name' in self:
            # [Impute scripts_folder from db_folder and scripts_name]
            self['sh-scripts_folder'] = '{}/{}'.format(self['project_folder'],self['sh-scripts_name'])

        if 'db_api_name' in self:
            # [Impute db_api_folder from repo_folder and ad_api_name]
            self['db_api_folder']= '{}/{}'.format(self['project_folder'],self['db_api_name'])

        #self['sql_folder']= '{}/{}'.format(self['db_folder'],'sql')

def main():
    from pprint import pprint
    # Target
    target = {
        "group": "00-samples",
        "branch": "#branch-delete-me",
        "project": "adopt-a-drain-nuxtjs",
        "folders":  [{"name":"aadDb",   "type":"db"},
                     {"name":"sql",      "type":"scripts"},
                     {"name":"aadDbApi", "type":"db_api"}]
    }

    gitDevelopment = GitDevelopment(
        target["group"], target["branch"], target["project"], target["folders"]
    ).setup()
    pprint(gitDevelopment)

if __name__ == "__main__":
    main()