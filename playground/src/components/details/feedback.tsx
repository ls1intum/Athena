import Feedback from "@/model/feedback";

type FeedbackDetailProps = {
  feedback: Feedback;
};

export default function FeedbackDetail({ feedback }: FeedbackDetailProps) {
  return (
    <div>
      <h3 className="text-lg font-bold">
        {feedback.text || "Feedback"}
      </h3>
      <pre>{feedback.detail_text}</pre>
      <pre>{feedback.id}</pre>
    </div>
  );
}

