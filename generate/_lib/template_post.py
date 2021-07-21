from lib.template import Template

class PostTemplate(Template):

    def __init__(self,api_name, folder='',filename=''):
        super().__init__(folder=folder,filename=filename)
        self.setMethod("POST")
        self.setApiName(api_name)
        self.load()
        self.sampleParameters ={"parameters": {
                    "token":{"name":"token","type":"TEXT"},
                    "form":{"name":"testForm","type":"JSON"}
                }
        }

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
    #pprint(configuration)
    #pprint(configuration.constants(parent=configuration['user']))
    print('Prototype=============================')
    #prototype = Document('../prototypes/','user.post.sql').load()
    #pprint(prototype)
    print('A ========================================')
    print('PostTemplate')
    apiName = 'user'
    template = PostTemplate(apiName,folder='../templates',filename='post.sql.template')\
                    .validate(configuration)\
                    .apply(configuration)

    #print(template.toString())

    #template.showDifferent(prototype)


if __name__ == "__main__":
    main()