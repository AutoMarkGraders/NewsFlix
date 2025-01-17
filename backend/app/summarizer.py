from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def full_summarize(input_text):
    model_name = "philschmid/bart-large-cnn-samsum"
    save_directory = "/saved_model_summary"
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=0)
    summary = summarizer(input_text)    #, min_length=50, max_length=75
    return summary[0]['summary_text']


#To be added to upload.py
"""
from summarizer import full_summarize
input_text='''As the world grapples with the escalating effects of climate change, a significant shift towards renewable energy is taking place across various countries. In the past few years, an increasing number of nations have set ambitious targets to transition away from fossil fuels and invest in clean energy alternatives. This shift is being driven by the urgency to mitigate carbon emissions, improve air quality, and meet the climate goals outlined in international agreements such as the Paris Agreement.
The Paris Agreement, signed in 2015, aims to limit global warming to below 2 degrees Celsius, with efforts to keep it under 1.5 degrees. Achieving this goal requires a drastic reduction in greenhouse gas emissions, and renewable energy sources like solar, wind, and hydropower are seen as critical components of this transition. Governments, private companies, and international organizations are investing billions of dollars in renewable energy projects to support this transition.
For instance, the European Union has committed to making the bloc carbon-neutral by 2050. This includes a massive expansion of wind farms across the North Sea, increased investment in solar power, and the development of hydrogen as a clean energy source. Germany, a leading country in the EU’s energy transition, has been focusing heavily on wind and solar power. Recently, the country shut down its last nuclear power plants and increased subsidies for renewable energy projects to meet its climate targets.
Meanwhile, in the United States, the Inflation Reduction Act, passed in 2022, has significantly boosted clean energy investment. The Act includes provisions for tax credits and subsidies for solar panel installations, electric vehicles, and battery storage systems. These incentives have led to a surge in renewable energy projects across states like Texas, California, and New York. Texas, traditionally known for its oil production, has emerged as a leader in wind energy production, while California continues to lead in solar power generation.
China, the world’s largest emitter of carbon dioxide, has also taken steps to reduce its dependence on coal. The country is the global leader in solar panel manufacturing and has been installing solar and wind power at an unprecedented rate. China's goal is to reach peak carbon emissions by 2030 and achieve carbon neutrality by 2060. Despite these efforts, the country still faces challenges due to its heavy reliance on coal for energy production, but the recent investments signal a willingness to shift towards a cleaner energy future.
In addition to government initiatives, the private sector is playing a crucial role in the renewable energy revolution. Tech giants like Google, Amazon, and Microsoft have committed to powering their data centers with 100% renewable energy. These companies have signed power purchase agreements (PPAs) with wind and solar farms to ensure a steady supply of green energy. Microsoft, for instance, has pledged to become carbon negative by 2030, meaning it will remove more carbon from the atmosphere than it emits.
The shift towards renewable energy is not without challenges. The intermittent nature of solar and wind energy means that there is a need for advancements in energy storage technologies, such as batteries, to ensure a consistent power supply. Additionally, the transition requires significant upgrades to the existing power grid infrastructure to accommodate the decentralized nature of renewable energy sources.
Moreover, the extraction of materials required for renewable energy technologies, like lithium for batteries and rare earth elements for wind turbines, raises concerns about environmental impacts and supply chain stability. Critics argue that while renewable energy is a crucial part of the solution to climate change, it is not entirely free of environmental trade-offs.
Despite these challenges, the momentum behind renewable energy continues to grow. According to the International Energy Agency (IEA), renewable energy sources accounted for nearly 90% of the global power capacity added in 2021. The IEA projects that solar power could become the largest source of electricity generation by 2050, surpassing coal.
Developing countries are also seeing the benefits of renewable energy. In regions like sub-Saharan Africa, where many communities lack access to reliable electricity, solar power is being used to provide off-grid solutions. Projects like solar mini-grids are helping to bring electricity to remote areas, improving access to education, healthcare, and economic opportunities.
The shift towards renewable energy is not just about reducing carbon emissions; it is also about creating economic opportunities. The renewable energy sector has become a major source of job creation, with millions of jobs being generated in solar installation, wind turbine manufacturing, and battery production. As fossil fuel industries decline, the clean energy sector offers a pathway for economic growth and sustainable development.
As the world moves towards a cleaner energy future, collaboration between countries, industries, and communities will be key. While challenges remain, the transition to renewable energy represents a crucial step in addressing the global climate crisis and ensuring a sustainable future for generations to come.'''
result=full_summarize(input_text)
print(result)
"""