from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from constants import CHROMA_DB_DIRECTORY, DJANGO_DOCS_URL

load_dotenv()


class ChromaBuilder:
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

    def build_database(self):
        # We are using the function that's defined above
        urls = self.django_docs_build_urls()

        # We can do the scraping ourselves and only look for .docs-content
        loader = WebBaseLoader(urls)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splitted_documents = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()

        db = Chroma.from_documents(
            splitted_documents,
            embeddings,
            collection_name="ask_django_docs",
            persist_directory=CHROMA_DB_DIRECTORY,
        )
        db.persist()


if __name__ == "__main__":
    agent = ChromaBuilder()
    agent.build_database()
