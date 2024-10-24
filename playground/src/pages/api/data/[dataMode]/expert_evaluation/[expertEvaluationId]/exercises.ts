import {NextApiRequest, NextApiResponse} from "next";
import {DataMode} from "@/model/data_mode";
import {getExpertEvaluationExercisesEager} from "@/helpers/get_data";
import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
import {Exercise} from "@/model/exercise";

function handler(req: NextApiRequest, res: NextApiResponse<Exercise[]>) {
    const {dataMode, expertEvaluationId} = req.query as { dataMode: DataMode; expertEvaluationId: string };

    const exercises = getExpertEvaluationExercisesEager(dataMode, expertEvaluationId);
    res.status(200).json(exercises);
}

export default function handlerWithMiddleware(
    req: NextApiRequest,
    res: NextApiResponse
) {
    validateDataModeMiddleware(req, res, () => handler(req, res));
}