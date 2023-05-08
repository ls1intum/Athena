import type {NextApiRequest, NextApiResponse} from 'next';
import type {Exercise} from '@/pages/model/exercise';

import fs from 'fs';
import path from 'path';

function readExerciseFile(exerciseId: number, fileName: string) {
    const filePath = path.join(process.cwd(), 'exercises', "" + exerciseId, fileName);
    return fs.readFileSync(filePath, 'utf-8');
  }

const exampleExercises: Exercise[] = [
    {
        id: 1,
        title: 'Hello World',
        type: 'programming',
        max_points: 10,
        bonus_points: 0,
        problem_statement: readExerciseFile(1, 'problem-statement.md'),
        grading_instructions: readExerciseFile(1, 'grading-instructions.md'),
        programming_language: 'java',
        solution_repository_url: 'http://localhost:3000/api/programming-material/1/solution.zip',
        template_repository_url: 'http://localhost:3000/api/programming-material/1/template.zip',
        tests_repository_url: 'http://localhost:3000/api/programming-material/1/tests.zip',
        meta: {}
    },
    {
        id: 2,
        title: 'What is your name?',
        type: 'text',
        max_points: 10,
        bonus_points: 0,
        grading_instructions: 'Give full points if the student provides their name.',
        problem_statement: 'Write your name in the text field below.',
        example_solution: 'Maximilian',
        meta: {},
    }
];

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<Exercise[]>
) {
    res.status(200).json(exampleExercises);
}
