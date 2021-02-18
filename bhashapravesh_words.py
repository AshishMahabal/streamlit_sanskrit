import streamlit as st
import json
import os

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

if os.path.exists('chapter1.words.classified'):
    with open('chapter1.words.classified', 'r') as file:
        cdict = sorted(json.loads(file.read()))
else:
    with open('chapter1.words', 'r') as file:
        cwords = sorted(json.loads(file.read()))
    cdict = {}
    for word in cwords:
        cdict[word] = ' '

st.title("Sorting words")
st.sidebar.title("Word types")

dispOpts = ["Unclassified", "धातवः", "नामाः", 'अव्ययानि', 'युजशब्दाः','असाधु','अन्य']
toDisplay = st.sidebar.radio(
	"What would you like to see?",
	dispOpts,
	index=0
)

if toDisplay == "Unclassified":
    unc = getKeysByValue(cdict, ' ')
    uncup = []
    rows = len(unc)//4
    for i in range(rows):
        cols = st.beta_columns(8)
        for j in range(4):
            n = i*4+j
            cols[j*2].write(unc[n])
            uncup.append(cols[j*2+1].selectbox(str(n),dispOpts))
            cdict[unc[n]] = uncup[len(uncup)-1]
            #cols[j*2+1].write(n)

    st.write(i,getKeysByValue(cdict, 'धातवः'))	
elif toDisplay == "धातवः":
    धातु = getKeysByValue(cdict, 'धातवः')
    st.write(धातु)

#st.write(cdict)

