from module_modelling_llm.helpers.models.diagram_types import DiagramType
from module_modelling_llm.prompts.submission_format.bpmn import submission_format_remarks as bpmn_submission_format_remarks


def get_submission_format_remarks(diagram_type: DiagramType) -> str:
    match diagram_type:
        case DiagramType.CLASS_DIAGRAM:
            return ""
        case DiagramType.OBJECT_DIAGRAM:
            return ""
        case DiagramType.ACTIVITY_DIAGRAM:
            return ""
        case DiagramType.USE_CASE_DIAGRAM:
            return ""
        case DiagramType.COMMUNICATION_DIAGRAM:
            return ""
        case DiagramType.COMPONENT_DIAGRAM:
            return ""
        case DiagramType.DEPLOYMENT_DIAGRAM:
            return ""
        case DiagramType.PETRI_NET:
            return ""
        case DiagramType.REACHABILITY_GRAPH:
            return ""
        case DiagramType.SYNTAX_TREE:
            return ""
        case DiagramType.FLOWCHART:
            return ""
        case DiagramType.BPMN:
            return bpmn_submission_format_remarks
