import SideBySideHeader from '@/components/expert_evaluation/expert_view/side_by_side_header';
import React, {useEffect, useState} from 'react';
import LikertScaleForm from "@/components/expert_evaluation/expert_view/likert_scale_form";
import {fetchExpertEvaluationExercisesEager} from "@/hooks/playground/exercises";
import {Exercise} from "@/model/exercise";
import {TextSubmission} from "@/model/submission";
import {fetchMetrics} from "@/hooks/playground/metrics";
import {Metric} from "@/model/metric";
import {
    fetchExpertEvaluationProgress,
    saveExpertEvaluationProgress
} from "@/hooks/playground/expert_evaluation_progress";
import {ExpertEvaluationProgress} from "@/model/expert_evaluation_progress";

function SideBySideExpertView() {
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [submissionsLength, setSubmissionsLength] = useState<number>(0);
    const [currentSubmissionIndex, setCurrentSubmissionIndex] = useState<number>(0);
    const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);
    const [metrics, setMetrics] = useState<Metric[]>([]);

    const [selectedValues, setSelectedValues] = useState<ExpertEvaluationProgress['selected_values']>({});

    const handleLikertValueChange = (feedbackType: string, metricTitle: string, value: number) => {
        const exerciseId = currentExercise.id.toString(); // Get current exercise ID
        let submissionId = "";
        if (currentExercise.submissions) {
            submissionId = currentExercise.submissions[currentSubmissionIndex].id.toString();
        }

  setSelectedValues((prevValues) => ({
    ...prevValues, // Preserve existing values for all exercises
    [exerciseId]: {
      ...prevValues[exerciseId], // Preserve existing values for this exercise
      [submissionId]: {
        ...prevValues[exerciseId]?.[submissionId], // Preserve existing values for this submission
        [feedbackType]: {
          ...prevValues[exerciseId]?.[submissionId]?.[feedbackType], // Preserve existing values for this feedback type
          [metricTitle]: value // Update the value for this specific metric
        }
      }
    }
  }));
};

    const expertEvaluationId = "23ccfc06-92bb-47de-a221-1c18b1d716cf"; //TODO hardcoded for now
    const dataMode = "expert_evaluation";
    const expertId = 1

    useEffect(() => {
            const fetchData = async () => {
                    try {
                        const exercises = await fetchExpertEvaluationExercisesEager(dataMode, expertEvaluationId);
                        setExercises(exercises);
                        const metrics = await fetchMetrics(dataMode, expertEvaluationId);
                        setMetrics(metrics);
                    } catch
                        (error) {
                        console.error('Error loading exercises: ', error);
                    }
                    try {
                        let progress = await fetchExpertEvaluationProgress(dataMode, expertEvaluationId, expertId);
                        setCurrentSubmissionIndex(progress.current_submission_index);
                        setCurrentExerciseIndex(progress.current_exercise_index);
                        setSelectedValues(progress.selected_values);
                    } catch (error) {
                        console.error('Error loading progress: ', error);
                    }
                }
            ;
            fetchData();
        }, []
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
        const progress: ExpertEvaluationProgress = {
            current_submission_index: currentSubmissionIndex,
            current_exercise_index: currentExerciseIndex,
            selected_values: selectedValues,
        };

        //setSelectedValues({});
        saveExpertEvaluationProgress(dataMode, expertEvaluationId, progress);
    }

    const currentExercise = exercises[currentExerciseIndex];
    const currentSubmission = currentExercise?.submissions?.[currentSubmissionIndex];
    //TODO
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