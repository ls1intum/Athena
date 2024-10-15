// TODO: Lara, please look at this code, maybe we can use it. If not, get rid of it.
// import type {NextApiRequest, NextApiResponse} from "next";
// import type {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";
// import {deleteExpertEvaluationConfig, getExpertEvaluationConfigs, saveExpertEvaluationConfig} from "@/helpers/get_data";
// import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
//
// // Fetches expert evaluation configs
// async function handleGet(req: NextApiRequest, res: NextApiResponse<ExpertEvaluationConfig[]>) {
//   try {
//     const configs = getExpertEvaluationConfigs();
//     res.status(200).json(configs);
//   } catch (error) {
//     console.error("Failed to fetch evaluation configs: " + error);
//     res.status(500).end("Failed to fetch evaluation configs: " + error);
//   }
// }
//
// // Saves a new or existing expert evaluation config
// async function handlePost(req: NextApiRequest, res: NextApiResponse<ExpertEvaluationConfig>) {
//   try {
//     const config = req.body as ExpertEvaluationConfig;
//     const savedConfig = saveExpertEvaluationConfig(config);
//     res.status(200).json(savedConfig);
//   } catch (error) {
//     res.status(500).end("Failed to save evaluation config: " + error);
//   }
// }
//
// // Deletes an expert evaluation config
// async function handleDelete(req: NextApiRequest, res: NextApiResponse) {
//   try {
//     const configId = req.query.configId as string;
//     const configName = req.query.configName as string;
//     deleteExpertEvaluationConfig(configId, configName);
//     res.status(200).json({ success: true });
//   } catch (error) {
//     res.status(500).end("Failed to delete evaluation config: " + error);
//   }
// }
//
// // Main handler with validation middleware
// export default function handlerWithMiddleware(req: NextApiRequest, res: NextApiResponse) {
//   validateDataModeMiddleware(req, res, async () => {
//     switch (req.method) {
//       case "GET":
//         await handleGet(req, res);
//         break;
//       case "PUT":
//       case "POST":
//         await handlePost(req, res);
//         break;
//       case "DELETE":
//         await handleDelete(req, res);
//         break;
//       default:
//         res.setHeader("Allow", ["GET", "PUT", "POST", "DELETE"]);
//         res.status(405).end(`Method ${req.method} Not Allowed`);
//     }
//   });
// }