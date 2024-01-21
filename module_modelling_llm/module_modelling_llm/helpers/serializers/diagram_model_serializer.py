import json
from typing import Optional
from xml.etree import ElementTree
from xml.dom import minidom

from module_modelling_llm.helpers.models.diagram_types import DiagramType
from module_modelling_llm.helpers.serializers.bpmn_serializer import BPMNSerializer


class DiagramModelSerializer:

    @staticmethod
    def serialize_model(model: dict) -> Optional[str]:
        """
        Serialize a given Apollon diagram model to string. At the moment, this method returns a native JSON
        serialization of the diagram for all diagram types other than BPMN diagrams. This diagram type is serialized in
        the BPMN 2.0 XML format as this format is following an official standard and therefore well understood by most
        LLMs.
        """
        match model.get("type"):
            case DiagramType.CLASS_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.OBJECT_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.ACTIVITY_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.USE_CASE_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.COMMUNICATION_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.COMPONENT_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.DEPLOYMENT_DIAGRAM:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.PETRI_NET:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.REACHABILITY_GRAPH:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.SYNTAX_TREE:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.FLOWCHART:
                # TODO: Evaluate if there is a more sensible serialization format for this diagram type
                return json.dumps(model)
            case DiagramType.BPMN:
                serializer = BPMNSerializer()
                serialized_model: str = ElementTree.tostring(serializer.serialize(model, omit_layout_info=True),
                                                             encoding='utf8')
                # The next line is only required to "pretty-print" the XML output for easier debugging
                return minidom.parseString(serialized_model).toprettyxml(indent="\t")

        return None
