// YourComponent.js

import React, { useState } from 'react';

const MovieCard = ({ title, overview, genres }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    return (
        <div className="flex justify-center mt-5 mb-5">
            <div className="bg-white rounded-lg shadow-lg p-6 w-[80vw] lg:w-[40vw]  border border-black">
                <h1 className="text-2xl font-bold mb-4">{title}</h1>
                <p className="text-gray-600 mb-4">{overview}</p>
                <div className="flex flex-wrap">
                    {genres.map((genre, index) => (
                        <span key={index} className="bg-blue-500 text-white rounded-full px-2 py-1 mr-2 mb-2 border">
                            {genre}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MovieCard;