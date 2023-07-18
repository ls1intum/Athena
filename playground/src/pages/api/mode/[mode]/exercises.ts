import type { NextApiRequest, NextApiResponse } from "next";
import type { Exercise } from "@/model/exercise";
import { getExercises } from "@/helpers/get_data";
import getOriginFromRequest from "@/helpers/origin_from_req";
import { validateModeMiddleware } from "@/helpers/validate_mode_middleware";
import { DataMode } from "@/model/data_mode";

function handler(req: NextApiRequest, res: NextApiResponse<Exercise[]>) {
  const { mode: dataMode } = req.query as { mode: DataMode };
  res.status(200).json(getExercises(dataMode, getOriginFromRequest(req)));
}

export default function handlerWithMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  validateModeMiddleware(req, res, () => handler(req, res));
}
