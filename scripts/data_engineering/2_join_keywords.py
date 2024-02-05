import sys

sys.path.append("../../")
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import loosejson
import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm.notebook import tqdm

from config import settings


def dedupe_keywords(keywords_df):
    # Construct a unified id to keywords mapping without duplicates
    mapping = {}
    for idx, row in keywords_df.iterrows():
        id = row["id"]
        keyword_dicts = row["keywords"]

        if id in mapping:
            existing_keyword_dicts = mapping[id]
            existing_keyword_strings = set([x["name"] for x in existing_keyword_dicts])

            for keyword_dict in keyword_dicts:
                if keyword_dict["name"] not in existing_keyword_strings:
                    existing_keyword_dicts.add(keyword_dict)
        else:
            mapping[id] = keyword_dicts

    data = list(mapping.items())
    keywords_deduped_df = pd.DataFrame(data, columns=["id", "keywords"])
    assert not keywords_deduped_df["id"].duplicated().any()
    return keywords_deduped_df


def main(movies_filepath, keywords_filepath, output_filepath):
    # Pre-process the keywords DF
    keywords_df = pd.read_csv(keywords_filepath, dtype={"id": object})
    keywords_df["keywords"] = keywords_df["keywords"].apply(
        lambda x: loosejson.parse_loosely_defined_json(x)
    )
    keywords_df = dedupe_keywords(keywords_df)
    keywords_df["keywords_human_readable"] = keywords_df["keywords"].apply(
        lambda arr: ", ".join([x["name"] for x in arr])
    )

    # Join the original DF with the pre-processed keyword columns
    movies_df = pd.read_csv(movies_filepath, dtype={"id": object})
    movies_with_keywords = movies_df.merge(keywords_df, how="left", on="id")
    # This is to ensure we have the same number of rows after joining the keywords.
    # # of rows can mismatch when there are duplicate IDs in the right dataframe
    assert len(movies_with_keywords) == len(
        movies_df
    ), f"Mismatch in lengths: {len(movies_with_keywords)} output vs {len(movies_df)} input"
    movies_with_keywords.to_csv(output_filepath, index=False)


if __name__ == "__main__":

    main(
        movies_filepath=settings.BASE_DIR / "data/movies_metadata_fixed_posters.csv",
        keywords_filepath=settings.BASE_DIR / "data/keywords.csv",
        output_filepath=settings.BASE_DIR / "data/movies_metadata_preprocessed.csv",
    )
