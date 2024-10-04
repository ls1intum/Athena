import React, {useState} from 'react';
import Popup from "@/components/expert_evaluation/expert_view/popup";

interface SideBySideHeaderProps {
    exercise: any;
    globalSubmissionIndex: number;
    totalSubmissions: number;
    onNext: () => void;
    onPrevious: () => void;
}

const SideBySideHeader: React.FC<SideBySideHeaderProps> = ({
                                                               exercise,
                                                               globalSubmissionIndex,
                                                               totalSubmissions,
                                                               onNext,
                                                               onPrevious,
                                                           }) => {

    const [isExerciseDetailOpen, setIsExerciseDetailOpen] = useState<boolean>(false);
    const [isMetricDetailOpen, setIsMetricDetailOpen] = useState<boolean>(false);
    const [isEvaluationTutorialOpen, setIsEvaluationTutorialOpen] = useState<boolean>(false);

    const openExerciseDetail = () => setIsExerciseDetailOpen(true);
    const closeExerciseDetail = () => setIsExerciseDetailOpen(false);
    const openMetricDetail = () => setIsMetricDetailOpen(true);
    const closeMetricDetail = () => setIsMetricDetailOpen(false);
    const openEvaluationTutorial = () => setIsEvaluationTutorialOpen(true);
    const closeEvaluationTutorial = () => setIsEvaluationTutorialOpen(false);

    if (!exercise) {
        return <div>Loading...</div>;
    }
    return (
        <div className={"mb-12"}>
            {/* Title and Submission Info Section */}
            <div
                className="flex flex-col md:flex-row items-start md:items-center justify-between mb-4 space-y-2 md:space-y-0">
                <h1 className="text-3xl font-semibold text-gray-900">Side by Side Evaluation</h1>
                <span className="text-lg text-gray-700">
          Submission <strong>{globalSubmissionIndex + 1}</strong> / {totalSubmissions}
        </span>
            </div>

            {/* Subtitle and Details Buttons Section */}
            <div className="flex flex-col md:flex-row justify-between items-end gap-4">
                <div className="flex flex-col gap-2 w-full md:w-auto">
          <span className="text-lg text-gray-800">
            {exercise.title} (id={exercise.id})
          </span>
                    <div className="flex flex-col md:flex-row gap-2 w-full">
                        <button
                            className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition"
                            onClick={openExerciseDetail}>
                            📄 Exercise Details
                        </button>
                        <Popup isOpen={isExerciseDetailOpen} onClose={closeExerciseDetail} title="Exercise Details">
                            <p><b>Exercise Problem Statement</b></p>
                            <p>{exercise.problem_statement}</p>
                            <p><b> Sample Solution</b></p>
                            <p>{exercise.example_solution}</p>
                        </Popup>
                        <button
                            className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition"
                            onClick={openMetricDetail}>
                            📊 Metric Details
                        </button>
                        <Popup isOpen={isMetricDetailOpen} onClose={closeMetricDetail} title="Metric Details">
                            TODO add metrics description
                        </Popup>
                        <button
                            className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition"
                            onClick={openEvaluationTutorial}>
                            📚 Evaluation Tutorial
                        </button>
                        <Popup isOpen={isEvaluationTutorialOpen} onClose={closeEvaluationTutorial}
                               title="Evaluation Tutorial">
                            This is how you do the evaluation: ...
                        </Popup>
                    </div>
                </div>

                {/* Navigation Buttons Section */}
                <div className="flex flex-col items-end gap-2 mt-4 md:mt-0 w-full md:w-[250px]">
                    <button
                        className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition w-full">
                        😴 Continue Later
                    </button>
                    <div className="flex gap-2 w-full">
                        <button
                            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition min-w-[120px] md:w-auto"
                            onClick={onPrevious}
                            disabled={globalSubmissionIndex === 0}>
                            ⬅️ Previous
                        </button>
                        <button
                            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition min-w-[120px] md:w-auto"
                            onClick={onNext}
                            disabled={globalSubmissionIndex === totalSubmissions - 1}>
                            Next ➡️
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SideBySideHeader;