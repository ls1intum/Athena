import type { NextApiRequest, NextApiResponse } from "next";
import type { Feedback } from "@/model/feedback";
import type { DataMode } from "@/model/dataMode";

import { getFeedbacks } from "@/helpers/getData";
import getOriginFromRequest from "@/helpers/originFromReq";
import { validateDataModeMiddleware } from "@/helpers/validateDataModeMiddleware";

function handler(req: NextApiRequest, res: NextApiResponse<Feedback[]>) {
  const { dataMode } = req.query as { dataMode: DataMode };
  const feedbacks = getFeedbacks(dataMode, undefined, getOriginFromRequest(req));
  res.status(200).json(feedbacks);
}

export default function handlerWithMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  validateDataModeMiddleware(req, res, () => handler(req, res));
}
