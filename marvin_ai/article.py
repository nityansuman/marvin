from nltk.corpus import wordnet as wn
from textblob import TextBlob
import re
import nltk

class Article:
    def __init__(self, title):
        self.title = title
        fp = open(title, mode="r")
        self.summary = fp.read()
        fp.close()


    def generate_trivia_sentences(self):
        sentences = nltk.sent_tokenize(self.summary)

        # Remove the first sentence - it's never a good one
        # del sentences[0] just kidding

        trivia_sentences = []
        for sentence in sentences:
            trivia = self.evaluate_sentence(sentence)
            if trivia:
                trivia_sentences.append(trivia)

        return trivia_sentences


    def get_similar_words(self, word):
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos='n')

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]

        # Get the hypernym for this synset (again, take the first)
        hypernym = synset.hypernyms()[0]

        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()

        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
            
            if similar_word != word:
                similar_words.append(similar_word)

            if len(similar_words) == 8:
                break

        return similar_words


    def evaluate_sentence(self, sentence):
        # if sentence starts with an adverb or is less than 4 words long
        # probably not the best fit
        tags = nltk.pos_tag(sentence)
        if tags[0][1] == 'RB' or len(nltk.word_tokenize(sentence)) < 4:
            return None

        tag_map = {word.lower(): tag for word, tag in tags}

        # extract noun phrases from the sentence
        noun_phrases = list()
        grammar1 = r""" CHUNK: {<NN.*|JJ>*<NN.*>} """
        grammar2 = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                {<NN>+<IN|DT>*<NNP>+}
                {<NNP>+<NNS>*}
            """
        chunker = nltk.RegexpParser(grammar2)
        tokens = nltk.word_tokenize(sentence)
        pos_tokens = nltk.tag.pos_tag(tokens)
        tree = chunker.parse(pos_tokens)

        # select phrase
        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                temp = ""
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                temp = temp.strip() # strip extra whitespace
                noun_phrases.append(temp)
        
        # replace nouns
        replace_nouns = []
        for word, tag in tags:
            for phrase in noun_phrases:
                if phrase[0] == '\'':
                    # If it starts with an apostrophe, ignore it
                    # (this is a weird error that should probably
                    # be handled elsewhere)
                    break
                if word in phrase:
                    # Blank out the last two words in this phrase
                    [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                    break
            # If we couldn't find the word in any phrases,
            # replace it on its own
            if len(replace_nouns) == 0:
                replace_nouns.append(word)
            break
        
        if len(replace_nouns) == 0:
            # Return none if we found no words to replace
            return None
        val = 99
        for i in replace_nouns:
            if len(i) < val:
                val = len(i)  

        trivia = {
            "Answer": " ".join(replace_nouns),
            "Anser_key": val
        }

        if len(replace_nouns) == 1:
            # If we're only replacing one word, use WordNet to find similar words
            trivia['similar_words'] = self.get_similar_words(replace_nouns[0])
        else:
            # If we're replacing a phrase, don't bother - it's too unlikely to make sense
            trivia['similar_words'] = []

        # Blank out our replace words (only the first occurrence of the word in the sentence)
        replace_phrase = ' '.join(replace_nouns)
        blanks_phrase = ('__________ ' * len(replace_nouns)).strip()

        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, str(sentence), count=1)

        trivia['Question'] = sentence
        return trivia
