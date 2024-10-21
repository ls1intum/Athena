import {NextApiRequest, NextApiResponse} from "next";
import {DataMode} from "@/model/data_mode";
import {getAnonymizedConfigFromFileSync, saveConfigToFileSync, randomizeSubmissionAndFeedbackTypeOrder} from "@/helpers/get_data";
import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";

function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method == 'POST') {
        const {dataMode} = req.query as { dataMode: DataMode };
        const expertEvaluationConfig: ExpertEvaluationConfig = req.body;

        //TODO maybe boolean if it should me randomized?
        expertEvaluationConfig.exercises.forEach((exercise) => {
             randomizeSubmissionAndFeedbackTypeOrder(exercise);
        });

        saveConfigToFileSync(dataMode, expertEvaluationConfig);
        return res.status(200).json({message: 'Config saved successfully'});

    } else if (req.method == 'GET') {
        const {dataMode, expertEvaluationId} = req.query as { dataMode: DataMode; expertEvaluationId: string };
        //TODO maybe boolean param set if needs to be anonymized

        let config = getAnonymizedConfigFromFileSync(dataMode, expertEvaluationId);
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