from datetime import datetime

import dynatrace.environment_v2.problems as pb
from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime
from dynatrace.configuration_v1.metag import METag
from dynatrace.configuration_v1.alerting_profiles import AlertingProfileStub
from dynatrace.environment_v2.monitored_entities import EntityStub, EntityId
from dynatrace.environment_v2.schemas import ManagementZone


def test_list(dt: Dynatrace):
    problems = dt.problems.list(time_from="now-3d")

    assert isinstance(problems, PaginatedList)
    assert len(list(problems)) == 2
    assert all(isinstance(p, pb.Problem) for p in problems)


def test_get(dt: Dynatrace):
    problem = dt.problems.get(problem_id="-1719139739592062093_1623004451641V2")

    # type checks
    assert isinstance(problem, pb.Problem)
    assert isinstance(problem.affected_entities, list)
    assert isinstance(problem.impacted_entities, list)
    assert isinstance(problem.management_zones, list)
    assert isinstance(problem.entity_tags, list)
    assert isinstance(problem.problem_filters, list)
    assert isinstance(problem.start_time, datetime)
    assert isinstance(problem.end_time, type(None))
    assert all(isinstance(ae, EntityStub) for ae in problem.affected_entities)
    assert all(isinstance(ae.entity_id, EntityId) for ae in problem.affected_entities)
    assert all(isinstance(ie, EntityStub) for ie in problem.impacted_entities)
    assert all(isinstance(ie.entity_id, EntityId) for ie in problem.impacted_entities)
    assert all(isinstance(mz, ManagementZone) for mz in problem.management_zones)
    assert all(isinstance(et, METag) for et in problem.entity_tags)
    assert all(isinstance(pf, AlertingProfileStub) for pf in problem.problem_filters)

    # value checks
    assert problem.problem_id == "-1719139739592062093_1623004451641V2"
    assert problem.display_id == "P-210620"
    assert problem.title == "custom host disconnected error"
    assert problem.impact_level == pb.ImpactLevel.INFRASTRUCTURE
    assert problem.severity_level == pb.SeverityLevel.AVAILABILITY
    assert problem.status == pb.Status.OPEN
    assert all(ae.entity_id.id == "HOST-44DD554D0DA01178" for ae in problem.affected_entities)
    assert all(ae.entity_id.type == "HOST" for ae in problem.affected_entities)
    assert all(ae.name == "TAG009444549397" for ae in problem.affected_entities)
    assert all(ie.entity_id.id == "HOST-44DD554D0DA01178" for ie in problem.impacted_entities)
    assert all(ie.entity_id.type == "HOST" for ie in problem.impacted_entities)
    assert all(ie.name == "TAG009444549397" for ie in problem.impacted_entities)
    assert problem.root_cause_entity
    assert all(et.context == "CONTEXTLESS" for et in problem.entity_tags)
    assert problem.start_time == int64_to_datetime(1623004451641)
