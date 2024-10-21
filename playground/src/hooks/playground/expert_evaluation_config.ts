import {useMutation, UseMutationOptions} from "react-query";
import baseUrl from "@/helpers/base_url";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";
import {DataMode} from "@/model/data_mode";
import {v4 as uuidv4} from "uuid";

// TODO: Lara, please look at this code, maybe we can use it. If not, get rid of it.

/** Saves a new or existing expert evaluation config to the server */
export async function saveExpertEvaluationConfig(
    dataMode: DataMode,
    config: ExpertEvaluationConfig) {

    //TODO PUT vs POST
    //const method = config.id ? "PUT" : "POST";
    //alert(method);
    const response = await fetch(`${baseUrl}/api/data/${dataMode}/expert_evaluation/${config.id}/config`, {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(config),
    });

    if (!response.ok) {
        throw new Error("Failed to save expert evaluation config");
    }
    return await response.json() as Promise<ExpertEvaluationConfig>;
}

export async function fetchExpertEvaluationConfig(
    dataMode: DataMode,
    expertEvaluationId: string
) {
    console.log("before fetch")
    const response = await fetch(`${baseUrl}/api/data/${dataMode}/expert_evaluation/${expertEvaluationId}/config`);


    if (!response.ok) {
        throw new Error("Failed to fetch expert evaluation configs");
    }

    return await response.json() as Promise<ExpertEvaluationConfig>;
}

/** Fetches the list of expert evaluation configs from the server */
export async function fetchAllExpertEvaluationConfigs(
    dataMode: DataMode
) {
    const response = await fetch(`${baseUrl}/api/data/${dataMode}/expert_evaluation/configs`);

    if (!response.ok) {
        throw new Error("Failed to fetch expert evaluation configs");
    }

    return await response.json() as Promise<ExpertEvaluationConfig[]>;
}

//TODO fetch for only one config

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
//TOOD no idea
/*export function useExpertEvaluationConfigs(
  options: Omit<UseQueryOptions<ExpertEvaluationConfig[], Error>, "queryFn"> = {}
) {
  return useQuery<ExpertEvaluationConfig[], Error>({
    queryKey: ["expertEvaluationConfigs"],
    queryFn: fetchExpertEvaluationConfigs,
    ...options,
  });
}*/

/**
 * Hook to save an expert evaluation config
 */ // TODO no idea
/*export function useSaveExpertEvaluationConfig(
  options: Omit<UseMutationOptions<ExpertEvaluationConfig, Error, ExpertEvaluationConfig>, "mutationFn"> = {}
) {
  return useMutation({
    mutationFn: saveExpertEvaluationConfig,
    ...options,
  });
}*/

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
