import json
import uuid
import xml.etree.ElementTree as ElementTree
from enum import Enum
from functools import reduce
from itertools import chain
from xml.dom import minidom

DEFAULT_XSI_PREFIX = "xsi"
DEFAULT_BPMN_PREFIX = "bpmn"
DEFAULT_BPMNDI_PREFIX = "bpmndi"
DEFAULT_DC_PREFIX = "dc"
DEFAULT_DI_PREFIX = "di"

INTERMEDIATE_CATCH_EVENT = "intermediateCatchEvent"
INTERMEDIATE_THROW_EVENT = "intermediateThrowEvent"


class BPMNElementType(str, Enum):
    BPMN_ANNOTATION = "BPMNAnnotation"
    BPMN_CALL_ACTIVITY = "BPMNCallActivity"
    BPMN_DATA_OBJECT = "BPMNDataObject"
    BPMN_DATA_STORE = "BPMNDataStore"
    BPMN_END_EVENT = "BPMNEndEvent"
    BPMN_GATEWAY = "BPMNGateway"
    BPMN_GROUP = "BPMNGroup"
    BPMN_INTERMEDIATE_EVENT = "BPMNIntermediateEvent"
    BPMN_POOL = "BPMNPool"
    BPMN_START_EVENT = "BPMNStartEvent"
    BPMN_SUBPROCESS = "BPMNSubprocess"
    BPMN_SWIMLANE = "BPMNSwimlane"
    BPMN_TASK = "BPMNTask"
    BPMN_TRANSACTION = "BPMNTransaction"


class BPMNStartEventType(str, Enum):
    DEFAULT = "default"
    MESSAGE = "message"
    TIMER = "timer"
    CONDITIONAL = "conditional"
    SIGNAL = "signal"


class BPMNIntermediateEventType(str, Enum):
    DEFAULT = "default"
    MESSAGE_CATCH = "message-catch"
    MESSAGE_THROW = "message-throw"
    TIMER_CATCH = "timer-catch"
    ESCALATION_CATCH = "escalation-catch"
    CONDITIONAL_CATCH = "conditional-catch"
    LINK_CATCH = "link-catch"
    LINK_THROW = "link-throw"
    COMPENSATION_THROW = "compensation-throw"
    SIGNAL_CATCH = "signal-catch"
    SIGNAL_THROW = "signal-throw"


class BPMNEndEventType(str, Enum):
    DEFAULT = "default"
    MESSAGE = "message"
    ESCALATION = "escalation"
    ERROR = "error"
    COMPENSATION = "compensation"
    SIGNAL = "signal"
    TERMINATE = "terminate"


class BPMNTaskType(str, Enum):
    DEFAULT = "default"
    USER = "user"
    SEND = "send"
    RECEIVE = "error"
    MANUAL = "manual"
    BUSINESS_RULE = "business-rule"
    SCRIPT = "script"


class BPMNGatewayType(str, Enum):
    COMPLEX = "complex"
    EVENT_BASED = "event-based"
    EXCLUSIVE = "exclusive"
    INCLUSIVE = "inclusive"
    PARALLEL = "parallel"


class BPMNSerializer:
    start_event_definition_map = {
        BPMNStartEventType.DEFAULT: None,
        BPMNStartEventType.MESSAGE: "messageEventDefinition",
        BPMNStartEventType.TIMER: "timerEventDefinition",
        BPMNStartEventType.SIGNAL: "signalEventDefinition",
        BPMNStartEventType.CONDITIONAL: "conditionalEventDefinition"
    }

    intermediate_event_type_map = {
        BPMNIntermediateEventType.DEFAULT: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.MESSAGE_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.MESSAGE_THROW: INTERMEDIATE_THROW_EVENT,
        BPMNIntermediateEventType.TIMER_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.ESCALATION_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.CONDITIONAL_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.LINK_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.LINK_THROW: INTERMEDIATE_THROW_EVENT,
        BPMNIntermediateEventType.COMPENSATION_THROW: INTERMEDIATE_THROW_EVENT,
        BPMNIntermediateEventType.SIGNAL_CATCH: INTERMEDIATE_CATCH_EVENT,
        BPMNIntermediateEventType.SIGNAL_THROW: INTERMEDIATE_THROW_EVENT
    }

    intermediate_event_definition_map = {
        BPMNIntermediateEventType.DEFAULT: None,
        BPMNIntermediateEventType.MESSAGE_CATCH: "messageEventDefinition",
        BPMNIntermediateEventType.MESSAGE_THROW: "messageEventDefinition",
        BPMNIntermediateEventType.TIMER_CATCH: "timerEventDefinition",
        BPMNIntermediateEventType.ESCALATION_CATCH: "escalationEventDefinition",
        BPMNIntermediateEventType.CONDITIONAL_CATCH: "conditionalEventDefinition",
        BPMNIntermediateEventType.LINK_CATCH: "linkEventDefinition",
        BPMNIntermediateEventType.LINK_THROW: "linkEventDefinition",
        BPMNIntermediateEventType.COMPENSATION_THROW: "compensationEventDefinition",
        BPMNIntermediateEventType.SIGNAL_CATCH: "signalEventDefinition",
        BPMNIntermediateEventType.SIGNAL_THROW: "signalEventDefinition"
    }

    end_event_definition_map = {
        BPMNEndEventType.DEFAULT: None,
        BPMNEndEventType.MESSAGE: "messageEventDefinition",
        BPMNEndEventType.ESCALATION: "escalationEventDefinition",
        BPMNEndEventType.ERROR: "errorEventDefinition",
        BPMNEndEventType.COMPENSATION: "compensationEventDefinition",
        BPMNEndEventType.SIGNAL: "signalEventDefinition",
        BPMNEndEventType.TERMINATE: "terminateEventDefinition"
    }

    task_type_map = {
        BPMNTaskType.DEFAULT: "task",
        BPMNTaskType.USER: "userTask",
        BPMNTaskType.SEND: "sendTask",
        BPMNTaskType.RECEIVE: "receive",
        BPMNTaskType.MANUAL: "manualTask",
        BPMNTaskType.BUSINESS_RULE: "businessRuleTask",
        BPMNTaskType.SCRIPT: "scriptTask"
    }

    gateway_type_map = {
        BPMNGatewayType.COMPLEX: "exclusiveGateway",
        BPMNGatewayType.EVENT_BASED: "eventBasedGateway",
        BPMNGatewayType.EXCLUSIVE: "exclusiveGateway",
        BPMNGatewayType.INCLUSIVE: "inclusiveGateway",
        BPMNGatewayType.PARALLEL: "parallelGateway"
    }

    xsi_prefix: str = ""
    bpmn_prefix: str = ""
    bpmndi_prefix: str = ""
    dc_prefix: str = ""
    di_prefix: str = ""

    def __init__(self,
                 xsi_prefix=DEFAULT_XSI_PREFIX,
                 bpmn_prefix=DEFAULT_BPMN_PREFIX,
                 bpmndi_prefix=DEFAULT_BPMNDI_PREFIX,
                 dc_prefix=DEFAULT_DC_PREFIX,
                 di_prefix=DEFAULT_DI_PREFIX
                 ):
        super().__init__()

        self.xsi_prefix = xsi_prefix
        self.bpmn_prefix = bpmn_prefix
        self.bpmndi_prefix = bpmndi_prefix
        self.dc_prefix = dc_prefix
        self.di_prefix = di_prefix

    @staticmethod
    def __prefix_tag(tag: str, prefix: str) -> str:
        """
        Prefix a XML tag with a given prefix
        :param tag: The prefixed tag
        :param prefix: The prefix to prepend
        """
        return f"{prefix}:{tag}"

    @staticmethod
    def __prefix_id(element_id: str, prefix: str = None) -> str:
        """
        Prefix an element id with a given prefix.
        If no prefix is provided, 'bpmn' is used as default.
        :param element_id: The element id that should be prefixed
        :param prefix: The prefix to prepend
        """
        if prefix is None:
            prefix = "bpmn"
        return f"{prefix}_{element_id}"

    @staticmethod
    def __omit_keys(dictionary: dict, omitted_keys: list) -> dict:
        """
        Copy a dictionary while omitting keys
        :param dictionary: The dictionary that is omitted from
        :param omitted_keys: A list of keys that should be omitted
        """
        return {key: dictionary[key] for key in dictionary.keys() if key not in omitted_keys}

    @staticmethod
    def __get_flows_connected_to_element(flows: list[dict], element_id: str) -> list[dict]:
        """
        Get all flows connected to an element
        :param flows: All flows in the diagram model
        :param element_id: The id of the element to which the retrieved flows should be connected to
        """
        return list(filter(lambda flow: flow.get("source").get("element") == element_id or flow.get("target").get(
            "element") == element_id, flows))

    def __serialize_base_element(self, element: dict, tag: str,
                                 connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN flow to XML
        :param element: A dictionary representing a BPMN flow element
        :param tag: The name of the tag the element should be serialized as
        :return: An Elementtree Element representing the serialized BPMN flow element
        """

        if connected_flows is None:
            connected_flows = []

        serialized_element: ElementTree.Element = ElementTree.Element(tag)
        serialized_element.set("id", self.__prefix_id(element.get("id")))
        serialized_element.set("name", element.get("name"))

        for connected_flow in connected_flows:
            if connected_flow.get("source").get("element") == element.get("id"):
                outgoing = ElementTree.Element(self.__prefix_tag("outgoing", self.bpmn_prefix))
                outgoing.text = self.__prefix_id(connected_flow.get("id"))
                serialized_element.append(outgoing)

            # This is deliberately not an "else" case as otherwise connections connecting an element with itself
            # would not be correctly serialized.
            if connected_flow.get("target").get("element") == element.get("id"):
                incoming = ElementTree.Element(self.__prefix_tag("incoming", self.bpmn_prefix))
                incoming.text = self.__prefix_id(connected_flow.get("id"))
                serialized_element.append(incoming)

        return serialized_element

    def __serialize_annotation(self, annotation: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN annotation object to XML
        :param annotation: A dictionary representing a BPMN annotation element
        :return: An Elementtree Element representing the serialized BPMN annotation element
        """

        tag: str = self.__prefix_tag("annotation", self.bpmn_prefix)
        serialized_annotation: ElementTree.Element = self.__serialize_base_element(annotation, tag, connected_flows)

        return serialized_annotation

    def __serialize_call_activity(self, call_activity: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize an BPMN call activity to XML
        :param call_activity: A dictionary representing an BPMN call activity element
        :return: An Elementtree Element representing the serialized BPMN call activity element
        """
        tag: str = self.__prefix_tag("callActivity", self.bpmn_prefix)
        serialized_call_activity: ElementTree.Element = self.__serialize_base_element(call_activity, tag,
                                                                                      connected_flows)

        return serialized_call_activity

    def __serialize_data_object(self, data_object: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN data object to XML
        :param data_object: A dictionary representing a BPMN data object element
        :return: An Elementtree Element representing the serialized BPMN data object element
        """
        tag: str = self.__prefix_tag("dataObject", self.bpmn_prefix)
        serialized_data_object: ElementTree.Element = self.__serialize_base_element(data_object, tag, connected_flows)

        return serialized_data_object

    def __serialize_data_store(self, data_store: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN data store object to XML
        :param data_store: A dictionary representing a BPMN data store element
        :return: An Elementtree Element representing the serialized BPMN data store element
        """
        tag: str = self.__prefix_tag("dataStore", self.bpmn_prefix)
        serialized_data_store: ElementTree.Element = self.__serialize_base_element(data_store, tag, connected_flows)

        return serialized_data_store

    def __serialize_end_event(self, end_event: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN end event object to XML
        :param end_event: A dictionary representing a BPMN end event element
        :return: An Elementtree Element representing the serialized BPMN end event element
        """
        tag: str = self.__prefix_tag("endEvent", self.bpmn_prefix)
        serialized_end_event: ElementTree.Element = self.__serialize_base_element(end_event, tag, connected_flows)

        event_type_tag: str = self.start_event_definition_map[end_event.get("eventType")]

        if event_type_tag:
            event_type_element: ElementTree.Element = ElementTree.Element(
                self.__prefix_tag(event_type_tag, self.bpmn_prefix))
            event_type_element.set("id", self.__prefix_id(str(uuid.uuid4())))
            serialized_end_event.append(event_type_element)

        return serialized_end_event

    def __serialize_flow(self, flow: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN flow to XML
        :param flow: A dictionary representing a BPMN flow element
        :return: An Elementtree Element representing the serialized BPMN flow element
        """
        tag: str = self.__prefix_tag("sequenceFlow", self.bpmn_prefix)
        serialized_flow: ElementTree.Element = self.__serialize_base_element(flow, tag, connected_flows)

        source_element: str = self.__prefix_id(flow.get("source").get("element"))
        target_element: str = self.__prefix_id(flow.get("target").get("element"))

        serialized_flow.set("sourceRef", source_element)
        serialized_flow.set("targetRef", target_element)

        return serialized_flow

    def __serialize_gateway(self, gateway: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN gateway object to XML
        :param gateway: A dictionary representing a BPMN gateway element
        :return: An Elementtree Element representing the serialized BPMN gateway element
        """
        gateway_type_tag: str = self.__prefix_tag(self.gateway_type_map[gateway.get("gatewayType")], self.bpmn_prefix)
        serialized_gateway = self.__serialize_base_element(gateway, gateway_type_tag, connected_flows)

        return serialized_gateway

    def __serialize_group(self, group: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN group to XML
        :param group: A dictionary representing a BPMN group element
        :return: An Elementtree Element representing the serialized BPMN group element
        """
        tag: str = self.__prefix_tag("group", self.bpmn_prefix)
        serialized_group: ElementTree.Element = self.__serialize_base_element(group, tag, connected_flows)

        return serialized_group

    def __serialize_intermediate_event(self, intermediate_event: dict,
                                       connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN intermediate event to XML
        :param intermediate_event: A dictionary representing a BPMN intermediate event element
        :return: An Elementtree Element representing the serialized BPMN intermediate event element
        """
        tag: str = self.__prefix_tag(self.intermediate_event_type_map[intermediate_event.get("eventType")],
                                     self.bpmn_prefix)
        serialized_intermediate_event: ElementTree.Element = self.__serialize_base_element(intermediate_event, tag,
                                                                                           connected_flows)

        event_type_tag: str = self.intermediate_event_definition_map[intermediate_event.get("eventType")]

        if event_type_tag:
            event_type_element = ElementTree.Element(self.__prefix_tag(event_type_tag, self.bpmn_prefix))
            event_type_element.set("id", self.__prefix_id(str(uuid.uuid4())))
            serialized_intermediate_event.append(event_type_element)

        return serialized_intermediate_event

    def __serialize_pool(self, pool: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN pool to XML
        :param pool: A dictionary representing a BPMN pool element
        :return: An Elementtree Element representing the serialized BPMN pool element
        """
        tag: str = self.__prefix_tag("laneSet", self.bpmn_prefix)
        serialized_pool: ElementTree.Element = self.__serialize_base_element(pool, tag, connected_flows)

        return serialized_pool

    def __serialize_start_event(self, start_event: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN start event to XML
        :param start_event: A dictionary representing a BPMN start event element
        :return: An Elementtree Element representing the serialized BPMN start event element
        """
        tag: str = self.__prefix_tag("startEvent", self.bpmn_prefix)
        serialized_start_event: ElementTree.Element = self.__serialize_base_element(start_event, tag, connected_flows)

        event_type_tag: str = self.start_event_definition_map[start_event.get("eventType")]

        if event_type_tag:
            event_type_element = ElementTree.Element(self.__prefix_tag(event_type_tag, self.bpmn_prefix))
            event_type_element.set("id", self.__prefix_id(str(uuid.uuid4())))
            serialized_start_event.append(event_type_element)

        return serialized_start_event

    def __serialize_subprocess(self, subprocess: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN subprocess to XML
        :param subprocess: A dictionary representing a BPMN subprocess element
        :return: An Elementtree Element representing the serialized BPMN subprocess element
        """
        tag: str = self.__prefix_tag("subprocess", self.bpmn_prefix)
        serialized_subprocess: ElementTree.Element = self.__serialize_base_element(subprocess, tag, connected_flows)

        return serialized_subprocess

    def __serialize_swimlane(self, swimlane: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN swimlane to XML
        :param swimlane: A dictionary representing a BPMN swimlane element
        :return: An Elementtree Element representing the serialized BPMN swimlane element
        """
        tag: str = self.__prefix_tag("swimlane", self.bpmn_prefix)
        serialized_swimlane: ElementTree.Element = self.__serialize_base_element(swimlane, tag, connected_flows)

        return serialized_swimlane

    def __serialize_task(self, task: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN task to XML
        :param task: A dictionary representing a BPMN task element
        :return: An Elementtree Element representing the serialized BPMN task element
        """
        task_tag: str = self.__prefix_tag(self.task_type_map[task.get("taskType")], self.bpmn_prefix)
        serialized_task: ElementTree.Element = self.__serialize_base_element(task, task_tag, connected_flows)

        return serialized_task

    def __serialize_transaction(self, transaction: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN transaction to XML
        :param transaction: A dictionary representing a BPMN transaction element
        :return: An Elementtree Element representing the serialized BPMN transaction element
        """
        tag: str = self.__prefix_tag("transaction", self.bpmn_prefix)
        serialized_transaction: ElementTree.Element = self.__serialize_base_element(transaction, tag, connected_flows)

        return serialized_transaction

    def __serialize_element(self, element: dict, connected_flows: list[dict] = None) -> ElementTree.Element:
        """
        Serialize a BPMN element to XML

        This method selects the serializer corresponding to the given element based on its type property
        :param element: A dictionary representing a BPMN element
        :return: An Elementtree Element representing the serialized BPMN element
        """

        match element.get("type"):
            case BPMNElementType.BPMN_ANNOTATION:
                return self.__serialize_annotation(element, connected_flows)
            case BPMNElementType.BPMN_CALL_ACTIVITY:
                return self.__serialize_call_activity(element, connected_flows)
            case BPMNElementType.BPMN_DATA_OBJECT:
                return self.__serialize_data_object(element, connected_flows)
            case BPMNElementType.BPMN_DATA_STORE:
                return self.__serialize_data_store(element, connected_flows)
            case BPMNElementType.BPMN_END_EVENT:
                return self.__serialize_end_event(element, connected_flows)
            case BPMNElementType.BPMN_GATEWAY:
                return self.__serialize_gateway(element, connected_flows)
            case BPMNElementType.BPMN_GROUP:
                return self.__serialize_group(element, connected_flows)
            case BPMNElementType.BPMN_INTERMEDIATE_EVENT:
                return self.__serialize_intermediate_event(element, connected_flows)
            case BPMNElementType.BPMN_POOL:
                return self.__serialize_pool(element, connected_flows)
            case BPMNElementType.BPMN_START_EVENT:
                return self.__serialize_start_event(element, connected_flows)
            case BPMNElementType.BPMN_SUBPROCESS:
                return self.__serialize_subprocess(element, connected_flows)
            case BPMNElementType.BPMN_SWIMLANE:
                return self.__serialize_swimlane(element, connected_flows)
            case BPMNElementType.BPMN_TASK:
                return self.__serialize_task(element, connected_flows)
            case BPMNElementType.BPMN_TRANSACTION:
                return self.__serialize_transaction(element, connected_flows)

    def __serialize_shape(self, element: dict) -> ElementTree.Element:
        """
        Serialize a BPMN element to a shape
        :param element: A dictionary representing a BPMN element
        :return: An Elementtree Element representing the serialized BPMN shape
        """

        tag: str = self.__prefix_tag("BPMNShape", self.bpmndi_prefix)
        serialized_shape: ElementTree.Element = ElementTree.Element(tag)
        serialized_shape.set("bpmnElement", self.__prefix_id(element.get("id")))

        bounds: dict = element.get("bounds")

        if bounds:
            serialized_bounds = ElementTree.Element("dc:Bounds")
            serialized_bounds.set("x", str(bounds.get("x")))
            serialized_bounds.set("y", str(bounds.get("y")))
            serialized_bounds.set("width", str(bounds.get("width")))
            serialized_bounds.set("height", str(bounds.get("height")))
            serialized_shape.append(serialized_bounds)

        return serialized_shape

    def __serialize_edge(self, relationship: dict) -> ElementTree.Element:
        """
        Serialize a BPMN relationship to an edge
        :param relationship: A dictionary representing a BPMN relationship
        :return: An Elementtree Element representing the serialized BPMN edge
        """

        tag: str = self.__prefix_tag("BPMNEdge", self.bpmndi_prefix)
        serialized_shape: ElementTree.Element = ElementTree.Element(tag)
        serialized_shape.set("bpmnElement", self.__prefix_id(relationship.get("id")))

        for point in relationship.get("path"):
            serialized_waypoint: ElementTree.Element = ElementTree.Element("di:waypoint")
            serialized_waypoint.set("x", str(point.get("x")))
            serialized_waypoint.set("y", str(point.get("y")))
            # serialized_shape.append(serialized_waypoint)

        return serialized_shape

    def __serialize_process(self, owned_elements: list[dict], relationships: list[dict]) -> ElementTree.Element:
        """
        Serialize the process tree of a given BPMN model
        :param owned_elements: A dictionary containing the elements owned by serialized process
        :param relationships: A dictionary the relationships contained in the diagram
        :return: An Elementtree Element representing the serialized BPMN process tree
        """

        process: ElementTree.Element = ElementTree.Element(self.__prefix_tag("process", self.bpmn_prefix))
        process.set("id", self.__prefix_id(str(uuid.uuid4())))
        process.set("isExecutable", "false")

        elements_by_type: dict[str, dict] = {}
        elements_by_owner: dict[str, dict] = {}

        serialized_relationships: list[ElementTree.Element] = []

        # We first gather all diagram elements and store them in index structures indexed
        # by the element type and by their owner
        for element in owned_elements:
            connected_flows = self.__get_flows_connected_to_element(relationships, element.get("id"))

            serialized_element = self.__serialize_element(element, connected_flows)

            element_type = element.get("type", "")

            if element_type:
                elements_by_type[element_type] = {
                    **elements_by_type.get(element_type, {}),
                    self.__prefix_id(element.get("id")): serialized_element
                }

            element_owner = self.__prefix_id(element.get("owner", ""))

            if element_owner:
                elements_by_owner[element_owner] = {
                    **elements_by_owner.get(element_owner, {}),
                    self.__prefix_id(element.get("id")): serialized_element
                }

        # We then gather all relationships
        for relationship in relationships:
            serialized_relationship = self.__serialize_flow(relationship)
            serialized_relationships.append(serialized_relationship)

        # Iterate over all pool elements and insert the owned swimlanes
        for serialized_pool in elements_by_type.get(BPMNElementType.BPMN_POOL, {}).values():
            owned_serialized_elements = elements_by_owner[serialized_pool.get("id")].values()

            for element in owned_serialized_elements:
                if elements_by_type.get(BPMNElementType.BPMN_SWIMLANE).get(element.get("id")):
                    # We know that the serialized element is a swimlane and therefore directly
                    # serialize it
                    serialized_pool.append(element)
                else:
                    # We know that the serialized element is noz swimlane and therefore insert
                    # a flow node ref for it
                    tag: str = self.__prefix_tag("flowNodeRef", self.bpmn_prefix)
                    flow_node_ref = ElementTree.Element(tag)
                    flow_node_ref.text = element.get("id")
                    serialized_pool.append(flow_node_ref)

            process.append(serialized_pool)

        # Iterate over all swimlanes and add flowNodeRefs for all elements within the current lane
        for serialized_swimlane in elements_by_type.get(BPMNElementType.BPMN_SWIMLANE, {}).values():
            owned_serialized_elements = elements_by_owner[serialized_swimlane.get("id")]
            for serialized_element in owned_serialized_elements.values():
                tag: str = self.__prefix_tag("flowNodeRef", self.bpmn_prefix)
                flow_node_ref = ElementTree.Element(tag)
                flow_node_ref.text = serialized_element.get("id")
                serialized_swimlane.append(flow_node_ref)

        # We get the dictionary of elements without pools and swimlanes
        non_bounding_elements = self.__omit_keys(elements_by_type, [
            BPMNElementType.BPMN_POOL,
            BPMNElementType.BPMN_SWIMLANE
        ])

        for serialized_element in chain.from_iterable([entry.values() for entry in non_bounding_elements.values()]):
            process.append(serialized_element)

        for relationship in serialized_relationships:
            process.append(relationship)

        return process

    def __serialize_plane(self, model: dict) -> ElementTree.Element:
        """
        Serialize the diagram tree of a given BPMN model
        :param model: A dictionary representing a BPMN diagram model
        :return: An Elementtree Element representing the serialized BPMN diagram tree
        """

        plane: ElementTree.Element = ElementTree.Element(self.__prefix_tag("BPMNPlane", self.bpmndi_prefix))
        plane.set("id", self.__prefix_id(str(uuid.uuid4())))
        plane.set("bpmnElement", "Minimal")

        for element in model.get("elements").values():
            serialized_shape: ElementTree.Element = self.__serialize_shape(element)
            plane.append(serialized_shape)

        for relationship in model.get("relationships").values():
            serialized_edge: ElementTree.Element = self.__serialize_edge(relationship)
            plane.append(serialized_edge)

        return plane

    def __split_elements_by_owning_pool(self, elements: dict) -> tuple[dict, list]:
        """
        Splits a given list of elements into a dictionary with the IDs of the root
        pool elements as keys and lists of elements contained within the respective pools
        as values. Elements that are not contained in a pool are returned as a list.
        :param elements: The list of elements that should be split
        :return: A tuple containing the dictionary of elements by owning pools and a list
        containing the elements without an owner.
        """
        elements_by_owning_pool = reduce(lambda acc, element: {
            **acc,
            element.get("id"): []
        } if element.get("type") == BPMNElementType.BPMN_POOL else acc, elements.values(), {})

        unowned_elements = []

        for element in elements:
            if not element.get("type") == BPMNElementType.BPMN_POOL:
                owner = self.__find_root_owner_id(elements, element.get("id"))

                # If the owner of an element is returned as the element's own ID,
                # the element is not contained in a pool. If the owner is not a key in the
                # elementy_by_owning_pool dictionary, we assume that the element is owned by
                # another container like a group that is not located within a pool.
                if owner == element.get("id") or not elements_by_owning_pool.get(owner, None):
                    unowned_elements.append(element)
                else:
                    elements_by_owning_pool[owner].append(element)

        return elements_by_owning_pool, unowned_elements

    def __find_root_owner_id(self, elements: dict, current_id: str) -> str:

        owner_id = elements.get(current_id).get("owner")

        if not owner_id:
            return current_id

        return self.__find_root_owner_id(elements, owner_id)

    def serialize(self, model: dict) -> ElementTree.Element:
        """
        Serialize a BPMN diagram in Apollon's native JSON format to XML according to the BPMN 2.0 standard
        :param model: A dictionary representing a BPMN diagram model
        :return: An Elementtree Element representing the serialized BPMN diagram
        """

        definitions: ElementTree.Element = ElementTree.Element(self.__prefix_tag("definitions", self.bpmn_prefix))

        definitions.set("id", "Definition")
        definitions.set(f"xmlns:{self.xsi_prefix}", "http://www.w3.org/2001/XMLSchema-instance")
        definitions.set(f"xmlns:{self.bpmn_prefix}", "http://www.omg.org/spec/BPMN/20100524/MODEL")
        definitions.set(f"xmlns:{self.bpmndi_prefix}", "http://www.omg.org/spec/BPMN/20100524/DI")
        definitions.set(f"xmlns:{self.dc_prefix}", "http://www.omg.org/spec/DD/20100524/DC")
        definitions.set(f"xmlns:{self.di_prefix}", "http://www.omg.org/spec/DD/20100524/DI")
        definitions.set("targetNamespace", "http://bpmn.io/schema/bpmn")

        elements_by_owning_pool, unowned_elements = self.__split_elements_by_owning_pool(model.get("elements", {}))

        relationships: list[dict] = list(model.get("relationships", {}).values())

        for owner in elements_by_owning_pool:
            serialized_process = self.__serialize_process(elements_by_owning_pool.get(owner), relationships)
            definitions.append(serialized_process)

        diagram: ElementTree.Element = ElementTree.Element(self.__prefix_tag("BPMNDiagram", self.bpmndi_prefix))
        serialized_plane = self.__serialize_plane(model)
        serialized_plane.set("bpmnElement", serialized_process.get("id"))
        diagram.append(serialized_plane)
        definitions.append(diagram)

        return definitions


if __name__ == "__main__":
    model = json.loads("""
        {
            "version": "3.0.0",
            "type": "BPMN",
            "size": {
                "width": 1540,
                "height": 940
            },
            "interactive": {
                "elements": {},
                "relationships": {}
            },
            "elements": {
                "57be7ebb-099e-47ec-bf5f-2d728437d987": {
                    "id": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "name": "Loan Applicant",
                    "type": "BPMNPool",
                    "owner": null,
                    "bounds": {
                        "x": 0,
                        "y": 0,
                        "width": 1370,
                        "height": 160
                    }
                },
                "6f8dba39-5d62-47d0-870b-37294b903ae7": {
                    "id": "6f8dba39-5d62-47d0-870b-37294b903ae7",
                    "name": "",
                    "type": "BPMNStartEvent",
                    "owner": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "bounds": {
                        "x": 60,
                        "y": 50,
                        "width": 40,
                        "height": 40
                    },
                    "eventType": "default"
                },
                "a3b67a31-a53e-4e20-9859-d1ee473e9e9f": {
                    "id": "a3b67a31-a53e-4e20-9859-d1ee473e9e9f",
                    "name": "Send credit request",
                    "type": "BPMNTask",
                    "owner": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "bounds": {
                        "x": 140,
                        "y": 40,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "909c768f-284b-42d3-9ec8-fbe7675b0f28": {
                    "id": "909c768f-284b-42d3-9ec8-fbe7675b0f28",
                    "name": "Quote received",
                    "type": "BPMNIntermediateEvent",
                    "owner": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "bounds": {
                        "x": 980,
                        "y": 50,
                        "width": 40,
                        "height": 40
                    },
                    "eventType": "message-catch"
                },
                "a5506560-9631-448f-85ee-aa42581ac048": {
                    "id": "a5506560-9631-448f-85ee-aa42581ac048",
                    "name": "Review quote",
                    "type": "BPMNTask",
                    "owner": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "bounds": {
                        "x": 1080,
                        "y": 40,
                        "width": 160,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "2dcc3930-cc74-41a9-bd7c-8218a2a14686": {
                    "id": "2dcc3930-cc74-41a9-bd7c-8218a2a14686",
                    "name": "",
                    "type": "BPMNEndEvent",
                    "owner": "57be7ebb-099e-47ec-bf5f-2d728437d987",
                    "bounds": {
                        "x": 1310,
                        "y": 50,
                        "width": 40,
                        "height": 40
                    },
                    "eventType": "default"
                },
                "e975fb67-ccc1-4373-b214-d3e8742930aa": {
                    "id": "e975fb67-ccc1-4373-b214-d3e8742930aa",
                    "name": "Credit Institute",
                    "type": "BPMNPool",
                    "owner": null,
                    "bounds": {
                        "x": 0,
                        "y": 200,
                        "width": 1370,
                        "height": 430
                    }
                },
                "607b811b-ab82-4aad-91c2-6bed096b5cc8": {
                    "id": "607b811b-ab82-4aad-91c2-6bed096b5cc8",
                    "name": "Loan Assessor",
                    "type": "BPMNSwimlane",
                    "owner": "e975fb67-ccc1-4373-b214-d3e8742930aa",
                    "bounds": {
                        "x": 40,
                        "y": 470,
                        "width": 1330,
                        "height": 160
                    }
                },
                "a78c7661-7823-4d40-9753-a87a92f3bc93": {
                    "id": "a78c7661-7823-4d40-9753-a87a92f3bc93",
                    "name": "Assess risk",
                    "type": "BPMNTask",
                    "owner": "607b811b-ab82-4aad-91c2-6bed096b5cc8",
                    "bounds": {
                        "x": 530,
                        "y": 520,
                        "width": 160,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "bde0718c-a52d-4141-a6d5-d697398a1ab2": {
                    "id": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "name": "Loan Provider",
                    "type": "BPMNSwimlane",
                    "owner": "e975fb67-ccc1-4373-b214-d3e8742930aa",
                    "bounds": {
                        "x": 40,
                        "y": 200,
                        "width": 1330,
                        "height": 270
                    }
                },
                "f108cf07-c22c-4284-b9ba-0b4af908c7ad": {
                    "id": "f108cf07-c22c-4284-b9ba-0b4af908c7ad",
                    "name": "Review request",
                    "type": "BPMNTask",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 270,
                        "y": 230,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "6ebb416a-1a47-49cf-9ba1-7ffdcb5dea56": {
                    "id": "6ebb416a-1a47-49cf-9ba1-7ffdcb5dea56",
                    "name": "Credit request received",
                    "type": "BPMNIntermediateEvent",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 190,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "eventType": "default"
                },
                "ab792872-1b3f-4d7a-afb6-aa01b1d7f785": {
                    "id": "ab792872-1b3f-4d7a-afb6-aa01b1d7f785",
                    "name": "",
                    "type": "BPMNGateway",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 450,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "gatewayType": "parallel"
                },
                "e206ad60-29b0-4bfc-8e5d-08eb28c31942": {
                    "id": "e206ad60-29b0-4bfc-8e5d-08eb28c31942",
                    "name": "Standard terms applicable?",
                    "type": "BPMNGateway",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 530,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "gatewayType": "exclusive"
                },
                "531d5776-832d-4ab0-b76c-dba85ec2d8a0": {
                    "id": "531d5776-832d-4ab0-b76c-dba85ec2d8a0",
                    "name": "Calculate terms",
                    "type": "BPMNTask",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 610,
                        "y": 230,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "b31e8aaa-54f2-4a36-8fd0-c374045c836c": {
                    "id": "b31e8aaa-54f2-4a36-8fd0-c374045c836c",
                    "name": "",
                    "type": "BPMNGateway",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 790,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "gatewayType": "exclusive"
                },
                "e409e5b5-ab11-45e7-ba78-4266473ecc17": {
                    "id": "e409e5b5-ab11-45e7-ba78-4266473ecc17",
                    "name": "Send quote",
                    "type": "BPMNTask",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 1130,
                        "y": 230,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "acf010ad-0c8c-4a9a-8949-52e17f13e55c": {
                    "id": "acf010ad-0c8c-4a9a-8949-52e17f13e55c",
                    "name": "Quote sent",
                    "type": "BPMNEndEvent",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 1310,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "eventType": "default"
                },
                "bdfce06b-db3e-45c8-9976-4ef57108218b": {
                    "id": "bdfce06b-db3e-45c8-9976-4ef57108218b",
                    "name": "",
                    "type": "BPMNGateway",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 1050,
                        "y": 240,
                        "width": 40,
                        "height": 40
                    },
                    "gatewayType": "parallel"
                },
                "be966228-7ed4-42c4-ad79-432f459f9feb": {
                    "id": "be966228-7ed4-42c4-ad79-432f459f9feb",
                    "name": "Prepare special terms",
                    "type": "BPMNTask",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 610,
                        "y": 380,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                },
                "1acbea80-c430-46f2-b7d2-a44a1bc1639c": {
                    "id": "1acbea80-c430-46f2-b7d2-a44a1bc1639c",
                    "name": "Prepare contract",
                    "type": "BPMNTask",
                    "owner": "bde0718c-a52d-4141-a6d5-d697398a1ab2",
                    "bounds": {
                        "x": 870,
                        "y": 230,
                        "width": 140,
                        "height": 60
                    },
                    "taskType": "default",
                    "marker": "none"
                }
            },
            "relationships": {
                "a6626dca-b9c5-45b5-9309-e5f0a3fb9a4f": {
                    "id": "a6626dca-b9c5-45b5-9309-e5f0a3fb9a4f",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 100,
                        "y": 70,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "6f8dba39-5d62-47d0-870b-37294b903ae7"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "a3b67a31-a53e-4e20-9859-d1ee473e9e9f"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "e81e5161-51c8-41b8-89f0-66e36da614c1": {
                    "id": "e81e5161-51c8-41b8-89f0-66e36da614c1",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 280,
                        "y": 70,
                        "width": 700,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 700,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "a3b67a31-a53e-4e20-9859-d1ee473e9e9f"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "909c768f-284b-42d3-9ec8-fbe7675b0f28"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "ca2e5065-6ee1-4548-8bcd-502077fa3e73": {
                    "id": "ca2e5065-6ee1-4548-8bcd-502077fa3e73",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 230,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "6ebb416a-1a47-49cf-9ba1-7ffdcb5dea56"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "f108cf07-c22c-4284-b9ba-0b4af908c7ad"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "73825150-a5bb-41ab-b557-cf36fdccb0a4": {
                    "id": "73825150-a5bb-41ab-b557-cf36fdccb0a4",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 210,
                        "y": 100,
                        "width": 1,
                        "height": 140
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 140
                        }
                    ],
                    "source": {
                        "direction": "Down",
                        "element": "a3b67a31-a53e-4e20-9859-d1ee473e9e9f"
                    },
                    "target": {
                        "direction": "Up",
                        "element": "6ebb416a-1a47-49cf-9ba1-7ffdcb5dea56"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "message"
                },
                "266c4919-88ad-4c2c-a1e4-c14947f44cde": {
                    "id": "266c4919-88ad-4c2c-a1e4-c14947f44cde",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 470,
                        "y": 280,
                        "width": 60,
                        "height": 270
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 270
                        },
                        {
                            "x": 60,
                            "y": 270
                        }
                    ],
                    "source": {
                        "direction": "Down",
                        "element": "ab792872-1b3f-4d7a-afb6-aa01b1d7f785"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "a78c7661-7823-4d40-9753-a87a92f3bc93"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "b605327e-6a48-4f12-a4d4-97665fb7f230": {
                    "id": "b605327e-6a48-4f12-a4d4-97665fb7f230",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 410,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "f108cf07-c22c-4284-b9ba-0b4af908c7ad"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "ab792872-1b3f-4d7a-afb6-aa01b1d7f785"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "33a69e1c-102b-498b-bb3b-c733c17c77bc": {
                    "id": "33a69e1c-102b-498b-bb3b-c733c17c77bc",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 490,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "ab792872-1b3f-4d7a-afb6-aa01b1d7f785"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "e206ad60-29b0-4bfc-8e5d-08eb28c31942"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "66fe2424-b0cc-4e50-988c-f0910dd92aa6": {
                    "id": "66fe2424-b0cc-4e50-988c-f0910dd92aa6",
                    "name": "yes",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 570,
                        "y": 220,
                        "width": 40,
                        "height": 41
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 40
                        },
                        {
                            "x": 40,
                            "y": 40
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "e206ad60-29b0-4bfc-8e5d-08eb28c31942"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "531d5776-832d-4ab0-b76c-dba85ec2d8a0"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "8263561f-d70e-4264-8e6e-6d545c9d4d57": {
                    "id": "8263561f-d70e-4264-8e6e-6d545c9d4d57",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 750,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "531d5776-832d-4ab0-b76c-dba85ec2d8a0"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "b31e8aaa-54f2-4a36-8fd0-c374045c836c"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "2c669dc1-ec78-4ce9-af27-6fd58b5f4e17": {
                    "id": "2c669dc1-ec78-4ce9-af27-6fd58b5f4e17",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1090,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "bdfce06b-db3e-45c8-9976-4ef57108218b"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "e409e5b5-ab11-45e7-ba78-4266473ecc17"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "3eae3c61-5acf-4687-95d0-c5e16bb689b2": {
                    "id": "3eae3c61-5acf-4687-95d0-c5e16bb689b2",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 830,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "b31e8aaa-54f2-4a36-8fd0-c374045c836c"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "1acbea80-c430-46f2-b7d2-a44a1bc1639c"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "c09d469a-0377-47f1-a2b5-6662f2afc0b1": {
                    "id": "c09d469a-0377-47f1-a2b5-6662f2afc0b1",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1010,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "1acbea80-c430-46f2-b7d2-a44a1bc1639c"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "bdfce06b-db3e-45c8-9976-4ef57108218b"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "a72d62b3-e113-4b90-bfd9-2480861d1186": {
                    "id": "a72d62b3-e113-4b90-bfd9-2480861d1186",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1270,
                        "y": 260,
                        "width": 40,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 40,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "e409e5b5-ab11-45e7-ba78-4266473ecc17"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "acf010ad-0c8c-4a9a-8949-52e17f13e55c"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "70b979b6-32e9-45c7-be45-518507652a30": {
                    "id": "70b979b6-32e9-45c7-be45-518507652a30",
                    "name": "no",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 550,
                        "y": 280,
                        "width": 60,
                        "height": 130
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 0,
                            "y": 130
                        },
                        {
                            "x": 60,
                            "y": 130
                        }
                    ],
                    "source": {
                        "direction": "Down",
                        "element": "e206ad60-29b0-4bfc-8e5d-08eb28c31942"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "be966228-7ed4-42c4-ad79-432f459f9feb"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "c6ac591f-51fd-4c6e-bdfa-ae74a029d73d": {
                    "id": "c6ac591f-51fd-4c6e-bdfa-ae74a029d73d",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 750,
                        "y": 280,
                        "width": 60,
                        "height": 130
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 130
                        },
                        {
                            "x": 60,
                            "y": 130
                        },
                        {
                            "x": 60,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "be966228-7ed4-42c4-ad79-432f459f9feb"
                    },
                    "target": {
                        "direction": "Down",
                        "element": "b31e8aaa-54f2-4a36-8fd0-c374045c836c"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "60e891d4-0604-45e4-b2c7-b6d6b9f72ba2": {
                    "id": "60e891d4-0604-45e4-b2c7-b6d6b9f72ba2",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 690,
                        "y": 280,
                        "width": 380,
                        "height": 270
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 270
                        },
                        {
                            "x": 380,
                            "y": 270
                        },
                        {
                            "x": 380,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "a78c7661-7823-4d40-9753-a87a92f3bc93"
                    },
                    "target": {
                        "direction": "Down",
                        "element": "bdfce06b-db3e-45c8-9976-4ef57108218b"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "2bcae199-700f-44b9-93e1-2dacb6061bd8": {
                    "id": "2bcae199-700f-44b9-93e1-2dacb6061bd8",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1240,
                        "y": 70,
                        "width": 70,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 70,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "a5506560-9631-448f-85ee-aa42581ac048"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "2dcc3930-cc74-41a9-bd7c-8218a2a14686"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "b409934a-f4ad-4bcb-a157-4457c97e17fb": {
                    "id": "b409934a-f4ad-4bcb-a157-4457c97e17fb",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1020,
                        "y": 70,
                        "width": 60,
                        "height": 1
                    },
                    "path": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 60,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Right",
                        "element": "909c768f-284b-42d3-9ec8-fbe7675b0f28"
                    },
                    "target": {
                        "direction": "Left",
                        "element": "a5506560-9631-448f-85ee-aa42581ac048"
                    },
                    "isManuallyLayouted": false,
                    "flowType": "sequence"
                },
                "aec45998-06bb-4213-a615-8e512c05a855": {
                    "id": "aec45998-06bb-4213-a615-8e512c05a855",
                    "name": "",
                    "type": "BPMNFlow",
                    "owner": null,
                    "bounds": {
                        "x": 1000,
                        "y": 90,
                        "width": 200,
                        "height": 140
                    },
                    "path": [
                        {
                            "x": 200,
                            "y": 140
                        },
                        {
                            "x": 200,
                            "y": 88.39453125
                        },
                        {
                            "x": 0,
                            "y": 88.39453125
                        },
                        {
                            "x": 0,
                            "y": 0
                        }
                    ],
                    "source": {
                        "direction": "Up",
                        "element": "e409e5b5-ab11-45e7-ba78-4266473ecc17"
                    },
                    "target": {
                        "direction": "Down",
                        "element": "909c768f-284b-42d3-9ec8-fbe7675b0f28"
                    },
                    "isManuallyLayouted": true,
                    "flowType": "message"
                }
            },
            "assessments": {}
        }
    """)

    model2 = json.loads(
        """{"version":"3.0.0","type":"BPMN","size":{"width":920,"height":440},"interactive":{"elements":{},"relationships":{}},"elements":{"b83370ae-4c60-48de-b2e7-b472c100e500":{"id":"b83370ae-4c60-48de-b2e7-b472c100e500","name":"Order Received","type":"BPMNStartEvent","owner":null,"bounds":{"x":0,"y":0,"width":40,"height":40},"eventType":"message"},"8fd5fbe0-f81d-457a-b7f6-c009e8fc394c":{"id":"8fd5fbe0-f81d-457a-b7f6-c009e8fc394c","name":"Bake Pizza","type":"BPMNTask","owner":null,"bounds":{"x":90,"y":0,"width":130,"height":40},"taskType":"default","marker":"none"},"001ff705-6703-49f4-ab68-e79a066596b8":{"id":"001ff705-6703-49f4-ab68-e79a066596b8","name":"Deliver Pizza","type":"BPMNTask","owner":null,"bounds":{"x":270,"y":0,"width":160,"height":40},"taskType":"default","marker":"none"},"561c077d-b2e0-4788-8436-278ee6b50adb":{"id":"561c077d-b2e0-4788-8436-278ee6b50adb","name":"","type":"BPMNEndEvent","owner":null,"bounds":{"x":480,"y":0,"width":40,"height":40},"eventType":"default"}},"relationships":{"22cbf288-11a6-462f-9540-c3d38b6dcfa8":{"id":"22cbf288-11a6-462f-9540-c3d38b6dcfa8","name":"","type":"BPMNFlow","owner":null,"bounds":{"x":40,"y":20,"width":50,"height":1},"path":[{"x":0,"y":0},{"x":50,"y":0}],"source":{"direction":"Right","element":"b83370ae-4c60-48de-b2e7-b472c100e500"},"target":{"direction":"Left","element":"8fd5fbe0-f81d-457a-b7f6-c009e8fc394c"},"isManuallyLayouted":false,"flowType":"sequence"},"c0fcff31-a656-4d2a-8bd9-5ef6bec80646":{"id":"c0fcff31-a656-4d2a-8bd9-5ef6bec80646","name":"","type":"BPMNFlow","owner":null,"bounds":{"x":220,"y":20,"width":50,"height":1},"path":[{"x":0,"y":0},{"x":50,"y":0}],"source":{"direction":"Right","element":"8fd5fbe0-f81d-457a-b7f6-c009e8fc394c"},"target":{"direction":"Left","element":"001ff705-6703-49f4-ab68-e79a066596b8"},"isManuallyLayouted":false,"flowType":"sequence"},"335069fe-4456-40df-bfc5-f1e1379e4010":{"id":"335069fe-4456-40df-bfc5-f1e1379e4010","name":"","type":"BPMNFlow","owner":null,"bounds":{"x":430,"y":20,"width":50,"height":1},"path":[{"x":0,"y":0},{"x":50,"y":0}],"source":{"direction":"Right","element":"001ff705-6703-49f4-ab68-e79a066596b8"},"target":{"direction":"Left","element":"561c077d-b2e0-4788-8436-278ee6b50adb"},"isManuallyLayouted":false,"flowType":"sequence"}},"assessments":{}}""")

    bpmn_serializer = BPMNSerializer()

    serialized_model = bpmn_serializer.serialize(model2)
    ElementTree.indent(serialized_model, space="\t", level=0)

    print(minidom.parseString(
        ElementTree.tostring(bpmn_serializer.serialize(model), encoding='utf8', xml_declaration=True)).toprettyxml(
        indent="\t"))
