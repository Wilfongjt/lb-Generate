from lib.api_configuration import ApiConfiguration

class ConfigurationSourceTest(ApiConfiguration):
    def __init__(self, folder='../config', filename='example.user.json.source'):
        super().__init__(folder, filename)
        self.load()
    def save(self):
        print('not savable')
        return self

class ConfigurationTargetTest(ApiConfiguration):
    def __init__(self, folder='../config', filename='example.target'):
        super().__init__(folder, filename)
        self.load()

    def save(self):
        print('not savable')
        return self

def main():
    from pprint import pprint
    configurationSourceTest = ConfigurationSourceTest()
    print('======= configurationSourceTest')
    pprint(configurationSourceTest.getConstants('user'))
    # architectureDocument.save()
    #pprint(configurationSourceTest)

    #configurationSourceTest = ConfigurationSourceTest()
    #configurationSourceTest.update(ConfigurationTargetTest())
    #configurationSourceTest = ConfigurationSourceTest().update(ConfigurationTargetTest())

    #pprint(configurationSourceTest)

if __name__ == "__main__":
    main()