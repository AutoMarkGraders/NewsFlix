from transformers import AutoModelForSeq2SeqLM, AutoModelForSequenceClassification, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def full_summarize(input_text):
    # model_name = "philschmid/bart-large-cnn-samsum"
    save_directory = "saved_summarizer"
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=0)
    summary = summarizer(input_text)    #, min_length=50, max_length=75
    return summary[0]['summary_text']

def full_classify(text):
    save_directory = "saved_classifier"
    model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0, max_length=512, truncation=True)
    result = classifier(text)
    return result[0]['label'] #only contain a list of dict len(list)=1 hence [0]. then result as dict we only need label

