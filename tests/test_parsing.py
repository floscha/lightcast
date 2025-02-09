import lightcast


def test_parsing_duration_from_total_seconds():
    test_duration = "100"

    parsed_duration = lightcast.core._parse_duration(test_duration)

    assert parsed_duration == 100

def test_parsing_duration_from_colon_separated_format():
    test_duration = "1:30:00"

    parsed_duration = lightcast.core._parse_duration(test_duration)

    assert parsed_duration == 5_400
