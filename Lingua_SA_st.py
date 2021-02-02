import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti
import random
import numpy as np
import os

st.title('Let us do some Sanskrit')



#st.sidebar.header('Noun tables')

#labels = ["प्रथमा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","संबोधन"]
vachanas = ['एक','द्वि','बहु']
sup = ["सु","औ","जस्","सु ","औ ","जस् ","अम्","औट्","शस्","टा",'भ्याम्','भिस्','ङे','भ्याम् ','भ्यस्',
    'ङसि','भ्याम्  ','भ्यस् ','ङस्','ओस्','आम् ','ङि','ओस् ','सुप्']

nouns = {}
nouns['राम (पु)'] = 'रामः#रामौ#रामाः#हे राम#हे रामौ#हे रामाः#रामम्#रामौ#रामान्#रामेण#रामाभ्याम्#रामैः#\
रामाय#रामाभ्याम्#रामेभ्यः#रामात्#रामाभ्याम्#रामेभ्यः#रामस्य#रामयोः#रामाणाम्#रामे#रामयोः#रामेषु'
nouns['रमा (स्त्री)'] = 'रमा#रमे#रमाः#हे रमे#हे रमे#हे रमाः#रमाम्#रमे#रमाः#रमया#रमाभ्याम्#रमाभिः#रमायै#रमाभ्याम्#रमाभ्यः#\
रमायाः#रमाभ्याम्#रमाभ्यः#रमायाः#रमयोः#रमाणाम्#रमायाम्#रमयोः#रमासु'
nouns['फल (न)'] = 'फलम्#फले#फलानि#हे फल#हे फले#हे फलानि#फलम्#फले#फलानि#फलेन#फलाभ्याम्#फलैः#फलाय#फलाभ्याम्#फलेभ्यः#\
फलात्#फलाभ्याम्#फलेभ्यः#फलस्य#फलयोः#फलानाम्#फले#फलयोः#फलेषु'
nouns['हरि (पु)'] = 'हरिः#हरी#हरयः#हे हरे#हे हरी#हे हरयः#हरिम्#हरी#हरीन्#हरिणा#हरिभ्याम्#हरिभिः#हरये#हरिभ्याम्#हरिभ्यः#\
हरेः#हरिभ्याम्#हरिभ्यः#हरेः#हर्योः#हरीणाम्#हरौ#हर्योः#हरिषु'
nouns['बालक (पु)'] = 'बालकः#बालकौ#बालकाः#हे बालक#हे बालकौ#हे बालकाः#बालकम्#बालकौ#बालकान्#बालकेन#बालकाभ्याम्#बालकैः#\
बालकाय#बालकाभ्याम्#बालकेभ्यः#बालकात्#बालकाभ्याम्#बालकेभ्यः#बालकस्य#बालकयोः#बालकानाम्#बालके#बालकयोः#बालकेषु'
nouns['गुरु (पु)'] = 'गुरुः#गुरू#गुरवः#हे गुरो#हे गुरू#हे गुरवः#गुरुम्#गुरू#गुरून्#गुरुणा#गुरुभ्याम्#गुरुभिः#गुरवे#गुरुभ्याम्#गुरुभ्यः#\
गुरोः#गुरुभ्याम्#गुरुभ्यः#गुरोः#गुर्वोः#गुरूणाम्#गुरौ#गुर्वोः#गुरुषु'
nouns['नदी (स्त्री)'] = 'नदी#नद्यौ#नद्यः#हे नदि#हे नद्यौ#हे नद्यः#नदीम्#नद्यौ#नदीः#नद्या#नदीभ्याम्#नदीभिः#नद्यै#नदीभ्याम्#नदीभ्यः#\
नद्याः#नदीभ्याम्#नदीभ्यः#नद्याः#नद्योः#नदीनाम्#नद्याम्#नद्योः#नदीषु'
nouns['युष्मद् (त्रि)'] = 'त्वम्#युवाम्#यूयम्####त्वाम्#युवाम्#युष्मान्#त्वया#युवाभ्याम्#युष्माभिः#तुभ्यम्#युवाभ्याम्#युष्मभ्यम्#\
त्वत्#युवाभ्याम्#युष्मत्#तव#युवयोः#युष्माकम्#त्वयि#युवयोः#युष्मासु'
nouns['अस्मद् (त्रि)'] = 'अहम्#आवाम्#वयम्####माम्/मा#आवाम्/नौ#अस्मान्/नः#मया#आवाभ्याम्#अस्माभिः#मह्यम्/मे#आवाभ्याम्/नौ#अस्माभ्यम्/नः#\
मत्#आव्याभ्याम्#अस्मत्#मम/मे#आवयोः/नौ#अस्माकम्/नः#मयि#आवयोः#अस्मासु'
nouns['तद् (पु)'] = 'स:#तौ#ते####तम्#तौ#तान्#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'
nouns['तद् (स्त्री)'] = 'सा#ते#ताः####ताम्#ते#ताः#तया#ताभ्याम्#ताभिः#तस्यै#ताभ्याम्#ताभ्यः#तस्याः#ताभ्याम्#ताभ्यः#तस्याः#तयोः#तासाम्#तस्याम्#तयोः#तासु'
nouns['तद् (न)'] = 'तत्#ते#तानि####तत्#ते#तानि#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'

sarvanouns = {}
sarvanouns['युष्मद् (त्रि)'] = 'त्वम्#युवाम्#यूयम्####त्वाम्#युवाम्#युष्मान्#त्वया#युवाभ्याम्#युष्माभिः#तुभ्यम्#युवाभ्याम्#युष्मभ्यम्#\
त्वत्#युवाभ्याम्#युष्मत्#तव#युवयोः#युष्माकम्#त्वयि#युवयोः#युष्मासु'
sarvanouns['अस्मद् (त्रि)'] = 'अहम्#आवाम्#वयम्####माम्/मा#आवाम्/नौ#अस्मान्/नः#मया#आवाभ्याम्#अस्माभिः#मह्यम्/मे#आवाभ्याम्/नौ#अस्माभ्यम्/नः#\
मत्#आव्याभ्याम्#अस्मत्#मम/मे#आवयोः/नौ#अस्माकम्/नः#मयि#आवयोः#अस्मासु'
sarvanouns['तद् (पु)'] = 'स:#तौ#ते####तम्#तौ#तान्#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'
sarvanouns['तद् (स्त्री)'] = 'सा#ते#ताः####ताम्#ते#ताः#तया#ताभ्याम्#ताभिः#तस्यै#ताभ्याम्#ताभ्यः#तस्याः#ताभ्याम्#ताभ्यः#तस्याः#तयोः#तासाम्#तस्याम्#तयोः#तासु'
sarvanouns['तद् (न)'] = 'तत्#ते#तानि####तत्#ते#तानि#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'

labels = ["प्रथमा","संबोधन","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी"]

# linga = { # Combine this with nounlinga
#         'rAma':'puM',
#         'bAlaka':'puM',
#         'phala':'napuMsaka',
#         'ramA':'strI',
#         'hari':'puM',
#         'nadI':'strI',
#         'guru':'puM',
#         'yuSmad':'tri',
#         'asfmad':'tri',
# #        'dhenu':'strI',
# #        'madhu':'napuMsaka',
# #        'dAtR': 'puM',
#         }

nounlinga = {
        'राम (पु)': 'rAma',
        'बालक (पु)': 'bAlaka',
        'फल (न)': 'phala',
        'रमा (स्त्री)':'ramA',
        'हरि (पु)':'hari',
        'नदी (स्त्री)':'nadI',
        'गुरु (पु)':'guru',
        'युष्मद् (त्रि)':'yuSmad',
        'अस्मद् (त्रि)':'wsfmad',
        'तद् (पु)':'tad',
        'तद् (स्त्री)':'tad',
        'तद् (न)':'tad',
#        'dhenu':'strI',
#        'madhu':'napuMsaka',
#        'dAtR': 'puM',
        }

sarvanounlinga = {
        '':'',
        'युष्मद् (त्रि)':'yuSmad',
        'अस्मद् (त्रि)':'wsfmad',
        'तद् (पु)':'tad',
        'तद् (स्त्री)':'tad',
        'तद् (न)':'tad',
        }

devnouns = list(nounlinga.keys())
sarvadevnouns = list(sarvanounlinga.keys())
#nouns = ['rAma','phala','ramA','hari','guru','dhenu','madhu']

def showdev(roman):
    return st.markdown(transliterate(roman))

def nountable(noun='rAma',linga='puM'):
    vibhaktis = ['prathamA','dvitIyA','tRtIyA','chaturthI','paMchamI','ShaShThI','saptamI','sMbodhana']
    df = pd.DataFrame([],columns=['',transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
    
    for vib in [0,7,1,2,3,4,5,6]:
        row = []
        row.append(transliterate(vibhaktis[vib]))
        for vachana in range(3):
            v = vibhakti(noun, linga, str(vib+1), str(vachana+1))
            s = sandhi(v)
            t = transliterate(s)
            row.append(t)
        df.loc[len(df)] = row
    return df

def nounlisttable(devnoun='राम (पु)'):
    vibhaktis = ['prathamA','sMbodhana', 'dvitIyA','tRtIyA','chaturthI','paMchamI','ShaShThI','saptamI']
    tdata = np.reshape(nouns[devnoun].split('#'), (8,3))
    #st.write(tdata)
    df = pd.DataFrame(tdata,columns=[transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
    df[transliterate("vibhakti")] = [transliterate(i) for i in vibhaktis]
    df = df.set_index(transliterate("vibhakti"))
    #st.write(len(vibhaktis))
    #st.write(df.to_markdown())
    return df

def nounlisttable2(devnouns=['अस्मद् (त्रि)','राम (पु)']):
    vibhaktis = ['prathamA','sMbodhana', 'dvitIyA','tRtIyA','chaturthI','paMchamI','ShaShThI','saptamI']
    if len(devnouns)==1:
        tdata = np.reshape(nouns[devnouns[0]].split('#'), (8,3))
        #st.write(tdata)
        df = pd.DataFrame(tdata,columns=[transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
    if len(devnouns)==2:
        tdata1 = np.reshape(nouns[devnouns[0]].split('#'), (8,3))
        #st.write(tdata)
        df1 = pd.DataFrame(tdata1,columns=[transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
        tdata2 = np.reshape(nouns[devnouns[1]].split('#'), (8,3))
        #st.write(tdata)
        df2 = pd.DataFrame(tdata2,columns=[transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
        df = df1.combine(df2, lambda x, y: x + ' ' + y)
    df[transliterate("vibhakti")] = [transliterate(i) for i in vibhaktis]
    df = df.set_index(transliterate("vibhakti"))
    #st.write(len(vibhaktis))
    #st.write(df.to_markdown())
    return df

# if st.sidebar.checkbox('Show nountable from prog'):
#     st.subheader('Nountable')
#     st.write(transliterate(noun), transliterate(linga[noun]))
#     st.write(devnoun)
#     df = nountable(noun,linga[noun])
#     df.set_index('', inplace=True)
#     st.write(df.to_markdown())

emojis = [':sunglasses:',':smile:',':smiley:',':heart:',':grin:',':triumph:',':star:',':musical_note:']

copts = []
opts = st.beta_columns(3)
copts.append(opts[0].checkbox('Notes',value='True'))
copts.append(opts[1].checkbox('Quiz'))
copts.append(opts[2].checkbox('Show'))
#copts.append(opts[3].selectbox('Select noun1',devnouns))

# st.write(copts)

# if copts[0]:
#     intro = 1
# else:
#     intro = 0

# #if st.sidebar.checkbox('Quiz nountable'):
# if st.checkbox('Quiz'):
#     quiz = 1
# else:
#     quiz = 0

# #if st.sidebar.checkbox('Show nountable from list'):
# if st.checkbox('Show'):
#     show = 1
# else: show = 0

#devnoun = st.sidebar.selectbox(

if copts[2]:
    sarvadevnoun = st.selectbox(
        'Select sarvanaam',
        sarvadevnouns,)
        #format_func=showdev)

devnoun = st.selectbox(
    'Select noun',
    devnouns,)
    #format_func=showdev)


noun = nounlinga[devnoun]

if copts[0]:
    st.subheader("Notes:")
    st.write("For the set of nouns in the drop down menu, you can see their forms\
    and/or quiz yourself about them. I created these especially to ensure I get the\
    hrasv/dirgha and halant correct for various nouns. I will add more nouns, and\
    features. Currently for the forms you get right, you will see emojis displayed\
    near those forms.")
    st.write("Conjuncts do not show up well on Safari.")
    st.write("In devnagari mode, use H for visarga sign.")

if copts[1]:
    st.subheader('Noun quiz')
    st.write("Please complete the following for ",devnoun)
    
    vibhaktis = []
    cvibhaktis = nouns[devnoun].split('#')
    #cvibhaktis = list(map(lambda it: it.strip(), cvibhaktis))
    cvibhaktis = [item.strip() for item in cvibhaktis]

    corrects = 0
    for i in range(len(labels)):
        cols = st.beta_columns(7)
        vibhaktis.append(cols[0].write(labels[i]))
        for j in range(3):
            vibhaktis.append(cols[j*2+1].text_input(sup[i*3+j],""))
            lab = str(i*3+j+1)
            if cvibhaktis[i*3+j] != vibhaktis[i*7+j*2+1].strip():
                vibhaktis.append(cols[j*2+2].write(''))
                #vibhaktis.append(cols[j*2+2].checkbox('',value=False,key=lab))
            else:
                vibhaktis.append(cols[j*2+2].write(random.choice(emojis)))
                #vibhaktis.append(cols[j*2+2].checkbox('',value=True,key=lab))
                corrects += 1
                

    st.write(corrects,"/24 correct")
    if corrects == 24:
        st.write(':sunglasses:')
    
if copts[2]:
    # We should get noun and linga here that way we can type
    # and not rely on the drop down list
    st.subheader('Nountable')
    #st.write(transliterate(noun), transliterate(linga[noun]))
    if len(sarvadevnoun)>0:
        st.write(sarvadevnoun+ ' ' + devnoun)
        df = nounlisttable2(devnouns=[sarvadevnoun,devnoun])
    else:
        st.write(devnoun)
        df = nounlisttable(devnoun)
    #df.set_index('', inplace=True)
    st.write(df.to_markdown())

# if st.sidebar.checkbox('Create nountable data'):
#     st.subheader('')
#     df = nountable(noun,linga[noun])
#     nlist = '#'.join([j for i in df.iloc[:,[1,2,3]].values.tolist() for j in i])
#     st.write("nouns['",devnoun,"'] = '",nlist,"'",sep='',end='')

#st.write(nounlisttable2(devnouns=['अस्मद् (त्रि)','राम (पु)']).to_markdown())

#st.write(nounlisttable2(devnouns=['राम (पु)']).to_markdown())

#os.system("gtts-cli -l hi 'नमस्ते महोदय' | ffmpeg -i pipe:0 -f wav pipe:1 | ~/Downloads/sox-14.4.2/play -t wav -")
audiostr = "gtts-cli -l hi --slow '%s' | ffmpeg -i pipe:0 -f wav pipe:1 | ~/Downloads/sox-14.4.2/play -t wav -" % nouns[devnoun]
os.system(audiostr)
#st.write(audiostr)