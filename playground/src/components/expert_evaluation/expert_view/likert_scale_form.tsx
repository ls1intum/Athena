import React from 'react';
import SingleChoiceLikertScale from "@/components/expert_evaluation/expert_view/likert_scale";
import TextSubmissionDetail from "@/components/details/submission_detail/text";
import type {TextSubmission} from "@/model/submission";
import {CategorizedFeedback} from "@/model/feedback";
import {Exercise} from "@/model/exercise";

// Define the metric data
const metrics = [
    {
        title: '✅ Correctness',
        summary: 'Is the feedback free of content errors?',
        description: `
            <b>good</b>: 'The feedback accurately reflects the submission, solution, and criteria, with no errors.',<br>
            mid: 'The feedback is mostly accurate but includes minor errors that don’t impact the overall evaluation.',<br>
            bad: 'The feedback contains major errors that misrepresent the submission or solution, likely causing confusion.'
        `
    },
    {
        title: '🎯 Actionability',
        summary: 'Can students realistically act on this feedback?',
        description: `
            good: 'The feedback is respectful and constructive, recognizing both strengths and areas for improvement.',<br>
            mid: 'The feedback is professional but mainly corrective, with little positive reinforcement.',<br>
            bad: 'The feedback is overly critical or dismissive, using unprofessional or disrespectful language.'
        `
    },
    {
        title: '💬 Tone',
        summary: 'Is the feedback respectful and constructive?',
        description: `
            good: 'The feedback is respectful and constructive, recognizing both strengths and areas for improvement.',<br>
            mid: 'The feedback is professional but mainly corrective, with little positive reinforcement.',<br>
            bad: 'The feedback is overly critical or dismissive, using unprofessional or disrespectful language.'
        `

    },
{
    title: '🔍 Completeness',
    summary: 'Does the feedback cover all relevant aspects without unnecessary information?',
    description: `
        good: 'The feedback addresses all key aspects and avoids irrelevant details.',<br>
        mid: 'The feedback covers most important points but may miss minor details or include some irrelevant information.',<br>
        bad: 'The feedback misses important aspects or includes too much irrelevant content.'
    `
},
];

interface LikertScaleFormProps {
    submission: TextSubmission;
    exercise: Exercise;
    feedback: CategorizedFeedback;
}


const LikertScaleForm: React.FC<LikertScaleFormProps> = ({submission, exercise, feedback}) => {

    if (!exercise || !submission) {
        return <div>Loading...</div>; // Show a loading state until the data is fetched
    }

    const shuffledFeedbacks = Object.entries(feedback).sort(() => Math.random() - 0.5);

    return (
        <div className="overflow-x-auto">
            <div className="flex min-w-[480px] space-x-6">
                {shuffledFeedbacks.map(([feedbackType, feedbackList]) => (
                    <div key={feedbackType} className="flex-1 min-w-[480px] flex flex-col">
                        {/* Render TextSubmissionDetail */}
                        <div className="flex-grow flex flex-col mb-6">
                            <TextSubmissionDetail
                                identifier={`id-${submission.id}`}
                                key={submission.id}
                                submission={submission}
                                feedbacks={feedbackList}
                                onFeedbacksChange={undefined}
                                hideFeedbackDetails={true}
                            />
                        </div>

                        {/* Render SingleChoiceLikertScale components */}
                        <div className="flex flex-col mt-auto">
                            {metrics.map((metric, index) => (
                                <div key={index} className="mb-4">
                                    <SingleChoiceLikertScale
                                        title={metric.title}
                                        summary={metric.summary}
                                        description={metric.description}
                                    />
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LikertScaleForm;