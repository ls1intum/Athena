import { Exercise } from "@/model/exercise";
import { Metric } from "@/model/metric";

export type ExpertEvaluationConfig = {
  type: "evaluation_config";
  creationDate: Date;
  id: string;
  name: string;
  metrics: Metric[];
  exercises: Exercise[];
  expertIds: string[];
};
