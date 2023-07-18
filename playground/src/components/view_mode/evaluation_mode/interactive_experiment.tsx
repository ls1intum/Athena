import Experiment from "@/model/experiment";

export default function InteractiveExperiment({ experiment }: { experiment: Experiment }) {
  return (
    <div className="bg-white rounded-md p-4 mb-8">
      <h3 className="text-2xl font-bold mb-4">Interactive Experiment</h3>
    </div>
  )
}
