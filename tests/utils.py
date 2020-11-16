def generate_mock_har_ga(*args) -> dict:
    """build facility for unit tests used to generate hars with GA hits

    GA hits will get values in argument

    Args:
        schema (list): 'dp' parameters for GA hits [A,x,B,..]

    Returns :
        dict : har
        example : build_mock_har_ga("A","B") ->
            ({'log': {'entries': [
                {'request': {'url': 'https://www.google-analytics.com/collect?v=1&dp=A'}},
                {'request': {'url': 'https://www.google-analytics.com/collect?v=1&dp=B'}}
            ]}}
    """

    ga_urls = [
        "https://www.google-analytics.com/collect?v=1&dp=" + dp for dp in [*args]
    ]
    har = {"log": {"entries": [{"request": {"url": url}} for url in ga_urls]}}
    return har
