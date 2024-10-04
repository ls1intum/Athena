import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faTrash, faSave, faPlus } from "@fortawesome/free-solid-svg-icons";

type Metric = {
  title: string;
  summary: string;
  description: string;
};

type MetricsFormProps = {
  metrics: Metric[];
  setMetrics: (metrics: Metric[]) => void;
};

export default function MetricsForm({ metrics, setMetrics }: MetricsFormProps) {
  const [editIndex, setEditIndex] = useState<number | null>(null);
  const [editingMetric, setEditingMetric] = useState<Metric>({
    title: "",
    summary: "",
    description: "",
  });
  const [newMetric, setNewMetric] = useState<Metric>({
    title: "",
    summary: "",
    description: "",
  });

  // Handle input changes for both editing and adding metrics
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    isEditing: boolean = false
  ) => {
    const { name, value } = e.target;
    if (isEditing) {
      setEditingMetric((prevMetric) => ({
        ...prevMetric,
        [name]: value,
      }));
    } else {
      setNewMetric((prevMetric) => ({
        ...prevMetric,
        [name]: value,
      }));
    }
  };

  // Add new metric
  const addMetric = () => {
    if (!newMetric.title.trim() || !newMetric.summary.trim() || !newMetric.description.trim()) {
      return; // Prevent adding empty metrics
    }

    setMetrics([...metrics, newMetric]);
    setNewMetric({ title: "", summary: "", description: "" }); // Reset form
  };

  // Start editing a metric in place
  const startEditMetric = (index: number) => {
    setEditIndex(index);
    setEditingMetric(metrics[index]);
  };

  // Save the edited metric
  const saveMetric = () => {
    if (editIndex !== null) {
      const updatedMetrics = metrics.map((metric, index) =>
        index === editIndex ? editingMetric : metric
      );
      setMetrics(updatedMetrics);
      setEditIndex(null); // Exit editing mode
    }
  };

  // Remove a metric by index
  const removeMetric = (index: number) => {
    setMetrics(metrics.filter((_, i) => i !== index));
  };

  return (
    <label className="flex flex-col">
      <span className="text-lg font-bold">Metrics</span>
      <div className="flex flex-col gap-4">

        {/* List of added metrics with in-place editing */}
        {metrics.map((metric, index) => (
          <div key={index} className="flex flex-col gap-2 border p-4 rounded-md shadow-sm">
            {editIndex === index ? (
              <div className="space-y-2">
                {/* Editable fields */}
                <input
                  type="text"
                  name="title"
                  value={editingMetric.title}
                  onChange={(e) => handleChange(e, true)}
                  className="border border-gray-300 rounded-md p-2 w-full"
                  placeholder="Metric Title"
                />
                <input
                  type="text"
                  name="summary"
                  value={editingMetric.summary}
                  onChange={(e) => handleChange(e, true)}
                  className="border border-gray-300 rounded-md p-2 w-full"
                  placeholder="Metric Summary"
                />
                <textarea
                  name="description"
                  value={editingMetric.description}
                  onChange={(e) => handleChange(e, true)}
                  className="border border-gray-300 rounded-md p-2 w-full"
                  rows={2}
                  placeholder="Metric Description"
                />
                <button
                  onClick={saveMetric}
                  className="bg-green-500 text-white rounded-md p-2 hover:bg-green-600 flex items-center gap-2"
                >
                  <FontAwesomeIcon icon={faSave} />
                  Save
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                {/* Display metric data */}
                <div className="flex flex-col gap-2">
                  <input
                    type="text"
                    value={metric.title}
                    readOnly
                    className="border border-gray-300 rounded-md p-2 w-full"
                    placeholder="Metric Title"
                  />
                  <input
                    type="text"
                    value={metric.summary}
                    readOnly
                    className="border border-gray-300 rounded-md p-2 w-full"
                    placeholder="Metric Summary"
                  />
                  <textarea
                    value={metric.description}
                    readOnly
                    className="border border-gray-300 rounded-md p-2 w-full"
                    rows={2}
                    placeholder="Metric Description"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => startEditMetric(index)}
                    className="bg-gray-500 text-white rounded-md p-2 hover:bg-gray-600 flex items-center gap-2"
                  >
                    <FontAwesomeIcon icon={faEdit} />
                    Edit
                  </button>
                  <button
                    onClick={() => removeMetric(index)}
                    className="bg-red-500 text-white rounded-md p-2 hover:bg-red-600 flex items-center gap-2"
                  >
                    <FontAwesomeIcon icon={faTrash} />
                    Remove
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}

        {/* Form to add a new metric */}
        <div className="flex flex-col gap-2 border p-4 rounded-md shadow-sm mt-4">
          <div>
            <label className="block text-sm">
              <span className="text-gray-700">Title</span>
              <input
                type="text"
                name="title"
                value={newMetric.title}
                onChange={(e) => handleChange(e, false)}
                className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                placeholder="Enter Metric Title"
              />
            </label>
          </div>

          <div>
            <label className="block text-sm">
              <span className="text-gray-700">Summary</span>
              <input
                type="text"
                name="summary"
                value={newMetric.summary}
                onChange={(e) => handleChange(e, false)}
                className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                placeholder="Enter Metric Summary"
              />
            </label>
          </div>

          <div>
            <label className="block text-sm">
              <span className="text-gray-700">Description</span>
              <textarea
                name="description"
                value={newMetric.description}
                onChange={(e) => handleChange(e, false)}
                className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                rows={3}
                placeholder="Enter Metric Description"
              />
            </label>
          </div>

          <div className="flex gap-2">
            <button
              onClick={addMetric}
              className="bg-green-600 text-white rounded-md p-2 hover:bg-green-700 flex items-center gap-2"
            >
              <FontAwesomeIcon icon={faPlus}/>
              Add Metric
            </button>
          </div>
          </div>
        </div>
    </label>
);
}
