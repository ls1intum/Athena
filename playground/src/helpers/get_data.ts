import type {Exercise} from "@/model/exercise";
import type {Submission} from "@/model/submission";
import type {CategorizedFeedback, Feedback} from "@/model/feedback";
import type {DataMode} from "@/model/data_mode";

import path from "path";
import fs from "fs";

import baseUrl from "@/helpers/base_url";
import {Metric} from "@/model/metric";
import {ExpertEvaluationProgress} from "@/model/expert_evaluation_progress";
import {ExpertEvaluationConfig} from "@/model/expert_evaluation_config";

/**
 * Splits the given data mode into its parts.
 *
 * @param dataMode - the data mode to split
 *
 * @returns the parts of the given data mode
 *  - ["example"] for "example"
 *  - ["evaluation"] for "evaluation"
 *  - ["evaluation", "custom"] for "evaluation-custom"
 */
export function getDataModeParts(dataMode: DataMode): string[] {
    const [mainMode, ...rest] = dataMode.split("-");
    const customMode = rest.join("-");
    return customMode ? [mainMode, customMode] : [mainMode];
}

function replaceJsonPlaceholders(
    dataMode: DataMode,
    json: any,
    exerciseId: number,
    athenaOrigin: string
) {
    // 1. Replace all file references found anywhere in the json with the file contents from data/example/<reference>
    //    File references look like this: `-> file:example.txt`
    // 2. Replace a few placeholders.
    //    Placeholders look like this: `{{placeholder}}`
    const jsonPlaceholders: { [key: string]: string } = {
        exerciseDataUrl: `${athenaOrigin}${baseUrl}/api/data/${dataMode}/exercise/${exerciseId}/data`,
    };
    const result: any = {};
    for (const key in json) {
        if (json.hasOwnProperty(key)) {
            let value = json[key];
            if (typeof value === "string") {
                // This is only for example exercises, for evaluation the data is already in the json
                if (value.startsWith("-> file:")) {
                    // file reference replacement
                    const filePath = path.join(
                        process.cwd(),
                        "data",
                        "example",
                        "exercise-" + exerciseId,
                        value.split(":")[1]
                    );
                    if (fs.existsSync(filePath)) {
                        value = fs.readFileSync(filePath, "utf8");
                    } else {
                        throw new Error(`File ${filePath} not found`);
                    }
                }
                // placeholder replacement
                for (const placeholderKey in jsonPlaceholders) {
                    if (jsonPlaceholders.hasOwnProperty(placeholderKey)) {
                        const placeholderValue = jsonPlaceholders[placeholderKey];
                        value = value.replace(
                            new RegExp(`{{${placeholderKey}}}`, "g"),
                            placeholderValue
                        );
                    }
                }
                result[key] = value;
            } else if (Array.isArray(value)) {
                result[key] = value.map((item) =>
                    replaceJsonPlaceholders(dataMode, item, exerciseId, athenaOrigin)
                );
            } else if (typeof value === "object" && value !== null) {
                result[key] = replaceJsonPlaceholders(
                    dataMode,
                    value,
                    exerciseId,
                    athenaOrigin
                );
            } else {
                result[key] = value;
            }
        }
    }
    return result;
}

/**
 * Adds the exercise type to all submissions and feedbacks in the given json.
 * This is only for the playground, because the exercise type is not provided in the json for convenience.
 *
 * @param json - the json to add the exercise type to
 * @returns the json with the exercise type added to all submissions and feedbacks
 */
function addExerciseTypeToSubmissionsAndFeedbacks(json: any): any {
    const exerciseType = json.type;

    json.submissions = json.submissions?.map((submissionJson: any) => {
        submissionJson.type = exerciseType;

        if (Array.isArray(submissionJson.feedbacks)) {
            submissionJson.feedbacks = submissionJson.feedbacks?.map((feedbackJson: any) => {
                feedbackJson.type = exerciseType;
                return feedbackJson;
            });
        }

        return submissionJson;
    });
    return json;
}

/**
 * Removes all null values from the given json.
 *
 * @param json - the json to remove the null values from
 * @param recursive - whether to remove null values recursively
 * @returns the json without null values
 */
function removeNullValues(json: any, recursive: boolean = true): any {
    if (Array.isArray(json)) {
        return json.filter(item => item !== null).map(item => {
            if (recursive && typeof item === "object" && item !== null) {
                return removeNullValues(item, recursive);
            } else {
                return item;
            }
        });
    } else if (typeof json === 'object' && json !== null) {
        const result: any = {};
        for (const key in json) {
            if (json.hasOwnProperty(key)) {
                const value = json[key];
                if (value !== null) {
                    if (recursive && typeof value === "object" && value !== null) {
                        result[key] = removeNullValues(value, recursive);
                    } else {
                        result[key] = value;
                    }
                }
            }
        }
        return result;
    } else {
        return json;
    }
}

function getExerciseJSON(
    dataMode: DataMode,
    exerciseId: number,
    athenaOrigin: string
): any {
    // find in cwd/data/<dataMode>/exercise-<exerciseId>.json
    // or in cwd/data/evaluation/<custom>/exercise-<exerciseId>.json if dataMode is evaluation-<custom>
    const exercisePath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `exercise-${exerciseId}.json`
    );
    if (fs.existsSync(exercisePath)) {
        let exerciseJson = JSON.parse(fs.readFileSync(exercisePath, "utf8"));
        exerciseJson = replaceJsonPlaceholders(
            dataMode,
            exerciseJson,
            exerciseId,
            athenaOrigin
        );
        exerciseJson = addExerciseTypeToSubmissionsAndFeedbacks(exerciseJson);
        if (exerciseJson.submissions) {
            exerciseJson.submissions = removeNullValues(exerciseJson.submissions);
        }
        return exerciseJson;
    }
    throw new Error(`Exercise ${exerciseId} not found`);
}

function getEvaluationConfigJSON(
    dataMode: DataMode,
    expertEvaluationId: string,
): any {

    const configPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_config_${expertEvaluationId}.json`
    );

    if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, "utf8"));
    }
    throw new Error(`Evaluation Config ${expertEvaluationId} not found`);
}


function getAllExerciseJSON(dataMode: DataMode, athenaOrigin: string): any[] {
    // find in cwd/data/<dataMode> all exercise-*.json
    // or in cwd/data/evaluation/<custom> all exercise-*.json if dataMode is evaluation-<custom>
    const parts = getDataModeParts(dataMode);
    const exercisesDir = path.join(process.cwd(), "data", ...parts);

    // Check if the directory exists
    if (!fs.existsSync(exercisesDir)) {
        return [];
    }

    const exerciseIds = fs
        .readdirSync(exercisesDir)
        .filter(
            (fileName) =>
                fileName.endsWith(".json") && fileName.startsWith("exercise-")
        )
        .map((fileName) => {
            return parseInt(fileName.split(".")[0].split("-")[1]);
        });
    return exerciseIds.map((id) => getExerciseJSON(dataMode, id, athenaOrigin));
}

function jsonToExercise(json: any): Exercise {
    const exercise = json as Exercise;
    // drop submissions from response to have a real Exercise
    // @ts-ignore
    delete exercise["submissions"];
    return exercise;
}

//TODO shuffle when exporting
function jsonToExerciseAndShuffleSubmissionsAndFeedback(json: any, addStructuredGrading: boolean = false): Exercise {
    let exercise = json as Exercise;

    const submissions = exercise.submissions;
    if (submissions) {
        // Shuffle submissions //TODO when creating config
        /*   exercise.submissions = submissions.sort(() => Math.random() - 0.5);*/

        for (const submission of submissions) {
            const feedback = submission.feedbacks;

            if (feedback) {
                // Shuffle the feedback categories //TODO when creating config
                /* const shuffledFeedbackEntries = Object.entries(feedback).sort(() => Math.random() - 0.5);
                 submission.feedbacks = Object.fromEntries(shuffledFeedbackEntries);*/

                if (addStructuredGrading) {
                    const processedFeedbacks: CategorizedFeedback = {};

                    Object.keys(feedback).forEach((category) => {
                        const categoryFeedback = feedback[category];
                        if (Array.isArray(categoryFeedback)) {
                            // Map over feedback and link structured grading instructions
                            processedFeedbacks[category] = feedback[category].map((feedbackItem) => {
                                // Link structured grading instructions
                                if (feedbackItem.structured_grading_instruction_id) {
                                    feedbackItem.structured_grading_instruction = exercise?.grading_criteria
                                        ?.flatMap((criteria) => criteria.structured_grading_instructions)
                                        .find((instruction) => instruction.id === feedbackItem.structured_grading_instruction_id);
                                }
                                return feedbackItem;
                            });
                        }
                    });
                    // Replace submission feedbacks with processed feedbacks
                    submission.feedbacks = processedFeedbacks;

                }
            }
        }
    }
    return exercise;
}

export function randomizeSubmissionAndFeedbackTypeOrder(exercise: Exercise){
    const submissions = exercise.submissions;
    if (submissions) {
        // Shuffle submissions
           exercise.submissions = submissions.sort(() => Math.random() - 0.5);

        for (const submission of submissions) {
            const feedback = submission.feedbacks;

            if (feedback) {
                // Shuffle the feedback categories
                 const shuffledFeedbackEntries = Object.entries(feedback).sort(() => Math.random() - 0.5);
                 submission.feedbacks = Object.fromEntries(shuffledFeedbackEntries);
            }
        }
    }
}

function jsonToSubmissions(json: any): Submission[] {
    return json.submissions.map((submissionJson: any) => {
        const submission = submissionJson as Submission;
        // exercise_id is not provided in the json for convenience, so we add it here
        submission.exercise_id = json.id;
        // drop feedbacks from response to have a real Submission
        // @ts-ignore
        delete submission["feedbacks"];
        return submission;
    });
}

function jsonToFeedbacks(json: any): Feedback[] {
    return json.submissions.flatMap((submissionJson: any) => {
        if (Array.isArray(submissionJson.feedbacks)) {
            const feedbacks = submissionJson.feedbacks.map((feedbackJson: any) => {
                const feedback = feedbackJson as Feedback;
                // exercise_id is not provided in the json for convenience, so we add it here
                feedback.exercise_id = json.id;
                // submission_id is not provided in the json for convenience, so we add it here
                feedback.submission_id = submissionJson.id;
                return feedback;
            });
            return feedbacks;
        }
        return [];
    });
}

function jsonToMetrics(json: any): Metric [] {
    return json.metrics;
}

export function getExercises(dataMode: DataMode, athenaOrigin: string): Exercise[] {
    return getAllExerciseJSON(dataMode, athenaOrigin).map(jsonToExercise);
}

export function getExercisesEager(dataMode: DataMode, athenaOrigin: string): Exercise[] {
    return getAllExerciseJSON(dataMode, athenaOrigin).map(json => jsonToExerciseAndShuffleSubmissionsAndFeedback(json));
}

export function getExpertEvaluationExercisesEager(dataMode: DataMode, expertEvaluationId: string): Exercise[] {
    return getEvaluationConfigJSON(dataMode, expertEvaluationId).exercises.map((json: any) => jsonToExerciseAndShuffleSubmissionsAndFeedback(json, true))
}

export function getSubmissions(
    dataMode: DataMode,
    exerciseId: number | undefined,
    athenaOrigin: string
): Submission[] {
    if (exerciseId !== undefined) {
        return jsonToSubmissions(getExerciseJSON(dataMode, exerciseId, athenaOrigin));
    }
    return getAllExerciseJSON(dataMode, athenaOrigin).flatMap(jsonToSubmissions);
}

export function getFeedbacks(
    dataMode: DataMode,
    exerciseId: number | undefined,
    athenaOrigin: string
): Feedback[] {
    if (exerciseId !== undefined) {
        return jsonToFeedbacks(getExerciseJSON(dataMode, exerciseId, athenaOrigin));
    }
    return getAllExerciseJSON(dataMode, athenaOrigin).flatMap(jsonToFeedbacks);
}

export function getMetrics(
    dataMode: DataMode,
    expertEvaluationId: string,
): Metric[] {

    return jsonToMetrics(getEvaluationConfigJSON(dataMode, expertEvaluationId));
}

export function saveProgressToFileSync(
    dataMode: DataMode,
    expertEvaluationId: string,
    expertId: string,
    expertEvaluationProgress: ExpertEvaluationProgress
) {
    const progressData = JSON.stringify(expertEvaluationProgress, null, 2);

    const progressPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_${expertEvaluationId}`,
        `evaluation_progress_${expertId}.json`
    );

    return fs.writeFileSync(progressPath, progressData, 'utf8');
}

export function saveConfigToFileSync(
    dataMode: DataMode,
    expertEvaluation: ExpertEvaluationConfig
) {
    const configData = JSON.stringify(expertEvaluation, null, 2);

    const configPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_config_${expertEvaluation.id}.json`
    );

    const progress: ExpertEvaluationProgress = {
        current_submission_index: 0,
        current_exercise_index: 0,
        selected_values: {},
    };
    const expertProgressData = JSON.stringify(progress, null, 2);

    let dirPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_${expertEvaluation.id}`);

    // Create parent directory
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, {recursive: true});
    }

    if (expertEvaluation.expertIds) {
        for (const expertId of expertEvaluation.expertIds) {
            // Create json for each expert
            let expertProgressPath = path.join(
                dirPath,
                `evaluation_progress_${expertId}.json`
            );

            fs.writeFileSync(expertProgressPath, expertProgressData, 'utf8');
        }
    }

    // Create config file with exercises and data
    return fs.writeFileSync(configPath, configData, 'utf8');
}

export function getProgressFromFileSync(
    dataMode: DataMode,
    expertEvaluationId: string,
    expertId: string
): ExpertEvaluationProgress | undefined {

    const progressPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_${expertEvaluationId}`,
        `evaluation_progress_${expertId}.json`
    );

    if (!fs.existsSync(progressPath)) {
        console.log(`Could not find find expert ${expertId}, belonging to expert evaluation ${expertEvaluationId}`);
        return undefined;
    }

    //TODO error handling?
    return JSON.parse(fs.readFileSync(progressPath, "utf8"));
}

export function getConfigFromFileSync(
    dataMode: DataMode,
    expertEvaluationId: string
): ExpertEvaluationConfig | undefined {
    const configPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_config_${expertEvaluationId}.json`
    );

    if (!fs.existsSync(configPath)) {
        console.log(`Could not find find expert evaluation ${expertEvaluationId}`);
        return undefined;
    }
    return JSON.parse(fs.readFileSync(configPath, "utf8"));
}

//TODO
export function getAnonymizedConfigFromFileSync(
    dataMode: DataMode,
    expertEvaluationId: string
): ExpertEvaluationConfig | undefined {
    const configPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode),
        `evaluation_config_${expertEvaluationId}.json`
    );

    if (!fs.existsSync(configPath)) {
        console.log(`Could not find find expert evaluation ${expertEvaluationId}`);
        return undefined;
    }

    const config: ExpertEvaluationConfig = JSON.parse(fs.readFileSync(configPath, "utf8"));
    delete config["expertIds"];

        //TODO rethink anonymization
/*
    const renamedFeedback: any = {};

    for (const exercise of config.exercises) {
        const submissions = exercise.submissions;

        if (submissions) {
            for (const submission of submissions) {
                const feedback = submission.feedbacks;

                if (feedback) {
                    const renamedFeedback: any = {}; // Temporary object for renamed feedback

                    // Rename the feedback categories to numbers starting from 0
                    Object.keys(feedback).forEach((category, index) => {
                        renamedFeedback[index] = feedback[category]; // Assign numeric keys
                    });

                    // Replace the original feedback with the renamed feedback
                    submission.feedbacks = renamedFeedback;
                }
            }
        }
    }*/
    return config;
}

export function getAllConfigsFromFilesSync(
    dataMode: DataMode,
): ExpertEvaluationConfig [] {

    const configPath = path.join(
        process.cwd(),
        "data",
        ...getDataModeParts(dataMode));

    const configs: ExpertEvaluationConfig[] = [];

    if (!fs.existsSync(configPath)) {
        return configs;
    }

    fs.readdirSync(configPath)
        .filter((file) => file.startsWith('evaluation_config_') && file.endsWith('.json'))
        .forEach((file) => {
            const filePath = path.join(configPath, file);
            const fileContents = fs.readFileSync(filePath, 'utf8');

            try {
                const config = JSON.parse(fileContents) as ExpertEvaluationConfig;
                configs.push(config);

            } catch (error) {
                console.error(`Error parsing JSON from file ${file}:`, error);
            }
        });

    return configs;
}

