# -*- coding: utf-8 -*-
"""Transformer-T5-model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14i1VnJ8IY2DvQ0s315FSlsVY7jYTbVUO
"""

!pip install simplet5

"""##Importing Necessary Libraries"""

import pandas as pd
import numpy as np
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

"""##Loading the dataset and calling for 2 columns which will be used for the text summarizaion purpose."""

df = pd.read_csv('news_summary.csv', encoding='latin1', usecols=['headlines', 'text'])

"""##Looking at the 1st few columns of the dataset"""

df.head()

"""##Renaming the columns"""

df = df.rename(columns={"headlines":"target_text", "text":"source_text"})

df = df[['source_text','target_text']]

df.head()

"""##T5 Data Preparation with Summarization Tax Prefix"""

df['source_text'] = "summarize: " + df['source_text']
df

"""##Preparing the dataset for the Training and Test"""

from sklearn.model_selection import train_test_split
train_df, test_df = train_test_split(df, test_size=0.3)
train_df.shape, test_df.shape

"""##Using SimpleT5 for Model Training

##Dowloading the Pre-Trained Model
"""

from simplet5 import SimpleT5

model= SimpleT5()
model.from_pretrained(model_type="t5", model_name="t5-base")

"""##Training the Model"""

model.train(train_df=train_df[:5000],
            eval_df=test_df[:100],
            source_max_token_len=128,
            target_max_token_len=50,
            batch_size=8, max_epochs=5, use_gpu=True)

"""##Output Folder Content"""

! ( cd outputs; ls )

"""##Model Inferencing"""

# let's load the trained model from the local output folder for inferencing:
model.load_model("t5","outputs/simplet5-epoch-1-train-loss-1.1623-val-loss-1.1656", use_gpu=True)

"""##Testing the model"""

text_to_summarize=""""summarize: Twitter’s interim resident grievance officer for India has stepped down, leaving the micro-blogging site without a grievance official as mandated by the new IT rules to address complaints from Indian subscribers, according to a source.

The source said that Dharmendra Chatur, who was recently appointed as interim resident grievance officer for India by Twitter, has quit from the post.

The social media company’s website no longer displays his name, as required under Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules 2021.

Twitter declined to comment on the development.

The development comes at a time when the micro-blogging platform has been engaged in a tussle with the Indian government over the new social media rules. The government has slammed Twitter for deliberate defiance and failure to comply with the country’s new IT rules."""
model.predict(text_to_summarize)

text_to_summarize="""summarize: Travellers vaccinated with Covishield may not be eligible for the European Union’s ‘Green Pass’ that will be available for use from July 1. Many EU member states have started issuing the digital “vaccine passport” that will enable Europeans to move freely for work or tourism. The immunity passport will serve as proof that a person has been vaccinated against the coronavirus disease (Covid-19), or recently tested negative for the virus, or has the natural immunity built up from earlier infection.Covishield, a version of AstraZeneca Covid vaccine manufactured by Pune-based Serum Institute of India (SII), has not been approved by the EMA for the European market. The EU green pass will only recognise the Vaxzervria version of the AstraZeneca vaccine that is manufactured in the UK or other sites around Europe.
"""
model.predict(text_to_summarize)