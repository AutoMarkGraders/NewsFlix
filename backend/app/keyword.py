from keybert import KeyBERT

kw_model = KeyBERT()
text = "A massive forest fire has devastated the region, causing widespread destruction and endangering wildlife."
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
print(keywords)  # Output: [('forest fire', 0.85), ('wildlife', 0.75), ('destruction', 0.70), ...]
