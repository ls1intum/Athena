import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy, faTrash, faCheck, faPlus } from "@fortawesome/free-solid-svg-icons";
import baseUrl from "@/helpers/base_url"; // Import the base URL

type ExpertLinksProps = {
  expertIds: string[];
  setExpertIds: (newExpertIds: string[]) => void;
  started: boolean;
  configId: string;
};

export default function ExpertLinks({ expertIds, setExpertIds, started, configId }: ExpertLinksProps) {
  const [copiedLink, setCopiedLink] = useState<string | null>(null);

  // Add a new expert ID
  const addExpertId = () => {
    const newExpertId = uuidv4();
    setExpertIds([...expertIds, newExpertId]);
  };

  // Copy the link to the clipboard
  const copyLink = (link: string) => {
    navigator.clipboard.writeText(link);
    setCopiedLink(link);
    setTimeout(() => setCopiedLink(null), 2000);
  };

  // Delete an expert ID
  const deleteExpertId = (id: string) => {
    setExpertIds(expertIds.filter((expertId) => expertId !== id));
  };

  return (
    <section className="flex flex-col">
      <div className="flex justify-between items-center mb-2">
        <span className="text-lg font-bold">Expert Links</span>

        {/* Add New Expert Button */}
        <button
          className="bg-green-500 text-white rounded-md p-2 hover:bg-green-600 flex items-center gap-2"
          onClick={addExpertId}
        >
          <FontAwesomeIcon icon={faPlus}/>
          Add New Expert
        </button>
      </div>

      {/* List of Expert Links */}
      <ul className="space-y-2">
        {expertIds.map((expertId) => {
          const expertLink = `${window.location.origin}${baseUrl}/${configId}/${expertId}/expert_view`;

          return (
            <li key={expertId} className="flex justify-between items-center border p-2 rounded-md shadow-sm">
              <a href={expertLink} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
                {expertLink}
              </a>

              <div className="flex space-x-2">
                {/* Copy Link Button */}
                <button
                  className="bg-blue-500 text-white rounded-md p-2 hover:bg-blue-600"
                  onClick={() => copyLink(expertLink)}
                  title="Copy Link"
                >
                  <FontAwesomeIcon icon={copiedLink === expertLink ? faCheck : faCopy} />
                </button>

                {/* Delete Button */}
                {!started && (
                  <button
                    className="bg-red-500 text-white rounded-md p-2 hover:bg-red-600"
                    onClick={() => deleteExpertId(expertId)}
                    title="Delete Link"
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                )}
              </div>
            </li>
          );
        })}
        {expertIds.length === 0 && <li className="border p-2 rounded-md shadow-sm bg-gray-50 text-center">No expert links added</li>}
      </ul>
    </section>
  );
}