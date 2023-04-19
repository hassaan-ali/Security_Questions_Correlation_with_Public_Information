import os
import spacy
import re
import nltk
import numpy as np
import json
import itertools

#nltk.download('punkt')

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 10000000

R = 2 #Number of questions to answered
#Fix this into a list to get personality name and input/output filename
PERSONALITY = 'Elon Musk'
INPUT_FILE = ['usps', 'united_airlines', 'bcs', 'spectrum']

def cleanFile(input_filename, output_filename):
  with open(input_filename, 'r', buffering=1000000) as input_file, open(output_filename, 'a') as output_file:
    text = input_file.readlines()
    seen_lines = set()
    for line in text:
      if len(line.strip()) > 1:
        sentences = nltk.sent_tokenize(line)
        for sentence in sentences:
          if sentence not in seen_lines:
            sentence_with_only_alphabetic_characters = re.sub(r'^[^A-Za-z0-9\s\.]+', '', sentence)
            output_file.write(sentence_with_only_alphabetic_characters.strip() + '\n')
            seen_lines.add(sentence)

def findSimilarity(answer_filename, question):
  question_answer = {}
  with open(answer_filename, 'r', buffering=1000000) as test_file:
    test_answers = test_file.readlines()
  max_similarity = 0
  most_similar_sentence = None
  target_text = nlp(process_text(question)).vector
  for sentence in test_answers:
    if len(sentence.split()) < 6 or sentence.startswith(' '):
      continue
    if starts_with_verb(sentence):
      continue
    if not check_intersection(question, sentence):
      continue
    doc = nlp(process_text(sentence)).vector
    similarity = np.dot(target_text, doc) / (np.linalg.norm(target_text) * np.linalg.norm(doc))
    if similarity >  max_similarity:
      max_similarity = similarity
      most_similar_sentence = sentence.rstrip()
    question_answer[question] = [str(round(max_similarity,2)), most_similar_sentence]
  json_object = json.dumps(question_answer, indent= 4)
  print(json_object)
  return [float(question_answer[question][0]), question_answer[question][1]]

def process_text(text):
    doc = nlp(text.lower())
    if doc.text[0] == 'why' or doc.text[0] == 'who' or doc.text[0] == 'what':
      return " "
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)

def check_intersection(question, sentence):
    doc1 = nlp(process_text(question))
    doc2 = nlp(process_text(sentence))

    words1 = set([token.text for token in doc1])
    words2 = set([token.text for token in doc2])

    common_words = words1.intersection(words2)

    if common_words:
      return True
    else:
      return False

def starts_with_verb(sentence):
  doc = nlp(sentence)
  first_token = doc[0]
  if first_token.pos_ == "VERB":
    return True
  elif first_token.text in ("What", "When", "Where", "Which", "Who", "Whom", "Whose", "Why", "Wow", "Do"):
    return True
  else:
    return False


def read_questions(file):
  with open(file, "r") as f:
    questions = f.readlines()
  questionList = []
  for line in questions:
    questionList.append(line)
  
  return questionList

def appendJson(filename, data):
  with open(filename, mode='a') as outfile:
    json.dump(data, outfile, indent=4)



if __name__ == "__main__":
  for input_file in INPUT_FILE:
   # cleanFile((PERSONALITY + '_' + input_file), (PERSONALITY + '_' + input_file + '-' + 'cleaned.txt'))

    questionList = read_questions('questions-' + input_file + '.txt')
    vulnerabilityScore = []
    outputDict = {}

    for question in questionList:
      outputDict[question] = findSimilarity((PERSONALITY + '_' + input_file + '-' + 'cleaned.txt'), question + ' ' + PERSONALITY)
      vulnerabilityScore.append(outputDict[question][0])
    
    if input_file == 'spectrum' or input_file == 'united_airlines':
      R = 1
    
    tempDict = {'Total Questions':len(questionList), 'Questions required for Password Reset': R, 'Combinations (nCr)': sum(1 for ignore in itertools.combinations(vulnerabilityScore, R)),f'Vulnerability Score for {PERSONALITY} on {input_file} website':round((sum(vulnerabilityScore)/len(vulnerabilityScore)),2)}
    print(tempDict)
    outputDict.update(tempDict)
    #Write output to JSON
    appendJson(input_file + '-' + PERSONALITY + '.json',outputDict)