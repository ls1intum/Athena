import { Exercise } from "./exercise";
import { Submission } from "./submission";

type Experiment = {
  exercise: Exercise;
  submissions: Submission[];
};

export default Experiment;
