import json
import uuid
import xml.etree.ElementTree as ElementTree
from enum import Enum


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


class BPMNSerializer:
    start_event_type_map = {
        "default": None,
        "message": "messageEventDefinition",
        "timer": "timerEventDefinition",
        "signal": "signalEventDefinition",
        "conditional": "conditionalEventDefinition"
    }

    intermediate_event_type_map = {
        "default": None,
        "message-catch": "messageCatchEventDefinition",
        "message-throw": "messageThrowEventDefinition",
        "timer-catch": "timerCatchEventDefinition",
        "escalation-catch": "escalationCatchEventDefinition",
        "conditional-catch": "conditionalCatchEventDefinition",
        "link-catch": "linkCatchEventDefinition",
        "link-throw": "linkThrowEventDefinition",
        "compensation-throw": "compensationThrowEventDefinition",
        "signal-catch": "signalCatchEventDefinition",
        "signal-throw": "signalThrowEventDefinition"
    }

    end_event_type_map = {
        "default": None,
        "message": "messageEventDefinition",
        "escalation": "escalationEventDefinition",
        "error": "errorEventDefinition",
        "compensation": "compensationEventDefinition",
        "signal": "signalEventDefinition",
        "terminate": "terminateEventDefinition"
    }

    task_type_map = {
        "default": "task",
        "user": "userTask",
        "send": "sendTask",
        "receive": "receiveTask",
        "manual": "manualTask",
        "business-rule": "businessRuleTask",
        "script": "scriptTask"
    }

    gateway_type_map = {
        "complex": "exclusiveGateway",
        "event-based": "eventBasedGateway",
        "exclusive": "exclusiveGateway",
        "inclusive": "inclusiveGateway",
        "parallel": "parallelGateway"
    }

    @staticmethod
    def __serialize_base_element(element: dict, tag: str) -> ElementTree.Element:
        """
        Serialize a BPMN flow to XML
        :param element: A dictionary representing a BPMN flow element
        :param tag: The name of the tag the element should be serialized as
        :return: An Elementtree Element representing the serialized BPMN flow element
        """
        serialized_element = ElementTree.Element(tag)
        serialized_element.set("id", element.get("id"))
        serialized_element.set("name", element.get("name"))

        return serialized_element

    @staticmethod
    def __serialize_annotation(annotation: dict) -> ElementTree.Element:
        """
        Serialize a BPMN annotation object to XML
        :param annotation: A dictionary representing a BPMN annotation element
        :return: An Elementtree Element representing the serialized BPMN annotation element
        """
        serialized_annotation = BPMNSerializer.__serialize_base_element(annotation, "annotation")

        return serialized_annotation

    @staticmethod
    def __serialize_call_activity(call_activity: dict) -> ElementTree.Element:
        """
        Serialize an BPMN call activity to XML
        :param call_activity: A dictionary representing an BPMN call activity element
        :return: An Elementtree Element representing the serialized BPMN call activity element
        """
        serialized_call_activity = BPMNSerializer.__serialize_base_element(call_activity, "callActivity")

        return serialized_call_activity

    @staticmethod
    def __serialize_data_object(data_object: dict) -> ElementTree.Element:
        """
        Serialize a BPMN data object to XML
        :param data_object: A dictionary representing a BPMN data object element
        :return: An Elementtree Element representing the serialized BPMN data object element
        """
        serialized_data_object = BPMNSerializer.__serialize_base_element(data_object, "dataObject")

        return serialized_data_object

    @staticmethod
    def __serialize_data_store(data_store: dict) -> ElementTree.Element:
        """
        Serialize a BPMN data store object to XML
        :param data_store: A dictionary representing a BPMN data store element
        :return: An Elementtree Element representing the serialized BPMN data store element
        """
        serialized_data_store = BPMNSerializer.__serialize_base_element(data_store, "dataStore")

        return serialized_data_store

    @staticmethod
    def __serialize_end_event(end_event: dict) -> ElementTree.Element:
        """
        Serialize a BPMN end event object to XML
        :param end_event: A dictionary representing a BPMN end event element
        :return: An Elementtree Element representing the serialized BPMN end event element
        """
        serialized_end_event = BPMNSerializer.__serialize_base_element(end_event, "endEvent")

        event_type_tag = BPMNSerializer.start_event_type_map[end_event.get("eventType")]

        if event_type_tag:
            event_type_element = ElementTree.Element(event_type_tag)
            event_type_element.set("id", str(uuid.uuid4()))
            serialized_end_event.append(event_type_element)

        return serialized_end_event

    @staticmethod
    def __serialize_flow(flow: dict) -> ElementTree.Element:
        """
        Serialize a BPMN flow to XML
        :param flow: A dictionary representing a BPMN flow element
        :return: An Elementtree Element representing the serialized BPMN flow element
        """
        serialized_flow = BPMNSerializer.__serialize_base_element(flow, "sequenceFlow")

        source_element = flow.get("source").get("element")
        target_element = flow.get("target").get("element")

        serialized_flow.set("sourceRef", source_element)
        serialized_flow.set("targetRef", target_element)

        return serialized_flow

    @staticmethod
    def __serialize_gateway(gateway: dict) -> ElementTree.Element:
        """
        Serialize a BPMN gateway object to XML
        :param gateway: A dictionary representing a BPMN gateway element
        :return: An Elementtree Element representing the serialized BPMN gateway element
        """
        gateway_type_tag = BPMNSerializer.gateway_type_map[gateway.get("gatewayType")]
        serialized_gateway = BPMNSerializer.__serialize_base_element(gateway, gateway_type_tag)

        return serialized_gateway

    @staticmethod
    def __serialize_group(group: dict) -> ElementTree.Element:
        """
        Serialize a BPMN group to XML
        :param group: A dictionary representing a BPMN group element
        :return: An Elementtree Element representing the serialized BPMN group element
        """
        serialized_group = BPMNSerializer.__serialize_base_element(group, "group")

        return serialized_group

    @staticmethod
    def __serialize_intermediate_event(intermediate_event: dict) -> ElementTree.Element:
        """
        Serialize a BPMN intermediate event to XML
        :param intermediate_event: A dictionary representing a BPMN intermediate event element
        :return: An Elementtree Element representing the serialized BPMN intermediate event element
        """
        serialized_intermediate_event = BPMNSerializer.__serialize_base_element(intermediate_event, "intermediateEvent")

        event_type_tag = BPMNSerializer.intermediate_event_type_map[intermediate_event.get("eventType")]

        if event_type_tag:
            event_type_element = ElementTree.Element(event_type_tag)
            event_type_element.set("id", str(uuid.uuid4()))
            serialized_intermediate_event.append(event_type_element)

        return serialized_intermediate_event

    @staticmethod
    def __serialize_pool(pool: dict) -> ElementTree.Element:
        """
        Serialize a BPMN pool to XML
        :param pool: A dictionary representing a BPMN pool element
        :return: An Elementtree Element representing the serialized BPMN pool element
        """
        serialized_pool = BPMNSerializer.__serialize_base_element(pool, "pool")

        return serialized_pool

    @staticmethod
    def __serialize_start_event(start_event: dict) -> ElementTree.Element:
        """
        Serialize a BPMN start event to XML
        :param start_event: A dictionary representing a BPMN start event element
        :return: An Elementtree Element representing the serialized BPMN start event element
        """
        serialized_start_event = BPMNSerializer.__serialize_base_element(start_event, "startEvent")

        event_type_tag = BPMNSerializer.start_event_type_map[start_event.get("eventType")]

        if event_type_tag:
            event_type_element = ElementTree.Element(event_type_tag)
            event_type_element.set("id", str(uuid.uuid4()))
            serialized_start_event.append(event_type_element)

        return serialized_start_event

    @staticmethod
    def __serialize_subprocess(subprocess: dict) -> ElementTree.Element:
        """
        Serialize a BPMN subprocess to XML
        :param subprocess: A dictionary representing a BPMN subprocess element
        :return: An Elementtree Element representing the serialized BPMN subprocess element
        """
        serialized_subprocess = BPMNSerializer.__serialize_base_element(subprocess, "subprocess")

        return serialized_subprocess

    @staticmethod
    def __serialize_swimlane(swimlane: dict) -> ElementTree.Element:
        """
        Serialize a BPMN swimlane to XML
        :param swimlane: A dictionary representing a BPMN swimlane element
        :return: An Elementtree Element representing the serialized BPMN swimlane element
        """
        serialized_swimlane = BPMNSerializer.__serialize_base_element(swimlane, "swimlane")

        return serialized_swimlane

    @staticmethod
    def __serialize_task(task: dict) -> ElementTree.Element:
        """
        Serialize a BPMN task to XML
        :param task: A dictionary representing a BPMN task element
        :return: An Elementtree Element representing the serialized BPMN task element
        """
        task_tag = BPMNSerializer.task_type_map[task.get("taskType")]
        serialized_task = BPMNSerializer.__serialize_base_element(task, task_tag)

        return serialized_task

    @staticmethod
    def __serialize_transaction(transaction: dict) -> ElementTree.Element:
        """
        Serialize a BPMN transaction to XML
        :param transaction: A dictionary representing a BPMN transaction element
        :return: An Elementtree Element representing the serialized BPMN transaction element
        """
        serialized_transaction = BPMNSerializer.__serialize_base_element(transaction, "transaction")

        return serialized_transaction

    @staticmethod
    def __serialize_element(element: dict) -> ElementTree.Element:
        """
        Serialize a BPMN element to XML

        This method selects the serializer corresponding to the given element based on its type property
        :param element: A dictionary representing a BPMN element
        :return: An Elementtree Element representing the serialized BPMN element
        """

        serialized_element = None

        match element.get("type"):
            case BPMNElementType.BPMN_ANNOTATION:
                serialized_element = BPMNSerializer.__serialize_annotation(element)
            case BPMNElementType.BPMN_CALL_ACTIVITY:
                serialized_element = BPMNSerializer.__serialize_call_activity(element)
            case BPMNElementType.BPMN_DATA_OBJECT:
                serialized_element = BPMNSerializer.__serialize_data_object(element)
            case BPMNElementType.BPMN_DATA_STORE:
                serialized_element = BPMNSerializer.__serialize_data_store(element)
            case BPMNElementType.BPMN_END_EVENT:
                serialized_element = BPMNSerializer.__serialize_end_event(element)
            case BPMNElementType.BPMN_GATEWAY:
                serialized_element = BPMNSerializer.__serialize_gateway(element)
            case BPMNElementType.BPMN_GROUP:
                serialized_element = BPMNSerializer.__serialize_group(element)
            case BPMNElementType.BPMN_INTERMEDIATE_EVENT:
                serialized_element = BPMNSerializer.__serialize_intermediate_event(element)
            case BPMNElementType.BPMN_POOL:
                serialized_element = BPMNSerializer.__serialize_pool(element)
            case BPMNElementType.BPMN_START_EVENT:
                serialized_element = BPMNSerializer.__serialize_start_event(element)
            case BPMNElementType.BPMN_SUBPROCESS:
                serialized_element = BPMNSerializer.__serialize_subprocess(element)
            case BPMNElementType.BPMN_SWIMLANE:
                serialized_element = BPMNSerializer.__serialize_swimlane(element)
            case BPMNElementType.BPMN_TASK:
                serialized_element = BPMNSerializer.__serialize_task(element)
            case BPMNElementType.BPMN_TRANSACTION:
                serialized_element = BPMNSerializer.__serialize_transaction(element)

        return serialized_element

    @staticmethod
    def __serialize_shape(element: dict) -> ElementTree.Element:
        """
        Serialize a BPMN element to a shape
        :param element: A dictionary representing a BPMN element
        :return: An Elementtree Element representing the serialized BPMN shape
        """

        serialized_shape = ElementTree.Element("bpmndi:BPMNShape")
        serialized_shape.set("bpmnElement", element.get("id"))

        bounds = element.get("bounds")

        if bounds:
            serialized_bounds = ElementTree.Element("dc:Bounds")
            serialized_bounds.set("x", str(bounds.get("x")))
            serialized_bounds.set("y", str(bounds.get("y")))
            serialized_bounds.set("width", str(bounds.get("width")))
            serialized_bounds.set("height", str(bounds.get("height")))
            serialized_shape.append(serialized_bounds)

        return serialized_shape

    @staticmethod
    def __serialize_edge(relationship: dict) -> ElementTree.Element:
        """
        Serialize a BPMN relationship to an edge
        :param relationship: A dictionary representing a BPMN relationship
        :return: An Elementtree Element representing the serialized BPMN edge
        """

        serialized_shape = ElementTree.Element("bpmndi:BPMNEdge")
        serialized_shape.set("bpmnElement", relationship.get("id"))

        for point in relationship.get("path"):
            serialized_waypoint = ElementTree.Element("di:waypoint")
            serialized_waypoint.set("x", str(point.get("x")))
            serialized_waypoint.set("y", str(point.get("y")))
            serialized_shape.append(serialized_waypoint)

        return serialized_shape

    @staticmethod
    def __serialize_process(model: dict) -> ElementTree.Element:
        """
        Serialize the process tree of a given BPMN model
        :param model: A dictionary representing a BPMN diagram model
        :return: An Elementtree Element representing the serialized BPMN process tree
        """

        process = ElementTree.Element("process")
        process.set("isExecutable", "false")

        for element in model.get("elements").values():
            serialized_element = BPMNSerializer.__serialize_element(element)
            process.append(serialized_element)

        for relationship in model.get("relationships").values():
            serialized_relationship = BPMNSerializer.__serialize_flow(relationship)
            process.append(serialized_relationship)

        return process

    @staticmethod
    def __serialize_diagram(model: dict) -> ElementTree.Element:
        """
        Serialize the diagram tree of a given BPMN model
        :param model: A dictionary representing a BPMN diagram model
        :return: An Elementtree Element representing the serialized BPMN diagram tree
        """

        diagram = ElementTree.Element("bpmndi:BPMNDiagram")
        plane = ElementTree.Element("bpmndi:BPMNPlane")
        plane.set("bpmnElement", "Minimal")
        diagram.append(plane)

        for element in model.get("elements").values():
            serialized_shape = BPMNSerializer.__serialize_shape(element)
            plane.append(serialized_shape)

        for relationship in model.get("relationships").values():
            serialized_edge = BPMNSerializer.__serialize_edge(relationship)
            plane.append(serialized_edge)

        return diagram

    @staticmethod
    def serialize(model: dict) -> ElementTree.Element:
        """
        Serialize a BPMN diagram in Apollon's native JSON format to XML according to the BPMN 2.0 standard
        :param model: A dictionary representing a BPMN diagram model
        :return: An Elementtree Element representing the serialized BPMN diagram
        """

        definitions = ElementTree.Element("definitions")

        definitions.set("id", "Definition")

        definitions.set("xmlns", "http://www.omg.org/spec/BPMN/20100524/MODEL")
        definitions.set("xmlns:xs", "http://www.w3.org/2001/XMLSchema-instance")
        definitions.set("xs:schemaLocation", "http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd")
        definitions.set("xmlns:bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
        definitions.set("xmlns:dc", "http://www.omg.org/spec/DD/20100524/DC")
        definitions.set("xmlns:di", "http://www.omg.org/spec/DD/20100524/DI")

        definitions.append(BPMNSerializer.__serialize_process(model))
        definitions.append(BPMNSerializer.__serialize_diagram(model))

        return definitions


if __name__ == "__main__":
    model = json.loads("""
        {
    "version": "3.0.0",
    "type": "BPMN",
    "size": {
      "width": 900,
      "height": 600
    },
    "interactive": {
      "elements": {},
      "relationships": {}
    },
    "elements": {
      "b83370ae-4c60-48de-b2e7-b472c100e500": {
        "id": "b83370ae-4c60-48de-b2e7-b472c100e500",
        "name": "",
        "type": "BPMNStartEvent",
        "owner": null,
        "bounds": {
          "x": 0,
          "y": 10,
          "width": 40,
          "height": 40
        },
        "eventType": "message"
      },
      "8fd5fbe0-f81d-457a-b7f6-c009e8fc394c": {
        "id": "8fd5fbe0-f81d-457a-b7f6-c009e8fc394c",
        "name": "Bake Pizza",
        "type": "BPMNTask",
        "owner": null,
        "bounds": {
          "x": 100,
          "y": 0,
          "width": 160,
          "height": 60
        },
        "taskType": "default",
        "marker": "none"
      },
      "001ff705-6703-49f4-ab68-e79a066596b8": {
        "id": "001ff705-6703-49f4-ab68-e79a066596b8",
        "name": "Deliver Pizza",
        "type": "BPMNTask",
        "owner": null,
        "bounds": {
          "x": 330,
          "y": 0,
          "width": 160,
          "height": 60
        },
        "taskType": "default",
        "marker": "none"
      },
      "561c077d-b2e0-4788-8436-278ee6b50adb": {
        "id": "561c077d-b2e0-4788-8436-278ee6b50adb",
        "name": "",
        "type": "BPMNEndEvent",
        "owner": null,
        "bounds": {
          "x": 550,
          "y": 10,
          "width": 40,
          "height": 40
        },
        "eventType": "default"
      }
    },
    "relationships": {
      "22cbf288-11a6-462f-9540-c3d38b6dcfa8": {
        "id": "22cbf288-11a6-462f-9540-c3d38b6dcfa8",
        "name": "",
        "type": "BPMNFlow",
        "owner": null,
        "bounds": {
          "x": 40,
          "y": 30,
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
          "element": "b83370ae-4c60-48de-b2e7-b472c100e500"
        },
        "target": {
          "direction": "Left",
          "element": "8fd5fbe0-f81d-457a-b7f6-c009e8fc394c"
        },
        "isManuallyLayouted": false,
        "flowType": "sequence"
      },
      "c0fcff31-a656-4d2a-8bd9-5ef6bec80646": {
        "id": "c0fcff31-a656-4d2a-8bd9-5ef6bec80646",
        "name": "",
        "type": "BPMNFlow",
        "owner": null,
        "bounds": {
          "x": 260,
          "y": 30,
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
          "element": "8fd5fbe0-f81d-457a-b7f6-c009e8fc394c"
        },
        "target": {
          "direction": "Left",
          "element": "001ff705-6703-49f4-ab68-e79a066596b8"
        },
        "isManuallyLayouted": false,
        "flowType": "sequence"
      },
      "335069fe-4456-40df-bfc5-f1e1379e4010": {
        "id": "335069fe-4456-40df-bfc5-f1e1379e4010",
        "name": "",
        "type": "BPMNFlow",
        "owner": null,
        "bounds": {
          "x": 490,
          "y": 30,
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
          "element": "001ff705-6703-49f4-ab68-e79a066596b8"
        },
        "target": {
          "direction": "Left",
          "element": "561c077d-b2e0-4788-8436-278ee6b50adb"
        },
        "isManuallyLayouted": false,
        "flowType": "sequence"
      }
    },
    "assessments": {}
  }
    """)

    serialized_model = BPMNSerializer.serialize(model)
    ElementTree.indent(serialized_model, space="\t", level=0)

    print(ElementTree.tostring(BPMNSerializer.serialize(model), encoding='utf8', xml_declaration=True))
