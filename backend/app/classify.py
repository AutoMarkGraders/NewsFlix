from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def full_classify(text):
    save_directory = "app/saved_model"
    model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0, max_length=512, truncation=True)
    result = classifier(text)
    return result[0]['label'] #only contain a list of dict len(list)=1 hence [0]. then result as dict we only need label


#To be added to upload.py
"""
from classify import full_classify
text="Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads."
result=full_classify(text)
print(result)
"""

