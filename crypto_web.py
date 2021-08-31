import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, date, timedelta
from cryptotradingindicator.params import MODEL_NAME, GCP_PATH, PATH_TO_LOCAL_MODEL, BUCKET_NAME
# from tensorflow.keras.models import load_model
from cryptotradingindicator.data import get_coingecko
# from cryptotradingindicator.data import get_xgecko, get_coingecko, get_train_data, feature_engineer, minmaxscaling
# import numpy as np

###SETTING SITE´S OVERHEAD
st.set_page_config(
    page_title="Cryp2️Moon", # => Quick reference - Streamlit  2️⃣🌚 🌕
    page_icon="💰",
    layout="centered", # wide
    initial_sidebar_state="auto"
    ) # collapsed



##### make a checkbox that decides if use the whole data or the coin_gecko data (timeline)
# st.checkbox("")


### RETRIEVING DATASET
# data_train_scaled, scaler = minmaxscaling(feature_engineer(get_train_data())[['log_close']])
# x_gecko = get_xgecko()


# # @st.cache    #  put the load model into a function and it will not be reloaded every time the user changes something.
# # model = get_model_from_gcp()
# #     # model = joblib.load("model2.joblib")

# ###CALLING THE MODEL AND STRING OUTPUT
# model = load_model("model/")
# prediction = model.predict(x_gecko)
# prediction = np.exp(scaler.inverse_transform(prediction))


### RETRIEVING DATA FROM COINGECKO
#coins = ["Bitcoin","Ethereum"]
coins = ["₿ - Bitcoin", "💰 more coming soon..."]
# data = get_train_data()
@st.cache
def coin():
    data = get_coingecko()
    return data

data = coin()
# data = pd.read_csv("raw_data/BTC-USD.csv")
data.index = pd.to_datetime(data.index, format='%Y-%m-%d')



## SIDEBAR
# but1, but2, but3, but4, but5 = st.sidebar.columns(5)
# but2.markdown("# Crypto ")
# but1.image('bitcoin 32x32.png')
# but4.markdown("#     Indicator")


### SIDEBAR CONFIGURATION
st.sidebar.markdown(
    "<h1 style='text-align: center; color: gray;'>Crypto Indicator</h1>",
    unsafe_allow_html=True
    )

coin = st.sidebar.selectbox(label="Cryptocurrency",
                                options=coins)


d = st.sidebar.date_input("Select the start date for visualization",
                          datetime.now() - timedelta(days=180),
                          min_value=datetime.strptime("2011-12-31 08:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                          max_value=  datetime.now()
                        )

d=  d.strftime('%Y-%m-%d %H:%M:%S')

### RESET TO SEE ALL DATA
# check later this reset
if st.sidebar.button('    Reset graph    '):
    d = data.Date[0]


## visualize indicators
# EMA
ema_curve = st.sidebar.checkbox("Do you want to visualize an EMA curve?", value = False)
t = 1
if ema_curve:
    t = st.sidebar.slider(label= " Select the period for EMA", min_value = 1, max_value= 99, value = 12)
ema = data.close.ewm(span=t).mean()
# df.close.rolling(t).mean()  # normal moving average
ema = ema.dropna()

# Bollinger Bands
bb_curve = st.sidebar.checkbox("Do you want to visualize the bollinger bands?", value = False)
bb = 20
if bb_curve:
    bb = st.sidebar.number_input(label = "Select the rate: ", min_value=1, max_value=100, step=1, value=20)
sma = data.close.rolling(bb).mean() # <-- Get SMA for 20 days
std = data.close.rolling(bb).std() # <-- Get rolling standard deviation for 20 days
bb_up = sma + std * 2 # Calculate top band
bb_down = sma - std * 2 # Calculate bottom band



###DESIGN MAIN PART OF THE SITE
st.markdown('''

''')



## Call api
@st.cache
def load_prediction():
    url = 'https://cryp2moon-idvayook4a-ew.a.run.app/predict'
    # display prediction
    response = requests.get(url).json()
    return response


# st.write(
#     f'''The Bitcoin price is expected to close at around US$ {round(load_prediction()["prediction"],2)} within the next 4 hours!'''
# )

###############
## print message with green or red/orange colors depending on whether the price prediction is higher or lower than the actual price
# 
# st.success('This is a success!')
#####################


st.markdown(
    "<h1 style='text-align: center; color: #FFC300;'>Cryptocurrency Price Indicator</h1>",
    unsafe_allow_html=True)

###BUTTON CREATION
col1, col2, col3 = st.columns(3)
if col2.button('    Prediction in 4 Hours    '):
    st.markdown(
        "This is a serious website who cares about you. Are you sure you wanna come to the moon with us?"
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    if col2.button("YES, OF COURSE"):
        st.write(f'''
            We are glad to hear that. Before continue please send a small donation of 5000 Euros to this paypal: \n
            TIMCARESABOUTYOU@THISISNOTASCAM.COM
            '''
        )
        col1, col2, col3 = st.columns(3)
        if col2.button("I´ve sent my small donation "):
            st.write(f'''
                The Bitcoin price is expected to close at around US$ {round(load_prediction()["prediction"],2)} within the next 4 hours!'''
                     )
    if col4.button("NO, I WANT TO KEEP LIVING MY BORING LIFE"):
        st.write(f'''
            TODO : BORING
            ''')


placeholder = st.empty()

#TO-DO = CREATE CONECTION WITH THE MODEL

# st.write('Bitcoin price')
# fig1, ax = plt.subplots(1,1, figsize=(15,10))
# ax.plot(data["Date"], data["Adj Close"])
# ax.set_ylabel("BTC price (USD)")
# st.write(fig1)
# st.line_chart(data=data['Adj Close'], width=0, height=0, use_container_width=True)



#### CANDEL PLOT

# FILTERING CANDELS
# mask = (data.index > d) & (data.index <= datetime.now())
# filtered_data = data.loc[mask]
# GRAPH

# @st.cache(allow_output_mutation=True)
def load_graph():
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,  #x=filtered_data.index,
            open=data['open'],  #open=filtered_data['open'],
            high=data['high'],  #high=filtered_data['high'],
            low=data['low'],  #low=filtered_data['low'],
            close=data['close']  #close=filtered_data['close']
        )
    ])
    return fig

# load figure
fig = load_graph()

# update figure
fig.update_layout(
    autosize=True,
    width=750, height=350,
    margin=dict(l=40, r=40, b=40, t=40),
    showlegend=False,
    xaxis=dict(rangeslider=dict(visible=False),
            type="date",
            showgrid=False,
            autorange=True),
    yaxis={
        'showgrid': False,
        "separatethousands": True,
        'autorange': True,
        "tickprefix": '$',
        "tickformat": " ,.2f",
        "rangemode": "normal"
    }
    )

# add EMA curve based on user decision
if ema_curve:
    fig.add_trace(
        go.Scatter(x=data.index, y=ema, line=dict(color='orange', width=1), showlegend=True, mode="lines"))

# add bollinger bands based on user decision
if bb_curve:
    fig.add_trace(
        go.Scatter(x=data.index, y=bb_up, line=dict(color='white', width=1), showlegend=True, mode="lines"))
    fig.add_trace(
        go.Scatter(x=data.index, y=bb_down, line=dict(color='white', width=1), showlegend=True, mode="lines"))


st.plotly_chart(fig)


# placeholder.success(
#     "The Bitcoin price is expected to close at around US$ " + str(round(load_prediction()["prediction"],2)) + " within the next 4 hours!")


placeholder.write(
       "<p style='text-align: center'>The Bitcoin price is expected to close at around US$ " + str(round(load_prediction()["prediction"],2)) + "within the next 4 hours!</p>",
    unsafe_allow_html=True)