from lyrebird_bugit import cache

def test_save_cache():
    data = '1'
    cache.put("TEST_JIRA", data)
    assert cache.get("TEST_JIRA") == '1'
