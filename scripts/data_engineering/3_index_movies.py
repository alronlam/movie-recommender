from datetime import datetime
from pathlib import Path

import pandas as pd
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from loguru import logger
from tqdm import tqdm

from config import settings


def rename_and_backup_directory(original_path):
    original_path = Path(original_path)

    # Check if the original directory exists
    if not original_path.exists() or not original_path.is_dir():
        print(f"Error: Directory '{original_path}' does not exist.")
        return

    # Generate a timestamp with milliseconds
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

    # Create a backup name by appending "-backup-" and the timestamp to the original name
    backup_name = original_path.stem + f"-backup-{timestamp}"

    # Construct the new path for the backup directory
    backup_path = original_path.parent / backup_name

    try:
        # Rename the original directory to the backup name
        original_path.rename(backup_path)
        print(f"Directory '{original_path}' renamed to '{backup_path}'.")
    except Exception as e:
        print(f"Error renaming directory: {e}")


def load_or_generate_faiss_index(docs, index_dir, cached_embedder, overwrite=False):
    index_path = Path(index_dir)

    # Rename and backup the dir if overwrite is True
    if index_path.exists() and overwrite:
        rename_and_backup_directory(index_dir)
        rename_and_backup_directory(
            cached_embedder.document_embedding_store.store.root_path
        )

    # Load the index if it exists and overwrite=False
    if index_path.exists() and not overwrite:
        db = FAISS.load_local(index_dir, cached_embedder)
    else:
        # Generate new index
        db = None
        with tqdm(total=len(docs), desc="Ingesting documents...") as pbar:
            for d in docs:
                if db:
                    db.add_documents([d])
                else:
                    db = FAISS.from_documents([d], cached_embedder)
                pbar.update(1)

        db.save_local(index_dir)

    return db


def main(
    model_name, embedding_cache_path, faiss_index_path, search_cols, overwrite=False
):
    # Load Embedding Model
    logger.info(f"Loading embedding model {model_name}")
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    bge_embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    # Initialize Embedding Cache
    logger.info(f"Initializing embedding cache at {embedding_cache_path}")
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        bge_embedding_model,
        document_embedding_cache=LocalFileStore(embedding_cache_path),
        namespace=namespace,
    )

    # Load Docs
    logger.info(f"Loading docs from {MOVIES_FILEPATH}")
    all_cols = pd.read_csv(MOVIES_FILEPATH).columns
    metadata_cols = [col for col in all_cols if col not in search_cols]
    docs = CSVLoader(file_path=MOVIES_FILEPATH, metadata_columns=metadata_cols).load()

    # Split Docs
    logger.info(f"Splitting docs")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    # Generate FAISS Index
    logger.info("Generating FAISS Index")
    db = load_or_generate_faiss_index(
        docs=documents,
        index_dir=faiss_index_path,
        cached_embedder=cached_embedder,
        overwrite=overwrite,
    )

    return db


if __name__ == "__main__":
    # Input Vars
    MOVIES_FILEPATH = settings.BASE_DIR / "data/movies_metadata_preprocessed.csv"
    OVERWRITE = False
    MODEL_NAME = "BAAI/bge-large-en-v1.5"
    SEARCH_COLS = ["title", "overview", "genres", "keywords_human_readable"]

    # Derived Vars
    model_name_wo_org = Path(MODEL_NAME).parts[-1]
    namespace = f"{model_name_wo_org}_title_overview_genres_keywords"
    faiss_index_path = settings.BASE_DIR / f"data/faiss_index_{namespace}"
    embedding_cache_path = settings.BASE_DIR / f"data/cache_{namespace}/"

    main(
        model_name=MODEL_NAME,
        embedding_cache_path=embedding_cache_path,
        faiss_index_path=faiss_index_path,
        search_cols=SEARCH_COLS,
        overwrite=OVERWRITE,
    )
