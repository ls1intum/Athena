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
        raise NotImplementedError("Not implemented")

    @staticmethod
    def __serialize_call_activity(call_activity: dict) -> ElementTree.Element:
        """
        Serialize an BPMN call activity to XML
        :param call_activity: A dictionary representing an BPMN call activity element
        :return: An Elementtree Element representing the serialized BPMN call activity element
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def __serialize_data_object(data_object: dict) -> ElementTree.Element:
        """
        Serialize a BPMN data object to XML
        :param data_object: A dictionary representing a BPMN data object element
        :return: An Elementtree Element representing the serialized BPMN data object element
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def __serialize_data_store(data_store: dict) -> ElementTree.Element:
        """
        Serialize a BPMN data store object to XML
        :param data_store: A dictionary representing a BPMN data store element
        :return: An Elementtree Element representing the serialized BPMN data store element
        """
        raise NotImplementedError("Not implemented")

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
        raise NotImplementedError("Not implemented")

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
        raise NotImplementedError("Not implemented")

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
        raise NotImplementedError("Not implemented")

    @staticmethod
    def __serialize_swimlane(swimlane: dict) -> ElementTree.Element:
        """
        Serialize a BPMN swimlane to XML
        :param swimlane: A dictionary representing a BPMN swimlane element
        :return: An Elementtree Element representing the serialized BPMN swimlane element
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def __serialize_task(task: dict) -> ElementTree.Element:
        """
        Serialize a BPMN task to XML
        :param task: A dictionary representing a BPMN task element
        :return: An Elementtree Element representing the serialized BPMN task element
        """
        task_tag = BPMNSerializer.task_type_map[task.get("taskType")]
        serialized_task = ElementTree.Element(task_tag)
        serialized_task.set("id", task.get("id"))
        serialized_task.set("name", task.get("name"))

        return serialized_task

    @staticmethod
    def __serialize_transaction(transaction: dict) -> ElementTree.Element:
        """
        Serialize a BPMN transaction to XML
        :param transaction: A dictionary representing a BPMN transaction element
        :return: An Elementtree Element representing the serialized BPMN transaction element
        """
        raise NotImplementedError("Not implemented")

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
            "width": 1140,
            "height": 480
        },
        "interactive": {
            "elements": {},
            "relationships": {}
        },
        "elements": {
            "3ecfdf8a-07b0-4752-a38b-7740fb2868c0": {
                "id": "3ecfdf8a-07b0-4752-a38b-7740fb2868c0",
                "name": "",
                "type": "BPMNStartEvent",
                "owner": null,
                "bounds": {
                    "x": 0,
                    "y": 190,
                    "width": 40,
                    "height": 40
                },
                "eventType": "message"
            },
            "68e80fd6-e064-4ca0-ac7e-5bb41694d758": {
                "id": "68e80fd6-e064-4ca0-ac7e-5bb41694d758",
                "name": "Identify how customer will pay",
                "type": "BPMNTask",
                "owner": null,
                "bounds": {
                    "x": 80,
                    "y": 180,
                    "width": 260,
                    "height": 60
                },
                "taskType": "default",
                "marker": "none"
            },
            "5f0c3b3d-dbfe-46bb-8126-4283c189a3df": {
                "id": "5f0c3b3d-dbfe-46bb-8126-4283c189a3df",
                "name": "",
                "type": "BPMNEndEvent",
                "owner": null,
                "bounds": {
                    "x": 990,
                    "y": 190,
                    "width": 40,
                    "height": 40
                },
                "eventType": "default"
            },
            "bc8c4a87-1399-4b55-ba7a-daf77c7aacde": {
                "id": "bc8c4a87-1399-4b55-ba7a-daf77c7aacde",
                "name": "Which payment method?",
                "type": "BPMNGateway",
                "owner": null,
                "bounds": {
                    "x": 390,
                    "y": 190,
                    "width": 40,
                    "height": 40
                },
                "gatewayType": "exclusive"
            },
            "21baf779-87a1-449f-9566-6d2ba3f150e5": {
                "id": "21baf779-87a1-449f-9566-6d2ba3f150e5",
                "name": "Process credit card",
                "type": "BPMNTask",
                "owner": null,
                "bounds": {
                    "x": 490,
                    "y": 370,
                    "width": 180,
                    "height": 60
                },
                "taskType": "default",
                "marker": "none"
            },
            "bc312e08-608e-4005-92a4-5116ea880a76": {
                "id": "bc312e08-608e-4005-92a4-5116ea880a76",
                "name": "Accept cash",
                "type": "BPMNTask",
                "owner": null,
                "bounds": {
                    "x": 490,
                    "y": 0,
                    "width": 180,
                    "height": 60
                },
                "taskType": "default",
                "marker": "none"
            },
            "eb871542-06f1-4ab7-a567-d0121c7fc4ff": {
                "id": "eb871542-06f1-4ab7-a567-d0121c7fc4ff",
                "name": "",
                "type": "BPMNGateway",
                "owner": null,
                "bounds": {
                    "x": 690,
                    "y": 190,
                    "width": 40,
                    "height": 40
                },
                "gatewayType": "exclusive"
            },
            "6c702676-039b-416d-b5fb-d07b60b8fb4c": {
                "id": "6c702676-039b-416d-b5fb-d07b60b8fb4c",
                "name": "Prepare item",
                "type": "BPMNTask",
                "owner": null,
                "bounds": {
                    "x": 790,
                    "y": 180,
                    "width": 160,
                    "height": 60
                },
                "taskType": "default",
                "marker": "none"
            }
        },
        "relationships": {
            "8e6e41d9-5e9e-4e42-9bd0-134c9d08a023": {
                "id": "8e6e41d9-5e9e-4e42-9bd0-134c9d08a023",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 40,
                    "y": 210,
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
                    "element": "3ecfdf8a-07b0-4752-a38b-7740fb2868c0"
                },
                "target": {
                    "direction": "Left",
                    "element": "68e80fd6-e064-4ca0-ac7e-5bb41694d758"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "217860de-e35c-44c9-b597-3a14b006618d": {
                "id": "217860de-e35c-44c9-b597-3a14b006618d",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 340,
                    "y": 210,
                    "width": 50,
                    "height": 1
                },
                "path": [
                    {
                        "x": 0,
                        "y": 0
                    },
                    {
                        "x": 50,
                        "y": 0
                    }
                ],
                "source": {
                    "direction": "Right",
                    "element": "68e80fd6-e064-4ca0-ac7e-5bb41694d758"
                },
                "target": {
                    "direction": "Left",
                    "element": "bc8c4a87-1399-4b55-ba7a-daf77c7aacde"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "2effec5d-72b3-4ea3-8ac5-7a5aa9e7c862": {
                "id": "2effec5d-72b3-4ea3-8ac5-7a5aa9e7c862",
                "name": "Cash",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 410,
                    "y": 30,
                    "width": 80,
                    "height": 160
                },
                "path": [
                    {
                        "x": 0,
                        "y": 160
                    },
                    {
                        "x": 0,
                        "y": 0
                    },
                    {
                        "x": 80,
                        "y": 0
                    }
                ],
                "source": {
                    "direction": "Up",
                    "element": "bc8c4a87-1399-4b55-ba7a-daf77c7aacde"
                },
                "target": {
                    "direction": "Left",
                    "element": "bc312e08-608e-4005-92a4-5116ea880a76"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "61ba5eb3-cab1-4165-9476-a0f61a31d2a2": {
                "id": "61ba5eb3-cab1-4165-9476-a0f61a31d2a2",
                "name": "Credit Card",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 410,
                    "y": 230,
                    "width": 87.392578125,
                    "height": 170
                },
                "path": [
                    {
                        "x": 0,
                        "y": 0
                    },
                    {
                        "x": 0,
                        "y": 170
                    },
                    {
                        "x": 80,
                        "y": 170
                    }
                ],
                "source": {
                    "direction": "Down",
                    "element": "bc8c4a87-1399-4b55-ba7a-daf77c7aacde"
                },
                "target": {
                    "direction": "Left",
                    "element": "21baf779-87a1-449f-9566-6d2ba3f150e5"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "6d9e5c30-1dfc-4809-8867-9282a174fa8c": {
                "id": "6d9e5c30-1dfc-4809-8867-9282a174fa8c",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 670,
                    "y": 30,
                    "width": 40,
                    "height": 160
                },
                "path": [
                    {
                        "x": 0,
                        "y": 0
                    },
                    {
                        "x": 40,
                        "y": 0
                    },
                    {
                        "x": 40,
                        "y": 160
                    }
                ],
                "source": {
                    "direction": "Right",
                    "element": "bc312e08-608e-4005-92a4-5116ea880a76"
                },
                "target": {
                    "direction": "Up",
                    "element": "eb871542-06f1-4ab7-a567-d0121c7fc4ff"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "3b81ab56-462a-4e41-a090-3bf047f354d4": {
                "id": "3b81ab56-462a-4e41-a090-3bf047f354d4",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 670,
                    "y": 230,
                    "width": 40,
                    "height": 170
                },
                "path": [
                    {
                        "x": 0,
                        "y": 170
                    },
                    {
                        "x": 40,
                        "y": 170
                    },
                    {
                        "x": 40,
                        "y": 0
                    }
                ],
                "source": {
                    "direction": "Right",
                    "element": "21baf779-87a1-449f-9566-6d2ba3f150e5"
                },
                "target": {
                    "direction": "Down",
                    "element": "eb871542-06f1-4ab7-a567-d0121c7fc4ff"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "7cba958f-172a-4086-98c3-89a923e6d8fa": {
                "id": "7cba958f-172a-4086-98c3-89a923e6d8fa",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 950,
                    "y": 210,
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
                    "element": "6c702676-039b-416d-b5fb-d07b60b8fb4c"
                },
                "target": {
                    "direction": "Left",
                    "element": "5f0c3b3d-dbfe-46bb-8126-4283c189a3df"
                },
                "isManuallyLayouted": false,
                "flowType": "sequence"
            },
            "b4570b0e-8e23-460d-90d8-11ccb582ad6b": {
                "id": "b4570b0e-8e23-460d-90d8-11ccb582ad6b",
                "name": "",
                "type": "BPMNFlow",
                "owner": null,
                "bounds": {
                    "x": 730,
                    "y": 210,
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
                    "element": "eb871542-06f1-4ab7-a567-d0121c7fc4ff"
                },
                "target": {
                    "direction": "Left",
                    "element": "6c702676-039b-416d-b5fb-d07b60b8fb4c"
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
