import type { NextApiRequest, NextApiResponse } from "next";
import type { Exercise } from "@/model/exercise";
import type { DataMode } from "@/model/dataMode";

import { getExercises } from "@/helpers/getData";
import getOriginFromRequest from "@/helpers/originFromReq";
import { validateDataModeMiddleware } from "@/helpers/validateDataModeMiddleware";

function handler(req: NextApiRequest, res: NextApiResponse<Exercise[]>) {
  const { dataMode } = req.query as { dataMode: DataMode };
  res.status(200).json(getExercises(dataMode, getOriginFromRequest(req)));
}

export default function handlerWithMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  validateDataModeMiddleware(req, res, () => handler(req, res));
}
