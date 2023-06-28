import useSWR from "swr";
import Feedback from "@/model/feedback";
import fetcher from "@/helpers/fetcher";
import baseUrl from "@/helpers/base_url";
import { Mode } from "@/model/mode";

type FeedbackSelectProps = {
  mode: Mode;
  exercise_id?: number;
  submission_id?: number;
  feedback?: Feedback;
  onChange: (feedback: Feedback) => void;
  isAllFeedback?: boolean;
  setIsAllFeedback?: (isAllFeedback: boolean) => void;
};

export default function FeedbackSelect({
  mode,
  exercise_id,
  submission_id,
  feedback,
  onChange,
  isAllFeedback,
  setIsAllFeedback,
}: FeedbackSelectProps) {
  const apiURL = `${baseUrl}/api/mode/${mode}/${
    exercise_id === undefined
      ? "feedbacks"
      : `exercise/${exercise_id}/feedbacks`
  }`;
  const { data, error, isLoading } = useSWR(apiURL, fetcher);
  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  let filteredFeedbacks = data;
  if (submission_id) {
    filteredFeedbacks = filteredFeedbacks.filter(
      (fb: Feedback) => fb.submission_id === submission_id
    );
  }

  return (
    <label className="flex flex-col">
      <span className="text-lg font-bold">Feedback</span>
      <select
        className="border border-gray-300 rounded-md p-2"
        value={isAllFeedback ? "all" : feedback?.id || ""}
        onChange={(e) => {
          const value = e.target.value;
          if (value === "all") {
            setIsAllFeedback!(true);
          } else {
            onChange(
              filteredFeedbacks.find(
                (fb: Feedback) => fb.id === parseInt(e.target.value)
              )
            );
            if (setIsAllFeedback) setIsAllFeedback(false);
          }
        }}
      >
        <option value={""} disabled>
          Select a feedback
        </option>
        { isAllFeedback !== undefined &&
          setIsAllFeedback !== undefined && (
          <option
            key="all"
            value="all"
            onClick={() => { setIsAllFeedback(!isAllFeedback)}
          }>
            ✨ All feedback
            </option>
          )}
        {filteredFeedbacks.map((fb: Feedback) => (
          <option key={fb.id} value={fb.id}>
            {fb.id} ({fb.credits} credits) {fb.text || fb.detail_text || "N/A"}
          </option>
        ))}
      </select>
    </label>
  );
}
