from dynatrace import Dynatrace
from datetime import datetime


def test_list(dt: Dynatrace):
    update_jobs = list(dt.activegates_autoupdate_jobs.list())
    assert isinstance(update_jobs, list)

    first_ag = update_jobs[0]
    assert first_ag.activegate_id == "-1556499193"
    assert len(first_ag.update_jobs) == 3

    first_job = first_ag.update_jobs[0]
    assert first_job.job_id == "-4754066816153208332"
    assert first_job.job_state == "SUCCEED"
    assert first_job.update_method == "MANUAL_INSTALLATION"
    assert first_job.update_type == "ACTIVE_GATE"
    assert not first_job.cancelable
    assert first_job.start_version == "1.217.89.20210506-182520"
    assert first_job.target_version == "1.217.96.20210507-181038"
    assert first_job.timestamp == datetime.utcfromtimestamp(1620419177047 / 1000)
    assert first_job.ag_type == "ENVIRONMENT"
    assert first_job.environments == ["eaa50379"]
    assert first_job.error is None
    assert first_job.duration is None


def test_get(dt: Dynatrace):
    update_jobs_list = dt.activegates_autoupdate_jobs.get("-1556499193")

    assert update_jobs_list.activegate_id == "-1556499193"
    assert isinstance(update_jobs_list.update_jobs, list)

    first_job = update_jobs_list.update_jobs[0]
    assert first_job.job_id == "-4754066816153208332"
    assert first_job.job_state == "SUCCEED"
    assert first_job.update_method == "MANUAL_INSTALLATION"
    assert first_job.update_type == "ACTIVE_GATE"
    assert not first_job.cancelable
    assert first_job.start_version == "1.217.89.20210506-182520"
    assert first_job.target_version == "1.217.96.20210507-181038"
    assert first_job.timestamp == datetime.utcfromtimestamp(1620419177047 / 1000)
    assert first_job.ag_type == "ENVIRONMENT"
    assert first_job.environments == ["eaa50379"]
    assert first_job.error is None
    assert first_job.duration is None
