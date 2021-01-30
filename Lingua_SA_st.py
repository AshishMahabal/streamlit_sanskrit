import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti
import random
import numpy as np

st.title('Let us do some Sanskrit')
st.sidebar.header('Noun tables')

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

labels = ["प्रथमा","संबोधन","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी"]

linga = { # Combine this with nounlinga
        'rAma':'puM',
        'bAlaka':'puM',
        'phala':'napuMsaka',
        'ramA':'strI',
        'hari':'puM',
        'nadI':'strI',
        'guru':'puM',
        'yuSmad':'tri',
        'asfmad':'tri',
#        'dhenu':'strI',
#        'madhu':'napuMsaka',
#        'dAtR': 'puM',
        }

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
#        'dhenu':'strI',
#        'madhu':'napuMsaka',
#        'dAtR': 'puM',
        }

devnouns = list(nounlinga.keys())
#nouns = ['rAma','phala','ramA','hari','guru','dhenu','madhu']

def showdev(roman):
    return st.markdown(transliterate(roman))

devnoun = st.sidebar.selectbox(
    'Select noun',
    devnouns,)
    #format_func=showdev)

noun = nounlinga[devnoun]

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

# if st.sidebar.checkbox('Show nountable from prog'):
#     st.subheader('Nountable')
#     st.write(transliterate(noun), transliterate(linga[noun]))
#     st.write(devnoun)
#     df = nountable(noun,linga[noun])
#     df.set_index('', inplace=True)
#     st.write(df.to_markdown())

if st.sidebar.checkbox('Show nountable from list'):
    # We should get noun and linga here that way we can type
    # and not rely on the drop down list
    st.subheader('Nountable')
    #st.write(transliterate(noun), transliterate(linga[noun]))
    st.write(devnoun)
    df = nounlisttable(devnoun)
    #df.set_index('', inplace=True)
    st.write(df.to_markdown())

# if st.sidebar.checkbox('Create nountable data'):
#     st.subheader('')
#     df = nountable(noun,linga[noun])
#     nlist = '#'.join([j for i in df.iloc[:,[1,2,3]].values.tolist() for j in i])
#     st.write("nouns['",devnoun,"'] = '",nlist,"'",sep='',end='')

emojis = [':sunglasses:',':smile:',':smiley:',':heart:',':grin:',':triumph:',':star:',':musical_note:']

if st.sidebar.checkbox('Quiz nountable debug'):
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
    