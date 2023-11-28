from datetime import datetime

import dynatrace.environment_v2.settings as st
from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList
payload = {"additionalInformation": [],
            "contactDetails":[{"email": 'unittest@contoso.com', "integrationType": "EMAIL"}],
            "description": 'unittest',
            "identifier":'unittest',
            "links": [],
            "name": 'unittest',
            "responsibilities": {"development": False,
                                    "infrastructure": False,
                                    "lineOfBusiness": True,
                                    "operations": False,
                                    "security": False},
            "supplementaryIdentifiers": []      }
def test_list(dt: Dynatrace):
    settings = dt.settings.list(schema_id="builtin:ownership.teams")
    assert isinstance(settings, PaginatedList)
    assert len(list(settings)) == 1
    assert all(isinstance(s, st.Settings) for s in settings)

def test_get(dt: Dynatrace):
    setting = dt.settings.get(object_id="vu9U3hXa3q0AAAABABdidWlsdGluOm93bmVyc2hpcC50ZWFtcwAGdGVuYW50AAZ0ZW5hbnQAJGVjN2UyNTdhLWM5MTktM2YzMC05NWFiLTliMzNkMmQwZGRkY77vVN4V2t6t")
    assert isinstance(setting, st.Settings)

def test_post(dt: Dynatrace):

    response = dt.settings.post(external_id='unittest',object_id='unittest',schema_id="builtin:ownership.teams",schema_version="1.0.6",scope="environment", value=payload,validate_only=False)
    assert response[0].get("code") == 200
    assert response[0].get("code") is not None

def test_put(dt: Dynatrace):
    payload["identifier"] = "unittestupdate"
    response = dt.settings.update("unittest",payload)
    print(response)