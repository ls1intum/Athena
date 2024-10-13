import {NextApiRequest, NextApiResponse} from "next";
import {DataMode} from "@/model/data_mode";
import {getMetrics} from "@/helpers/get_data";
import {validateDataModeMiddleware} from "@/helpers/validate_data_mode_middleware";
import {Metric} from "@/model/metric";

function handler(req: NextApiRequest, res: NextApiResponse<Metric[]>) {
    const {dataMode, expertEvaluationId} = req.query as { dataMode: DataMode; expertEvaluationId: string };

    const metrics = getMetrics(dataMode, expertEvaluationId);
    res.status(200).json(metrics);
}

export default function handlerWithMiddleware(
    req: NextApiRequest,
    res: NextApiResponse
) {
    validateDataModeMiddleware(req, res, () => handler(req, res));
}