import type { NextApiRequest, NextApiResponse } from "next";
import type { Submission } from "@/model/submission";
import { getSubmissions } from "@/helpers/get_data";
import getOriginFromRequest from "@/helpers/origin_from_req";
import { validateModeMiddleware } from "@/helpers/validate_mode_middleware";
import { DataMode } from "@/model/data_mode";

function handler(req: NextApiRequest, res: NextApiResponse<Submission[]>) {
  const { mode: dataMode } = req.query as { mode: DataMode };
  const submissions = getSubmissions(
    dataMode,
    undefined,
    getOriginFromRequest(req)
  );
  res.status(200).json(submissions);
}

export default function handlerWithMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  validateModeMiddleware(req, res, () => handler(req, res));
}
