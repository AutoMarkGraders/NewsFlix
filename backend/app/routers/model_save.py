from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#AutoModelForSequenceClassification: This is a class from the Hugging Face transformers library. 
#It is used to load models that are specifically designed for sequence classification tasks.
#AutoTokenizer: This class is used to load tokenizers, which convert text into numerical representations that models can understand.
#pipeline: This utility provides a simple interface for using various NLP models without needing to write much code.

# Model name
model_name = "classla/multilingual-IPTC-news-topic-classifier"

# downloads the pre-trained model from the Hugging Face Hub and returns an instance of it with the architecture automatically determined.
model = AutoModelForSequenceClassification.from_pretrained(model_name)

#This function saves the tokenizer files to the same directory
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save them to a pre defined directory on your disk.
save_directory = "./saved_model"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

#Print the location you saved.
print(f"Model and tokenizer saved to {save_directory}")
