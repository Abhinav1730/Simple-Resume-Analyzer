import React, { useState } from "react";
import axios from "axios";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post("https://simple-resume-analyzer-backand.onrender.com/upload", formData);
      setData(res.data);
    } catch (error) {
      console.error(error);
      alert("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center px-4 py-10"
      style={{ backgroundImage: "url('/job.jpg')" }}
    >
      <div className="bg-white bg-opacity-90 rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 w-full max-w-5xl space-y-8 overflow-y-auto max-h-screen">
        <h2 className="text-2xl sm:text-3xl font-bold text-center text-gray-800">
          📄 Upload Your Resume
        </h2>

        {/* Upload input */}
        <div className="flex flex-col items-center gap-4">
          <label className="cursor-pointer px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition shadow-md">
            Upload Resume
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
              accept=".pdf,.txt"
            />
          </label>

          {file && (
            <p className="text-sm text-gray-700">
              Selected: <span className="font-medium">{file.name}</span>
            </p>
          )}

          {file && (
            <button
              onClick={handleUpload}
              className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition duration-200"
            >
              Analyze
            </button>
          )}

          {loading && (
            <div className="flex justify-center mt-4">
              <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
        </div>

        {/* Results Section */}

        {data && (
          <div className="space-y-10 mt-6">
            {/* Extracted Skills */}

            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">
                🛠 Extracted Skills
              </h3>
              <div className="flex flex-wrap gap-3">
                {data.skills.map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium shadow-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Skill Plot */}

            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">
                📊 Top Jobs Based on Your Resume
              </h3>
              <div className="flex justify-center">
                <img
                  src={`http://localhost:5000${data.plot}`}
                  alt="Skill Match Plot"
                  className="rounded-lg shadow-lg w-full max-w-xl"
                />
              </div>
            </div>

            {/* Recommended Jobs */}

            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">
                💼 Recommended Jobs
              </h3>
              <div className="grid gap-6 grid-cols-1 sm:grid-cols-2">
                {data.jobs.map((job, index) => (
                  <div
                    key={index}
                    className="bg-white shadow-md rounded-lg p-6 border border-gray-200 hover:shadow-lg transition"
                  >
                    <h4 className="text-lg font-semibold text-blue-700">
                      {job.title}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      <em>{job.company_name}</em> — {job.location}
                    </p>
                    <p className="text-sm mt-2 text-gray-700">
                      {job.description}
                    </p>
                    <a
                      href={job.job_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block mt-3 text-sm font-medium text-blue-600 hover:underline"
                    >
                      Apply Now →
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadResume;
