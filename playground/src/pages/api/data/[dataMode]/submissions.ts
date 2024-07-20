import type { NextApiRequest, NextApiResponse } from "next";
import type { Submission } from "@/model/submission";
import type { DataMode } from "@/model/dataMode";

import { getSubmissions } from "@/helpers/getData";
import getOriginFromRequest from "@/helpers/originFromReq";
import { validateDataModeMiddleware } from "@/helpers/validateDataModeMiddleware";

function handler(req: NextApiRequest, res: NextApiResponse<Submission[]>) {
  const { dataMode } = req.query as { dataMode: DataMode };
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
  validateDataModeMiddleware(req, res, () => handler(req, res));
}
