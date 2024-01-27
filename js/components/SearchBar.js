import React from "react";
import { useForm } from "react-hook-form";

const SearchBar = () => {
    const { register, handleSubmit } = useForm();
    const onSubmit = (d) => alert(JSON.stringify(d));

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
        </div>

    );

}

export default SearchBar;