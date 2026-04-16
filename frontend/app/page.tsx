"use client";
import { useState, useEffect } from 'react';
import axios from 'axios';
import { BookOpen, MessageCircle, Star } from 'lucide-react';

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/books/').then(res => setBooks(res.data));
  }, []);

  const handleAsk = async () => {
    setLoading(true);
    const res = await axios.post('http://127.0.0.1:8000/api/chat/', { question });
    setAnswer(res.data.answer);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900">Document Intelligence Platform</h1>
        <p className="text-gray-500">AI-Powered Book Insights & RAG Querying</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Book List */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
          {books.map(book => (
            <div key={book.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
              <h3 className="font-bold text-xl mb-2">{book.title}</h3>
              <div className="flex items-center text-yellow-500 mb-2">
                <Star size={16} fill="currentColor" /> <span className="ml-1 text-sm">{book.rating}</span>
              </div>
              <p className="text-gray-600 text-sm line-clamp-3 mb-4">{book.description}</p>
              <a href={book.url} target="_blank" className="text-blue-600 text-sm font-medium hover:underline">View Source →</a>
            </div>
          ))}
        </div>

        {/* AI Chat Sidebar */}
        <div className="bg-white p-6 rounded-xl shadow-lg border border-blue-100 h-fit sticky top-8">
          <div className="flex items-center gap-2 mb-4 text-blue-600">
            <MessageCircle />
            <h2 className="font-bold text-lg">Ask the Librarian</h2>
          </div>
          <textarea 
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
            rows={4}
            placeholder="e.g. Which books talk about humanity?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button 
            onClick={handleAsk}
            className="w-full mt-4 bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
            disabled={loading}
          >
            {loading ? "Thinking..." : "Query RAG Pipeline"}
          </button>
          
          {answer && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
              <p className="text-sm text-gray-800 leading-relaxed">{answer}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}