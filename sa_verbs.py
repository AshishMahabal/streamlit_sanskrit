import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti
import random
import numpy as np
import os
import json

st.title('Let us do some Sanskrit (Verbs)')

vachanas = ['एक','द्वि','बहु']
# these elements need to be distinct. Use this later for vikaran and purush pratya.
तिङ् = {} # तिप्‍तस्‍झिसिप्‍थस्‍थमिब्‍वस्‍मस्‍ताताञ्झथासाथाम्‍ध्‍वमिड्वहिमहिङ्
तिङ्['परस्मै'] = "तिप्#तस्#झि#सिप्#थस्#थ#मिप्#वस्#मस्".split('#')
तिङ्['आत्मने'] = "त#आताम्#झ#थास्#आथाम्#ध्वम्#इट्#वहि#महिङ्".split('#')

purush = ['प्रथम','मध्यम','उत्तम']

with open("verbs.json", "rb") as f:
    verbs = json.loads(f.read())

def showdev(roman):
    return st.markdown(transliterate(roman))

def verblisttable(verb='अस',pada='परस्मै',lakAra='लट्'):
    पुरुष = ['प्रथम','मध्यम','उत्तम']
    tdata = np.reshape(verbs[verb][pada][lakaara].split('#'), (3,3))
    df = pd.DataFrame(tdata,columns=['एकवचन','द्विवचन','बहुवचन'])
    df['पुरुष'] = पुरुष
    df = df.set_index('पुरुष')
    return df

emojis = [':sunglasses:',':smile:',':smiley:',':heart:',':grin:',':triumph:',':star:',':musical_note:']

copts = []
opts = st.beta_columns(3)
copts.append(opts[0].checkbox('Notes',value='True'))
copts.append(opts[1].checkbox('Quiz'))
copts.append(opts[2].checkbox('Show'))
#copts.append(opts[3].selectbox('Select noun1',devnouns))

vopts = []
sopts = st.beta_columns(3)
vopts.append(sopts[0].selectbox(
    'Select verb',
    list(verbs.keys()),)
)
verb = vopts[0]
vopts.append(sopts[1].selectbox('Select pada',verbs[verb]['pada']))
pada = vopts[1]
vopts.append(sopts[2].selectbox('Select pada',list(verbs[verb][pada].keys())))
lakaara = vopts[2]
गण = verbs[verb]['गण']

#st.write('Curent selections: ',verb,pada,lakaara)

if copts[0]:
    st.subheader("Notes:")
    st.write("For the set of verbs in the drop down menu, you can see their forms\
    and/or quiz yourself about them. I will add more verbs, padas, and lakaar.\
    And features. Currently for the forms you get right, you will see emojis displayed\
    near those forms.")
    st.write("Conjuncts do not show up well on Safari. In devnagari mode, use H for visarga sign.")

if copts[1]: # quiz
    st.subheader('Verb quiz')
    st.write("Please complete the following for ",verb,'धातु (गण ',गण,') ',pada,'पद ',lakaara,'लकार')
    
    #st.write(verbs[verb])
    #st.write(verb)
    purushas = []
    cpurushas = verbs[verb][pada][lakaara].split('#')
    cpurushas = [item.strip() for item in cpurushas]

    corrects = 0
    for i in range(len(purush)):
        cols = st.beta_columns(7)
        purushas.append(cols[0].write(purush[i]))
        for j in range(3):
            purushas.append(cols[j*2+1].text_input(तिङ्[pada][i*3+j],""))
            lab = str(i*3+j+1)
            if cpurushas[i*3+j] != purushas[i*7+j*2+1].strip():
                purushas.append(cols[j*2+2].write(''))
                #vibhaktis.append(cols[j*2+2].checkbox('',value=False,key=lab))
            else:
                purushas.append(cols[j*2+2].write(random.choice(emojis)))
                #vibhaktis.append(cols[j*2+2].checkbox('',value=True,key=lab))
                corrects += 1
                

    st.write(corrects,"/9 correct")
    if corrects == 9:
        st.write(':sunglasses:')
    
if copts[2]: # show
    # We should get noun and linga here that way we can type
    # and not rely on the drop down list
    st.subheader('Verbtable')
    st.write(verb,' धातु (गण ',गण,') ',pada,'पद ',lakaara,'लकार selected')
    df = verblisttable(verb,pada,lakaara)
    st.write(df.to_markdown())


# #os.system("gtts-cli -l hi 'नमस्ते महोदय' | ffmpeg -i pipe:0 -f wav pipe:1 | ~/Downloads/sox-14.4.2/play -t wav -")
# audiostr = "gtts-cli -l hi --slow '%s' | ffmpeg -i pipe:0 -f wav pipe:1 | ~/Downloads/sox-14.4.2/play -t wav -" % nouns[devnoun]
# os.system(audiostr)
# #st.write(audiostr)
