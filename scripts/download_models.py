from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder.CrossEncoder import CrossEncoder

from config import settings

if __name__ == "__main__":
    cache_dir = settings.BASE_DIR / "models"

    print("Downloading cross-encoder...")
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
    model.save(str(cache_dir / "cross-encoder/ms-marco-MiniLM-L-12-v2"))

    print("Downloading embedder...")
    model = SentenceTransformer("BAAI/llm-embedder")
    model.save(str(cache_dir / "BAAI/llm-embedder"))
