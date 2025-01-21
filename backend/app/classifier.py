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

