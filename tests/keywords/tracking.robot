*** Settings ***
Library                     ../../gaunit/GAUnit.py
*** Keywords ***
Tracking Should be Correct
    [Documentation]  takes the name of a Test case and a har file for inputs and check if tracking is correct
    [Arguments]     ${test_case}    ${har}
    ${checklist} =      Check Tracking From HAR     ${test_case}    ${har}
    Should Not Contain   ${checklist}  ${False}  