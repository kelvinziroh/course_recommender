import transformers
from transformers import AutoTokenizer, AutoModel
import pandas as pd
import torch
import torch.nn as nn
import streamlit as st
from data_loader import persist_data

# Load the dataset
df = st.session_state.df

# Define the sentiment classes
sentiment_classes = ['negative', 'neutral', 'positive']

# Load the tokenzier
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

# Define the Sentiment Classifier class
class BertSentimentClassifier(nn.Module):

    def __init__(self, n_classes):
        super(BertSentimentClassifier, self).__init__()
        self.pretrained_bert = AutoModel.from_pretrained('bert-base-cased')
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.pretrained_bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.pretrained_bert(
            input_ids = input_ids,
            attention_mask = attention_mask,
            return_dict = False
        )
        output = self.drop(pooled_output)
        return self.out(output)

# Load the finetuned model weights
model_path = '/Users/ziro/Developer/projects/ongoing_projects/data_science/course_recommender/assets/model/best_bert_model_state.bin'
model = BertSentimentClassifier(len(sentiment_classes))
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))

# Set the model into evaluation mode
model.eval()

# Define the maximum string length
MAX_LEN = 200

# Define a function to encode text and get sentiment predictions
def predict_sentiment(review):
    # Encode the text
    encoded_course_review = tokenizer.encode_plus(
        review,
        max_length = MAX_LEN,
        add_special_tokens = True,
        truncation = True,
        padding = 'max_length',
        return_attention_mask = True,
        return_tensors = 'pt',
    )

    # Get the sentiment prediction from the model
    input_ids = encoded_course_review['input_ids'] 
    attention_mask = encoded_course_review['attention_mask']
    output = model(input_ids, attention_mask)

    _, prediction = torch.max(output, dim=1)
    return sentiment_classes[prediction]

st.title("Review Sentiment Analysis")

course_name = st.text_input("Course Name")
course_source = st.text_input("Course Source")
course_rating = st.slider("Course Rating", 1, 5)
course_review = st.text_area("Course Review")

if st.button("Classify Sentiment"):
    if course_name and course_review:  # Validate required fields
        with st.spinner("Analyzing sentiment..."):
            try:
                predicted_sentiment = predict_sentiment(course_review)
                st.write("Predicted Sentiment:", predicted_sentiment)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please fill in required fields (Course Name and Review)")

if st.button("Save"):
    # Add the new records to the dataframe
    if course_name and course_review:  
        predicted_sentiment = predict_sentiment(course_review)
        review = (
            course_name,
            course_source,
            course_rating,
            course_review,
            predicted_sentiment
        )
        # df = df.append(new_row, ignore_index=True)
        # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        persist_data(review)
        st.success("Review analysis successfully added!")
    else:
        st.warning("Please fill in required fields (Course Name and Review)")
