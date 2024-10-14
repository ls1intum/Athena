import {DataMode} from "@/model/data_mode";
import baseUrl from "@/helpers/base_url";
import {ExpertEvaluationProgress} from "@/model/expert_evaluation_progress";

export async function saveExpertEvaluationProgress(dataMode: DataMode, expertEvaluationId: string, progress: ExpertEvaluationProgress) {
  const response = await fetch(`${baseUrl}/api/data/${dataMode}/expert_evaluation/${expertEvaluationId}/progress`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(progress),
  });

  return response.status;
}

export async function fetchExpertEvaluationProgress(
    dataMode: DataMode,
    expertEvaluationId: string,
    expertId: number
) {
    const response = await fetch(`${baseUrl}/api/data/${dataMode}/expert_evaluation/${expertEvaluationId}/progress`);

    return await response.json() as Promise<ExpertEvaluationProgress>;
}
