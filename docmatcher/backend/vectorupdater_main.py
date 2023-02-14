import pickle
from os import environ

from vectorupdater.app import create_app
from vectorupdater.vectorizer import WordExtractor, Vectorizer

word_extractor = WordExtractor(ipadic_path="tmp/mecab-ipadic-neologd")

with open("tmp/jawiki.all_vectors.300d.pkl", mode="rb") as f:
    model = pickle.load(f)

vectorizer = Vectorizer(word_extractor=word_extractor, model=model)

app = create_app(vectorizer=vectorizer)

if __name__ == "__main__":
    import uvicorn

    port = int(environ.get("PORT", "3001"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
