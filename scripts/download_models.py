from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder.CrossEncoder import CrossEncoder

from config import settings

if __name__ == "__main__":
    cache_dir = settings.BASE_DIR / "models"

    print("Downloading cross-encoder...")
    model = CrossEncoder(settings.RERANKER_MODEL)
    model.save(str(cache_dir / settings.RERANKER_MODEL))

    print("Downloading embedder...")
    model = SentenceTransformer(settings.EMBEDDER_MODEL)
    model.save(str(cache_dir / settings.EMBEDDER_MODEL))
