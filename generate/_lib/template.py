from lib.document import Document
import os
import sys
from pprint import pprint

'''
x = template (folder, filename)
    load template (template and custom-code)
x = x.apply(apiDefinition)
        setConfiguration(apiDefinition)
        generate additional keys by running the custom-code
        for each line of template apply all custom-code keys 
'''

class Template(Document):
    def __init__(self, folder='', filename=''):
        super().__init__(folder,filename)
        self.error = False
        self.api_name = None # eg 'user'
        self.method = None # POST, GET, PUT, or DELETE
        self.methods = 'methods'
        self.data = None # entire configuration file contents
        self.beforeCode = self.BeforeCode()
        self.load()
        self.kind = 'api-definition || api-static'
        self.sampleHeaders = {"headers": {
                    "authorization":{"name":"token","type":"TEXT"},
                    "test":{"name":"testForm","type":"TEXT"}
                }}
        self.sampleParameters={}
        self.sampleRoles={
            "roles":{
                "api_user":{"template":["    -- custom code here"]}
            }
        }
        '''
        self.sampleChelate={
            "pk":"<pk-field-name>#<value> ",
            "sk": "const#<TYPE>",
            "tk": "<field-name>#<value> || guid#<value> || guid",
            "form": {
                "<pk-field-name>": {"name": "<pk_field_name>","type":"email | password | TEXT"},
                "<field-name1>": "<value1>",
                "<field-name2>": "<value2>"
            },
            "active": {"default": True},
            "created": {"default": "NOW()"},
            "updated": {"default": "NOW()"},
            "owner": {"default": "current_setting('request.jwt.claim.key')"}
        }
        '''
        self.sampleTest={}

    def setMethod(self, method):
        self.method = method
        return self

    def setKey(self, key_name):
        self.api_name = key_name
        return self

    def setApiName(self, api_name):
        #self.api_name = api_name
        self.setKey(api_name)
        return self

    def load(self):
        # load or reload file.template
        self.clear()

        with open('{}/{}'.format(self.folder,self.filename)) as file:
            data = file.readlines()
            load_template = False
            load_before_code = False
            for ln in data:
                #print('load ln', ln)
                if '</script>' in ln:
                    load_template = False
                    load_before_code = False

                if load_template:
                    self.append(ln)

                if load_before_code:
                    self.beforeCode.append(ln)

                if '<script "id":"template">' in ln:
                    load_template = True

                if '<script "id":"before-code">' in ln:
                    load_before_code = True

        return self

    def getConstants(self, api_name=None,data=None):
        if api_name:
            self.api_name = api_name
        if data:
            self.data = data
        print('====template data====')
        pprint(self.data)
        return self.data.constants(parent=self.data[self.api_name])
    '''
    def getLists(self,api_name=None,data=None):
        if api_name:
            self.api_name = api_name
        if data:
            self.data = data
        print('========= data ', type(self.data))
        pprint(self.data)
        return self.data.list(parent=self.data[self.api_name])
    '''


    #    def applyTemplate(self, api_name, method, data):
    def apply(self, key_name, method, data):
        if self.error:
            pprint(self.error)
            return self

        self.api_name = key_name
        self.method = method
        self.data = data
        # [Run Before Code]

        self.beforeCode.applyConfiguration(self.api_name, self.method, self.data)

        constants = self.getConstants()
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

    class BeforeCode(list):
        def __init__(self):
            self.data = []
            self.api_name = None
            self.method = None
            self.data = None

        def applyConfiguration(self, api_name, method, data):
            self.api_name = api_name
            self.method = method
            self.data = data
            self.execute()


        def getCode_(self):
            code = ''.join(self)
            return code
            #return code + 'before(self.data)'

        def execute(self):
            code=None
            try:
                code = self.getCode_()
                if len(code.strip()) > 0:
                    code += 'before(self.data)'
                    exec(code)
                else:
                    print('************ No code defined ****************')
            except NameError as err:
                print("NameError: {0}".format(err))
                raise Exception("NameError: {0}".format(err))
            except KeyError as err:
                print("KeyError: {0}".format(err))
                raise Exception("KeyError: {0}".format(err))
            except:
                print("Unexpected error:{} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                raise Exception("Unexpected error:{} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            return self


    def toString(self):
        return ' '.join(self)


    def validate(self,configuration):
        self.error = False
        # chelate
        if 'chelate' not in configuration:
            self.error = {"api_name": self.api_name, "method": self.method,
                          "error": "{} key not found".format('chelate')}
                          #"sample": self.sampleChelate}


        # methods
        if self.api_name not in configuration:
            self.error = {"api_name":self.api_name,"method":self.method, "error": "{} key not found".format(self.api_name)}
        elif 'methods' not in configuration[self.api_name]:
            self.error = {"api_name":self.api_name,"method":self.method, "error": "{} key not found".format(self.methods)}
        elif self.method not in configuration[self.api_name][self.methods]:
            self.error = {"api_name":self.api_name,"method": self.method, "error": "{} key not found".format(self.method)}
        elif 'headers' not in configuration[self.api_name][self.methods][self.method]:
            self.error = {"api_name":self.api_name,
                          "method": self.method,
                          "error": "{} key not found".format('headers'),
                          "sample": self.sampleHeaders
                         }
        elif 'parameters' not in configuration[self.api_name][self.methods][self.method]:
            self.error = {"api_name":self.api_name,
                          "method": self.method,
                          "error": "{} key not found".format('parameters'),
                          "sample": self.sampleParameters
                         }
        elif 'roles' not in configuration[self.api_name][self.methods][self.method]:
            self.error = {"api_name":self.api_name,
                          "method": self.method,
                          "error": "{} key not found".format('roles'),
                          "sample": self.sampleRoles
                         }
        return self


def main():
    import os
    from pprint import pprint
    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest

    # setup test configuration
    print('A ========================================')
    configuration = ConfigurationSourceTest()\
        .update(ConfigurationTargetTest())
    #pprint(configuration)
    print('B Open template ========================================')
    #template = Template('../templates','user.post.sql.template').load()
    template = Template('../templates','post.sql.template')

    #pprint(template)
    print('C getCode_ ========================================')

    #pprint(template.beforeCode.getCode_())
    assert('<script "id":"before-code">' not in template.beforeCode.getCode_())
    assert('</script>' not in template.beforeCode.getCode_())
    assert('before(self.data)' not in template.beforeCode.getCode_())

    print('D constants ========================================')
    #pprint(template.getConstants(api_name='user',data=configuration))

    print('E applyTemplate ========================================')
    template.apply('user','POST', configuration)

    #pprint(template.data)

    assert('_tasks' in template.data['user'])
    assert ({} != template.data['user']['_tasks'])

    assert ('funcPattern' in template.data['user']['methods']['POST'])
    assert ('user(TEXT,JSON)' in template.data['user']['methods']['POST']['funcPattern'])

    assert('grant' in template.data['user']['methods']['POST'])
    assert('grant EXECUTE on FUNCTION' in template.data['user']['methods']['POST']['grant'])

    assert('POST-scope-verification-condition' not in template.data['user'])
    #assert('not(' in template.data['user']['POST-scope-verification-condition'])

    assert('scopeVerificationCondition' in template.data['user']['methods']['POST'])
    assert('not(' in template.data['user']['methods']['POST']['scopeVerificationCondition'])

    assert('POST-requiredFieldCondition' not in template.data['user'])
    #assert('not(_form ?' in template.data['user']['POST-requiredFieldCondition'])

    assert('requiredFieldCondition' in template.data['user']['methods']['POST'])
    assert('not(_form ?' in template.data['user']['methods']['POST']['requiredFieldCondition'])

    assert('passwordHash' in template.data['user']['methods']['POST'])
    assert(False != template.data['user']['methods']['POST']['passwordHash'] and '' != template.data['user']['methods']['POST']['passwordHash'])

    assert('customRoleCode' in template.data['user']['methods']['POST'])

    #pprint(template)
    #print(template.toString())
if __name__ == "__main__":
    main()
