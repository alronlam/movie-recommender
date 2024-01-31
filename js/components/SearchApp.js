import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import MovieCard from "./MovieCard";

const SearchApp = () => {
    const { register, setValue } = useForm();
    const [apiData, setApiData] = useState([]);

    useEffect(() => {
        let debounceTimeout;

        const fetchData = async (query) => {
            const url = `/recommend?query=${encodeURIComponent(query)}`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                setApiData(data);
            } catch (error) {
                console.error(error);
            }
        };

        // Fetch data initially with an empty query or default query
        fetchData("");

        // Listen for changes in the query field and trigger fetch after debouncing
        const handleChange = (event) => {
            const query = event.target.value;

            clearTimeout(debounceTimeout);

            debounceTimeout = setTimeout(() => {
                setValue("query", query);
                if (query.trim() === "") {
                    // Clear the MovieCards if the query is blank
                    setApiData([]);
                } else {
                    fetchData(query);
                }
            }, 100); // Adjust the debounce delay as needed (e.g., 300 milliseconds)
        };

        // Attach the event listener
        const inputElement = document.getElementById("searchInput");
        if (inputElement) {
            inputElement.addEventListener("input", handleChange);
        }

        // Cleanup the event listener on component unmount
        return () => {
            if (inputElement) {
                inputElement.removeEventListener("input", handleChange);
            }
        };
    }, [setValue]);

    return (
        <div>
            <header className="sticky top-0 bg-slate-600 p-4 flex items-center justify-center h-[10vh] w-screen">
                <input
                    id="searchInput"
                    autoFocus
                    className="w-full md:w-3/5  px-4 py-2 border rounded"
                    placeholder="Describe the kind of movie you like..."
                    type="search"
                    {...register("query")}
                />

            </header>

            {apiData.map((item, index) => (
                <MovieCard
                    key={index}
                    title={item.title}
                    overview={item.overview}
                    genres={item.genres ?? []}
                    year={item.year ?? ""}
                    imdbUrl={item.imdb_url ?? ""}
                    imageUrl={item.poster_url ?? ""}
                />
            ))}
        </div>
    );
};

export default SearchApp;
