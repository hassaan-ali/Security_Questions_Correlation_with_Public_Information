import spacy
import re
from spacy import displacy
import nltk
from collections import defaultdict

#nltk.download('punkt')

nlp = spacy.load('en_core_web_md')
nlp.max_length = 10000000



OUTPUT_FILE = 'SerenaWilliams-cleaned.txt'
QUESTION_FILE = 'questions.txt'

def cleanFile(input_filename, output_filename):
  with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
    text = input_file.read()
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
      output_file.write(sentence + '\n')

def findSimilarity(answer_filename, question):
  question_answer = defaultdict(list)
  with open(answer_filename, 'r') as test_file:
    test_answers = test_file.readlines()
  max_similarity = 0
  most_similar_sentence = None
  target_text = nlp(question)
  for sentence in test_answers:
    doc = nlp(sentence)
    similarity = doc.similarity(target_text)
    if similarity > max_similarity and similarity > 0.7:
      most_similar_sentence = sentence
      max_similarity = similarity
      question_answer[question].append((max_similarity,most_similar_sentence))
  return question_answer


if __name__ == "__main__":
  cleanFile('test.txt', 'test-cleaned.txt')
  question = "What was your favorite meal as a child?"
  print(findSimilarity('test-cleaned.txt', question))

