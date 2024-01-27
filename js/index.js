import React from 'react';
import ReactDOM from "react-dom/client";
import MovieCard from './components/MovieCard';
import SearchBar from './components/SearchBar';
import "./styles/tailwind.css";


const page = (
    <div>
        <SearchBar />
        <MovieCard title="Title" overview="Overview" genres={["Comedy", "Romance"]} />
        <MovieCard title="Title" overview="Overview" genres={["Comedy", "Romance"]} />
        <MovieCard title="Title" overview="Overview" genres={["Comedy", "Romance"]} />

    </div>
);


const root = document.getElementById('root');
const rootContainer = ReactDOM.createRoot(root);
rootContainer.render(page);