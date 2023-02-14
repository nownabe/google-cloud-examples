import MeCab
import numpy as np
from gensim.models.keyedvectors import KeyedVectors


class WordExtractor:
    STOP_POS = (
        "その他",
        "フィラー",
        "副詞",
        "助動詞",
        "助詞",
        "動詞-接尾",
        "動詞-非自立",
        "名詞-動詞非自立的",
        "名詞-特殊-助動詞語幹",
        "名詞-接尾-サ変接続",
        "名詞-接尾-副詞可能",
        "名詞-接尾-人名",
        "名詞-接尾-助動詞語幹",
        "名詞-接尾-形容動詞語幹",
        "名詞-接尾-特殊",
        "名詞-非自立",
        "感動詞",
        "接続詞",
        "接頭詞-動詞接続",
        "接頭詞-形容詞接続",
        "形容詞-接尾",
        "形容詞-非自立",
        "記号-一般",
        "記号-句点",
        "記号-括弧閉",
        "記号-括弧開",
        "記号-空白",
        "記号-読点",
        "連体詞"
    )

    @classmethod
    def from_gcs(cls):
        # TODO
        return cls(ipadic_path="dummy")

    def __init__(self, ipadic_path: str):
        self._mecab = MeCab.Tagger(f"-r mecabrc -d {ipadic_path} -Ochasen")

    def extract(self, sentence: str) -> list[str]:
        result = self._mecab.parse(sentence).splitlines()[:-1]
        words = [line.split("\t") for line in result]
        entities = {word[0] for word in words if self._is_valid(word)}

        return entities

    def _is_valid(self, word) -> bool:
        return not word[3].startswith(self.STOP_POS)


class Vectorizer:
    @classmethod
    def from_gcs(cls, word_extractor: WordExtractor):
        # TODO
        return cls(word_extractor=word_extractor, model=None)

    def __init__(self, word_extractor: WordExtractor, model: KeyedVectors):
        self._extractor = word_extractor
        self._model = model

    def vectorize(self, sentence: str) -> np.ndarray:
        words = self._extractor.extract(sentence)
        vectors = [self._model[w] for w in words if w in self._model]
        return sum(vectors) / len(vectors)
