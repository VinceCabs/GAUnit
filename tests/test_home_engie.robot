*** Settings ***
Library                     SeleniumLibrary
Library                     Collections
Library                     OperatingSystem
Resource                    ./keywords/tracking.robot

*** Test Cases ***
home_engie
    ${json}=     Get File    ./tests/home_engie.har
    ${har}=     Evaluate    json.loads('''${json}''')   json
    Tracking Should be Correct   ${TEST NAME}    ${har}
