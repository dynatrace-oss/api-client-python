from dynatrace import Dynatrace


def test_parse_multiple_date_formats(dt: Dynatrace):
    """
    The API can currently return two different date formats.
    If a token is created exactly at 0, then the millisecond portion is not returned by the API.
    E.g., 2025-01-19T21:36:02.000Z will be returned as 2025-01-19T21:36:02Z by API.
    This test ensures that both are parsed correctly.
    """
    tokens = dt.tokens.list()
    assert len(tokens) == 2
