from backend.services.embedding_service import (
    store_chunks,
    retrieve,
)


def test_retrieve_relevant_chunk():

    store_chunks(
        [
            "Paris is the capital of France",
            "Python is a programming language",
        ],
        "user1"
    )

    results = retrieve(
        "What is the capital of France?",
        "user1"
    )

    assert "Paris" in results[0]