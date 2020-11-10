from collections import defaultdict
from datetime import datetime
import logging
from typing import Dict, Optional, List

from requests import Response

from dynatrace.activegate import ActiveGate
from dynatrace.custom_device import CustomDevicePushMessage
from dynatrace.dashboard import DashboardStub, Dashboard
from dynatrace.endpoint import EndpointShortRepresentation
from dynatrace.entity import Entity, EntityShortRepresentation
from dynatrace.entity_type import EntityType
from dynatrace.extension import ExtensionDto, Extension, ExtensionShortRepresentation, ExtensionConfigurationDto
from dynatrace.http_client import HttpClient
from dynatrace.metric import MetricSeriesCollection, MetricDescriptor
from dynatrace.pagination import PaginatedList
from dynatrace.plugins import PluginShortRepresentation, PluginState
from dynatrace.synthetic_third_party import (
    ThirdPartySyntheticTests,
    ThirdPartySyntheticLocation,
    ThirdPartySyntheticMonitor,
    SyntheticTestLocation,
    ThirdPartySyntheticResult,
    ThirdPartySyntheticLocationTestResult,
    SyntheticMonitorStepResult,
    SyntheticTestStep,
    ThirdPartyEventResolvedNotification,
    ThirdPartyEventOpenNotification,
    ThirdPartySyntheticEvents,
)
from dynatrace.timeseries import TimeseriesRegistrationMessage


class Dynatrace:
    def __init__(
        self, base_url: str, token: str, log: logging.Logger = None, proxies: Dict = None, too_many_requests_strategy=None
    ):
        self.__http_client = HttpClient(base_url, token, log, proxies, too_many_requests_strategy)
        self.__open_third_party_events: Dict[str, int] = defaultdict(int)

    def get_entities(
        self,
        entity_selector: str,
        time_from: str = "now-2h",
        time_to: str = "now",
        fields: Optional[str] = None,
        page_size=50,
        threads=20,
    ) -> PaginatedList[Entity]:
        """
        Lists entities observed within the specified timeframe along with their properties.

        :param entity_selector: Defines the scope of the query. Only entities matching the specified criteria are included into response.

            You need to set one of these criteria:

            Entity type: type("value").
            Dynatrace entity ID: entityId("id"). You can specify several IDs, separated by a comma (entityId("id-1","id-2")).

            And you can add one or several of the following criteria:

            Tag: tag("value"). Tags in [context]key:value, key:value, and value formats are detected and parsed automatically.
            If a value-only tag has a colon (:) in it, you must escape the colon with a backslash \\.
            Otherwise, the tag will be parsed as a key:value tag. All tag values are case-sensitive.
            Management zone ID: mzId("ID")
            Management zone name: mzName("value"). Management zone names are case-sensitive.
            Dynatrace entity name: entityName("value"). You can specify several entity names, separated by a comma (entityName("name-1","name-2")).
            Entity names are case-sensitive.
            Health state (HEALTHY,UNHEALTHY): healthState("HEALTHY")

            Further information can be found at https://www.dynatrace.com/support/help/dynatrace-api/environment-api/entity-v2/.
            To set several criteria, separate them with a comma (,). For example, type("HOST"),healthState("HEALTHY").
            Only results matching all criteria are included in response.

            The length of the string is limited to 10,000 characters.

            The field is required when you're querying the first page of results.

        :param time_from: The start of the requested timeframe.

            You can use one of the following formats:

            Timestamp in UTC milliseconds.
            Human-readable format of 2019-12-21T05:57:01.123+01:00. If no time zone is specified, UTC is used. You can use a space character instead of the T. Seconds and fractions of a second are optional.
            Relative timeframe, back from now. The format is now-NU/A, where N is the amount of time, U is the unit of time, and A is an alignment. For example, now-1y/w is one year back, aligned by a week. The alignment rounds to the past. Supported time units for the relative timeframe are:
            m: minutes
            h: hours
            d: days
            w: weeks
            M: months
            y: years

            If not set, the relative timeframe of two weeks is used (now-2w).

        :param time_to: The end of the requested timeframe.

            You can use one of the following formats:

            Timestamp in UTC milliseconds.
            Human-readable format of 2019-12-21T05:57:01.123+01:00. If no time zone is specified, UTC is used. You can use a space character instead of the T. Seconds and fractions of a second are optional.
            Relative timeframe, back from now. The format is now-NU/A, where N is the amount of time, U is the unit of time, and A is an alignment. For example, now-1y/w is one year back, aligned by a week. The alignment rounds to the past. Supported time units for the relative timeframe are:
            m: minutes
            h: hours
            d: days
            w: weeks
            M: months
            y: years

            If not set, the relative timeframe of two weeks is used (now-2w).

        :param fields:  Defines the list of entity properties included in the response.
            The ID and the name of an entity are always included to the response.

            To add properties, list them with leading plus +. You can specify several properties,
            separated by a comma (for example fields=+lastSeenTms,+properties.BITNESS).

            Use the GET /entityTypes/{type} request to fetch the list of properties available for your entity type.
            Fields from the properties object must be specified in the properties.FIELD format (for example, properties.BITNESS).

        :param page_size: The desired amount of entities in a single response payload.
            The maximal allowed page size is configurable per environment.
            If not set, 50 is used.

        :return: A list of monitored entities along with their properties.
        """
        params = {"pageSize": page_size, "entitySelector": entity_selector, "from": time_from, "to": time_to, "fields": fields}
        return PaginatedList(Entity, self.__http_client, "/api/v2/entities", params, list_item="entities")

    def get_entity_types(self, page_size=50) -> PaginatedList[EntityType]:
        """
        Gets a list of properties for all entity types

        :param page_size: The desired amount of entities in a single response payload.
            The maximal allowed page size is 500.
            If not set, 50 is used.
        :return: A list of properties of all available entity types.
        """
        params = {"pageSize": page_size}
        return PaginatedList(EntityType, self.__http_client, "/api/v2/entityTypes", params, list_item="types")

    def query_metrics(
        self,
        metric_selector: str,
        page_size: int = None,
        resolution: str = None,
        time_from=None,
        time_to=None,
        entity_selector=None,
    ) -> PaginatedList[MetricSeriesCollection]:
        """
        Gets data points of the specified metrics

        :param metric_selector: Selects metrics for the query by their keys. You can select up to 10 metrics for one query.
            You can specify multiple metric keys separated by commas (for example, metrickey1,metrickey2).
            To select multiple metrics belonging to the same parent, list the last part of the required metric keys in parentheses, separated by commas,
            while keeping the common part untouched.
            For example, to list the builtin:host.cpu.idle and builtin:host.cpu.user metric, write: builtin:host.cpu.(idle,user).
            You can set additional transformation operators, separated by a colon (:).
            See the Metrics API - selector transformations help page for additional information on available result transformations.
            The length of the string is limited to 1,000 characters.

        :param page_size: The desired amount of primary entities in a single response payload.
            The maximal allowed page size is 5000.
            If not set, 100 is used.
            If a value higher than 5000 is used, only 5000 results per page are returned.

        :param resolution: The desired resolution of data points.
            You can use one of the following options:

            One aggregated data point of each series. Set Inf to use this option.
            The desired amount of data points. This is the default option.
            This is a reference number of points, which is not necessarily equal to the number of the returned data points.
            The desired timespan between data points. This is a reference timespan, which is not necessarily equal to the returned timespan.
            To use this option, specify the unit of the timespan.

            Valid units for the timespan are:

            m: minutes
            h: hours
            d: days
            w: weeks
            M: months
            y: years

            If not set, the default is 120 data points.

        :param time_from: The start of the requested timeframe.

            You can use one of the following formats:

            Timestamp in UTC milliseconds.
            Human-readable format of 2019-12-21T05:57:01.123+01:00. If no time zone is specified, UTC is used. You can use a space character instead of the T. Seconds and fractions of a second are optional.
            Relative timeframe, back from now. The format is now-NU/A, where N is the amount of time, U is the unit of time, and A is an alignment. For example, now-1y/w is one year back, aligned by a week. The alignment rounds to the past. Supported time units for the relative timeframe are:
            m: minutes
            h: hours
            d: days
            w: weeks
            M: months
            y: years

            If not set, the relative timeframe of two weeks is used (now-2w).

        :param time_to:
            The end of the requested timeframe.

            You can use one of the following formats:

            Timestamp in UTC milliseconds.
            Human-readable format of 2019-12-21T05:57:01.123+01:00. If no time zone is specified, UTC is used. You can use a space character instead of the T. Seconds and fractions of a second are optional.
            Relative timeframe, back from now. The format is now-NU/A, where N is the amount of time, U is the unit of time, and A is an alignment. For example, now-1y/w is one year back, aligned by a week. The alignment rounds to the past. Supported time units for the relative timeframe are:
            m: minutes
            h: hours
            d: days
            w: weeks
            M: months
            y: years

            If not set, the relative timeframe of two weeks is used (now-2w).

        :param entity_selector: Specifies the entity scope of the query. Only data points delivered by matched entities are included in response.
            You need to set one of these criteria:

            Entity type: type("value").
            Dynatrace entity ID: entityId("id"). You can specify several IDs, separated by a comma (entityId("id-1","id-2")).

            And you can add one or several of the following criteria:

            Tag: tag("value"). Tags in [context]key:value, key:value, and value formats are detected and parsed automatically. If a value-only tag has a colon (:) in it, you must escape the colon with a backslash(\). Otherwise, the tag will be parsed as a key:value tag. All tag values are case-sensitive.
            Management zone ID: mzId("ID")
            Management zone name: mzName("value"). Management zone names are case-sensitive.
            Dynatrace entity name: entityName("value"). You can specify several entity names, separated by a comma (entityName("name-1","name-2")). Entity names are case-sensitive.
            Health state (HEALTHY,UNHEALTHY): healthState("HEALTHY")

            Further information can be found here. To set several criteria, separate them with a comma (,). For example, type("HOST"),healthState("HEALTHY"). Only results matching all criteria are included in response.

            The length of the string is limited to 10,000 characters.
            Use the GET /metrics/{metricId} call to fetch the list of possible entity types for your metric.
            To set a universal scope matching all entities, omit this parameter.
        :return: A list of metrics and their data points.
        """

        params = {
            "pageSize": page_size,
            "metricSelector": metric_selector,
            "resolution": resolution,
            "from": time_from,
            "to": time_to,
            "entitySelector": entity_selector,
        }
        return PaginatedList(MetricSeriesCollection, self.__http_client, "/api/v2/metrics/query", params, list_item="result")

    def get_metrics(self, metric_selector: str = None, text: str = None, fields: str = None, page_size=100):
        """

        Lists all available metrics

        :param metric_selector: Selects metrics for the query by their keys.
            You can specify multiple metric keys separated by commas (for example, metrickey1,metrickey2).
            To select multiple metrics belonging to the same parent,
            list the last part of the required metric keys in parentheses, separated by commas,
            while keeping the common part untouched.
            For example, to list the builtin:host.cpu.idle and builtin:host.cpu.user metric, write: builtin:host.cpu.(idle,user).

            You can select a full set of related metrics by using a trailing asterisk (*) wildcard.
            For example, builtin:host.* selects all host-based metrics and builtin:* selects all Dynatrace-provided metrics.
            You can set additional transformation operators, separated by a colon (:).
            See the Metrics API - selector transformations help page for additional information on available result transformations.

            The length of the string is limited to 1,000 characters.
            To find metrics based on a search term, rather than metric_id, use the text query parameter instead of this one.

        :param text: Metric registry search term
            Only show metrics that contain the term in their ID, display name, or description.
            Use the metric_selector parameter instead of this one to select a complete metric hierarchy instead of doing a text-based search.

        :param fields: Defines the list of metric properties included in the response.
            metric_id is always included in the result. The following additional properties are available:
            display_name: The name of the metric in the user interface. Enabled by default.
            description: A short description of the metric. Enabled by default.
            unit: The unit of the metric. Enabled by default.
            aggregation_types: The list of allowed aggregations for the metric. Note that it may be different after a transformation is applied.
            default_aggregation: The default aggregation of the metric. It is used when no aggregation is specified or the :auto transformation is set.
            dimension_definitions: The fine metric division (for example, process group and process ID for some process-related metric).
            transformations: A list of transformations that can be applied to the metric.
            entity_type: A list of entity types supported by the metric.

            To add properties, list them with leading plus +. To exclude default properties, list them with leading minus -.

            To specify several properties, join them with a comma (for example fields=+aggregationTypes,-description).

            If you specify just one property, the response contains the metric key and the specified property.
            To return metric keys only, specify metric_id here.

        :param page_size: The desired amount of primary entities in a single response payload.
            The maximal allowed page size is 5000.
            If not set, 100 is used.
            If a value higher than 5000 is used, only 5000 results per page are returned.
        :return: A list of metric descriptors
        :rtype: PaginatedList[MetricDescriptor]
        """

        params = {
            "pageSize": page_size,
            "metricSelector": metric_selector,
            "text": text,
            "fields": fields,
        }
        return PaginatedList(MetricDescriptor, self.__http_client, "/api/v2/metrics", params, list_item="metrics")

    def get_metric(self, metric_id: str) -> MetricDescriptor:
        """
        Gets the descriptor of the specified metric

        :param metric_id: The key of the required metric.
            You can set additional transformation operators, separated by a colon (:). See the Metrics API - selector transformations help page for additional information on available result transformations.
            The length of the string is limited to 1,000 characters.
        :return: The metric descriptor
        """
        response = self.__http_client.make_request(f"/api/v2/metrics/{metric_id}").json()
        return MetricDescriptor(self.__http_client, None, response)

    def get_activegates(
        self,
        hostname: str = None,
        os_type: str = None,
        network_address: str = None,
        activegate_type: str = None,
        network_zone: str = None,
        update_status: str = None,
        version_compare_type: str = None,
        version: str = None,
    ) -> PaginatedList[ActiveGate]:
        """
        Lists all available ActiveGates

        :param hostname: Filters the resulting set of ActiveGates by the name of the host it's running on.
            You can specify a partial name. In that case, the CONTAINS operator is used.

        :param os_type: Filters the resulting set of ActiveGates by the OS type of the host it's running on.
            Available values : LINUX, WINDOWS

        :param network_address: Filters the resulting set of ActiveGates by the network address.
            You can specify a partial address. In that case, the CONTAINS operator is used.

        :param activegate_type: Filters the resulting set of ActiveGates by the ActiveGate type.
            Available values : ENVIRONMENT, ENVIRONMENT_MULTI

        :param network_zone: Filters the resulting set of ActiveGates by the network zone.
            You can specify a partial name. In that case, the CONTAINS operator is used.

        :param update_status: Filters the resulting set of ActiveGates by the auto-update status.
            Available values : INCOMPATIBLE, OUTDATED, SUPPRESSED, UNKNOWN, UP2DATE, UPDATE_IN_PROGRESS, UPDATE_PENDING, UPDATE_PROBLEM

        :param version_compare_type: Filters the resulting set of ActiveGates by the specified version.
            Specify the comparison operator here.
            Available values : EQUAL, GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL
            Default value : EQUAL

        :param version: Filters the resulting set of ActiveGates by the specified version.
            Specify the version in <major>.<minor>.<revision> format (for example, 1.195.0) here.

        :return: A list of ActiveGates.
        """
        params = {
            "hostname": hostname,
            "osType": os_type,
            "networkAddress": network_address,
            "ActivegateType": activegate_type,
            "networkZone": network_zone,
            "updateStatus": update_status,
            "versionCompareType": version_compare_type,
            "version": version,
        }
        return PaginatedList(ActiveGate, self.__http_client, "/api/v2/activeGates", params, list_item="activeGates")

    def get_plugins(self) -> PaginatedList[PluginShortRepresentation]:
        """
        List all uploaded plugins
        """
        return PaginatedList(PluginShortRepresentation, self.__http_client, "/api/config/v1/plugins", list_item="values")

    def get_plugin_states(self, plugin_id) -> PaginatedList[PluginState]:
        """
        List the states of the specified plugin
        """
        return PaginatedList(PluginState, self.__http_client, f"/api/config/v1/plugins/{plugin_id}/states", list_item="states")

    def delete_plugin(self, plugin_id) -> Response:
        """
        Deletes the ZIP file of the specified plugin
        :param plugin_id: The ID of the plugin to be deleted
        """
        return self.__http_client.make_request(f"/api/config/v1/plugins/{plugin_id}/binary", method="DELETE")

    def get_endpoints(self, plugin_id: str) -> PaginatedList[EndpointShortRepresentation]:
        """
        Lists endpoints of the specified ActiveGate plugin
        """
        return PaginatedList(
            EndpointShortRepresentation, self.__http_client, f"/api/config/v1/plugins/{plugin_id}/endpoints", list_item="values"
        )

    def get_dashboards(self, owner: str = None, tags: List[str] = None) -> PaginatedList[DashboardStub]:
        """
        Lists all dashboards of the environment
        :param owner: The owner of the dashboard.
        :param tags: A list of tags applied to the dashboard.
            The dashboard must match all the specified tags.
        """
        params = {"owner": owner, "tags": tags}
        return PaginatedList(DashboardStub, self.__http_client, f"/api/config/v1/dashboards", params, list_item="dashboards")

    def delete_dashboard(self, dashboard_id: str) -> Response:
        """
        Deletes the specified dashboard
        """
        return self.__http_client.make_request(f"/api/config/v1/dashboards/{dashboard_id}", method="DELETE")

    def get_dashboard(self, dashboard_id: str) -> Dashboard:
        """
        Gets the properties of the specified dashboard
        """
        response = self.__http_client.make_request(f"/api/config/v1/dashboards/{dashboard_id}").json()
        return Dashboard(self.__http_client, None, response)

    def get_extensions(self, page_size: int = 200) -> PaginatedList[ExtensionDto]:
        """
        List all uploaded extensions

        :param page_size: The number of results per result page. Must be between 1 and 500
            Default value : 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(ExtensionDto, self.__http_client, f"/api/config/v1/extensions", params, list_item="extensions")

    def get_extension(self, extension_id: str):
        response = self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}").json()
        return Extension(self.__http_client, None, response)

    def get_extension_instances(self, extension_id: str, page_size: int = 200) -> PaginatedList[ExtensionShortRepresentation]:
        params = {"pageSize": page_size}
        return PaginatedList(
            ExtensionShortRepresentation,
            self.__http_client,
            f"/api/config/v1/extensions/{extension_id}/instances",
            list_item="configurationsList",
            target_params=params,
        )

    def get_extension_instance(self, extension_id: str, configuration_id: str):
        response = self.__http_client.make_request(
            f"/api/config/v1/extensions/{extension_id}/instances/{configuration_id}"
        ).json()
        return ExtensionConfigurationDto(self.__http_client, None, response)

    def post_extension_instance(self, extension_configuration: ExtensionConfigurationDto):
        return extension_configuration.post()

    def create_extension_instance(
        self,
        extension_id: str,
        enabled: bool = True,
        use_global: bool = True,
        properties: dict = None,
        host_id: str = None,
        active_gate: EntityShortRepresentation = None,
        endpoint_id: str = None,
        endpoint_name: str = None,
    ) -> ExtensionConfigurationDto:

        return ExtensionConfigurationDto(
            self.__http_client, extension_id, enabled, use_global, properties, host_id, active_gate, endpoint_id, endpoint_name
        )

    def report_simple_thirdparty_synthetic_test(
        self,
        engine_name: str,
        timestamp: datetime,
        location_id: str,
        location_name: str,
        test_id: str,
        test_title: str,
        schedule_interval: int,
        success: bool,
        response_time: int,
        icon_url: str = None,
        edit_link: str = None,
        step_title: Optional[str] = None,
        detailed_steps: Optional[List[SyntheticTestStep]] = None,
        detailed_step_results: Optional[List[SyntheticMonitorStepResult]] = None,
    ):

        location = ThirdPartySyntheticLocation(self.__http_client, location_id, location_name)
        synthetic_location = SyntheticTestLocation(self.__http_client, location_id)
        if detailed_steps is None:
            detailed_steps = [SyntheticTestStep(self.__http_client, 1, step_title)]

        monitor = ThirdPartySyntheticMonitor(
            self.__http_client,
            test_id,
            test_title,
            [synthetic_location],
            schedule_interval,
            steps=detailed_steps,
            edit_link=edit_link,
        )
        if detailed_step_results is None:
            detailed_step_results = [
                SyntheticMonitorStepResult(self.__http_client, 1, timestamp, response_time_millis=response_time)
            ]
        location_result = ThirdPartySyntheticLocationTestResult(
            self.__http_client, location_id, timestamp, success, step_results=detailed_step_results
        )
        test_result = ThirdPartySyntheticResult(self.__http_client, test_id, len(detailed_steps), [location_result])
        tests = ThirdPartySyntheticTests(
            self.__http_client, engine_name, timestamp, [location], [monitor], [test_result], synthetic_engine_icon_url=icon_url
        )
        return tests.post()

    def create_synthetic_test_step_result(
        self, step_id: int, timestamp: datetime, response_time: int
    ) -> SyntheticMonitorStepResult:
        return SyntheticMonitorStepResult(self.__http_client, step_id, timestamp, response_time_millis=response_time)

    def create_synthetic_test_step(self, step_id: int, step_title: str) -> SyntheticTestStep:
        return SyntheticTestStep(self.__http_client, step_id, step_title)

    def report_simple_thirdparty_synthetic_test_event(
        self,
        test_id: str,
        name: str,
        location_id: str,
        timestamp: datetime,
        state: str,
        event_type: str,
        reason: str,
        engine_name: str,
    ):
        opened_events: List[ThirdPartyEventOpenNotification] = []
        resolved_events = []
        if state == "open":
            self.__open_third_party_events[test_id] += 1
            event_id = f"{test_id}_{self.__open_third_party_events[test_id]}"

            opened_events.append(
                ThirdPartyEventOpenNotification(
                    self.__http_client, test_id, event_id, name, event_type, reason, timestamp, [location_id]
                )
            )
        else:
            if test_id in self.__open_third_party_events:
                event_ids = [f"{test_id}_{i + 1}" for i in range(self.__open_third_party_events[test_id])]
                for event_id in event_ids:
                    resolved_events.append(ThirdPartyEventResolvedNotification(self.__http_client, test_id, event_id, timestamp))
                del self.__open_third_party_events[test_id]

        if opened_events or resolved_events:
            events = ThirdPartySyntheticEvents(self.__http_client, engine_name, opened_events, resolved_events)
            return events.post()

    def create_custom_device(
        self,
        device_id: str,
        display_name: Optional[str] = None,
        group: Optional[str] = None,
        ip_addresses: Optional[List[str]] = None,
        listen_ports: Optional[List[int]] = None,
        technology: Optional[str] = None,
        favicon: Optional[str] = None,
        config_url: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        series: Optional[List] = None,
        host_names: Optional[List[str]] = None,
    ) -> CustomDevicePushMessage:
        return CustomDevicePushMessage(
            self.__http_client,
            device_id=device_id,
            display_name=display_name,
            group=group,
            ip_addresses=ip_addresses,
            listen_ports=listen_ports,
            technology=technology,
            favicon=favicon,
            config_url=config_url,
            properties=properties,
            tags=tags,
            series=series,
            host_names=host_names,
        )

    def create_timeseries(
        self,
        metric_id: str,
        display_name: Optional[str],
        unit: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        technologies: Optional[List[str]] = None,
    ) -> TimeseriesRegistrationMessage:

        return TimeseriesRegistrationMessage(
            self.__http_client,
            metric_id=metric_id,
            display_name=display_name,
            unit=unit,
            dimensions=dimensions,
            technologies=technologies,
        )
