export type ExerciseType = "text" | "programming" | "modelling";

export type StructuredGradingInstruction = {
  id: number;
  credits: number;
  feedback: string;
  usage_count: number;
  grading_scale: string;
  instruction_description: string;
};

export type GradingCriteria = {
  id: number;
  title: string;
  structured_grading_instructions: StructuredGradingInstruction[]
};

type ExerciseBase = {
  id: number;
  course_id: number;
  title: string;
  type: ExerciseType;
  max_points: number;
  bonus_points: number;
  grading_instructions?: string;
  grading_criteria?: GradingCriteria[];
  problem_statement?: string;
  meta: {
    [key: string]: any;
  };
};

export type TextExercise = ExerciseBase & {
  type: "text";
  example_solution?: string;
};

export type ProgrammingExercise = ExerciseBase & {
  type: "programming";
  programming_language: string;
  solution_repository_uri: string;
  template_repository_uri: string;
  tests_repository_uri: string;
};

export type ModellingExercise = ExerciseBase & {
  type: "modelling";
  example_solution?: string;
};

export type Exercise = TextExercise | ProgrammingExercise | ModellingExercise;
