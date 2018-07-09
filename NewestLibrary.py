#coding=utf-8
import json
import sys  # 导入sys模块，用于引入thrift生成的文件
import xlrd
reload(sys)
sys.setdefaultencoding('utf8')
#print os.path.abspath('..\\searchClient')
sys.path.append("../searchClient")
#sys.path.append(r'''E:\AutoTestInterface\search-service''')
from lib.Client import  Client
#from searchClient.lib.Client import Client
from xlwt import Style
from xlutils.copy import copy
sys.path.append('../gen-py')


class NewestLibrary(object):
    def __init__(self):
        self._result=''

    def get_dataTable(self,sheetName):
        data = xlrd.open_workbook(r'../testcases/case.xls')  # 读取excel
        table = data.sheet_by_name(sheetName)  # 通过索引顺序获取 0：sheet1
        self.caseName = table.col_values(0, 1)
        self.testData = table.col_values(1, 1)
        self.exceptResult = table.col_values(2, 1)
        self.sheetName=sheetName


    def get_TestData(self,dataType):
        if dataType=='caseName':
            return self.caseName
        elif dataType=='testData':
            return self.testData
        elif dataType=='exceptResult':
            return self.exceptResult
        else:
            raise AssertionError('There is no %s ' % (dataType))


    def excu_search_v4(self,params):
        print(params)
        print(type(params))
        self.caseParam = params
        client = Client('172.20.17.67', 9090).setClass('Search').setMethod('getSearchData_v4').getApi()  # 连接服务器
        params = params.encode('utf-8')
        result = client.getSearchData_v4(params)# 调用接口
        self._result=result
        #print("res:%s",(self._result))

    def excu_search_v3(self,params):
        print(params)
        self.caseParam = params
        client = Client('172.20.17.67', 9090).setClass('Search').setMethod('getSearchStore_v3').getApi()  # 连接服务器
        params = params.encode('utf-8')
        result = client.getSearchData_v4(params)# 调用接口
        print(result)
        self._result=result

    def _resultToPython(self):
        #self._setSearchWord(self.caseParam)
        json_to_python = json.loads(self._result)
        result = json_to_python[self.searchWord]
        return result


    # 检查rows里面每个商品详情
    def result_check(self,excepted,sheetName):
        self._setSearchWord()
        result = self._resultToPython()
        # 返回为空
        print "result type:%s" %(type(result))
        print "excepted type:%s,excepted:%s" %(type(excepted),excepted)
        if result == False:
            if excepted == 0:
                print("22222222222")
                pass
            else:
                print("3333333333")
                raise AssertionError("except is not same as result!!%s%s" %(type(excepted),excepted))
        else:
            if excepted == 1:
                print("1111")
                pass
            else:
                # 有商品返回
                for i in range(0,len(result.values()[2].get('rows'))):
                    print("row_size:%d") %(len(result.values()[2].get('rows')))
                    itemResult = result.values()[2].get('rows')[i]
                    itemRes = self.result_should_be(excepted, itemResult, sheetName)
                    if itemRes == False:
                        print "1111111111111111111111111111111111111111111111111111"
                        raise AssertionError("result[%d] cannot pass the case" %(i))

    # 预期与实际结果对比
    def result_should_be(self, excepted, itemResult, sheetName):
        defaultRes = False
        exitResult = 0
        # 第二版复杂数据：assert数据:{"1":{"a":"AA"},"2":{"b":"BB","c":"CC"}},1和2是or关系
        if sheetName.strip().startswith('extend_v4'):
            excepteds = eval(excepted.encode("utf-8"))

            keylist = excepteds.keys()
            print('aaaaaa:')
            keylist.sort()
            for i in keylist:
                exp = str(excepteds[i]).replace('\'','\"')
                print(exp)
                resultNum = self._comparaResult(exp,itemResult)
                exitResult += resultNum
        else:
            #第一版简单数据：assert数据：{"a":"AA","b":"BB|CC"} ，a和b是and关系
            print('bbbbbbbb:')
            exitResult = self._comparaResult(excepted, itemResult)

        if exitResult >0:
            defaultRes = True

        return defaultRes

    def _comparaResult(self,expected,result):
        if expected == False:
            return 0
        else:
            print('999999--')
            expectDict = json.loads(expected)
            print expectDict
            print type(expectDict)
            expectKeys = list(expectDict.keys())  # 获取预期结果的keys
            expectValues = expectDict.values()  # 获取预期结果的values

            for i in range(0, len(expectKeys)):
                print 'len:%d' %(len(expectKeys))
                expectKey = expectKeys[i]
                if result.has_key(expectKey):
                    realValue = result.get(expectKey)
                else:
                    continue
                judge = False
                #兼容doc中有list值得数据
                if(isinstance(realValue,list)):
                    print('111111')
                    for j in range(0,len(realValue)):
                        print "realvalue:%s" %(realValue[j])
                        judgeItem = self._isinlist(realValue[j],expectValues[i].split('|'))
                        if judgeItem == True:
                            judge = True
                            break
                        else:
                            pass
                else:
                    if(expectValues[i].find('-')== -1):
                        print ("hellloooo")
                        judge = self._isinlist(realValue, expectValues[i].split('|'))
                    else:
                        print ("world~~~,%s,%s" % (expectValues[i][1:],realValue))
                        judge = self._exceptlist(realValue,expectValues[i])
                print(judge)
                if judge == False:
                    return 0
            return 1


    def _isinlist(self,realValue, lists):
        lens = len(lists)
        #print 'real:%d' %(realValue)
        #print 'type:%s,expect:%s' %(lists[0],type(lists[0]))
        #print 'listlen:%d' %(lens)
        returnres = False
        for i in range(0,lens):
            if realValue == lists[i]:
                return True
            elif isinstance(realValue,int):
                if realValue == int(lists[i]):
                    return True
                else:
                    returnres = False
            else:
                returnres = False
        return returnres

    def _exceptlist(self,realValue,strs):
        if realValue != strs:
            print ("asssssss")
            return True
        else:
            print ("zzzzz")
            return False

    def _setSearchWord(self):
        params = self.caseParam
        #.encode('utf-8')  # unicode转str
        # 关键词提取
        res = json.loads(self._result)
        if json.loads(params).has_key("search"):
            if res.has_key("correct_keyword"):
                search_word = res["correct_keyword"]
            else:
                search_word = json.loads(params)["search"]
        else:
            search_word = ''
        self.searchWord = search_word

    def _setExceptedResult(self,index):
        self.excepted=self.exceptResult[index]

    def page_check(self,excepted):
        self._setSearchWord()
        result = self._resultToPython()

        exceptedKeys = json.loads(excepted).keys()
        exceptedValues = json.loads(excepted).values()
        for i in range(0,len(exceptedKeys)):
            print(result["data"].get(exceptedKeys[i]))
            realValue = result["data"].get(exceptedKeys[i])
            exceptedValue_int = int(exceptedValues[i].encode())
            if realValue != exceptedValue_int:
                print("1111")
                raise AssertionError("not pass the case!")



if __name__ == '__main__':
    test=NewestLibrary()

    #test.get_dataTable('basic_v4')
    #test.get_dataTable()

    test.excu_search_v4('{"search_type":0,"rows_per_page":100,"pre":1}')
    test.result_check('TRUE','basic_v4')
    '''
    test.excu_search_v4('{"search_type":0,"category_id":[508,507,509]}')
    test.result_check('{"{"category_id_4":"509"}','basic_v4')
    '''
    #test.excu_search_v4('{"search_type":0,"category_id":[508,507,509]}')
    #test.excu_search_v4('{"search_type": 0,"search":"ysld","proposeAutoCorrect":0}')
    #test.result_check('FALSE','basic_v4')

    #test.excu_search_v4('{"rows_per_page": 100,"search":"口红 "}')
    #test.page_check('{"pageNumber":"1"}')