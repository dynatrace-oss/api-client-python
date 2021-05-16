from datetime import datetime

from dynatrace import Dynatrace
from dynatrace.environment_v2.monitored_entities import Entity

from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime


def test_list(dt: Dynatrace):
    entities = dt.entities.list(
        'type("HOST")', fields="+fromRelationships,+toRelationships,+icon,+properties,+tags,+managementZones,+firstSeenTms,+lastSeenTms"
    )
    assert isinstance(entities, PaginatedList)
    entities_list = list(entities)
    assert len(entities_list) == 1

    entity = entities_list[0]
    assert isinstance(entity, Entity)
    assert entity.entity_id == "HOST-82F576674F19AC16"
    assert entity.display_name == "arch-david"
    assert entity.first_seen == int64_to_datetime(1620821456242)
    assert entity.last_seen == int64_to_datetime(1621177614119)
    assert entity.properties["bitness"] == "64"
    assert len(entity.tags) == 1
    assert entity.tags[0].key == "citrix-prod"
    assert len(entity.management_zones) == 0
    assert entity.icon.primary_icon_type == "linux"
    assert entity.from_relationships["isHostOfContainer"][0].id == "DOCKER_CONTAINER_GROUP_INSTANCE-8E2ED6F4E2AFDD89"
    assert entity.to_relationships["runsOn"][0].id == "PROCESS_GROUP-3AD9FB79C914520C"


def test_get(dt: Dynatrace):
    entity = dt.entities.get(
        "HOST-82F576674F19AC16",
        time_from=datetime.utcfromtimestamp(1618585701),
        time_to=datetime.utcfromtimestamp(1621177701),
        fields="+fromRelationships,+toRelationships,+icon,+properties,+tags,+managementZones,+firstSeenTms,+lastSeenTms",
    )
    assert isinstance(entity, Entity)
    assert entity.entity_id == "HOST-82F576674F19AC16"
    assert entity.display_name == "arch-david"
    assert entity.first_seen == int64_to_datetime(1620821456242)
    assert entity.last_seen == int64_to_datetime(1621177614119)
    assert entity.properties["bitness"] == "64"
    assert len(entity.tags) == 1
    assert entity.tags[0].key == "citrix-prod"
    assert len(entity.management_zones) == 0
    assert entity.icon.primary_icon_type == "linux"
    assert entity.from_relationships["isHostOfContainer"][0].id == "DOCKER_CONTAINER_GROUP_INSTANCE-8E2ED6F4E2AFDD89"
    assert entity.to_relationships["runsOn"][0].id == "PROCESS_GROUP-3AD9FB79C914520C"
