// QuizApp.js
"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload } from "lucide-react";
import apiClient from "@/components/service/axios";
import Questions from "@/components/questions";
import { db,auth } from "@/components/service/firebase";
import { collection, addDoc, doc, setDoc } from "firebase/firestore";
import { v4 as uuidv4 } from "uuid"; // For random test ID


export default function QuizApp() {
  const [file, setFile] = useState(null);
  const [generatedQuestions, setGeneratedQuestions] = useState({});
  const [selectedQuestions, setSelectedQuestions] = useState({});
  const [ws, setWs] = useState(null);
  const [progress, setProgress] = useState(0);
  const [flag, setFlag] = useState(false);
  const [showPopup, setShowPopup] = useState(false); // New state for popup visibility
  const [generatedUrl, setGeneratedUrl] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setSelectedQuestions((prev) => ({ ...prev, [name]: checked }));
  };

const sub = async () => {
  try {
    const userId = auth.currentUser.uid;
    const testId = uuidv4();
    const questions = Object.keys(selectedQuestions).filter(
      (key) => selectedQuestions[key] === true
    );

    const codesRef = doc(db, "tests", userId, "codes", testId);
    const url = `${document.location.origin}/test/${userId}/${testId}`; // Use forward slashes
    await setDoc(codesRef, {
      "questions": questions,
      "url": url
    });

    console.log("Created successfully");
    console.log(url);
    setGeneratedUrl((prev)=>url); // Store the URL
    setShowPopup(true); // Show the popup
    console.log(selectedQuestions);
  } catch (error) {
    console.error("Error uploading to Firebase:", error);
  }
};

  const initializeWebSocket = () => {
    let token = sessionStorage.getItem("access_token");
    const websocket = new WebSocket(`ws://localhost:8000/ws/?user_id=${token}`);

    websocket.onmessage = function (event) {
      const data = JSON.parse(event.data);
      setProgress(data.progress);
      console.log(parseFloat(data.progress));
      if (parseFloat(data.progress) >= 100) setFlag(false);
    };

    websocket.onopen = () => {
      console.log("WebSocket connected");
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    websocket.onclose = () => {
      console.log("WebSocket closed");
    };

    setWs(websocket);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const action = event.nativeEvent.submitter.name;

    if (action === "upload" && file) {
      const uploadData = new FormData();
      uploadData.append("file", file);

      try {
        const res = await apiClient.post("/uploadfile", uploadData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log("Upload Response:", res.data);
        uploadData.delete("file");
        initializeWebSocket();
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    } else if (action === "generate") {
      try {
        generate();
      } catch (error) {
        console.error("Error generating content:", error);
      }
    }
  };

  useEffect(() => {
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [ws]);

  useEffect(() => {
    console.log(generatedQuestions, "hehe");
  }, [generatedQuestions]);

  const generate = () => {
    apiClient
      .get("/gen-questions")
      .then((res) => {
        setGeneratedQuestions(res.data.questions || {});
        console.log(res.data);
      })
      .catch((error) => {
        console.error("Error fetching questions:", error);
        setGeneratedQuestions({});
      });
  };

  const hasQuestions = Object.keys(generatedQuestions).length > 0;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-black to-blue-800 relative overflow-hidden">
      <div className="absolute inset-0 opacity-10">
        <svg className="w-full h-full" viewBox="0 0 1440 320">
          <path
            fill="#ffffff"
            fillOpacity="0.2"
            d="M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
          >
            <animate
              attributeName="d"
              dur="10s"
              repeatCount="indefinite"
              values="..."
            />
          </path>
        </svg>
      </div>

      <div className="w-full max-w-7xl mx-2 flex flex-col md:flex-row z-10">
        {/* Left Section: File Uploader or Questions */}
        {hasQuestions ? (
            <Questions
            questions={generatedQuestions}
            selectedAnswers={selectedQuestions}
            onCheckboxChange={handleCheckboxChange}
            sub={sub}
            />
        ) : (
          <>
          <Card className="w-full md:w-1/2 p-6 shadow-lg rounded-2xl bg-gray-900 text-white">
            <CardContent className="flex flex-col items-center gap-4">
              <h2 className="text-xl font-bold text-center">Upload a Document</h2>
              <form onSubmit={handleFormSubmit} className="w-full flex flex-col gap-4">
                <label className="cursor-pointer bg-gray-800 px-4 py-2 rounded-lg hover:bg-gray-700 transition w-full text-center">
                  <input
                    type="file"
                    className="hidden"
                    onChange={handleFileChange}
                    />
                  <div className="flex items-center justify-center gap-2">
                    <Upload className="w-5 h-5 text-blue-400" />
                    <span>{file ? file.name : "Choose a file"}</span>
                  </div>
                </label>
                <Button
                  type="submit"
                  name="upload"
                  disabled={!file}
                  className="w-full bg-blue-700 hover:bg-blue-800 text-white"
                  >
                  Upload
                </Button>
              </form>
            </CardContent>
          </Card>
        

        <Card className="w-full md:w-1/2 p-6 shadow-lg rounded-2xl bg-gray-900 text-white">
          <CardContent className="flex flex-col gap-4">
            <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${progress}%` }}
                ></div>
            </div>
            <h2 className="text-xl font-bold text-center">Generated Questions</h2>
            <form onSubmit={handleFormSubmit} className="flex flex-col gap-4">
              {!hasQuestions && (
                <div className="mt-4 p-4 bg-gray-800 rounded-lg text-center text-gray-400">
                  <p>No questions generated yet</p>
                </div>
              )}
              <Button
                type="submit"
                name="generate"
                disabled={flag}
                className="w-full bg-blue-700 hover:bg-blue-800 text-white"
                >
                Generate
              </Button>
            </form>
          </CardContent>
        </Card>
        </>
        )}
      </div>
      {showPopup && (
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div className="bg-gray-900 p-6 rounded-lg shadow-lg text-white max-w-md w-full">
          <h3 className="text-lg font-bold mb-4">Test Link Generated</h3>
          <div className="flex items-center gap-2 mb-4">
            <input
              type="text"
              value={generatedUrl}
              readOnly
              className="w-full p-2 bg-gray-800 rounded text-white"
            />
            <Button
  onClick={() => {
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(generatedUrl)
        .then(() => alert("Link copied to clipboard!"))
        .catch((err) => {
          console.error("Failed to copy: ", err);
          alert("Copy failed");
        });
    } else {
      alert("Clipboard API not available");
    }
  }}
  className="bg-blue-700 hover:bg-blue-800"
>
  Copy
</Button>
          </div>
          <Button
            onClick={() => setShowPopup(false)}
            className="w-full bg-gray-700 hover:bg-gray-600"
          >
            Close
          </Button>
        </div>
      </div>
    )}
    </div>
  );
}