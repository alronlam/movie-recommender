import React, { useState } from "react";
import { useForm } from "react-hook-form";
import MovieCard from "./MovieCard";

const SearchApp = () => {
    const { register, handleSubmit } = useForm();
    const [apiData, setApiData] = useState([]);

    const onSubmit = (d) => {
        const url = `/recommend?query=${encodeURIComponent(d["query"])}`;
        fetch(url)  // get the data from the API
            .then(res => res.json())  // parse to JSON
            .then(
                (responseJson) => {
                    setApiData(responseJson);
                }
            ).catch(error => console.error(error));
    };

    return (
        <div>
            <header className="sticky top-0 bg-slate-600 p-4 flex items-center justify-center h-[10vh] w-screen">
                <form onSubmit={handleSubmit(onSubmit)} action="/search" method="GET" className='w-full flex items-center justify-center'>
                    <input
                        autoFocus
                        className="w-full md:w-3/5  px-4 py-2 border rounded"
                        placeholder="Describe the kind of movie you like..."
                        type="search"
                        {...register("query")}
                    />
                </form>
            </header>

            {apiData.map((item, index) => (
                <MovieCard
                    key={index}
                    title={item.title}
                    overview={item.overview}
                    genres={item.genres}
                    year={item.year}
                    imdbUrl={item.imdbUrl}
                    imageUrl={item.imageUrl}
                />
            ))}

        </div>

    );

}

export default SearchApp;