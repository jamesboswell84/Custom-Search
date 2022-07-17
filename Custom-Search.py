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

#url_file = "urls_to_search.csv"
url_file = st.file_uploader("Choose a URL file")
st.write("""
Example URL file here.
""")

#word_file = "words_to_search.csv"
word_file = st.file_uploader("Choose a Word file")
st.write("""
Example Word file here.
""")


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
    content_area = st.text_input('Specify regex to find div classes within your content areas:')
    
    ### The following loop opens each url 1 by 1 and saves the text in "div class="layout__region layout__region--content container" to text_column_data
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
    counter = 0
    tot = len(words)
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
        counter = counter + 1
        progress_variable_1_to_100 = counter/tot
        st.progress(progress_variable_1_to_100)
        output[word] = search_column_data

#print(output)
    st.write("""
    # Data preview:
    """)
    st.table(data.iloc[0:10])        
    ### The following prints the output and saves it to csv file
    #if st.button('Export CSV'):

    #output.to_csv("custom search output.csv")
    st.download_button('Download file', output)



