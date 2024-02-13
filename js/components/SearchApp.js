import React, { useState } from "react";
import { useForm } from "react-hook-form";
import MovieCard from "./MovieCard";

const SearchApp = () => {

    const rankingOptions = [
        { value: 'relevance', text: 'Show hidden gems 💎' },
        { value: 'popularity', text: 'Prioritize popular ⭐' },
    ];

    const { register, handleSubmit, setValue, watch } = useForm();
    const selectedRanking = watch('ranking');
    const [apiData, setApiData] = useState([]);
    const [loading, setLoading] = useState(false);

    const loadingImgUrl = URLS.loadingImgUrl;
    const emptyImgUrl = URLS.emptyImgUrl;


    const fetchData = async (query, ranking) => {
        setLoading(true);
        const url = `/recommend?query=${encodeURIComponent(query)}&ranking=${encodeURIComponent(ranking)}`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            setApiData(data);
        } catch (error) {
            setApiData([]);
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const onSubmit = (data) => {
        const query = data.query.trim();
        const ranking = data.ranking.trim();

        if (query === "") {
            setApiData([]);
        } else {
            fetchData(query, ranking);
        }
    };

    // Manually trigger form submission on select change
    const handleSelectChange = (event) => {
        setValue('ranking', event.target.value);
        handleSubmit(onSubmit)();
    };

    return (
        <div>
            <header className="sticky top-0 bg-slate-600 p-4 flex items-center justify-center h-[10vh] w-screen">
                <form id="searchForm" className="w-full md:w-4/5 lg:w-3/5 flex items-center justify-center" onSubmit={handleSubmit(onSubmit)}>


                    {/* Search Input */}
                    <input
                        id="searchInput"
                        autoFocus
                        className="w-full px-4 py-2 border rounded"
                        placeholder="Describe the kind of movie you want..."
                        type="search"

                        {...register("query")}
                    />

                    {/* Dropdown Menu */}
                    <select
                        className="ml-2 px-4 py-2 border rounded"
                        {...register("ranking")}
                        onChange={handleSelectChange}
                        value={selectedRanking}
                    >
                        {rankingOptions.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.text}
                            </option>
                        ))}
                    </select>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="ml-2 px-4 py-2 bg-green-500 text-white rounded"
                    >
                        Go
                    </button>
                </form>
            </header>


            <div>
                {loading ? (
                    <div className="flex justify-center items-center h-[90vh]">
                        <a href={"https://www.reddit.com/r/PixelArt/comments/10uravr/snes_just_chilling/"} target="_blank">
                            <img
                                src={loadingImgUrl}
                                alt="Loading..."
                                className="w-[90vw] md:w-[500px]"
                            />

                            <figcaption className="flex justify-center text-sm italic"><a href={"https://dribbble.com/shots/19097276-Pixel-Art-Loading-Screen-Animation"} target="_blank">Searching... (© Jayant Prasad)</a></figcaption>
                        </a>
                    </div>
                ) :

                    apiData.length === 0 ? (
                        <div className="flex justify-center items-center h-[90vh]">
                            <figure>
                                <a href={"https://www.reddit.com/r/PixelArt/comments/10uravr/snes_just_chilling/"} target="_blank">
                                    <img
                                        src={emptyImgUrl}
                                        alt="Empty"
                                        className="w-[90vw] md:w-[500px]"
                                    />
                                </a>
                                <figcaption className="flex justify-center text-xl italic">Nothing to see here. Try a new search.</figcaption>
                                <figcaption ><a className="flex justify-center text-sm italic" href={" https://www.reddit.com/r/PixelArt/comments/10uravr/snes_just_chilling/"} target="_blank">© u/teubase from Reddit</a></figcaption>
                            </figure>
                        </div>
                    ) : (
                        apiData.map((item, index) => (
                            <MovieCard
                                key={index}
                                title={item.title}
                                overview={item.overview}
                                genres={item.genres ?? []}
                                year={item.year ?? ""}
                                imdbUrl={item.imdb_url ?? ""}
                                imageUrl={item.poster_url ?? ""}
                                rating={item.vote_average ?? 0}
                                ratingCount={item.vote_count ?? 0}
                            />
                        ))
                    )

                }
            </div >
        </div >
    );
};

export default SearchApp;
