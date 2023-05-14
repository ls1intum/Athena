import type {NextApiRequest, NextApiResponse} from 'next';
import type Feedback from "@/pages/model/feedback";
import {getExampleFeedbacks} from "@/pages/api/get_examples";


export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<Feedback[]>
) {
    res.status(200).json(getExampleFeedbacks());
}
