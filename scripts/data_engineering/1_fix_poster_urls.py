import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

from config import settings


def get_poster_path(tmdb_id, api_key):
    base_url = "https://api.themoviedb.org/3/movie/"
    endpoint = str(tmdb_id)
    api_url = f"{base_url}{endpoint}?api_key={api_key}"

    try:
        response = requests.get(api_url)
        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return poster_path
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def main(input_movies_filepath, output_movies_filepath, api_key):

    # Ensure we don't accidentally overwrite the input CSV
    assert output_movies_filepath != input_movies_filepath

    # Read in Movies DF, and (in parallel) get the TMDB poster urls for each row
    movies_df = pd.read_csv(input_movies_filepath)

    error_tmdb_ids = []
    poster_paths = []

    with ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(
                    lambda row: (row.id, get_poster_path(row.id, api_key)),
                    movies_df.itertuples(),
                ),
                total=len(movies_df),
            )
        )

    # Iterate over results to populate poster_paths and handle errors
    for tmdb_id, poster_path in results:
        if poster_path:
            poster_paths.append(poster_path)
        else:
            print(f"Error retrieving poster URL for {tmdb_id}")
            error_tmdb_ids.append(tmdb_id)
            poster_paths.append(None)

    # Update the DF and save to a new CSV
    movies_df["poster_path"] = poster_paths
    movies_df.to_csv(output_movies_filepath, index=False)

    print(f"{len(error_tmdb_ids)} errors:\n{error_tmdb_ids}")


if __name__ == "__main__":
    in_filepath = settings.BASE_DIR / "data/movies_metadata.csv"
    out_filepath = settings.BASE_DIR / "data/movies_metadata_fixed_posters.csv"

    load_dotenv(settings.BASE_DIR / ".env")
    api_key = os.getenv("TMDB_API_KEY")

    main(in_filepath, out_filepath, api_key)
