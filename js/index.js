import React from 'react';
import ReactDOM from "react-dom/client";
import SearchApp from './components/SearchApp';
import "./styles/tailwind.css";


const page = (
    <div>
        <SearchApp />
    </div>
);


const root = document.getElementById('root');
const rootContainer = ReactDOM.createRoot(root);
rootContainer.render(page);