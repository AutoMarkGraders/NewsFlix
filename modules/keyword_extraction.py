from keybert import KeyBERT
import time

start_time = time.time()
kw_model = KeyBERT()
load_time = time.time()
print(f"Time taken to load model: {load_time - start_time}")

text = '''Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads
'''
keywords = kw_model.extract_keywords(
    text, 
    keyphrase_ngram_range=(1, 2), 
    stop_words='english', 
    top_n=1, 
    #use_maxsum=True,  # Avoid redundancy in keywords
    #diversity=0.7     # Increase diversity of keywords
)
print(f"Time taken to process: {time.time() - load_time}")

print(keywords[0][0])
# eg: output: [('forest fire', 0.85), ('wildlife', 0.75), ('destruction', 0.70), ...]
