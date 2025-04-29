// components/Questions.js
import React from "react";
import { Button } from "@/components/ui/button";

export default function Questions({ questions, selectedAnswers, onCheckboxChange,sub }) {
  // Convert questions object to array of [key, value] pairs
//   const questionEntries = Object.entries(questions);

  return (
    <div className="w-full p-6 shadow-lg rounded-2xl bg-gray-900 text-white">
      <h2 className="text-xl font-bold text-center mb-4">Generated Questions</h2>
      <div className="space-y-4">
        {questions.map(( question,key) => (
          <label key={key} className="flex items-center gap-2">
            <input
              type="checkbox"
              name={question}
              checked={selectedAnswers[question] || false}
              onChange={onCheckboxChange}
              className="h-5 w-5 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500"
            />
            <span className="text-white">{question}</span>
          </label>
        ))}
      </div>
         <Button onClick={sub}
            className="w-full bg-blue-700 mt-4 hover:bg-blue-800 text-white"
         >
            Create Test
         </Button>
    </div>
  );
}