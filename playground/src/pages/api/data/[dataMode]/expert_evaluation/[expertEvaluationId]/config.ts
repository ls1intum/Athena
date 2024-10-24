import {NextApiRequest, NextApiResponse} from "next";
import {DataMode} from "@/model/data_mode";
import {
    getAnonymizedConfigFromFileSync,
    saveConfigToFileSync,
    addStructuredGradingInstructionsToFeedback,
    anonymizeFeedbackCategoriesAndShuffle
} from "@/helpers/get_data";
import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";

function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method == 'POST') {
        const {dataMode} = req.query as { dataMode: DataMode };
        const expertEvaluationConfig: ExpertEvaluationConfig = req.body;

        anonymizeFeedbackCategoriesAndShuffle(expertEvaluationConfig);
        console.log("After anonymize " + expertEvaluationConfig.mappings?.size);
        saveConfigToFileSync(dataMode, expertEvaluationConfig);

        return res.status(200).json({message: 'Config saved successfully'});

    } else if (req.method == 'GET') {
        const {dataMode, expertEvaluationId} = req.query as { dataMode: DataMode; expertEvaluationId: string };

        let config = getAnonymizedConfigFromFileSync(dataMode, expertEvaluationId);
        if (config) {
            config.exercises.forEach((exercise) => {
                addStructuredGradingInstructionsToFeedback(exercise);
            });
        }

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