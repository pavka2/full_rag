import os

from constants import COLLECTION_NAME
from dotenv import load_dotenv
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()


def answer_query(*, question: str, use_gpt_4o: bool):
    gpt_model = "gpt-3.5-turbo-0125"

    if use_gpt_4o:
        gpt_model = "gpt-4o"

    embeddings = OpenAIEmbeddings()
    collection_name = COLLECTION_NAME

    connection = os.environ.get("POSTGRES_URL")  # Uses psycopg3!

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )

    custom_retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    # Use Langchain's LLM to process the retrieved documents and generate the answer
    llm = ChatOpenAI(model=gpt_model, temperature=0.7)

    # Create the chain using the retrieved documents
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=custom_retriever,  # Replace the retriever with your retrieved docs
        chain_type_kwargs={"verbose": True},
    )

    result = chain({"question": question}, return_only_outputs=True)
    return result

def ask_question():
    use_gpt_4o = input("Would you like to use gpt-4o (y/n): ").lower().strip() in [
        "y",
        "yes",
    ]

    question = input("Ask a question related to Django: ")

    result = answer_query(question=question, use_gpt_4o=use_gpt_4o)

    print(result["answer"])
    print(result["sources"])


if __name__ == "__main__":
    ask_question()
