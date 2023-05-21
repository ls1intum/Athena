import path from "path";
import fs from "fs";

import {Exercise} from "@/model/exercise";
import {Submission} from "@/model/submission";
import Feedback from "@/model/feedback";
import baseUrl from "@/helpers/base_url";


const jsonPlaceholders: { [key: string]: string } = {
    "baseUrl": baseUrl,
};


function replaceJsonPlaceholders(json: any, exerciseId: number) {
    // 1. Replace all file references found anywhere in the json with the file contents from examples/<reference>
    //    File references look like this: `-> file:example.txt`
    // 2. Replace placeholders from the jsonPlaceholders object.
    //    Placeholders look like this: `{{placeholder}}`
    const result: any = {};
    for (const key in json) {
        if (json.hasOwnProperty(key)) {
            let value = json[key];
            if (typeof value === 'string') {
                if (value.startsWith('-> file:')) {
                    // file reference replacement
                    const filePath = path.join(process.cwd(), 'examples', 'exercise-' + exerciseId, value.split(':')[1]);
                    if (fs.existsSync(filePath)) {
                        value = fs.readFileSync(filePath, 'utf8');
                    } else {
                        throw new Error(`File ${filePath} not found`);
                    }
                }
                // placeholder replacement
                for (const placeholderKey in jsonPlaceholders) {
                    if (jsonPlaceholders.hasOwnProperty(placeholderKey)) {
                        const placeholderValue = jsonPlaceholders[placeholderKey];
                        value = value.replace(new RegExp(`{{${placeholderKey}}}`, 'g'), placeholderValue);
                    }
                }
                result[key] = value;
            } else if (Array.isArray(value)) {
                result[key] = value.map((item) => replaceJsonPlaceholders(item, exerciseId));
            } else if (typeof value === 'object') {
                result[key] = replaceJsonPlaceholders(value, exerciseId);
            } else {
                result[key] = value;
            }
        }
    }
    return result;
}

function getExampleExerciseJSON(exerciseId: number): any {
    // find in cwd/examples/submissions/<exerciseId>.json
    const submissionsPath = path.join(process.cwd(), 'examples', `exercise-${exerciseId}.json`);
    if (fs.existsSync(submissionsPath)) {
        const exerciseJson = JSON.parse(fs.readFileSync(submissionsPath, 'utf8'));
        return replaceJsonPlaceholders(exerciseJson, exerciseId);
    }
    throw new Error(`No example submissions found for exercise ${exerciseId}`);
}

function getAllExampleExerciseJSON(): any[] {
    // find in cwd/examples/submissions/*.json
    const submissionsPath = path.join(process.cwd(), 'examples');
    const exerciseIds = fs.readdirSync(submissionsPath)
        .filter((fileName) => fileName.endsWith('.json'))
        .map((fileName) => {
            // filename looks like `exercise-<exerciseId>.json`
            return parseInt(fileName.split('.')[0].split('-')[1]);
        });
    return exerciseIds.map(getExampleExerciseJSON);
}


function jsonToExercise(json: any): Exercise {
    const exercise = json as Exercise;
    // drop submissions from response to have a real Exercise
    // @ts-ignore
    delete exercise['submissions'];
    return exercise;
}

function jsonToSubmissions(json: any): Submission[] {
    return json.submissions.map((submissionJson: any) => {
        const submission = submissionJson as Submission;
        // exercise_id is not provided in the json for convenience, so we add it here
        submission.exercise_id = json.id;
        // drop feedbacks from response to have a real Submission
        // @ts-ignore
        delete submission['feedbacks'];
        return submission;
    });
}

function jsonToFeedbacks(json: any): Feedback[] {
    let feedbacks: Feedback[] = [];

    json.submissions.forEach((submissionJson: any) => {
        if (submissionJson.feedbacks) {
            const additionalFeedbacks = submissionJson.feedbacks.map((feedbackJson: any) => {
                const feedback = feedbackJson as Feedback;
                // exercise_id is not provided in the json for convenience, so we add it here
                feedback.exercise_id = json.id;
                // submission_id is not provided in the json for convenience, so we add it here
                feedback.submission_id = submissionJson.id;
                return feedback;
            });
            feedbacks = [...feedbacks, ...additionalFeedbacks];
        }
    });

    return feedbacks;
}


export function getExampleExercises(): Exercise[] {
    return getAllExampleExerciseJSON().map(jsonToExercise);
}

export function getExampleSubmissions(exerciseId?: number): Submission[] {
    if (exerciseId !== undefined) {
        return jsonToSubmissions(getExampleExerciseJSON(exerciseId));
    }
    return getAllExampleExerciseJSON().flatMap(jsonToSubmissions);
}

export function getExampleFeedbacks(exerciseId?: number): Feedback[] {
    if (exerciseId !== undefined) {
        return jsonToFeedbacks(getExampleExerciseJSON(exerciseId));
    }
    return getAllExampleExerciseJSON().flatMap(jsonToFeedbacks);
}