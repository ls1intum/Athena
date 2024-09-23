import React from 'react';
import SingleChoiceLikertScale from "@/components/expert_evaluation/expert_view/likert_scale";
import TextSubmissionDetail from "@/components/details/submission_detail/text";
import type { TextSubmission } from "@/model/submission";
import {TextFeedback} from "@/model/feedback";

// Define the metric data
const metrics = [
  {
    title: '✅ Correctness',
    summary: 'Is the feedback free of content errors?',
    description: `
    **Good**: The feedback accurately reflects the submission, solution, and criteria, with no errors.
    **Mid**: The feedback is mostly accurate but includes minor errors that don’t impact the overall evaluation.
    **Bad**: The feedback contains major errors that misrepresent the submission or solution, likely causing confusion.
    `,
  },
  {
    title: '🎯 Actionability',
    summary: 'Can students realistically act on this feedback?',
    description: `
    **Good**: The feedback provides specific steps for improvement or reinforces correct approaches.
    **Mid**: The feedback notes correctness or errors but lacks detailed improvement guidance.
    **Bad**: The feedback identifies errors without solutions or offers no additional insights for correct work.
    `,
  },
  {
    title: '💬 Tone',
    summary: 'Is the feedback respectful and constructive?',
    description: `
    **Good**: The feedback is respectful and constructive, recognizing both strengths and areas for improvement.
    **Mid**: The feedback is professional but mainly corrective, with little positive reinforcement.
    **Bad**: The feedback is overly critical or dismissive, using unprofessional or disrespectful language.
    `,
  },
  {
    title: '🔍 Completeness',
    summary: 'Does the feedback cover all relevant aspects without unnecessary information?',
    description: `
    **Good**: The feedback addresses all key aspects and avoids irrelevant details.
    **Mid**: The feedback covers most important points but may miss minor details or include some irrelevant information.
    **Bad**: The feedback misses important aspects or includes too much irrelevant content.
    `,
  },
];

// Define the submission and feedbacks data
const submission: TextSubmission = {
  exercise_id: 0,
  meta: {},
  type: "text",
  id: 1,
  text: 'Groups are a loosely coupled amount of people whereas teams are people who work for the same goal together.'
};

// Define the Feedbacks type
type Feedbacks = {
  Tutor: TextFeedback[];
  LLM: TextFeedback[];
  Coffee: TextFeedback[];
};

const feedbacks: Feedbacks = {
  Tutor: [
    {
      id: 37715264,
      title: undefined,
      description: "Instead of stating what comprises a team and a group, please provide differences between the two, and explain these differences by means of two examples",
      credits: 0.0,
      type: "text",
      exercise_id: 0,
      submission_id: 1,
      meta: {}
    },
    {
      id: 37715265,
      title: undefined,
      description: "Your answer is quite short, please elaborate more in the future, also use examples to illustrate your point",
      credits: 0.0,
      type: "text",
      exercise_id: 0,
      submission_id: 1,
      meta: {}
    }
  ],
  LLM: [
    {
      id: 1722786968303000,
      title: undefined,
      description: "Good explanation of a difference between groups and teams. You clearly stated that groups are loosely coupled, while teams work towards the same goal.",
      credits: 1.0,
      type: "text",
      exercise_id: 0,
      submission_id: 1,
      meta: {}
    },
    {
      id: 1722786968303001,
      title: undefined,
      description: "You did not provide any examples to illustrate the differences between groups and teams. Including examples would strengthen your explanation.",
      credits: 0.0,
      type: "text",
      exercise_id: 0,
      submission_id: 1,
      meta: {}
    }
  ],
  Coffee: [
    // Add Coffee feedbacks here if available
  ]
};

const LikertScaleForm: React.FC = () => {
  return (
    <div className="overflow-x-auto">
      <div className="flex min-w-[480px] space-x-6">
        {Object.entries(feedbacks).map(([feedbackType, feedbackList]) => (
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