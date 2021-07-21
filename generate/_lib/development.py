from lib.system import Environment

class Development(Environment):
    # [Development]
    # [Description: Defines development source environment]
    # [Extends: Environment]
    # ..LyttleBit/code/Development/group/branch/app_name/db/sql
    def __init__(self):
        super().__init__()
        # [Define system_name]
        self['system_name'] = 'code'
        # [Define environment_name]
        self['environment_name'] = 'Development'
        # [Impute system_folder]
        self['system_folder']='{}/{}'.format(self.getPortfolioFolder(),self['system_name'])
        # [Impute development_folder]
        self['development_folder']='{}/{}'.format(self['system_folder'],self['environment_name'])

    def getSystemFolder(self):
        # [Method: getSystemFolder to return imputed system_folder]
        return self['system_folder']

    def getDevelopmentFolder(self):
        # [Method: getDevelopmentFolder to return imputed developement_folder]
        return self['development_folder']