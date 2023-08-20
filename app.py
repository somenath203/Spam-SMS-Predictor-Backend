from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
import pickle


app = FastAPI()


origins = ["*"]


nltk.download('punkt')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

model = pickle.load(open('mnbmodel.pkl', 'rb'))


class smsModel(BaseModel):
    smsText: str


nltk.download('stopwords')

ps = PorterStemmer()


def preprocess_text(text):
    text = text.lower()  

    text = nltk.word_tokenize(text)

    y = []

    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]

    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]

    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.get('/')
def welcome():
    return {
        'success': True,
        'message': 'server of "sms spam predictor" is up and running successfully '
    }


@app.post('/predict')
async def predict(smsTextValue: smsModel):

    proccessed_text = preprocess_text(smsTextValue.smsText)

    proccessed_text_vectorized = vectorizer.transform([proccessed_text])

    prediction = model.predict(proccessed_text_vectorized)

    pred_result_msg = ''

    if prediction[0] == 1:
        pred_result_msg = 'spam'
    else:
        pred_result_msg = 'not spam'

    return {
        'success': True,
        'message': pred_result_msg,
        'pred_value': float(prediction[0])
    }
