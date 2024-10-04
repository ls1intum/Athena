import SideBySideHeader from '@/components/expert_evaluation/expert_view/side_by_side_header';
import React, {useEffect, useState} from 'react';
import LikertScaleForm from "@/components/expert_evaluation/expert_view/likert_scale_form";
import {fetchExercisesEager} from "@/hooks/playground/exercises";
import {Exercise} from "@/model/exercise";
import {TextSubmission} from "@/model/submission";

function SideBySideExpertView() {
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [submissionsLength, setSubmissionsLength] = useState<number>(0);
    const [currentSubmissionIndex, setCurrentSubmissionIndex] = useState<number>(0);
    const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const exercises = await fetchExercisesEager("expert_evaluation");
                setExercises(exercises);

                let total_submissions = 0;
                for (const exercise of exercises) {
                    if (exercise.submissions) {
                        exercise.submissions = exercise.submissions.sort(() => Math.random() - 0.5);
                        total_submissions += exercise.submissions.length;
                    }
                    setSubmissionsLength(total_submissions);
                }

            } catch (error) {
                console.error('Error loading exercises and submissions:', error);
            }
        };
        fetchData();
    }, []);


    const handleNext = () => { //TODO save on next
        const currentExercise = exercises[currentExerciseIndex];

        // If we are at the last submission for the current exercise, go to the next exercise
        if (currentSubmissionIndex < currentExercise.submissions!.length - 1) {
            setCurrentSubmissionIndex((prevIndex) => prevIndex + 1);

        } else if (currentExerciseIndex < exercises.length - 1) {
            // Move to the next exercise, reset submission index
            setCurrentExerciseIndex((prevIndex) => prevIndex + 1);
            setCurrentSubmissionIndex(0); // Reset submission index for the new exercise
        }
    };

    const handlePrevious = () => { //TODO save on prev
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
                />
                <LikertScaleForm submission={currentSubmission as TextSubmission}
                                 exercise={currentExercise}
                                 feedback={currentSubmission.feedbacks}/>
            </div>
        );
    } else {
        return <div>Loading...</div>;
    }
}

export default SideBySideExpertView;