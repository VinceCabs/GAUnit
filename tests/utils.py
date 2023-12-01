def generate_mock_har(*args, transport_url="https://www.google-analytics.com") -> dict:
    """build facility for unit tests used to generate hars with GA hits

    GA hits will get values in argument

    Args:
        schema (list): 'dp' parameters for GA hits "A" ,"x", "B",..
        transport_url (str): custom transport URL for server side GTM.
            Defaults to "https://www.google-analytics"

    Returns :
        dict : har
        example : generate_mock_har_ga("A","B") ->
            ({'log': {'entries': [
                {'request': {'url': 'https://www.google-analytics.com/collect?v=1&dp=A'}},
                {'request': {'url': 'https://www.google-analytics.com/collect?v=1&dp=B'}}
            ]}}
    """

    ga_urls = [transport_url + "/collect?v=1&dp=" + dp for dp in [*args]]
    har = {
        "log": {
            "entries": [{"request": {"method": "GET", "url": url}} for url in ga_urls]
        }
    }
    return har


def generate_mock_perf_log(
    *args, transport_url="https://www.google-analytics.com"
) -> list:
    """build facility for unit test used to generate webdriver Performance Log

    GA hits will get values in argument

    Returns:
        list: performance log
        example : generate_mock_perf_log_ga("A") ->
            [{
                "level": "INFO",
                "message": "{\"message\":{\"method\":\"Network.requestWillBeSent\",\"params\":{\"request\":"
                    +"{\"url\":\"https://www.google-analytics.com/collect?v=1&t=pageview&dp=dp=A\""
                    + "}}}}"

            }]
    """
    # fmt: off
    perf_log = [
        {
            "level": "INFO",
            "message": "{\"message\":{\"method\":\"Network.requestWillBeSent\",\"params\":{\"request\":{\"url\":\"" 
                + transport_url
                + "/collect?v=1&t=pageview&dp=" 
                + dp
                + "\"}}}}"
        }
        for dp in [*args]
    ]
    # fmt: on
    return perf_log
