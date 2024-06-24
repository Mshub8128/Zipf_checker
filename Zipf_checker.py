from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

def Zipf(url,bool):
    page = requests.get(url)
    print("\n",page.url,"\n")
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #list(soup.children)

    textPage= (len(soup.find(id='bodyContent').find_all(['p','h2','h3'])))
    text=[]
    #regex used to filter out all the square citation/edit/etc brackets 
    pattern =  r'\s*\[.*?\]\s*'

    #print the title 
    # print("---",soup.find_all('h1')[0].get_text(),"---\n")
    title = soup.find_all('h1')[0].get_text()
    text.append(title)
    for j in range(textPage):
    
        textline = (soup.find(id='bodyContent').find_all(['p','h2','h3','li'])[j])
        #prevents "standard" wikipedia subheadings following content such as "see also" and "references"
        if textline.name == 'h2' and (re.sub(pattern,'',textline.get_text()) == "See also" or re.sub(pattern,'',textline.get_text()) == "References"):
            # print("\n")
            break
        #prevents leading "contents" subheading
        elif textline.name == 'h2' and textline.get_text() != "Contents":
            # print("--",re.sub(pattern,'',textline.get_text()),"--")
            text.append(re.sub(pattern,'',textline.get_text()))
        elif textline.name == 'h3':
            # print("-",re.sub(pattern,'',textline.get_text()),"-")
            text.append(re.sub(pattern,'',textline.get_text()))
        elif textline.name == 'p':
            # print(re.sub(pattern,'',textline.get_text()))
            text.append(re.sub(pattern,'',textline.get_text())) 
        elif textline.name =='li':
            # print(re.sub(pattern,'',textline.get_text()))
            text.append(re.sub(pattern,'',textline.get_text()))

    text = (" ".join(text))
    uniform_text = re.sub(r'[^\w\s]', '', text).lower() #remove punct. and forces lowercase
    uniform_text = re.sub(r'\d+', '', uniform_text)  # Remove digits
    words = uniform_text.split()
    word_count = Counter(words)
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    words_array = [item[0] for item in sorted_words]
    counts_array = [item[1] for item in sorted_words]
    if bool:
        print(words_array,counts_array)

    total = sum(counts_array)
    for i in range(len(counts_array)):
        counts_array[i] = counts_array[i]/total
    if bool:
        print(words_array,counts_array)

    df = pd.DataFrame({f'occurrences in {title}\n{str(len(words_array))} unique words':counts_array}, index=words_array)
    plotTitle = "Zipf"
    plot = df.plot(loglog = True, title = plotTitle)
    plt.show()

#Zipf("https://en.wikipedia.org/wiki/Special:Random")
Zipf("https://en.wikipedia.org/wiki/Albert_Einstein",False)