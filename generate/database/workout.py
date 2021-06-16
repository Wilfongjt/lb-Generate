from lib.api_configuration import ApiConfiguration
from pprint import pprint




def main():
    from lib.configuration_tests import ConfigurationSourceTest

    # data = ApiConfiguration().load(_definitions=absoluteSys)
    data = ConfigurationSourceTest()
    #pprint(data)

    # want ['authorization=token', 'test=testForm']
    # have ['user']['methods]['POST']['headers'] {
    #                     "authorization":{"name":"token","type":"TEXT"},
    #                     "test":{"name":"testForm","type":"TEXT"}
    #                 }
    header_doc = ['{}={}'.format(y[0],y[1]['name']) for y in [x for x in data['user']['methods']['POST']['headers'].items()]]
    print(header_doc)

    # want ['authorization=token', 'test=testForm']
    # have ['user']['methods]['POST']['parameters'] {
    #                     "token":{"name":"token","type":"TEXT"},
    #                     "test":{"name":"testForm","type":"JSON"}
    #                 }
    param_doc = ['{}={}'.format(y[0],y[1]['name']) for y in [x for x in data['user']['methods']['POST']['parameters'].items()]]
    print(param_doc)

    # want ['TEXT', 'JSON']
    # have ['user']['methods]['POST']['parameters'] {
    #                     "token":{"name":"token","type":"TEXT"},
    #                     "test":{"name":"testForm","type":"JSON"}
    #                 }
    param_doc = ['{}'.format(y[1]['type']) for y in [x for x in data['user']['methods']['POST']['parameters'].items()]]
    print(param_doc)

    #want
    #{'DELETE': 'user(TEXT, TEXT)',
    # 'GET': 'user(TEXT, JSON, JSON)',
    # 'POST': 'user(TEXT, JSON)',
    # 'PUT': 'user(TEXT, TEXT, JSON)'}
    print('==== Grant Execute Functions by Method ====')

    methods = {}
    function_name = 'user'
    key = 'parameters'
    for m in data['user']['methods']:
        params = ['{}'.format(y[1]['type']) for y in [x for x in data[function_name]['methods'][m][key].items()]]
        params = ','.join(params)
        methods[m]='{}({})'.format(function_name,params)
    pprint(methods)

    # want not(_form ? 'username') or not(_form ? 'password')
    # have
    #print('Privileges')
    #methods = {}
    #function_name = 'user'
    #key = 'privileges'
    #for m in data[function_name]['methods']:
    #    #params = ['{}'.format(y[1]['type']) for y in [x for x in data[function_name]['methods'][m][key].items()]]
    #    privileges =  ['not(\'{}\')'.format(p) for p in [x for x in data[function_name]['methods'][m][key]]]
    #    privileges = ' or '.join(privileges)
    #    #print(privileges)
    #    methods[m]='{}'.format(privileges)
    #print(methods)




    print('==== Required Field Conditions ====')
    methods = {}
    function_name = 'user'
    o2m = {'C':"POST","R":"GET","U":"PUT","D":"DELETE"}
    for operation in ['C',"R","U","D"]:
        required = ['not(_form ? \'{}\')'.format(r) for r in[fld[0] for fld in data[function_name]['chelate']['form'].items() if operation in fld[1]['operations']]]
        methods[o2m[operation]] =  ' or '.join(required)
    pprint(methods)


    print('==== User Specific Conditions ====')
    methods = {}
    method = 'POST'
    function_name = 'user'
    key = 'roles'

    role_statements = 'el'.join(['if CURRENT_USER=\'{}\' then\n {}\n'.format(r, '\n'.join(t['template']))
                       for r, t in data[function_name]['methods'][method][key].items()])
    role_statements = role_statements.split('\n')
    pprint(role_statements)


    # want not(_form ? 'username') or not(_form ? 'password')
    # have
    print('==== Privileges ====')
    methods = {}
    function_name = 'user'
    key = 'roles'
    for m in data[function_name]['methods']:

        privileges =  ['not(\'{}\')'.format(p) for p in [x for x in data[function_name]['methods'][m][key]]]
        privileges = ' or '.join(privileges)
        methods[m]='{}'.format(privileges)
    print(methods)


    #want grant EXECUTE on FUNCTION api_0_0_1.user(TEXT,JSON)  to api_admin;
    #want    {'DELETE': ['grant EXECUTE on FUNCTION user(TEXT, TEXT) to [[roles]]'],
    #         'GET':    ['user(TEXT, JSON, JSON)'],
    #         'POST':   ['user(TEXT, JSON)'],
    #         'PUT':    ['user(TEXT, TEXT, JSON)']}
    print('==== Grant Execute Functions by Method and Role ====')
    print('==== replace [[data-methods-POST-grant-execute]]')
    methods = {}
    function_name = 'user'
    #function_execute_name = 'user'
    key = 'roles'
    key2 = 'parameters'

    for m in data[function_name]['methods']:
        print('m', m)
        # param-type, param-type
        param_types = ['{}'.format(y[1]['type']) for y in [x for x in data[function_name]['methods'][m][key2].items()]]
        param_types = ','.join(param_types)

        privileges =  ['grant EXECUTE on FUNCTION {}({}) to {}'.format(function_name,param_types,p) for p in [x for x in data[function_name]['methods'][m][key]]]
        privileges = '; '.join(privileges)
        methods[m] = '{}'.format(privileges)
    print(methods)

    print('==== Password Hash Field ====')

    method = 'POST'
    function_name = 'user'
    passwordHashField = 'password-hash-field'

    #passwordHashField = ' '.join(
    #                              [h[1]['name'] for h in data[function_name]['chelate']['form'].items()
    #                                               if h[1]['type']=='password']
    #                        )
    passwordHashField = [h[1]['name'] for h in data[function_name]['chelate']['form'].items()
                                              if h[1]['type']=='password' \
                                                  and ('C' in h[1]['operations'].upper()
                                                       or 'U' in h[1]['operations'].upper())]
    passwordHashField = ''.join(passwordHashField) or False
    print('passwordHashField')
    pprint(passwordHashField)
    exit(0)


    print('==== Custom Role Code ====')
    method='GET'
    roles='roles'
    code = ''
    #[[data-methods-POST-customRoleCode]]
    #for r in data[function_name]['methods'][method][roles]:
    #    code = ['{}'.format(c) for c in data[function_name]['methods'][method][roles][r]['template']]
    #    code = ' \n'.join(code) or False
    #data[function_name]['methods'][method]['customRoleCode'] = code

    #pprint(data[function_name]['methods'][method]['customRoleCode'])
    roleList = []
    for r in data[function_name]['methods'][method][roles]:
        code = ['    {}'.format(c) for c in data[function_name]['methods'][method][roles][r]['template']]
        code = '\n'.join(code)
        roleList.append('if CURRENT_USER == \'{}\' then\n    {}\n'.format(r,code) )
    print('el'.join(roleList) + '\n end if;')

if __name__ == "__main__":
    main()