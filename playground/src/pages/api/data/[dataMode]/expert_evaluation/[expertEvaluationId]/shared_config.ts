import {NextApiRequest, NextApiResponse} from "next";
import {DataMode} from "@/model/data_mode";
import {getConfigFromFileSync, saveConfigToFileSync} from "@/helpers/get_data";
import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";

function handler(req: NextApiRequest, res: NextApiResponse) {
   if (req.method == 'GET') {
        console.log("in backend")
        const {dataMode, expertEvaluationId} = req.query as { dataMode: DataMode; expertEvaluationId: string };

        let config = getConfigFromFileSync(dataMode, expertEvaluationId);
        return res.status(200).json(config)
    } else {
        res.setHeader('Allow', ['POST']);
        return res.status(405).json({message: 'Only GET or POST requests allowed'});
    }
}

export default function handlerWithMiddleware(
    req: NextApiRequest,
    res: NextApiResponse
) {
    validateDataModeMiddleware(req, res, () => handler(req, res));
}