import pandas as pd
import sys
from bs4 import BeautifulSoup

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io

### The following readies the output dataframe
output = pd.DataFrame()

### The following section loads the urls and words into python as lists
url_file = "C:/Users/44754/Documents/Python Scripts/Custom Search/urls_to_search.csv"
urls = pd.read_csv(url_file, header=0)
urls = urls['URL'].to_list()
word_file = "C:/Users/44754/Documents/Python Scripts/Custom Search/words_to_search.csv"
words = pd.read_csv(word_file, header=0)
words = words['WORD'].to_list()

### The following creates placeholder lists to save our loop data to
url_column_data = []
text_column_data = []
### The following loop opens each url 1 by 1 and saves the text in "div class="layout__region layout__region--content container" to text_column_data
for url in urls:
    try:   
        fd = urlopen(url)
        f = io.BytesIO(fd.read()) 

        soup = BeautifulSoup(f, 'html.parser')
        content_div_html = soup.find("div", {"class":"layout__region layout__region--content container"})
        content_div_text = content_div_html.get_text().lower()
        url_column_data.append(url)
        text_column_data.append(content_div_text)
    except:
        pass

### The following adds the url data to our main output dataframe
output["url"] = url_column_data

### The following loop opens each word 1 by 1
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

### The following prints the output and saves it to csv file
print(output)
output.to_csv("custom search output.csv")




