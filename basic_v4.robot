#coding=utf-8
*** Settings ***
Documentation     Example test cases using the keyword-driven testing approach.
...
...               All tests contain a workflow constructed from keywords in
...               ``testLiblary.py``. Creating new tests or editing
...               existing is easy even for people without programming skills.
...
...               The _keyword-driven_ appoach works well for normal test
...               automation, but the _gherkin_ style might be even better
...               if also business people need to understand tests. If the
...               same workflow needs to repeated multiple times, it is best
...               to use to the _data-driven_ approach.
Test Template     Search
Library           ../RF/NewestLibrary.py
Test Setup        Get Data


*** Test Cases ***      expression      expected
#Get Data    [Template]    Get Data
#            testData      exceptResult    basic_v4

case0       @{testData}[0]      @{exceptResult}[0]

case1       @{testData}[1]      @{exceptResult}[1]

case2       @{testData}[2]      @{exceptResult}[2]

case3       @{testData}[3]      @{exceptResult}[3]

case4       @{testData}[4]      @{exceptResult}[4]

case5       @{testData}[5]      @{exceptResult}[5]

case6       @{testData}[6]      @{exceptResult}[6]

case7       @{testData}[7]      @{exceptResult}[7]

case8       @{testData}[8]      @{exceptResult}[8]

case9       @{testData}[9]      @{exceptResult}[9]

case10       @{testData}[10]      @{exceptResult}[10]

case11       @{testData}[11]      @{exceptResult}[11]

case12       @{testData}[12]      @{exceptResult}[12]

case13       @{testData}[13]      @{exceptResult}[13]

case14       @{testData}[14]      @{exceptResult}[14]

case15       @{testData}[15]      @{exceptResult}[15]

case16       @{testData}[16]      @{exceptResult}[16]

case17       @{testData}[17]      @{exceptResult}[17]

case18       @{testData}[18]      @{exceptResult}[18]

case19       @{testData}[19]      @{exceptResult}[19]

case20       @{testData}[20]      @{exceptResult}[20]

case21       @{testData}[21]      @{exceptResult}[21]

case22       @{testData}[22]      @{exceptResult}[22]

case23       @{testData}[23]      @{exceptResult}[23]

case24       @{testData}[24]      @{exceptResult}[24]

case25       @{testData}[25]      @{exceptResult}[25]

case26       @{testData}[26]      @{exceptResult}[26]

case27       @{testData}[27]      @{exceptResult}[27]

case28       @{testData}[28]      @{exceptResult}[28]

case29       @{testData}[29]      @{exceptResult}[29]

case30       @{testData}[30]      @{exceptResult}[30]

case31       @{testData}[31]      @{exceptResult}[31]

case32       @{testData}[32]      @{exceptResult}[32]

case33       @{testData}[33]      @{exceptResult}[33]

case34       @{testData}[34]      @{exceptResult}[34]

case35       @{testData}[35]      @{exceptResult}[35]

case36       @{testData}[36]      @{exceptResult}[36]

case37       @{testData}[37]      @{exceptResult}[37]

case38       @{testData}[38]      @{exceptResult}[38]

case39       @{testData}[39]      @{exceptResult}[39]

case40       @{testData}[40]      @{exceptResult}[40]

case41       @{testData}[41]      @{exceptResult}[41]

case42       @{testData}[42]      @{exceptResult}[42]

case43       @{testData}[43]      @{exceptResult}[43]

case44       @{testData}[44]      @{exceptResult}[44]

case45       @{testData}[45]      @{exceptResult}[45]

case46       @{testData}[46]      @{exceptResult}[46]

case47       @{testData}[47]      @{exceptResult}[47]

case48       @{testData}[48]      @{exceptResult}[48]

case49       @{testData}[49]      @{exceptResult}[49]

case50       @{testData}[50]      @{exceptResult}[50]

case51       @{testData}[51]      @{exceptResult}[51]


*** Keywords ***
Search
    [Arguments]    ${expression}    ${expected}
    excu search v4    ${expression}
    result check    ${expected}  basic_v4



Get Data
    #[Arguments]    ${expression1}       ${expression2}      ${sheetname}
    #${testData}=    get TestData     ${expression1}      ${sheetname}
    #${exceptResult}=    get TestData     ${expression2}     ${sheetname}
    #Set Global Variable    @{testData}
    #Set Global Variable    @{exceptResult}
    get dataTable    basic_v4
    @{testData}=    get TestData    testData
    @{exceptResult}=     get TestData    exceptResult
    @{caseName}=    get TestData    caseName
    Set Global Variable    @{testData}
    Set Global Variable    @{exceptResult}
    Set Global Variable    @{caseName}
