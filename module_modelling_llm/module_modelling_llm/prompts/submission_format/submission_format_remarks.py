from module_modelling_llm.helpers.models.diagram_types import DiagramType
from module_modelling_llm.prompts.submission_format.bpmn import submission_format_remarks as bpmn_submission_format_remarks


def get_submission_format_remarks(diagram_type: DiagramType) -> str:
    match diagram_type:
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
            return bpmn_submission_format_remarks
