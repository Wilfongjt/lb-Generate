from lib.template import Template

class GetTemplate(Template):
    def __init__(self,def_name, folder='',filename=''):
        super().__init__(folder=folder,filename=filename)
        self.setMethod("GET")
        self.setApiName(def_name)
        self.load()
        self.sampleParameters = {
            "parameters": {
                "token": {"name": "token", "type": "TEXT"},
                "form": {"name": "form", "type": "JSON"},
                "options": {"name": "options", "type": "JSON"}
            }
        }

    def apply(self, configuration):
        super().apply(self.api_name, self.method, configuration)
        return self
    #def getCurrentUserStatement(self):
    #    function_name = self.api_def_name
    #    # [Assemble Custom Code into text]
    #    role_statements = 'el'.join(['if CURRENT_USER=\'{}\' then\n {}\n'.format(r, '\n'.join(t['template']))
    #                                 for r, t in self.apiConfig[function_name]['methods'][self.method]['roles'].items()])
    #    # [Disassembe Custom Code text into list]
    #    return role_statements

    #def assembleCode(self):
    #    rc = '''
    #    -- [Assemble Data]
    #    -- [Assemble User specific data]
    #    {}
    #    end if;
    #    '''.format(self.getCurrentUserStatement())
    #    return rc.split('\n')

def main():
    import os
    from pprint import pprint
    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest
    from lib.document import Document

    print('Source===============================')
    configuration = ConfigurationSourceTest()
    print('Target================================')
    configuration = configuration.update(ConfigurationTargetTest())
    #pprint(configuration)
    #pprint(configuration.constants(parent=configuration['user']))
    print('Prototype=============================')
    prototype = Document('../prototypes/','user.get.sql').load()
    #pprint(prototype)
    print('A ========================================')

    print('GetTemplate')

    template = GetTemplate('user',folder='../templates',filename='get.sql.template') \
        .validate(configuration) \
        .apply(configuration)
    #pprint(configuration)
    #pprint(configuration.constants(parent=configuration['user']))
    #print('-----')
    #print(template.toString())
    #print('-----')
    #template.showDifferent(prototype)

if __name__ == "__main__":
    main()