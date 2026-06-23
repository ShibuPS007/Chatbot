from sentence_transformers import SentenceTransformer
import chromadb
import uuid

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def get_embedding_model():
    return model


def store_chunks(chunks,user_id):

    embeddings = model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[str(uuid.uuid4()) for _ in chunks],
        metadatas=[{"user_id": user_id}] * len(chunks)
    )


def retrieve(question: str,user_id:str):

    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3,
        where={"user_id": user_id}
    )

    return results["documents"][0]