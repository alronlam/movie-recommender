// YourComponent.js

import React, { useState } from 'react';
import { FaStar } from "react-icons/fa";

const MovieCard = ({ title, overview, genres, year, imdbUrl, imageUrl, rating, ratingCount }) => {
    const [imageLoaded, setImageLoaded] = useState(true);

    const handleError = () => {
        setImageLoaded(false);
    };

    const renderStars = () => {
        const maxStars = 10;
        const displayStars = 5;
        const filledStars = Math.round((rating / maxStars) * displayStars);
        const blankStars = displayStars - filledStars;

        const stars = [];

        // Filled stars
        for (let i = 0; i < filledStars; i++) {
            stars.push(<FaStar key={i} color="#ffc107" />);
        }

        // Blank stars
        for (let i = 0; i < blankStars; i++) {
            stars.push(<FaStar key={filledStars + i} color="#ddd" />);
        }

        return stars;
    };

    return (
        <div className="flex flex-col lg:flex-row justify-center items-center mt-5 mb-5 ">
            <div className="flex bg-white rounded-lg shadow-lg p-6 w-[80vw] border border-black">
                {/* Movie Poster */}
                {imageLoaded ? (
                    <img className="h-64 mr-5 self-center" src={imageUrl} alt="Movie Poster" onError={handleError} />
                ) : (
                    <img className="h-64 mr-5 self-center" src="/static/poster-missing.webp" alt="Movie Poster" onError={handleError} />
                )}


                {/* Text Content */}
                <div>
                    <a className="text-2xl font-bold mb-10 underline" target="_blank" href={imdbUrl}>
                        {title} ({year})
                    </a>
                    <div className="flex items-center">
                        {renderStars()}
                        <span className="ml-2">{`${rating} (${ratingCount} ratings)`}</span>
                    </div>
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