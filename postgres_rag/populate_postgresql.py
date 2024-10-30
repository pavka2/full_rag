import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from constants import COLLECTION_NAME, DJANGO_DOCS_URL
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()


class PostgresSQLVectorStore:

    def build_database(self):
        script_path = "postgre_rag/rebuild_db.sh"
        subprocess.run(["bash", script_path], capture_output=True, text=True)

        # We are using the function that's defined above
        urls = self.django_docs_build_urls()

        # We can do the scraping ourselves and only look for .docs-content
        loader = WebBaseLoader(urls)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_documents = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()

        connection = os.environ.get("POSTGRES_URL")  # Uses psycopg3!
        collection_name = COLLECTION_NAME

        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection,
            use_jsonb=True,
        )

        texts = []
        metadatas = []

        for doc in split_documents:
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)

        vector_store.add_texts(texts, metadatas)
        print("Finish")

    def django_docs_build_urls(self):
        root_url = DJANGO_DOCS_URL
        user_agent = {"User-agent": "Mozilla/5.0"}

        root_response = requests.get(root_url, headers=user_agent)
        root_html = root_response.content.decode("utf-8")
        soup = BeautifulSoup(root_html, "html.parser")
        root_url_parts = urlparse(root_url)
        root_links = soup.find_all("a", attrs={"class": "reference internal"})

        result = set()

        for root_link in root_links:
            path = root_url_parts.path + root_link.get("href")
            path = str(Path(path).resolve())
            path = urlparse(path).path  # remove the hashtag

            url = f"{root_url_parts.scheme}://{root_url_parts.netloc}{path}"

            if not url.endswith("/"):
                url = url + "/"

            result.add(url)

        return list(result)


if __name__ == "__main__":
    agent = PostgresSQLVectorStore()
    agent.build_database()
