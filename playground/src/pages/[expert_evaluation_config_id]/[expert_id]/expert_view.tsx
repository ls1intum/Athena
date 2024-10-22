import SideBySideHeader from '@/components/expert_evaluation/expert_view/side_by_side_header';
import React, {useEffect, useState} from 'react';
import LikertScaleForm from "@/components/expert_evaluation/expert_view/likert_scale_form";
import {Exercise} from "@/model/exercise";
import {TextSubmission} from "@/model/submission";
import {Metric} from "@/model/metric";
import {
    fetchExpertEvaluationProgress,
    saveExpertEvaluationProgress
} from "@/hooks/playground/expert_evaluation_progress";
import {ExpertEvaluationProgress} from "@/model/expert_evaluation_progress";
import {useRouter} from "next/router";
import {fetchExpertEvaluationConfig} from "@/hooks/playground/expert_evaluation_config";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";

function SideBySideExpertView() {
    const router = useRouter();
    const {expert_evaluation_config_id, expert_id} = router.query as {
        expert_evaluation_config_id: string;
        expert_id: string
    };
    const dataMode = "expert_evaluation";

    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [submissionsLength, setSubmissionsLength] = useState<number>(0);
    const [currentSubmissionIndex, setCurrentSubmissionIndex] = useState<number>(0);
    const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [selectedValues, setSelectedValues] = useState<ExpertEvaluationProgress['selected_values']>({});
    const [evaluationStarted, setEvaluationStarted] = useState<boolean>(false);

    useEffect(() => {
            const fetchData = async () => {
                    if (expert_evaluation_config_id && expert_id) {
                        try {
                            // Fetch and set data from evaluation config
                            // TODO SharedExpertEvaluationConfig anonym and no links
                            const config: ExpertEvaluationConfig = await fetchExpertEvaluationConfig(dataMode, expert_evaluation_config_id);
                            setExercises(config.exercises);
                            setMetrics(config.metrics);
                            setEvaluationStarted(config.started);

                        } catch
                            (error) {
                            console.error('Error loading expert evaluation configuration: ', error);
                        }

                        try {
                            let expertEvaluationProgress = await fetchExpertEvaluationProgress(dataMode, expert_evaluation_config_id, expert_id);
                            setCurrentSubmissionIndex(expertEvaluationProgress.current_submission_index);
                            setCurrentExerciseIndex(expertEvaluationProgress.current_exercise_index);
                            setSelectedValues(expertEvaluationProgress.selected_values);

                        } catch (error) {
                            console.error('Error loading expert evaluation progress: ', error);
                        }
                    }
                }
            ;fetchData();
        }, [expert_evaluation_config_id, expert_id]
    );

    useEffect(() => {
        if (exercises && exercises.length > 0) {
            let total_submissions = 0;
            for (const exercise of exercises) {
                if (exercise.submissions) {
                    total_submissions += exercise.submissions.length;
                }
            }
            setSubmissionsLength(total_submissions);
        }
    }, [exercises, metrics]);

    const handleNext = () => {
        const currentExercise = exercises[currentExerciseIndex];
        // If we are at the last submission for the current exercise, go to the next exercise
        if (currentSubmissionIndex < currentExercise.submissions!.length - 1) {
            setCurrentSubmissionIndex((prevIndex) => prevIndex + 1);

        } else if (currentExerciseIndex < exercises.length - 1) {
            // Move to the next exercise, reset submission index
            setCurrentExerciseIndex((prevIndex) => prevIndex + 1);
            setCurrentSubmissionIndex(0);
        }
    };

    useEffect(() => {
        if (currentSubmissionIndex > 0) {
            saveProgress();
        }
    }, [currentSubmissionIndex]);

    const handlePrevious = () => {
        // If we are not at the first submission, just decrement the submission index
        if (currentSubmissionIndex > 0) {
            setCurrentSubmissionIndex((prevIndex) => prevIndex - 1);


        } else if (currentExerciseIndex > 0) {
            setCurrentExerciseIndex((prevIndex) => prevIndex - 1);
            // Set the submission index to the last submission of the previous exercise
            const previousExercise = exercises[currentExerciseIndex - 1];
            setCurrentSubmissionIndex(previousExercise.submissions!.length - 1);
        }
    };

    const saveProgress = () => {
        if (expert_evaluation_config_id && expert_id) {
            const progress: ExpertEvaluationProgress = {
                current_submission_index: currentSubmissionIndex,
                current_exercise_index: currentExerciseIndex,
                selected_values: selectedValues,
            };
            saveExpertEvaluationProgress(dataMode, expert_evaluation_config_id, expert_id, progress);
        }
    }

    const handleLikertValueChange = (feedbackType: string, metricId: string, value: number) => {
        const exerciseId = currentExercise.id.toString();
        let submissionId = "";
        if (currentExercise.submissions) {
            submissionId = currentExercise.submissions[currentSubmissionIndex].id.toString();
        }

        setSelectedValues((prevValues) => ({
            ...prevValues,
            [exerciseId]: {
                ...prevValues[exerciseId],
                [submissionId]: {
                    ...prevValues[exerciseId]?.[submissionId],
                    [feedbackType]: {
                        ...prevValues[exerciseId]?.[submissionId]?.[feedbackType],
                        [metricId]: value
                    }
                }
            }
        }));
    }

    if (!exercises && !metrics) {
        return <div className={"bg-white p-6 text-red-60"}>
            Could not fetch config data for expert evaluation (id={expert_evaluation_config_id})
        </div>;
    }

    if (!evaluationStarted) {
        return <div className={"bg-white p-6 text-red-60"}>The expert evaluation (id={expert_evaluation_config_id}) has not yet
            started.</div>;
    }

    if (!currentSubmissionIndex && !currentExerciseIndex && !selectedValues) {
        return <div className={"bg-white p-6 text-red-600"}>
            Could not find expert (id={expert_id}) belonging to expert evaluation (id={expert_evaluation_config_id}).
        </div>;
    }

    const currentExercise = exercises[currentExerciseIndex];
    const currentSubmission = currentExercise?.submissions?.[currentSubmissionIndex];
    const globalSubmissionIndex = exercises.slice(0, currentExerciseIndex).reduce((sum, exercise) => sum + exercise.submissions!.length, 0) + currentSubmissionIndex;

    if (currentExercise && currentSubmission && currentSubmission.feedbacks) {
        return (
            <div className={"bg-white p-6"}>
                <SideBySideHeader
                    exercise={exercises[currentExerciseIndex]}
                    globalSubmissionIndex={globalSubmissionIndex}
                    totalSubmissions={submissionsLength}
                    onNext={handleNext}
                    onPrevious={handlePrevious}
                    metrics={metrics}
                    onContinueLater={saveProgress}
                />
                <LikertScaleForm submission={currentSubmission as TextSubmission}
                                 exercise={currentExercise}
                                 feedback={currentSubmission.feedbacks}
                                 metrics={metrics}
                                 selectedValues={selectedValues}
                                 onLikertValueChange={handleLikertValueChange}/>
            </div>
        );
    } else {
        return <div>Loading...</div>;
    }
}

export default SideBySideExpertView;