from lib.development import Development

class LocalDevelopment(Development):
    # [Local Development project]
    # [Description: Define and imput project source folders]
    def __init__(self, group, project, folders):
        super().__init__()
        # [Define project path]
        self['group_name'] = group   # 01-app
        #self['branch_name'] = branch # #NN.desc
        self['project_name'] = project # project is same as home
        # [Define multiple folder configuration types]
        if type(folders) is str:
            print("unhandled string {}".format(folders))
        elif type(folders) is dict: # {}
            print("unhandled dict {}".format(folders))
        elif type(folders) is list: # {}
            # [Handle multiple project folder types]
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
                else:
                    # [Handle Undefined types]
                    print('Undefined app type {}', application['type'])
        # [Impute group_folder]
        self['group_folder'] = '{}/{}'.format(self.getDevelopmentFolder(), self['group_name'])

        # [Impute group_folder from group_folder and branch_name]
        self['project_folder'] = '{}/{}'.format(self['group_folder'], self['project_name'])

        # [Impute project_folder from group_folder and project_name]
        self['env_folder'] = '{}/{}'.format(self['group_folder'], self['project_name'])
        if 'db_name' in self:

            # [Impute db_folder from project_folder and db_name]
            self['db_folder']= '{}/{}'.format(self['project_folder'],self['db_name'])

        if 'scripts_name' in self:

            # [Impute scripts_folder from db_folder and scripts_name]
            self['scripts_folder'] = '{}/{}'.format(self['db_folder'],self['scripts_name'])

        if 'db_api_name' in self:

            # [Impute db_api_folder from project_folder and ad_api_name]
            self['db_api_folder']= '{}/{}'.format(self['project_folder'],self['db_api_name'])

        #self['sql_folder']= '{}/{}'.format(self['db_folder'],'sql')

def main():
    from pprint import pprint
    # Target
    target = {
        "group": "00-samples",
        "project": "test-delete-me",
        "folders":  [{"name":"testDb",   "type":"db"},
                     {"name":"sql",      "type":"scripts"},
                     {"name":"testDbDpi", "type":"db_api"}]
    }

    localDevelopment = LocalDevelopment(
        target["group"], target["project"], target["folders"]
    ).setup()
    pprint(localDevelopment)

if __name__ == "__main__":
    main()