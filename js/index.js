import React from 'react';
import ReactDOM from "react-dom/client";
import SearchBar from './components/SearchBar';
import "./index.css";


const page = (
    <div>
        <SearchBar />
    </div>
);


const root = document.getElementById('root');
const rootContainer = ReactDOM.createRoot(root);
rootContainer.render(page);