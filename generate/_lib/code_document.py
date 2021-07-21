from lib.document import Document
import os
import sys
from pprint import pprint

class dep_CodeDocument(Document):
    def __init__(self, folder,filename):
        super().__init__(folder=folder, file_name=filename)
        self.data = {}

    def setConfiguration(self, configuration):
        self.data = configuration
        return self

    def load(self, lst=[]):
        self.clear()
        load_line = False
        if len(lst) == 0:
            with open('{}/{}'.format(self.folder, self.filename)) as file:
                data = file.readlines()
                for ln in data:
                    if '**/' in ln:
                        load_line = False

                    if load_line:
                        self.append(ln)

                    if '/**' in ln:
                        load_line = True
        else:
            for ln in lst:
                if '**/' in ln:
                    load_line = False
                if '/**' in ln:
                    load_line = True
                elif load_line:
                    self.append(ln)

        return self

    def executeBefore(self):
        #print('executeBefore 1')
        try:
            #print('A execBefore 1')
            exec(self.getBefore())
            #print('A execBefore 2', self.data)
        except NameError as err:
            print("NameError: {0}".format(err))
            raise("NameError: {0}".format(err))
        except KeyError as err:
            print("KeyError: {0}".format(err))
            raise("KeyError: {0}".format(err))
        except:
            print("Unexpected error:{} {}".format(sys.exc_info()[0],sys.exc_info()[1]))
            raise("Unexpected error:{} {}".format(sys.exc_info()[0],sys.exc_info()[1]))
        #print('A executeBefore out')
        return self

    def getBefore(self):
        #print('B getBefore 1')
        code = []
        load_line=False
        for ln in self:
            if 'def ' in ln:
                load_line = False
            if 'def before(' in ln:
                load_line = True
            if load_line:
                code.append(ln)

        #print('B getBefore 2')
        code.append("before(self.data)")
        #print('B getBefore 3', self.data)
        #pprint(self.data)
        #print('B getBefore out')
        return ''.join(code)

    def getAfter(self):
        code = []
        load_line = False
        for ln in self:
            #code.append(ln)

            if 'def ' in ln:
                load_line = False
            if 'def after' in ln:
                load_line = True
            if load_line:
                code.append(ln)

        return ' '.join(code)

def main():
    import os
    #from lib.post_template import PostTemplate
    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest

    #apiName = 'user'
    print('Source===============================')
    configuration = ConfigurationSourceTest()
    print('Target================================')
    configuration = configuration.update(ConfigurationTargetTest())
    template = CodeDocument('../templates', "user.post.sql.template")\
        .setConfiguration(configuration)\
        .load()
    print('Execute ================================')
    template.executeBefore()

    assert('_tasks' in template.data['user'])
    assert ({} != template.data['user']['_tasks'])

    assert('funcPattern' in template.data['user']['methods']['POST'])
    assert('user(TEXT,JSON)' in template.data['user']['methods']['POST']['funcPattern'])

    assert('grant' in template.data['user']['methods']['POST'])
    assert('grant EXECUTE on FUNCTION' in template.data['user']['methods']['POST']['grant'])


    assert('POST-scope-verification-condition' not in template.data['user'])
    #assert('not(' in template.data['user']['POST-scope-verification-condition'])

    assert('scope-verification-condition' in template.data['user']['methods']['POST'])
    assert('not(' in template.data['user']['methods']['POST']['scope-verification-condition'])

    assert('POST-form-required-field-condition' not in template.data['user'])
    #assert('not(_form ?' in template.data['user']['POST-form-required-field-condition'])

    assert('requiredFieldCondition' in template.data['user']['methods']['POST'])
    assert('not(_form ?' in template.data['user']['methods']['POST']['requiredFieldCondition'])

    assert('passwordHashField' in template.data['user']['methods']['POST'])
    assert(False != template.data['user']['methods']['POST']['passwordHashField'] and '' != template.data['user']['methods']['POST']['passwordHashField'])

    assert('customRoleCode' in template.data['user']['methods']['POST'])


    #assert('passwordHashField' in template.data['user']['methods']['POST'])

    #pprint(template.data)
    #pprint(configuration.conatants())
    print('=======')
    pprint(configuration.constants(parent=configuration['user']))    #codeDoc = Code('../templates', "user.post.sql.template").load()
    #codeDoc.execute()

    #code = Code().execute()


if __name__ == "__main__":
    main()

