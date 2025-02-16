import React, { useState } from 'react';
import './App.css'; // Import your CSS

function App() {
    const [topic, setTopic] = useState('');
    const [sources, setSources] = useState(''); // New state for sources input
    const [newsResults, setNewsResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleTopicChange = (event) => {
        setTopic(event.target.value);
    };

    const handleSourcesChange = (event) => {
        setSources(event.target.value);
    };

        const fetchNews = async () => {
        console.log("fetchNews function called!"); // <--- ADD THIS LINE

        setLoading(true);
        setError(null);
        setNewsResults([]); // Clear previous results

        console.log("Before fetch() call..."); // <--- ADD THIS LINE

        try {
            const queryString = new URLSearchParams({ topic: topic, sources: sources }).toString();
            const response = await fetch(`http://127.0.0.1:5000/api/scrape?${queryString}`);
            console.log("After fetch() call, response received..."); // <--- ADD THIS LINE
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setNewsResults(data);
            console.log("News results updated:", data); // <--- ADD THIS LINE
        } catch (e) {
            setError(e);
            console.error("Error fetching news:", e);
            console.log("Error caught:", e); // <--- ADD THIS LINE
        } finally {
            setLoading(false);
            console.log("fetchNews function finally block executed, loading set to false."); // <--- ADD THIS LINE
        }
    };

    return (
        <div className="App">
            <h1>News Scraper</h1>
            <div className="input-area">
                <label htmlFor="topic-input">Enter Topic:</label>
                <input
                    type="text"
                    id="topic-input"
                    value={topic}
                    onChange={handleTopicChange}
                    placeholder="e.g., Technology, Finance, Sports"
                />
                <label htmlFor="sources-input">Enter Sources (comma-separated, optional):</label>
                <input
                    type="text"
                    id="sources-input"
                    value={sources}
                    onChange={handleSourcesChange}
                    placeholder="e.g., bbc-news,cnn"
                />
                <button onClick={fetchNews} disabled={loading}>
                    {loading ? 'Scraping...' : 'Scrape News'}
                </button>
            </div>

            {error && <p className="error">Error: {error.message}</p>}
            {loading && <p>Loading news...</p>}

            <div className="results-container">
                {newsResults.map((result, index) => (
                    <div key={index} className={`news-pane ${index < 2 ? 'large-pane' : ''}`}>
                        <h3><a href={result.link} target="_blank" rel="noopener noreferrer">{result.title}</a></h3>
                        {result.summary && <p>{result.summary}</p>}
                        <p><a href={result.link} target="_blank" rel="noopener noreferrer">Read More</a> (Source: {result.source})</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;