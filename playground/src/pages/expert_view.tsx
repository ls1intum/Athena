import SideBySideHeader from '@/components/expert_evaluation/expert_view/side_by_side_header';
import React, {useEffect, useState} from 'react';
import LikertScaleForm from "@/components/expert_evaluation/expert_view/likert_scale_form";
import {fetchExercises} from "@/hooks/playground/exercises";
import {fetchSubmissions} from "@/hooks/playground/submissions";
import {Exercise} from "@/model/exercise";
import {Submission} from "@/model/submission";

function SideBySideExpertView() {
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [submissions, setSubmissions] = useState<any[]>([]);
    const [currentSubmissionIndex, setCurrentSubmissionIndex] = useState<number>(0);
    const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const exercises = await fetchExercises("evaluation");
                setExercises(exercises);

                let allSubmissions: Submission[] = [];
                for (const exercise of exercises) {
                    let submissionsData = await fetchSubmissions(exercise, "evaluation");

                    // Randomize the order of submissions for this exercise
                    submissionsData = submissionsData.sort(() => Math.random() - 0.5);
                    allSubmissions = [...allSubmissions, ...submissionsData]; // Accumulate submissions
                }

                setSubmissions(allSubmissions);
            } catch (error) {
                console.error('Error loading exercises and submissions:', error);
            }
        };
        fetchData();
    }, []);

    if (!exercises) {
        return <div>Loading...</div>;
    }

    const handleNext = () => { //TODO save on next
        setCurrentSubmissionIndex((prevIndex) => Math.min(prevIndex + 1, submissions.length - 1));
        if (submissions[currentSubmissionIndex].exercise_id !== exercises[currentExerciseIndex].id) {
            setCurrentExerciseIndex(currentExerciseIndex + 1);
        }


    };

    const handlePrevious = () => { //TODO save on prev
        setCurrentSubmissionIndex((prevIndex) => Math.max(prevIndex - 1, 0));
        if (submissions[currentSubmissionIndex].exercise_id !== exercises[currentExerciseIndex].id) {
            setCurrentExerciseIndex(currentExerciseIndex - 1);
        }
    };

    return (
        <div className={"bg-white p-6"}>
            <SideBySideHeader
                exercise={exercises[currentExerciseIndex]}
                currentSubmissionIndex={currentSubmissionIndex}
                totalSubmissions={submissions.length}
                onNext={handleNext}
                onPrevious={handlePrevious}
            />
            <LikertScaleForm submission={submissions[currentSubmissionIndex]}
                             exercise={exercises[currentExerciseIndex]}/>
        </div>
    );
}

export default SideBySideExpertView;