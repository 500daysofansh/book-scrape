"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [syncing, setSyncing] = useState(false);

  useEffect(() => {
    // Fetch books from your GET /api/books/ endpoint
    axios.get("http://127.0.0.1:8000/api/books/").then((res) => setBooks(res.data));
  }, []);

  const triggerScraper = async () => {
    setSyncing(true);
    await axios.post("http://127.0.0.1:8000/api/process/");
    alert("Scraping finished! Refreshing data...");
    const res = await axios.get("http://127.0.0.1:8000/api/books/");
    setBooks(res.data);
    setSyncing(false);
  };

  return (
    <div className="max-w-7xl mx-auto p-6 mt-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Intelligence Library</h1>
        <button 
          onClick={triggerScraper}
          disabled={syncing}
          className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 disabled:opacity-50"
        >
          {syncing ? "🔄 Scraping Web..." : "➕ Sync New Books"}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {books.map((book: any) => (
          <div key={book.id} className="border p-5 rounded-lg shadow-sm hover:shadow-md transition bg-white">
            <h2 className="text-xl font-bold text-gray-800 line-clamp-1">{book.title}</h2>
            <p className="text-sm text-gray-500 mb-2">Author: {book.author}</p>
            <span className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded mb-3">
              Rating: {book.rating}
            </span>
            <p className="text-gray-600 text-sm line-clamp-3 mb-4">{book.description}</p>
            <Link href={`/book/${book.id}`} className="text-blue-500 hover:underline text-sm font-semibold">
              View Full Insights &rarr;
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}