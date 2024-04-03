from api.api_calls import use_requests, use_langchain


def test_requests_call():
    assert use_requests()


def test_use_langchain():
    assert use_langchain()


def tests_identical():
    assert use_langchain() == use_requests()
