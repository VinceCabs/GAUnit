*** Settings ***
Documentation               Tracking
Library                     SeleniumLibrary
Library                     Collections
Library                     OperatingSystem
Library                     BrowserMobProxyLibrary
Library                     RequestsLibrary
*** Keywords ***
Start_Proxy
    [Documentation]         Start chrome browser
    Set Selenium Implicit Wait  10
    ## Init BrowserMob Proxy
    Start Local Server
    ## Create dedicated proxy on BrowserMob Proxy
    &{port}    Create Dictionary    port=8082
   # Create dedicated proxy on BrowserMob Proxy 
    ${BrowserMob_Proxy}=    Create Proxy    ${port}

# Configure Webdriver to use BrowserMob Proxy
    ${options}=  Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --proxy-server\=localhost:8082
    Call Method    ${options}    add_argument     --ignore-certificate-errors
    ${options.add_argument}=  Set Variable  --allow-running-insecure-content
    ${options.add_argument}=  Set Variable  --disable-web-security
    ${options.add_argument}=  Set Variable  --ignore-certificate-errors
    Create WebDriver    Chrome     chrome_options=${options}
Close Browsers
    Close All Browsers
    Stop Local Server