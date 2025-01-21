from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def full_summarize(input_text):
    # model_name = "philschmid/bart-large-cnn-samsum"
    save_directory = "app/saved_model_summary"
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=0)
    summary = summarizer(input_text)    #, min_length=50, max_length=75
    return summary[0]['summary_text']

