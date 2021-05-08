from dynatrace import Dynatrace


def test_start_rotation(dt: Dynatrace):
    token_config = dt.tenant_tokens.start_rotation()
    assert token_config.active.value == "hRCnr6Yd3BFrtxaF"
    assert token_config.old.value == "prv0bYw93v8sU9b1"


def test_cancel_rotation(dt: Dynatrace):
    token_config = dt.tenant_tokens.cancel_rotation()
    assert token_config.active.value == "prv0bYw93v8sU9b1"
    assert token_config.old.value is None


def test_finish_rotation(dt: Dynatrace):
    token_config = dt.tenant_tokens.finish_rotation()
    assert token_config.active.value == "prv0bYw93v8sU9b1"
    assert token_config.old.value is None
