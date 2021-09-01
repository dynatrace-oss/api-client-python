from datetime import datetime

import dynatrace.environment_v2.problems as pb
from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime
from dynatrace.configuration_v1.alerting_profiles import AlertingProfileStub
from dynatrace.environment_v2.monitored_entities import EntityStub, EntityId
from dynatrace.environment_v2.schemas import ManagementZone
from dynatrace.environment_v2.custom_tags import METag

PROBLEM_ID = "-1719139739592062093_1623004451641V2"
COMMENT_ID = "-7228967546616810529_1623004451641"


def test_list(dt: Dynatrace):
    problems = dt.problems.list(time_from="now-3d")

    assert isinstance(problems, PaginatedList)
    assert len(list(problems)) == 2
    assert all(isinstance(p, pb.Problem) for p in problems)


def test_get(dt: Dynatrace):
    problem = dt.problems.get(problem_id=PROBLEM_ID)

    # type checks
    assert isinstance(problem, pb.Problem)
    assert isinstance(problem.affected_entities, list)
    assert isinstance(problem.impacted_entities, list)
    assert isinstance(problem.management_zones, list)
    assert isinstance(problem.entity_tags, list)
    assert isinstance(problem.problem_filters, list)
    assert isinstance(problem.start_time, datetime)
    assert isinstance(problem.end_time, datetime)
    assert all(isinstance(ae, EntityStub) for ae in problem.affected_entities)
    assert all(isinstance(ae.entity_id, EntityId) for ae in problem.affected_entities)
    assert all(isinstance(ie, EntityStub) for ie in problem.impacted_entities)
    assert all(isinstance(ie.entity_id, EntityId) for ie in problem.impacted_entities)
    assert isinstance(problem.root_cause_entity, EntityStub)
    assert all(isinstance(mz, ManagementZone) for mz in problem.management_zones)
    assert all(isinstance(et, METag) for et in problem.entity_tags)
    assert all(isinstance(pf, AlertingProfileStub) for pf in problem.problem_filters)
    assert isinstance(problem.evidence_details, pb.EvidenceDetails)
    assert all(isinstance(e, pb.Evidence) for e in problem.evidence_details.details)
    assert all(isinstance(e.entity, EntityStub) for e in problem.evidence_details.details)
    assert all(isinstance(e.grouping_entity, EntityStub) for e in problem.evidence_details.details)
    assert isinstance(problem.recent_comments, pb.CommentList)
    assert all(isinstance(c, pb.Comment) for c in problem.recent_comments.comments)
    assert isinstance(problem.impact_analysis, pb.ImpactAnalysis)
    assert all(isinstance(i, pb.Impact) for i in problem.impact_analysis.impacts)

    # value checks
    assert problem.problem_id == PROBLEM_ID
    assert problem.display_id == "P-210617"
    assert problem.title == "Multiple infrastructure problems"
    assert problem.impact_level == pb.ImpactLevel.INFRASTRUCTURE
    assert problem.severity_level == pb.SeverityLevel.RESOURCE_CONTENTION
    assert problem.status == pb.Status.CLOSED
    assert all(ae.entity_id.id == "PROCESS_GROUP_INSTANCE-8092E71D6FBB914E" for ae in problem.affected_entities)
    assert all(ae.entity_id.type == "PROCESS_GROUP_INSTANCE" for ae in problem.affected_entities)
    assert all(ae.name == "easytravel.customer.frontend" for ae in problem.affected_entities)
    assert all(ie.entity_id.id == "PROCESS_GROUP_INSTANCE-8092E71D6FBB914E" for ie in problem.impacted_entities)
    assert all(ie.entity_id.type == "PROCESS_GROUP_INSTANCE" for ie in problem.impacted_entities)
    assert all(ie.name == "easytravel.customer.frontend" for ie in problem.impacted_entities)
    assert problem.root_cause_entity.entity_id.id == "PROCESS_GROUP-C44FB250621B8036"
    assert problem.root_cause_entity.entity_id.type == "PROCESS_GROUP"
    assert problem.root_cause_entity.name == "easytravel.customer.frontend"
    assert problem.management_zones[0].id == "8692695975020499402"
    assert problem.management_zones[0].name == "Operations Team"
    assert all(str(et.context) == "CONTEXTLESS" for et in problem.entity_tags)
    assert problem.start_time == int64_to_datetime(1622807640000)
    assert problem.end_time == int64_to_datetime(1622807820000)
    assert problem.evidence_details.total_count == 4
    assert len(problem.evidence_details.details) == 4
    assert problem.recent_comments.total_count == 2
    assert len(problem.recent_comments.comments) == 2


def test_close(dt: Dynatrace):
    close_result = dt.problems.close(problem_id=PROBLEM_ID, message="Closing this. 1234")

    # type checks
    assert isinstance(close_result, pb.ProblemCloseResult)
    assert isinstance(close_result.comment, pb.Comment)
    assert isinstance(close_result.close_timestamp, datetime)
    assert isinstance(close_result.closing, bool)

    # value checks
    assert close_result.problem_id == PROBLEM_ID
    assert close_result.comment.id == COMMENT_ID
    assert close_result.comment.created_at == int64_to_datetime(1623047022173)
    assert close_result.comment.content == "Closing this. 1234"
    assert close_result.comment.author == "radu.stefan@dynatrace.com"
    assert close_result.comment.context == "dynatrace-problem-close"
    assert close_result.close_timestamp == int64_to_datetime(1623047022173)
    assert close_result.closing == True


def test_list_comments(dt: Dynatrace):
    comments = dt.problems.list_comments(problem_id=PROBLEM_ID, page_size=20)

    assert isinstance(comments, PaginatedList)
    assert len(list(comments)) == 2
    assert all(isinstance(c, pb.Comment) for c in comments)


def test_get_comment(dt: Dynatrace):
    comment = dt.problems.get_comment(problem_id=PROBLEM_ID, comment_id=COMMENT_ID)

    assert isinstance(comment, pb.Comment)

    assert comment.id == COMMENT_ID
    assert comment.created_at == int64_to_datetime(1623047022173)
    assert comment.content == "Closing this. 1234"
    assert comment.context == "dynatrace-problem-close"
    assert comment.author == "radu.stefan@dynatrace.com"
