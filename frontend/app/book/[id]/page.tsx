"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "next/navigation";

export default function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState<any>(null);

  useEffect(() => {
    if (id) {
      axios.get(`http://127.0.0.1:8000/api/books/${id}/`).then((res) => setBook(res.data));
    }
  }, [id]);

  if (!book) return <div className="p-10 text-center text-xl">Loading Intelligence...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6 mt-10">
      <div className="bg-white border rounded-xl shadow-lg p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">{book.title}</h1>
        <p className="text-lg text-gray-600 mb-6">By {book.author}</p>

        <div className="flex gap-4 mb-8">
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
            Genre: {book.genre}
          </span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
            Sentiment: {book.sentiment}
          </span>
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-bold border-b pb-2 mb-4">AI Summary</h2>
          <p className="text-gray-700 italic border-l-4 border-orange-400 pl-4 bg-gray-50 py-2">
            {book.summary}
          </p>
        </div>

        <div>
          <h2 className="text-xl font-bold border-b pb-2 mb-4">Full Description</h2>
          <p className="text-gray-800 leading-relaxed whitespace-pre-line">
            {book.description}
          </p>
        </div>

        <div className="mt-8 pt-4 border-t">
          <a href={book.url} target="_blank" rel="noreferrer" className="text-blue-500 hover:underline">
            View Original Source ↗
          </a>
        </div>
      </div>
    </div>
  );
}