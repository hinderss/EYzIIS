import dataclasses

import spacy
from lemminflect import getAllInflections, getAllInflectionsOOV
from nltk.stem import PorterStemmer

from .translation import tags_translation_ru, pos_translation_ru


@dataclasses.dataclass(frozen=True)
class Lexeme:
    word: str
    stem: str
    lemma: str | None
    pos: str
    tag: str
    suffix: str
    inflections: dict[str, str]
    possible_suffixes: list[tuple[str, str, str]]

    def __hash__(self):
        return hash((self.stem, self.lemma, self.pos, self.tag, self.suffix))


class WordAnalyzer:
    def __init__(self, explain_lang='en'):
        self.lang = explain_lang
        self.nlp = spacy.load("en_core_web_sm")
        self.stemmer = PorterStemmer()

    @staticmethod
    def word_difference(word1, word2):
        if word2 in word1 or word2[:1] in word1:
            for char in word2:
                word1 = word1.replace(char, '', 1)
            return word1

    def stem(self, word):
        return self.stemmer.stem(word)

    def analyze(self, lexeme, word=None):
        doc = self.nlp(lexeme)
        result = None

        for token in doc:
            result = Lexeme(
                word=word if word else token.text,
                lemma=token.text,
                stem=self.stem(token.text),
                pos=token.pos_,
                tag=token.tag_,
                suffix=token.suffix_,
                inflections=getAllInflections(token.text),
                possible_suffixes=[],
            )

            for tag, inflections in result.inflections.items():
                for inflection in inflections:
                    suffix = self.word_difference(inflection, token.text)
                    if not suffix:
                        continue
                    if len(inflection) == len(token.text):
                        continue
                    if len(suffix) == 0:
                        continue
                    if not token.text == inflection:
                        result.possible_suffixes.append((
                            inflection, suffix, tag,
                        ))
        return result

    def get_lexeme(self, word):
        doc = self.nlp(word)
        lexeme = None
        for token in doc:
            lexeme = token.lemma_
        return self.analyze(lexeme)

    @staticmethod
    def get_inflected_form(word, feature_tag, pos):
        inflections = getAllInflections(word, upos=pos)

        if feature_tag in inflections:
            return inflections[feature_tag][0]
        else:
            inflections_oov = getAllInflectionsOOV(word, upos=pos)
            return inflections_oov[feature_tag][0]

    def explain_tag(self, term: str):
        if self.lang == "ru":
            return tags_translation_ru[term]
        return spacy.explain(term)

    def explain_pos(self, term: str):
        if self.lang == "ru":
            return pos_translation_ru[term]
        return spacy.explain(term)
