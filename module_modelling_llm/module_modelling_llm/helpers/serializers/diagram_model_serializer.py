import json
import xml.etree.ElementTree as ElementTree

from athena.modelling import Submission
from module_modelling_llm.helpers.models.diagram_types import DiagramType
from module_modelling_llm.helpers.serializers.bpmn_serializer import BPMNSerializer


class DiagramModelSerializer:

    @staticmethod
    def serialize_model_for_submission(submission: Submission) -> str:
        model: dict = json.loads(submission.model)

        match model.get("type"):
            case DiagramType.CLASS_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.OBJECT_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.ACTIVITY_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.USE_CASE_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.COMMUNICATION_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.COMPONENT_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.DEPLOYMENT_DIAGRAM:
                raise NotImplementedError("not implemented")
            case DiagramType.PETRI_NET:
                raise NotImplementedError("not implemented")
            case DiagramType.REACHABILITY_GRAPH:
                raise NotImplementedError("not implemented")
            case DiagramType.SYNTAX_TREE:
                raise NotImplementedError("not implemented")
            case DiagramType.FLOWCHART:
                raise NotImplementedError("not implemented")
            case DiagramType.BPMN:
                serialized_model: ElementTree.Element = BPMNSerializer.serialize(model)
                ElementTree.indent(serialized_model, space="\t", level=0)
                return ElementTree.tostring(BPMNSerializer.serialize(model), encoding='utf8', xml_declaration=True)