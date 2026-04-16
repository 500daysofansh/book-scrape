"use client";
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'next/navigation';

export default function BookDetails() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    // Fetch book details
    axios.get(`http://127.0.0.1:8000/api/books/${id}/`).then(res => setBook(res.data));
    // Fetch recommendations
    axios.get(`http://127.0.0.1:8000/api/books/${id}/recommend/`).then(res => setRecs(res.data));
  }, [id]);

  if (!book) return <div className="p-10">Loading Intelligence...</div>;

  return (
    <div className="max-w-4xl mx-auto p-10">
      <h1 className="text-4xl font-black mb-4">{book.title}</h1>
      <div className="flex gap-2 mb-6">
        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold uppercase">{book.genre}</span>
        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold uppercase">Sentiment: {book.sentiment}</span>
      </div>

      <div className="bg-slate-50 p-6 rounded-2xl border-l-4 border-blue-500 mb-8">
        <h2 className="font-bold mb-2">AI Generated Summary</h2>
        <p className="text-slate-700 italic">"{book.summary}"</p>
      </div>

      <h3 className="font-bold text-xl mb-4">Recommended for you</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recs.map(r => (
          <div key={r.id} className="border p-4 rounded-xl hover:shadow-md transition">
            <h4 className="font-bold text-sm">{r.title}</h4>
            <p className="text-xs text-slate-500 mt-1 line-clamp-1">{r.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}