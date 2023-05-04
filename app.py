'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date: 2021-Dec-18
'''

import pickle
import streamlit as st
import numpy as np
from PIL import Image

image = Image.open('logo.png')

st.image(image)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.wallpapersafari.com/96/66/qhGnAH.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
st.header('VIT Book Recommender System')
model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url,final_rating["rating"]       



selected_books = st.selectbox( 
    "Choose your Book",
    book_names
)

ids = np.where(final_rating['title'] == selected_books)[0][0]
url = final_rating.iloc[ids]['image_url']
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    #st.image(url)
    #width = st.slider('What is the width in pixels?', 0, 700, 350)
    st.image(url, width=170)
    st.subheader(selected_books)
with col3:
    st.write(' ')


if st.button('Show Recommendation'):
    recommended_books,poster_url,final_rating = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(1,6):
        if(final_rating[i]==0):
            final_rating[i]=10
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
        st.text("Rating (out of 10): "+str(final_rating[1]))
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])
        st.text("Rating (out of 10): "+str(final_rating[2]))
    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
        st.text("Rating (out of 10): "+str(final_rating[3]))
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
        st.text("Rating (out of 10): "+str(final_rating[4]))
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])
        st.text("Rating (out of 10): "+str(final_rating[5]))