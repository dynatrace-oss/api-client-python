from datetime import datetime

from dynatrace import Dynatrace
from dynatrace.environment_v2.monitored_entities import (
    Entity,
    EntityIcon,
    ToPosition,
    FromPosition,
    EntityType,
    EntityTypePropertyDto,
    MessageType,
    CustomDeviceCreation,
)
from dynatrace.environment_v2.schemas import ManagementZone
from dynatrace.environment_v2.custom_tags import METag

from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime


def test_list(dt: Dynatrace):
    entities = dt.entities.list(
        'type("HOST")', fields="+fromRelationships,+toRelationships,+icon,+properties,+tags,+managementZones,+firstSeenTms,+lastSeenTms"
    )
    entities_list = list(entities)

    # type checks
    assert isinstance(entities, PaginatedList)
    assert all(isinstance(e, Entity) for e in entities)

    # value checks
    assert len(entities_list) == 1


def test_get(dt: Dynatrace):
    entity = dt.entities.get(
        "HOST-82F576674F19AC16",
        time_from=datetime.utcfromtimestamp(1618585701),
        time_to=datetime.utcfromtimestamp(1621177701),
        fields="+fromRelationships,+toRelationships,+icon,+properties,+tags,+managementZones,+firstSeenTms,+lastSeenTms",
    )

    # type checks
    assert isinstance(entity, Entity)
    assert isinstance(entity.entity_id, str)
    assert isinstance(entity.display_name, str)
    assert isinstance(entity.first_seen, (datetime, type(None)))
    assert isinstance(entity.last_seen, (datetime, type(None)))
    assert isinstance(entity.properties, dict)
    assert isinstance(entity.tags, list)
    assert all(isinstance(t, METag) for t in entity.tags)
    assert isinstance(entity.management_zones, list)
    assert all(isinstance(mz, ManagementZone) for mz in entity.management_zones)
    assert isinstance(entity.icon, EntityIcon)
    assert isinstance(entity.from_relationships, dict)
    assert isinstance(entity.to_relationships, dict)

    # value checks
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


def test_list_types(dt: Dynatrace):
    entity_types = dt.entities.list_types(page_size=3)
    entity_types_list = list(entity_types)

    # type checks
    assert isinstance(entity_types, PaginatedList)
    assert all(isinstance(et, EntityType) for et in entity_types)

    # value checks
    assert len(entity_types_list) == 2


def test_get_types(dt: Dynatrace):
    entity_type = dt.entities.get_types(entity_type="DISK")

    # type checks
    assert isinstance(entity_type, EntityType)
    assert isinstance(entity_type.type, str)
    assert isinstance(entity_type.dimension_key, str)
    assert isinstance(entity_type.entity_limit_exceeded, bool)
    assert isinstance(entity_type.properties, list)
    assert all(isinstance(p, EntityTypePropertyDto) for p in entity_type.properties)
    for prop in entity_type.properties:
        assert isinstance(prop.display_name, str)
        assert isinstance(prop.id, str)
        assert isinstance(prop.type, str)
    assert isinstance(entity_type.tags, str)
    assert isinstance(entity_type.management_zones, str)
    assert isinstance(entity_type.from_relationships, list)
    assert all(isinstance(fr, FromPosition) for fr in entity_type.from_relationships)
    for rel in entity_type.from_relationships:
        assert isinstance(rel.id, str)
        assert isinstance(rel.to_types, list)
        assert all(isinstance(tt, str) for tt in rel.to_types)
    assert isinstance(entity_type.to_relationships, list)
    assert all(isinstance(tr, ToPosition) for tr in entity_type.to_relationships)
    for rel in entity_type.to_relationships:
        assert isinstance(rel.id, str)
        assert isinstance(rel.from_types, list)
        assert all(isinstance(ft, str) for ft in rel.from_types)

    # value checks
    assert entity_type.type == "DISK"
    assert entity_type.display_name == "Disk"
    assert entity_type.dimension_key == "dt.entity.disk"
    assert entity_type.entity_limit_exceeded == False
    assert entity_type.properties[0].id == "awsNameTag"
    assert entity_type.properties[0].type == "String"
    assert entity_type.properties[0].display_name == "awsNameTag"
    assert entity_type.tags == "List"
    assert entity_type.management_zones == "List"
    assert entity_type.from_relationships[0].id == "isDiskOf"
    assert entity_type.from_relationships[0].to_types[0] == "HOST"
    assert entity_type.to_relationships[0].id == "isEbsVolumeOf"
    assert entity_type.to_relationships[0].from_types[0] == "EBS_VOLUME"


def test_create_custom_device(dt: Dynatrace):
    device = dt.entities.create_custom_device(
        custom_device_id="device-one",
        display_name="Test Device",
        group="group-one",
        device_type="IoT Beacon",
        ip_addresses=["10.20.0.0", "192.168.0.1"],
        listen_ports=[80, 8080],
        favicon_url="https://awesome-pics.img.com/icon",
        config_url="http://www.dashboard.com/device-one",
        dns_names=["testdevice.testnet.net"],
        properties={"this": "that", "lorem": "ipsum"},
        message_type=MessageType.CUSTOM_DEVICE,
    )

    # type checks
    assert isinstance(device, CustomDeviceCreation)
    assert isinstance(device.custom_device_id, str)
    assert isinstance(device.display_name, str)
    assert isinstance(device.group, str)
    assert isinstance(device.type, str)
    assert isinstance(device.ip_addresses, list)
    assert all(isinstance(ip, str) for ip in device.ip_addresses)
    assert isinstance(device.listen_ports, list)
    assert all(isinstance(port, int) for port in device.listen_ports)
    assert isinstance(device.favicon_url, str)
    assert isinstance(device.config_url, str)
    assert isinstance(device.dns_names, list)
    assert all(isinstance(dns, str) for dns in device.dns_names)
    assert isinstance(device.properties, dict)
    assert isinstance(device.message_type, MessageType)

    # value checks
    assert device.custom_device_id == "device-one"
    assert device.display_name == "Test Device"
    assert device.group == "group-one"
    assert device.type == "IoT Beacon"
    assert device.ip_addresses[0] == "10.20.0.0"
    assert device.listen_ports[0] == 80
    assert device.favicon_url == "https://awesome-pics.img.com/icon"
    assert device.config_url == "http://www.dashboard.com/device-one"
    assert device.dns_names[0] == "testdevice.testnet.net"
    assert device.properties["this"] == "that"
    assert device.message_type == MessageType.CUSTOM_DEVICE
