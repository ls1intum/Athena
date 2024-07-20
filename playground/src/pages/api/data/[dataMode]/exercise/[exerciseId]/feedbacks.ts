import type { NextApiRequest, NextApiResponse } from "next";
import type { Feedback } from "@/model/feedback";
import type { DataMode } from "@/model/dataMode";

import { getFeedbacks } from "@/helpers/getData";
import getOriginFromRequest from "@/helpers/originFromReq";
import { validateDataModeMiddleware } from "@/helpers/validateDataModeMiddleware";

function handler(req: NextApiRequest, res: NextApiResponse<Feedback[]>) {
  const { dataMode, exerciseId } = req.query as { dataMode: DataMode; exerciseId: string };
  const parsedExerciseId = exerciseId ? parseInt(exerciseId) : undefined;
  if (parsedExerciseId === undefined) {
    res.status(404).json([]);
    return;
  }
  try {
    const feedbacks = getFeedbacks(
      dataMode,
      parsedExerciseId,
      getOriginFromRequest(req)
    );
    res.status(200).json(feedbacks);
  } catch (e) {
    console.error(e);
    res.status(404).json([]);
  }
}

export default function handlerWithMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  validateDataModeMiddleware(req, res, () => handler(req, res));
}
