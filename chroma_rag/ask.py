from constants import CHROMA_DB_DIRECTORY
from dotenv import load_dotenv
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def answer_query(*, question: str, use_gpt_4o: bool):
    embeddings = OpenAIEmbeddings()
    db = Chroma(
        collection_name="ask_django_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIRECTORY,
    )
    gpt_model = "gpt-3.5-turbo-0125"

    if use_gpt_4o:
        gpt_model = "gpt-4o"

    llm = ChatOpenAI(model=gpt_model, temperature=0.7)

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
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
