import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from "react-query";
import baseUrl from "@/helpers/base_url";
import { ExpertEvaluationConfig } from "@/model/expert_evaluation_config";

// TODO: Lara, please look at this code, maybe we can use it. If not, get rid of it.

/** Fetches the list of expert evaluation configs from the server */
async function fetchExpertEvaluationConfigs() {
  const response = await fetch(`${baseUrl}/api/data/evaluation/expert_evaluation_config`);
  if (!response.ok) {
    throw new Error("Failed to fetch expert evaluation configs");
  }
  return await response.json() as Promise<ExpertEvaluationConfig[]>;
}

/** Saves a new or existing expert evaluation config to the server */
async function saveExpertEvaluationConfig(config: ExpertEvaluationConfig) {
  const method = config.id ? "PUT" : "POST";
  const response = await fetch(`${baseUrl}/api/data/evaluation/expert_evaluation_config`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  });
  if (!response.ok) {
    throw new Error("Failed to save expert evaluation config");
  }
  return await response.json() as Promise<ExpertEvaluationConfig>;
}

/** Deletes an expert evaluation config from the server */
async function deleteExpertEvaluationConfig(configId: string) {
  const response = await fetch(`${baseUrl}/api/data/evaluation/expert_evaluation_config/${configId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to delete expert evaluation config");
  }
  return await response.json() as Promise<{ success: boolean }>;
}

/**
 * Hook to fetch expert evaluation configs
 */
export function useExpertEvaluationConfigs(
  options: Omit<UseQueryOptions<ExpertEvaluationConfig[], Error>, "queryFn"> = {}
) {
  return useQuery<ExpertEvaluationConfig[], Error>({
    queryKey: ["expertEvaluationConfigs"],
    queryFn: fetchExpertEvaluationConfigs,
    ...options,
  });
}

/**
 * Hook to save an expert evaluation config
 */
export function useSaveExpertEvaluationConfig(
  options: Omit<UseMutationOptions<ExpertEvaluationConfig, Error, ExpertEvaluationConfig>, "mutationFn"> = {}
) {
  return useMutation({
    mutationFn: saveExpertEvaluationConfig,
    ...options,
  });
}

/**
 * Hook to delete an expert evaluation config
 */
export function useDeleteExpertEvaluationConfig(
  options: Omit<UseMutationOptions<{ success: boolean }, Error, string>, "mutationFn"> = {}
) {
  return useMutation({
    mutationFn: deleteExpertEvaluationConfig,
    ...options,
  });
}
