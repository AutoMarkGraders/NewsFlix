from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# AutoModelForSequenceClassification: This is a class from the Hugging Face transformers library. 
# It is used to load models that are specifically designed for sequence classification tasks.
# AutoTokenizer: This class is used to load tokenizers, which convert text into numerical representations that models can understand.
# pipeline: This utility provides a simple interface for using various NLP models without needing to write much code.

# Load the model and tokenizer from the saved directory
save_directory = "./saved_model"
model = AutoModelForSequenceClassification.from_pretrained(save_directory)
tokenizer = AutoTokenizer.from_pretrained(save_directory)

# Load a multi-class classification pipeline - if the model runs on CPU, comment out "device"
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0, max_length=512, truncation=True)
# device=0: Uses the GPU, max_length=512: Limits the input text length to 512 tokens.
# truncation=True: Truncates texts longer than max_length
# Checks if the model is already downloaded. If not, it downloads from the HF Model Hub.

#texts to classify
texts = [
    """Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads.""",
    """Moment dog sparks house fire after chewing power bank An indoor monitoring camera shows the moment a dog unintentionally caused a house fire after chewing on a portable lithium-ion battery power bank. In the video released by Tulsa Fire Department in Oklahoma, two dogs and a cat can be seen in the living room before a spark started the fire that spread within minutes. Tulsa Fire Department public information officer Andy Little said the pets escaped through a dog door, and according to local media the family was also evacuated safely. "Had there not been a dog door, they very well could have passed away," he told CBS affiliate KOTV.""",
    """Iran Attack Israel Live: Israel’s military Wednesday said it is engaged in “close-range” operations in southern Lebanon and dismantled Hezbollah’s infrastructure through precision-guided munitions. The Israel Defence Forces (IDF) added that “over 150 terrorist infrastructure sites have been destroyed in air strikes, including Hezbollah’s HQ, weapon storage facilities, and rocket launchers.” Meanwhile, Hezbollah said it was clashing with Israeli troops in the border town of Maroun el-Ras after it had pushed back forces near another border town. The group said it had also fired rockets at military posts inside Israel. This comes at a time when the conflict between Israel and Iran escalated following Tehran firing a barrage of missiles at Tel Aviv on Tuesday.What’s the current situation? Israel will launch a “significant retaliation” against Iran’s missile attack within days, and the response may include targeting oil production facilities in Iran, news agency Reuters reported, citing Axios. The report quoted Israeli officials as saying that the response would be much more substantial than the limited strike Israel conducted in response to the Iranian missile attack in April.Background: Iran fired at least 200 ballistic missiles into Israel on Tuesday, leaving the country to fight on three fronts simultaneously. While many of the rockets were intercepted by Israel’s air defence system, some landed in central and southern Israel, according to the Israeli military. Residents scrambled into bomb shelters as air raid sirens blared and the orange glow of missiles streaked across the night sky. Israel promised retaliation for the attack, which it said caused only a few injuries. However, one Palestinian man was killed by falling shrapnel in the occupied West Bank.""",
    """അർജന്റൈൻ ഇതിഹാസ ഫുട്ബോളർ ലയണൽ മെസി കരിയർ കിരീട നേട്ടത്തിൽ പുതിയ റെക്കോഡ് കുറിക്കാൻ തയാറെടുക്കുന്നു. 2023 മുതൽ മേജർ ലീഗ് സോക്കർ ( എം എൽ എസ് ) ക്ലബ്ബായ ഇന്റർ മയാമി സി എഫിന് ഒപ്പമാണ് ലയണൽ മെസി. എട്ടു പ്രാവശ്യം ലോക ഫുട്ബോളറിനുള്ള ബാലൺ ഡി ഓർ സ്വന്തമാക്കിയ ലയണൽ മെസി, കരിയർ ട്രോഫി നേട്ടത്തിൽ തന്റെ റെക്കോഡ് പുതുക്കാനുള്ള തയാറെടുപ്പിലാണ്.എം എൽ എസ് ലീഗ് റൗണ്ടിന്റെ അടുത്ത മത്സരത്തിൽ ഇന്റർ മയാമി സി എഫ് ജയിച്ചാൽ അവർക്ക് സപ്പോർട്ടേഴ്സ് ഷീൽഡ് ട്രോഫി സ്വന്തമാക്കാം. വ്യാഴാഴ്ച ( ഒക്ടോബർ 3 ) ഇന്ത്യൻ സമയം പുലർച്ചെ 5.15 ന് കൊളംബസ് എഫ് സിക്ക് എതിരേയാണ് ഇന്റർ മയാമിയുടെ അടുത്ത മത്സരം. നിലവിൽ 31 മത്സരങ്ങളിൽ 65 പോയിൻറാണ് ഇന്റർ മയാമിക്ക് ഉള്ളത്. രണ്ടാം സ്ഥാനത്തുള്ള ലോസ് ആഞ്ചലസ് എഫ് സിക്ക് ഇത്രയും മത്സരങ്ങളിൽ നിന്ന് 58 പോയിന്റ് മാത്രമേയുള്ളൂ."""
]

# Classify the texts
results = classifier(texts)

# Output the results
for result in results:
    print(result)
