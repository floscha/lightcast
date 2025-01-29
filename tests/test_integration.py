from datetime import datetime, timezone

from lightcast import search_podcasts


def test_integration():
    top_search_result = search_podcasts("huberman")[0]

    assert top_search_result.name == "Huberman Lab"

    first_episode = top_search_result.episodes[-1]
    assert first_episode.title == "Welcome to the Huberman Lab Podcast"
    assert "SCIM5670648609" in first_episode.audio_url
    assert first_episode.publication_date == datetime(2020, 12, 21, 5, 22, tzinfo=timezone.utc)
    assert first_episode.duration == 262  # 4m 22s
