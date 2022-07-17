import pandas as pd
import sys
import re
from bs4 import BeautifulSoup
import streamlit as st

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io

### The following readies the output dataframe
output = pd.DataFrame()

### The following section loads the urls and words into python as lists

st.write("""
# Custom Search
Screaming Frog's custom search function, but you can add all of your searches via an input file instead of adding them manually and individually.
""")

st.write("""
# 1.
""")
#url_file = "urls_to_search.csv"
url_file = st.file_uploader("Choose your URL CSV file:")
see_example_url_file = st.checkbox(
    "See example URL file", False, help="Use example file to see what format your input file has to be"
)
if see_example_url_file:
    uploaded_url_file = "urls_to_search.csv"
    uploaded_url_file = pd.read_csv(uploaded_url_file, header=0)
    st.dataframe(uploaded_url_file.head())

st.write("""
# 2.
""")
#word_file = "words_to_search.csv"
word_file = st.file_uploader("Choose your Words CSV file:")
see_example_words_file = st.checkbox(
    "See example Words file", False, help="Use example file to see what format your input file has to be"
)
if see_example_words_file:
    uploaded_words_file = "words_to_search.csv"
    uploaded_words_file = pd.read_csv(uploaded_words_file, header=0)
    st.dataframe(uploaded_words_file.head())

st.write("""
# 3.
""")
content_area = st.text_input('Specify regex to find div classes within your content areas:')

if st.button('Start Search'):
    urls = pd.read_csv(url_file, header=0)
    urls = urls['URL'].to_list()
    words = pd.read_csv(word_file, header=0)
    words = words['WORD'].to_list()
    
    ### The following creates placeholder lists to save our loop data to
    url_column_data = []
    text_column_data = []

    ### This is the variable for div class to search
    #content_area = input("Enter regex rule for your content area:")
    #content_area = st.text_input('Specify regex to find div classes within your content areas:')
    
    ### The following loop opens each url 1 by 1 and saves the text in "div class="layout__region layout__region--content container" to text_column_data
    with st.spinner("Loading URLs..."):
        for url in urls:
            try:   
                fd = urlopen(url)
                f = io.BytesIO(fd.read()) 

                soup = BeautifulSoup(f, 'html.parser')
                content_div_html = soup.find("div", {"class": re.compile(f"{content_area}")})
                content_div_text = content_div_html.get_text().lower()
                url_column_data.append(url)
                text_column_data.append(content_div_text)
            except:
                pass

    ### The following adds the url data to our main output dataframe
        output["url"] = url_column_data

    ### The following loop opens each word 1 by 1
    with st.spinner("Searching for words..."):
        for word in words:
            search_column_data = []
            try:
                ### The following loop within a loop opens the text_column_data list 1 by 1 and counts each word 1 by 1
                for text in text_column_data:      
                    word_count_in_text = text.count(word)
                    search_column_data.append(word_count_in_text)
            except:
                pass
            ### The following adds the count data for each word to our output dataframe
            output[word] = search_column_data

#print(output)
        st.write("""
        # Data preview:
        """)
        st.table(output.iloc[0:10])        
        ### The following prints the output and saves it to csv file
        #if st.button('Export CSV'):
        def convert_df(output):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return output.to_csv().encode('utf-8')
        #output.to_csv("custom search output.csv")
        st.download_button('Download file', output, file_name="custom search output.csv",mime='text/csv')



