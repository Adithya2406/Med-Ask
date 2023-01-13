from flask import Flask, render_template, url_for, request
from os import access
import tweepy
import openai
import random
import pandas as pd
import sys
import copy

df = pd.read_csv(
    r'med_list.csv', on_bad_lines='skip')
df = df.applymap(lambda s: s.lower() if type(s) == str else s)
df1 = pd.read_csv(
    r'med_list2.csv', on_bad_lines='skip')
df1 = df1.applymap(lambda s: s.lower() if type(s) == str else s)
df_quotes = pd.read_csv(
    r'quotes.csv', on_bad_lines='skip')
df_in = pd.read_csv(
    r'in_query.csv', on_bad_lines='skip')

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    returnquote = quote()
    return render_template("index.html", quotes=returnquote)


@app.route('/inaccurate.html')
def inaccurate():
    # var2=query()
    return render_template("inaccurate.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    input_query = request.form.to_dict()
    print(input_query)
    query = input_query["query"]

    output = working(query)

    xyz = quote()

    return render_template('index.html', query=output, quotes=xyz)


@app.route('/', methods=['POST', 'GET'])
def quote():

    list_quotes = []
    list_quotes = df_quotes["Quotes"].tolist()
    randno = random.randint(0, len(list_quotes)-1)
    output_quote = list_quotes[randno]

    return output_quote


@app.route('/inaccurate', methods=['POST', 'GET'])
def query():
    listcsv = df_in.values.tolist()
    
    in_query = request.form.to_dict()
    input_query_value = in_query["query"]
    print(input_query_value)
    
    list123 = df.values.tolist()

    listqwerty = []
    list_test = copy.deepcopy(listqwerty)

    list_of_in_query = input_query_value.split()
    # print(input_query_value)
    
    list123= df.values.tolist()
    # df1 = pd.DataFrame(list_of_in_query, columns=['Inaccurate Query'])
    # print(df1)
    
    listqwerty=[]
    print(list_of_in_query)
    list_test = copy.deepcopy(listqwerty)

        # df1 = pd.DataFrame(input_query_value, columns=['Inaccurate Query'])
    for i in list_of_in_query:
        if [i,] not in list123:
            if i not in listcsv:
                listqwerty.append(i)
    print(listqwerty)
    
    for i in listcsv:
        list_test.append(i[1])
    print(list_test)
    
    listqwerty = listqwerty+list_test
    print(listqwerty)
    
    df2 = pd.DataFrame(listqwerty)
    df2.drop_duplicates(subset=None, inplace=True)
    df2.to_csv(
        r'in_query.csv')
    print(df2)

        
    var1 = '''
    Thank you for your response. 
    We have accepted your request.'''
    return render_template('inaccurate.html', var1=var1)


def working(query):

    api_key = "JJ61HMGdIyz6Vmw4irIoHEpW0"
    api_secret = "Vwplf1OYcy2YwoOpPEs0dNpWbEPFuT13oVTT3Ij9MmEe4XUCVo"
    access_key = "1586563005088530433-8ymjkSmAnguZ99C83Q0IplFWRpfFZr"
    access_key_secret = "TQSff2CkRasGCs1IMhCHJHdK0ca5Yy8qeWIlieEzzhPgl"
    openai_key = "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"

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_key, access_key_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    openai.api_key = openai_key

    prom_input = query
    sentence = prom_input
    sentence = sentence.lower()
    tokens = sentence.split()
    list2 = []

    for i in tokens:
        df1 = df[(df['Terms'] == i)]
        # if len(df1)==0:
        #     df1 = df1[(df1['Terms']==i)]
        list2 = list2 + df1["Terms"].tolist()

    print(list2)

    if (len(list2) == 0):
        return ("Not a Medical Query")
    else:
        # print("Medical Query")
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prom_input, max_tokens=400)
        text = response.choices[0].text
        text2 = "It is a medical Query & Solution is : "+text

        final_tweet = 'Question: ' + prom_input + '\n' + 'Answer: ' + text
        if(len(final_tweet)<200):
            api.update_status(final_tweet)

        return text2


app.run(debug=True, port=5002)