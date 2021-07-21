from lib.template import Template

class TestTemplate(Template):
    def __init__(self,api_name, method, template_name, folder='../templates'):
        super().__init__(folder=folder, filename=template_name)
        self.setMethod(method.upper())
        self.setApiName(api_name)
        self.load()

    def apply(self, configuration):
        super().apply(self.api_name, self.method, configuration)
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
    pprint(configuration)
    print('===============================')

    print('constants')

    pprint(configuration.getConstants('user'))

    assert('test' in configuration['user']['methods']['DELETE'])
    #pprint(configuration.getConstants('user'))
    #pprint(configuration.getList('user'))
    assert('data-methods-DELETE-test-setup_script' in configuration.getConstants('user'))

    #pprint(configuration.constants(parent=configuration['user']))
    print('Prototype=============================')
    #prototype = Document('../prototypes/', 'user.delete.sql').load()
    print('A ========================================')

    print('DeleteTemplate')
    apiName = 'user'
    method = 'DELETE'
    template = TestTemplate(apiName, method, 'delete.test.sql.template')\
        .apply(configuration)

    #pprint(configuration)

    #template = DeleteTestTemplate(apiName,folder='../templates',filename='delete.sql.template')\
    #             .apply(configuration)

    print(template.toString())

    #template.showDifferent(prototype)

if __name__ == "__main__":
    main()