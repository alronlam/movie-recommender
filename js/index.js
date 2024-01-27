import React from 'react';
import ReactDOM from "react-dom/client";

import { useForm } from "react-hook-form";
import "./index.css";


const SearchBar = () => {
    const { register, handleSubmit } = useForm();
    const onSubmit = (d) => alert(JSON.stringify(d));

    return (
        <div>
            <header className="sticky top-0 bg-neongreen p-4 flex items-center justify-center h-[8vh] w-screen">

                <form onSubmit={handleSubmit(onSubmit)} action="/search" method="GET" className='w-full flex items-center justify-center'>
                    <input
                        autoFocus
                        className="w-4/5 md:w-3/5 lg:w-2/5  px-4 py-2 border rounded"
                        placeholder="Describe the kind of movie you like..."
                        type="search"
                        {...register("q")}
                    />
                </form>
            </header>
        </div>

    );

}

export default SearchBar;

const page = (
    <div>
        <SearchBar />
    </div>
);


const root = document.getElementById('root');
const rootContainer = ReactDOM.createRoot(root);
rootContainer.render(page);