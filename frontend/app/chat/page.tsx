"use client";
import { useState } from "react";
import axios from "axios";
import Link from "next/link";

export default function QnAPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [referencedBooks, setReferencedBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat/", { question });
      setAnswer(res.data.answer);
      setReferencedBooks(res.data.referenced_books || []);
    } catch (error) {
      setAnswer("Error connecting to the AI brain. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto p-6 mt-10">
      <h1 className="text-3xl font-bold mb-8">Intelligence Q&A</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Box */}
        <div className="border rounded-lg p-4 bg-gray-50 shadow-sm flex flex-col">
          <label className="block text-sm font-bold text-gray-700 mb-2">YOUR QUESTION</label>
          <textarea
            className="w-full h-48 p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            placeholder="e.g., Which books talk about history or human evolution?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button 
            onClick={askQuestion}
            disabled={loading}
            className="w-full py-3 bg-orange-500 text-white rounded-md hover:bg-orange-600 font-bold transition disabled:opacity-50 flex justify-center items-center gap-2"
          >
            {loading ? <span className="animate-spin text-xl">⏳</span> : "SUBMIT QUERY"}
          </button>
        </div>

        {/* Output Box */}
        <div className="border rounded-lg p-4 bg-white shadow-sm flex flex-col">
          <label className="block text-sm font-bold text-gray-700 mb-2">AI INSIGHT</label>
          <div className="w-full h-48 p-3 border rounded-md bg-gray-50 overflow-y-auto text-gray-800 mb-4 whitespace-pre-wrap">
            {loading ? "AI is analyzing the library..." : answer || "Submit a question..."}
          </div>
        </div>
      </div>

      {/* Requirement: Display summary / genre / recommendations */}
      {referencedBooks.length > 0 && (
        <div className="mt-8 border-t pt-6">
          <h2 className="text-2xl font-bold mb-4">📚 Sources & Metadata</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {referencedBooks.map((book: any) => (
              <div key={book.id} className="border p-4 rounded-lg bg-white shadow-sm border-l-4 border-l-blue-500">
                <h3 className="font-bold text-lg mb-1">{book.title}</h3>
                
                {/* Display Genre */}
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mb-2">
                  Genre: {book.genre}
                </span>
                
                {/* Display Summary */}
                <p className="text-sm text-gray-600 italic mb-3 line-clamp-2">
                  <span className="font-semibold not-italic">Summary:</span> {book.summary}
                </p>

                {/* Display Recommendations Link */}
                <Link 
                  href={`/book/${book.id}`} 
                  className="text-sm font-semibold text-orange-600 hover:underline"
                >
                  View Full Details & Recommendations &rarr;
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}