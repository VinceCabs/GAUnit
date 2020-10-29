*** Settings ***
Library                     SeleniumLibrary
Library                     Collections
Library                     OperatingSystem
Library                     ../../gaunit/GAUnit.py

*** Variables ***
${tracking_plan_path}           ${CURDIR}/tracking_plan.json
${har_path}                     ${CURDIR}/home_engie.har

*** Test Cases ***
home_engie
    ${json}=     Get File    ${har_path}
    ${har}=     Evaluate    json.loads('''${json}''')   json
    ${checklist} =      Check Tracking From HAR     ${TEST_NAME}    ${har}
    Should Not Contain   ${checklist}  ${False}  
