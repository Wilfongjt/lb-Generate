from lib.template import Template
from lib.api_configuration import ApiConfiguration
from pprint import pprint

class ScriptTemplate(Template):

    def __init__(self,key_name, folder='',filename=''):
        super().__init__(folder=folder,filename=filename)
        #self.setMethod("DELETE")
        #self.setApiName(api_name)
        self.setKey(key_name)
        self.load()


    def apply(self, constants):
        if self.error:
            pprint(self.error)
            return self

        #self.setKey(key_name)
        #self.method = method
        #self.data = data
        # [Run Before Code]

        #self.beforeCode.applyConfiguration(self.api_name, self.method, self.data)
        #constants = data.flatten('database')
        #constants = self.getConstants()
        #_list = self.getLists()

        # Templatize
        #print('template constants')
        #pprint(constants)
        #print('===========')
        i = 0
        for ln in self:
            for key in constants:
                if type(constants[key]) is str:
                    ln = ln.replace('[[{}]]'.format(key), constants[key])
                elif type(constants[key]) is list:
                    #print('key', key, 'value', constants[key])
                    if len(constants[key])>0 and type(constants[key][0]) is str:
                        ln = ln.replace('[[{}]]'.format(key), '\n'.join(constants[key]))

            if '[[' in ln:
                # handle injected constants
                for key in constants:
                    if type(constants[key]) is str:
                        ln = ln.replace('[[{}]]'.format(key), constants[key])

                #print('line', ln)
            self[i]=ln

            i += 1

        return self


    #def validate(self, configuration):
    #    super().validate(configuration)
    #    if not self.error:
    #        if 'test' not in configuration[self.api_name][self.methods][self.method]:
    #            self.error = {"method": self.method, "error": "{} key not found".format('test')}
    #    return self

def main():
    import os
    from pprint import pprint

    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest
    from lib.document import Document

    # setup test configuration
    conf = {
        "source": {
            "kind": "repo-source",
            "umbrella": "01-lb-ab",
            "branch": "#1.init",
            "project": "lb-ab",
            "folders": [{"name": "lb-a", "type": "nuxtjs-app"},
                        {"name": "lb-b", "type": "nuxtjs-app"},
                        {"name": "lb-c", "type": "nuxtjs-app"},
                        {"name": "hapi-api", "type": "hapi-api"}
                        ]
        },
        "target": {
            "kind": "local-target",
            "umbrella": "00-Testing",
            "branch": ".",
            "project": "lb-ab",
            "folders": [{"name": "lb-a", "type": "nuxtjs-app"},
                        {"name": "lb-b", "type": "nuxtjs-app"},
                        {"name": "lb-c", "type": "nuxtjs-app"},
                        {"name": "hapi-api", "type": "hapi-api"}]
        }
    }
    configuration = ApiConfiguration().load(conf)
    pprint(configuration.constants(configuration['source']))
    #print('Source===============================')
    #configuration = ConfigurationSourceTest()
    #print('Target================================')
    #configuration = configuration.update(ConfigurationTargetTest())
    #pprint(configuration)
    #pprint(configuration.constants(parent=configuration['user']))
    #print('Prototype=============================')
    #prototype = Document('../prototypes/', 'user.delete.sql').load()
    #print('A ========================================')

    print('ScriptTemplate')

    keyName = 'lb-a'
    pprint(configuration)
    pprint(configuration.flatten())
    template = ScriptTemplate(keyName,folder='../templates',filename='heroku.create.app.template') \
        .apply(configuration.flatten())

    print(template.toString())
    print('===========')
    #pprint(configuration.flatten(keyName))


if __name__ == "__main__":
    main()