// YourComponent.js

import React, { useState } from 'react';

const MovieCard = ({ title, overview, genres, year, imdbUrl, imageUrl }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    return (
        <div className="flex flex-col lg:flex-row justify-center items-center mt-5 mb-5 ">
            <div className="flex bg-white rounded-lg shadow-lg p-6 w-[80vw] border border-black">
                {/* Movie Poster */}
                <img className="h-64 mr-5 self-center" src={imageUrl} alt="Movie Poster" />

                {/* Text Content */}
                <div>
                    <a className="text-2xl font-bold mb-10 underline" target="_blank" href={imdbUrl}>
                        {title} ({year})
                    </a>
                    <p className="text-gray-600 mt-5 mb-4">{overview}</p>
                    <div className="flex flex-wrap">
                        {genres.map((genre, index) => (
                            <span key={index} className="bg-blue-500 text-white rounded-full px-2 py-1 mr-2 mb-2 border">
                                {genre}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>

    );
};

export default MovieCard;