import React from 'react';

function SideBySideHeader() {
  return (
    <div className={"mb-12"}>
      {/* Title and Submission Info Section */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-4 space-y-2 md:space-y-0">
        <h1 className="text-3xl font-semibold text-gray-900">Side by Side Evaluation</h1>
        <span className="text-lg text-gray-700">
          Submission <strong>15</strong> / 105
        </span>
      </div>

      {/* Subtitle and Details Buttons Section */}
      <div className="flex flex-col md:flex-row justify-between items-end gap-4">
        <div className="flex flex-col gap-2 w-full md:w-auto">
          <span className="text-lg text-gray-800">
            Exercise L13E02 Strategy vs. Bridge (id=642)
          </span>
          <div className="flex flex-col md:flex-row gap-2 w-full">
            <button className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition">
              📄 Exercise Details
            </button>
            <button className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition">
              📊 Metric Details
            </button>
            <button className="w-full md:w-auto px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition">
              📚 Evaluation Tutorial
            </button>
          </div>
        </div>

        {/* Navigation Buttons Section */}
        <div className="flex flex-col items-end gap-2 mt-4 md:mt-0 w-full md:w-[250px]">
          <button className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition w-full">
            😴 Continue Later
          </button>
          <div className="flex gap-2 w-full">
            <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition min-w-[120px] md:w-auto">
              ⬅️ Previous
            </button>
            <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition min-w-[120px] md:w-auto">
              Next ➡️
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SideBySideHeader;