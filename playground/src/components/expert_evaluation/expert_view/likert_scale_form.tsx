import React, {useEffect, useState} from 'react';
import SingleChoiceLikertScale from "@/components/expert_evaluation/expert_view/likert_scale";
import TextSubmissionDetail from "@/components/details/submission_detail/text";
import type {TextSubmission} from "@/model/submission";
import {CategorizedFeedback} from "@/model/feedback";
import {Exercise} from "@/model/exercise";
import {Metric} from "@/model/metric";

interface LikertScaleFormProps {
    submission: TextSubmission;
    exercise: Exercise;
    feedback: CategorizedFeedback;
    metrics: Metric[];
    selectedValues: { // Selected values for each exercise, submission, and feedback type
    [exerciseId: string]: { //TODO define somewhere
      [submissionId: string]: {
        [feedbackType: string]: {
          [metricTitle: string]: number; // The Likert scale value for each metric
        };
      };
    };
  };
    onLikertValueChange: (feedbackType: string, metricTitle: string, value: number) => void;
}


const LikertScaleForm: React.FC<LikertScaleFormProps> = ({submission, exercise, feedback, metrics,selectedValues, onLikertValueChange}) => {
const [resetState, setResetState] = useState<boolean>(false);
        useEffect(() => {
            setResetState(!resetState);
  }, [submission, exercise]); // Trigger when submission or exercise changes
    //TODO is this needed


    if (!exercise || !submission) {
        return <div>Loading...</div>; // Show a loading state until the data is fetched
    }


    return (
        <div className="overflow-x-auto">
            <div className="flex min-w-[480px] space-x-6">
                {Object.entries(feedback).map(([feedbackType, feedbackList]) => (
                    <div key={feedbackType} className="flex-1 min-w-[480px] flex flex-col">
                        {/* Render TextSubmissionDetail */}
                        <div className="flex-grow flex flex-col mb-6">
                            <TextSubmissionDetail
                                identifier={`id-${submission.id}-${feedbackType}`}
                                key={submission.id}
                                submission={submission}
                                feedbacks={feedbackList}
                                onFeedbacksChange={undefined}
                                hideFeedbackDetails={true}
                            />
                        </div>

                        {/* Render SingleChoiceLikertScale components */}
                        <div className="flex flex-col mt-auto">
                            {metrics.map((metric, index) => {
                                const selectedValue =
                                    selectedValues?.[exercise.id]?.[submission.id]?.[feedbackType]?.[metric.title] ?? null;
                                return (
                                    <div key={index} className="mb-4">
                                        <SingleChoiceLikertScale
                                            title={metric.title}
                                            summary={metric.summary}
                                            description={metric.description}
                                            passedValue={selectedValue}
                                            onLikertChange={(value: number) => onLikertValueChange(feedbackType, metric.title, value)}
                                            resetState={resetState}
                                        />
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LikertScaleForm;