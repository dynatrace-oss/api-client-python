from datetime import datetime
from typing import List
from dynatrace import Dynatrace
from dynatrace.environment_v2.remote_configuration import (
    RemoteConfigurationManagementOperation,
    RemoteConfigurationManagementOperationActiveGateRequest,
    AttributeType,
    OperationType,
    EntityType,
    RemoteConfigurationManagementJobPreview,
    RemoteConfigurationManagementJobSummary
)
from dynatrace.pagination import PaginatedList

TEST_ENTITY_ID = "0x2b7c0b02"

def test_list(dt: Dynatrace):
    jobs = dt.activegates_remote_configuration.list()
    
    assert isinstance(jobs, PaginatedList)
    
    for job in jobs:
        assert isinstance(job, RemoteConfigurationManagementJobSummary)
        assert hasattr(job, "id")
        assert hasattr(job, "entity_type")
        assert hasattr(job, "start_time")
        assert isinstance(job.entity_type, EntityType)
        break

def test_post(dt: Dynatrace):
    operation = RemoteConfigurationManagementOperation.build(
        attribute=AttributeType.NETWORK_ZONE,
        operation=OperationType.SET,
        value="test-zone",
    )
    
    job = dt.activegates_remote_configuration.post(entities=[TEST_ENTITY_ID], operations=[operation])
    
    assert job is not None
    assert job.id is not None
    assert job.entity_type == EntityType.ACTIVE_GATE
    assert len(job.operations) == 1
    assert job.operations[0].attribute == AttributeType.NETWORK_ZONE
    assert job.operations[0].operation == OperationType.SET
    assert job.operations[0].value == "test-zone"

def test_get_current(dt: Dynatrace):
    current_job = dt.activegates_remote_configuration.get_current()
    
    if current_job is not None:
        assert current_job.id is not None
        assert hasattr(current_job, "timeout_time")
        assert current_job.processed_entities_count <= current_job.total_entities_count

def test_post_preview(dt: Dynatrace):
    operation = RemoteConfigurationManagementOperation.build(
        attribute=AttributeType.NETWORK_ZONE,
        operation=OperationType.SET,
        value="test-zone",
    )
    
    previews = dt.activegates_remote_configuration.post_preview(
        entities=[TEST_ENTITY_ID],
        operations=[operation],
    )
    
    assert isinstance(previews, PaginatedList)
    
    for preview in previews:
        assert isinstance(preview, RemoteConfigurationManagementJobPreview)
        assert preview.attribute == AttributeType.NETWORK_ZONE
        assert preview.operation == OperationType.SET
        assert preview.value == "test-zone"
        assert isinstance(preview.already_configured_entities_count, int)
        assert isinstance(preview.target_entities_count, int)
        break

def test_validate(dt: Dynatrace):
    operation = RemoteConfigurationManagementOperation.build(
        attribute=AttributeType.NETWORK_ZONE,
        operation=OperationType.SET,
        value="test-zone",
    )
    validation_result = dt.activegates_remote_configuration.validate(
        entities=[TEST_ENTITY_ID],
        operations=[operation]
    )
    
    # If validation succeeds, result should be None
    # If validation fails, result should contain error details
    if validation_result is not None:
        assert hasattr(validation_result, "invalid_entities")
        assert hasattr(validation_result, "invalid_operations")
        assert isinstance(validation_result.invalid_entities, list)
        assert isinstance(validation_result.invalid_operations, list)

def test_get_job(dt: Dynatrace):
    ID = "7974003406714390819"
    job = dt.activegates_remote_configuration.get(ID)
    
    assert job is not None
    assert job.id == ID
    assert job.entity_type == EntityType.ACTIVE_GATE
    assert len(job.operations) == 1
    assert job.operations[0].attribute == AttributeType.NETWORK_ZONE
    assert job.operations[0].operation == OperationType.SET
    assert job.operations[0].value == "test-zone"