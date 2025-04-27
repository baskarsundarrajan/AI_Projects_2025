"use client";
import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { db } from "@/components/service/firebase";
import { getDoc, doc } from '@firebase/firestore';
import apiClient from '@/components/service/axios';

const QuestionsPage = () => {
  const [result, setResult] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [apiResponse, setApiResponse] = useState(null); // New state for API response
  const [isSubmitted, setIsSubmitted] = useState(false); // New state for submission status
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const params = useParams();
  const testId = params.testId;

  // Fetch questions from Firestore on component mount
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const codesRef = doc(db, "tests", testId[0], "codes", testId[1]);
        const docSnap = await getDoc(codesRef);
        if (docSnap.exists()) {
          const fetchedQuestions = docSnap.data()["questions"];
          setQuestions(fetchedQuestions);
        } else {
          setError('No questions found');
        }
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch questions');
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [testId]);

  // Handle answer input changes
  const handleAnswerChange = (questionIndex, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: value
    }));
  };

  // Handle form submission for all answers
  const handleSubmit = async () => {
    try {
      // Prepare results
      const results = questions.map((q, index) => ({
        question: q,
        answer: answers[index] || '',
      }));
      setResult(results); // Update result state
      setIsSubmitted(true); // Disable textareas

      // Send to API
      const res = await apiClient.post("/evaluate-batch", { batch: results });
      console.log('API Response:', res.data);
      setApiResponse(res.data); // Store API response
    } catch (err) {
      console.error('Submission failed:', err);
      setError('Failed to submit answers');
      setIsSubmitted(false); // Re-enable textareas on error
    }
  };

  if (loading) return <div className="text-white text-center mt-20">Loading...</div>;
  if (error) return <div className="text-red-500 text-center mt-20">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white relative overflow-hidden">
      {/* Background SVG */}
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
              values="
                M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z;
                M0,192L48,181.3C96,171,192,149,288,154.7C384,160,480,192,576,197.3C672,203,768,181,864,165.3C960,149,1056,139,1152,144C1248,149,1344,171,1392,181.3L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z;
                M0,224L48,213.3C96,203,192,181,288,165.3C384,149,480,139,576,149.3C672,160,768,192,864,197.3C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
            />
          </path>
        </svg>
      </div>

      {/* Main content */}
      <div className="relative z-10 container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-8 text-center">Questions</h1>
        
        <div className="space-y-6">
          {questions.map((item, index) => (
            <div 
              key={index}
              className="bg-gray-800 rounded-lg p-6 shadow-lg"
            >
              <h2 className="text-xl font-semibold mb-4">{item}</h2>
              
              <div className="flex flex-col gap-4">
                <textarea
                  value={answers[index] || ''}
                  onChange={(e) => handleAnswerChange(index, e.target.value)}
                  placeholder="Type your answer here..."
                  disabled={isSubmitted} // Disable textarea after submission
                  className={`flex-1 p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:border-blue-500 text-white resize-y min-h-[100px] ${isSubmitted ? 'opacity-50 cursor-not-allowed' : ''}`}
                />
                {/* Display API response under the textarea */}
                {apiResponse && apiResponse.results[index] && (
                  <div className="text-sm mt-2">
                    <p className={apiResponse.results[index].evaluation==="correct" ? 'text-green-400' : 'text-red-400'}>
                      {apiResponse.results[index].evaluation==="correct" ? 'Correct' : 'Incorrect'}
                    </p>
                    {apiResponse.results[index].justification && (
                      <p className="text-gray-300">{apiResponse.results[index].justification}</p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {/* Single Submit Button */}
          {questions.length > 0 && !isSubmitted && (
            <div className="flex justify-center mt-8">
              <button
                onClick={handleSubmit}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-lg font-semibold transition-colors"
              >
                Submit All Answers
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuestionsPage;