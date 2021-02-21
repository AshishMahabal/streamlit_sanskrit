import streamlit as st
import json
import os

def getKeysByValue(dictOfElements, valueToFind):
    #st.write(len(dictOfElements))
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

if os.path.exists('chapter1.words.classified'):
    #st.write('exists')
    with open('chapter1.words.classified', 'r') as file:
        cdict = json.loads(file.read())
        #st.write(cdict)
else:
    with open('chapter1.words', 'r') as file:
        cwords = sorted(json.loads(file.read()))
    cdict = {}
    for word in cwords:
        cdict[word] = 'Unclassified'

st.title("Sorting words")
st.sidebar.title("Word types")

dispOpts = ["Unclassified", "धातवः", "नामाः", 'अव्ययानि', 'युजशब्दाः','असाधु','अन्य']
toDisplay = st.sidebar.radio(
	"What would you like to see?",
	dispOpts,
	index=0
)

if toDisplay == "Unclassified":
    
    unc = getKeysByValue(cdict, 'Unclassified')
    st.write(toDisplay, len(unc))
    i=0
    for key in unc:
        i+=1
        topts = dispOpts.copy()
        # cols = st.beta_columns(2)
        # cols[0].write(key)
        # chosen = cols[1].selectbox(str(i),dispOpts)
        topts.insert(0,key)
        st.write(key)
        chosen = st.selectbox(str(i),topts)
        if chosen != key:
            cdict[key] = chosen
            with open('chapter1.words.classified', 'w') as fp:
                json.dump(cdict, fp)
            break
            #cols[j*2+1].write(n)

    #st.write(i,getKeysByValue(cdict, 'धातवः'))
else:
    tdict = getKeysByValue(cdict,toDisplay)
    st.write(toDisplay, len(tdict))
    st.write(tdict)
# elif toDisplay == "धातवः":
#     धातु = getKeysByValue(cdict, 'धातवः')
#     st.write(धातु)

#st.write(cdict)

