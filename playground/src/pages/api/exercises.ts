import type {NextApiRequest, NextApiResponse} from 'next';
import type { Exercise } from '@/model/exercise';
import {getExampleExercises} from "@/helpers/get_examples";
import getOriginFromRequest from '@/helpers/origin_from_req';

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<Exercise[]>
) {
    res.status(200).json(getExampleExercises(getOriginFromRequest(req)));
}
