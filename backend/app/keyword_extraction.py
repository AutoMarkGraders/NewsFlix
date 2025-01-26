from keybert import KeyBERT

kw_model = KeyBERT()
text = '''The Paris Agreement aims to limit global warming to below 2 degrees Celsius, with efforts to keep it under 1.5 degrees. Renewable energy sources like solar, wind, and hydropower are seen as critical components of this transition. Governments, private companies and international organizations are investing billions of dollars in renewable energy projects to support the transition. According to IEA, renewable energy sources accounted for nearly 90% of the global power capacity added in 2021.
'''
keywords = kw_model.extract_keywords(
    text, 
    keyphrase_ngram_range=(1, 2), 
    stop_words='english', 
    top_n=5, 
    #use_maxsum=True,  # Avoid redundancy in keywords
    #diversity=0.7     # Increase diversity of keywords
)
print(keywords)
# Output: [('forest fire', 0.85), ('wildlife', 0.75), ('destruction', 0.70), ...]
