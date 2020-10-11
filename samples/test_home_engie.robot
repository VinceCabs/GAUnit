*** Settings ***
Library                     SeleniumLibrary
Library                     Collections
Library                     OperatingSystem
Resource                    ./keywords/proxy.robot
Resource                    ./keywords/tracking.robot
Suite Setup                 Start_Proxy
Suite Teardown              Close Browsers
*** Variables ***
# ${PAGE_URL}             https://particuliers.engie.fr?env_work=acc
${PAGE_URL}             https://particuliers.engie.fr
# ${bouton_je_valide_cookies}     xpath=//*[@id="privacy-cat-modal"]/div/div/div[1]/button[2]
${bouton_souscription}     xpath=//*[@id='engie_fournisseur_d_electricite_et_de_gaz_naturel_headerhp_souscrire_a_une_offre_d_energie']

*** Test Cases ***
home_engie
    set selenium implicit wait    10
    # set selenium speed    2
    New Har    ${TEST NAME}
    Go To    ${PAGE_URL}
    # Wait Until Page Contains    cookies
    # Click Element    ${bouton_je_valide_cookies} 
    Click Element    ${bouton_souscription}
    ${har}=     Get Har As Json
    Tracking Should be Correct   ${TEST NAME}    ${har}
