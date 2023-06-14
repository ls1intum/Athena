import { ModuleMeta } from "@/model/health_response";
import TextEvaluation from "./text_evaluation";

export default function EvaluationMode({
  athenaUrl,
  athenaSecret,
  module,
}: {
  athenaUrl: string;
  athenaSecret: string;
  module: ModuleMeta;
}) {
  return (
    <div className="bg-white rounded-md p-4 mt-8">
      <h1 className="text-2xl font-bold mb-4">Evaluate</h1>
      <p className="text-gray-500 mb-4">
        Data in <code className="bg-gray-100 p-1">/data</code> directory will be used for evaluation.
      </p>
      {(module.type === "text" && (
        <TextEvaluation athenaUrl={athenaUrl} athenaSecret={athenaSecret} module={module} />
      )) || (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 text-sm text-yellow-700">
          The <b>{module.type}</b> module is not supported yet in evaluation
          mode.
        </div>
      )}
    </div>
  );
}
