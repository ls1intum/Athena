import useSWR from "swr";
import Submission from "@/pages/model/submission";
import fetcher from "@/pages/fetcher";

export default function SubmissionSelect(
    {exercise_id, submission, onChange}: { exercise_id?: number, submission: Submission | null, onChange: (submission: Submission) => void}
) {
    const {data, error, isLoading} = useSWR("/api/submissions", fetcher);
    if (error) return <div>failed to load</div>;
    if (isLoading) return <div>loading...</div>;

    const filteredSubmissions = exercise_id ? data.filter((sub: Submission) => sub.exercise_id === exercise_id) : data;

    return (
        <label className="flex flex-col">
            <span className="text-lg font-bold">Submission</span>
            <select className="border border-gray-300 rounded-md p-2" value={submission?.id} onChange={e => onChange(filteredSubmissions.find((sub: Submission) => sub.id === parseInt(e.target.value)))}>
                {filteredSubmissions.map((sub: Submission) => <option key={sub.id} value={sub.id}>{sub.id} {sub.content.substring(0, 80)}</option>)}
            </select>
        </label>
    );
}
