from dynatrace import Dynatrace


def test_ingest(dt: Dynatrace):
    events = [
        {
            "id": "HOST-82F576674F19AC16",
            "tags:custom.test": {"test": "test"},
        }
    ]
    response = dt.openpipeline.smartscape_eventv1_ingest(events)