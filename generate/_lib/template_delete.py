from lib.template import Template

class DeleteTemplate(Template):

    def __init__(self,api_name, folder='',filename=''):
        super().__init__(folder=folder,filename=filename)
        self.setMethod("DELETE")
        self.setApiName(api_name)
        self.load()
        self.sampleParameters= {
            "parameters": {
                "token": {"name": "token", "type": "TEXT"},
                "key": {"name": "pk", "type": "TEXT"}
            }
        }

    def apply(self, configuration):
        super().apply(self.api_name, self.method, configuration)
        return self

    def validate(self, configuration):
        super().validate(configuration)
        if not self.error:
            if 'test' not in configuration[self.api_name][self.methods][self.method]:
                self.error = {"method": self.method, "error": "{} key not found".format('test')}
        return self

def main():
    import os
    from pprint import pprint

    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest
    from lib.document import Document

    # setup test configuration

    print('Source===============================')
    configuration = ConfigurationSourceTest()
    print('Target================================')
    configuration = configuration.update(ConfigurationTargetTest())
    #pprint(configuration)
    #pprint(configuration.constants(parent=configuration['user']))
    print('Prototype=============================')
    prototype = Document('../prototypes/', 'user.delete.sql').load()
    print('A ========================================')

    print('DeleteTemplate')
    apiName = 'user'
    template = DeleteTemplate(apiName,folder='../templates',filename='delete.sql.template') \
        .validate(configuration) \
        .apply(configuration)

    #print(template.toString())

    #template.showDifferent(prototype)

if __name__ == "__main__":
    main()