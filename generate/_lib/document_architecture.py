from lib.document import Document
from lib.api_configuration import ApiConfiguration
import datetime
from pprint import pprint

class ArchitectureDocument(Document):
    def __init__(self, configuration, folder='', filename=''):
        super().__init__(folder, filename)
        self.configuration = configuration
        #self.configuration = ApiConfiguration()
        #self.sourceConfiguration=None
        #self.targetConfiguration=None

    def setConfiguration(self, configuration):
        if configuration != None:
            self.configuration = configuration
        return self
    def source(self):
        return self['source']
    def target(self):
        return self['target']

    '''    
    def setSource(self, sourceConfiguration):
        if sourceConfiguration != None:
            self.sourceConfiguration=sourceConfiguration
        return self

    def setTarget(self, targetConfiguration):
        self.targetConfiguration = targetConfiguration
        return self
    '''
    def getUI(self, method):
        if method == 'POST':
            return 'Create'
        if method == 'GET':
            return 'Read'
        if method == 'PUT':
            return 'Update'
        if method == 'DELETE':
            return 'Delete'
        return "undefined"

    def getParameterNames(self,methods, method):
        rc = []
        # [<param-name>, <param-name>, ...]
        for p in methods[method]:
            rc.append(p)
        return ', '.join(rc)

    def getParameterTypes(self, methods, method):
        rc = []
        # for p in apiDef['parameters'][method]:
        #        rc.append(apiDef['parameters'][method][p])
        for p in methods[method]:
            rc.append(methods[method][p])
        return ', '.join(rc)

    def getHeaderNames(self,methods, method):
        rc = []
        # [<header-name>, <header-name>, ...]
        for p in methods[method]:
            rc.append(p)
        return ', '.join(rc)

    def getBaseFunction(self, method):
        if method == 'POST':
            return 'insert(chelate)'
        if method == 'GET':
            return 'query(chelate)'
        if method == 'PUT':
            return 'update(chelate)'
        if method == 'DELETE':
            return 'delete(chelate)'
        return "undefined"

    def getTable(self, database, method):
        rc = database['table']['name']
        return rc

    def build(self):

        # [Merge Source and Target]
        #configuration = ApiConfiguration()
        #self.configuration.update(self.sourceConfiguration)
        #self.configuration.update(self.targetConfiguration)

        pprint(self.configuration)
        # [Make a list of APIs]
        print('names',[nm for nm in self.configuration])
        apiNameList = [nm for nm in self.configuration
                       if self.configuration[nm]['kind'] == 'api-definition'
                       or self.configuration[nm]['kind'] == 'api-static']
        print('apiNameList',apiNameList)

        # [Give document a Title]
        self.append('# API Architectures')
        self.append('Date: {}'.format(datetime.datetime.now()))
        self.append('Sources:')

        #if self.sourceConfiguration.filename != '':
        #    self.append('* {}'.format(self.sourceConfiguration.filename))
        #if self.targetConfiguration.filename != '':
        #    self.append('* {}'.format(self.targetConfiguration.filename))

        for apiName in apiNameList:
            # apiMdFilename = '{}.{}.{}.api.architecture.md'.format(
            #    apiConfiguration[apiName]['prefix'],
            #    apiConfiguration[apiName]['schema'],
            #    apiConfiguration[apiName]['name'])
            # print('apiScriptFilename ', apiMdFilename)
            self.append(' ')

            self.append('## {}'.format(apiName))
            arch = []
            arch.append('| {} |'.format(' | '.join(['', '', '', '', ''])))
            arch.append('| {} |'.format(' | '.join([' - ', ' - ', ' - ', ' - ', ' - '])))

            uiList = ['UI']

            uiList.extend(['{}'.format(self.getUI(m)) for m in self.configuration.getMethods(apiName, 'parameters')])

            arch.append('| {} |'.format(' | '.join(uiList)))

            httpList = ['HTTP']

            httpList.extend(['{}'.format(m) for m in self.configuration.getMethods(apiName, 'parameters')])

            arch.append('| {} |'.format(' | '.join(httpList)))
            # [ROUTES Line]
            routeList = ['Routes']
            routeList.extend(['/{}'.format(apiName) for m in self.configuration.getMethods(apiName, 'parameters')])
            arch.append('| {} |'.format(' | '.join(routeList)))
            # [DB CLIENT Line]
            dbClientList = ['Db Client']
            dbClientList.extend(['pg.query( {}({}) )'.format(apiName, self.getParameterNames(
                self.configuration.getMethods(apiName, 'parameters'), m)) for m in
                                 self.configuration.getMethods(apiName, 'parameters')])

            arch.append('| {} |'.format(' | '.join(dbClientList)))
            schema = self.configuration[apiName]['schema']

            # [API SQL FUNCTION Line]
            apiSqlList = ['API SQL Function']
            apiSqlList.extend(['{}.{}({})'.format(schema, apiName,
                                                  self.getParameterTypes(self.configuration.getMethods(apiName, 'parameters'),
                                                                    m)) for m in
                               self.configuration.getMethods(apiName, 'parameters')])
            arch.append('| {} |'.format(' | '.join(apiSqlList)))

            # [STATIC BASE FUNCTION Line]
            staticBaseList = ['Static Base Function']
            staticBaseList.extend(['{}.{}'.format('base_0_0_1', self.getBaseFunction(m)) for m in
                                   self.configuration.getMethods(apiName, 'parameters')])
            arch.append('| {} |'.format(' | '.join(staticBaseList)))

            # [Table Line]
            tableList = ['Table']
            database = self.configuration['_tasks']
            tableList.extend(
                ['{}'.format(self.getTable(database, m)) for m in self.configuration.getMethods(apiName, 'parameters')])
            arch.append('| {} |'.format(' | '.join(tableList)))

            #pprint(arch)
            self.append(" ")
            self.extend(arch)

        return self

def main():
    from pprint import pprint
    from lib.configuration_tests import ConfigurationSourceTest
    from lib.configuration_tests import ConfigurationTargetTest
    print(ConfigurationTargetTest())
    print(ConfigurationSourceTest())
    print(ConfigurationSourceTest().update(ConfigurationTargetTest()))

    config = ConfigurationSourceTest().update(ConfigurationTargetTest())
    print(config)
    architectureDocument = ArchitectureDocument(config)
    #architectureDocument.setConfiguration(config)
    #architectureDocument.setSource(ConfigurationSourceTest())

    #architectureDocument.setSource(ConfigurationSourceTest())
    #architectureDocument.setTarget(ConfigurationTargetTest())
    architectureDocument.build()
    #architectureDocument.save()
    pprint(architectureDocument)

if __name__ == "__main__":
    main()
