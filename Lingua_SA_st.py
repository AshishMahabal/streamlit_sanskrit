import streamlit as st
from SA import sandhi, vibhakti, transliterate
import pandas as pd
#import unicode

st.title('Let us do some Sanskrit')

st.sidebar.header('Noun tables')

linga = {
        'rAma':'puM',
        'phala':'napuMsaka',
        'ramA':'strI',
        'hari':'puM',
        'guru':'puM',
#        'dhenu':'strI',
#        'madhu':'napuMsaka',
#        'dAtR': 'puM',
        }
nouns = list(linga.keys())
#nouns = ['rAma','phala','ramA','hari','guru','dhenu','madhu']

def showdev(roman):
    return st.markdown(transliterate(roman))

noun = st.sidebar.selectbox(
    'Select noun',
    nouns,)
    #format_func=showdev)

tests = {}
tests['राम'] = 'राम:#रामौ#रामा:##रामम्#रामौ#रामान्##रामेण#रामाभ्याम्#रामै:##रामाय#रामाभ्याम्#रामेभ्य:##\
रामात्#रामाभ्याम्#रामेभ्य:##रामस्य#रामयो:#रामाणाम्##रामे#रामयो:#रामेषु##हे राम#हे रामौ#हे रामा:'

def nountable(noun='rAma',linga='puM'):
    vibhaktis = ['prathamA','dvitIyA','tRtIyA','chaturthI','paMchamI','ShaShThI','saptamI','sMbodhana']
    df = pd.DataFrame([],columns=['',transliterate('ekavachana'), 
            transliterate('dvivachana'), transliterate('bahuvachana')])
    
    for vib in range(8):
        row = []
        row.append(transliterate(vibhaktis[vib]))
        for vachana in range(3):
            v = vibhakti(noun, linga, str(vib+1), str(vachana+1))
            s = sandhi(v)
            t = transliterate(s)
            row.append(t)
        df.loc[len(df)] = row
    return df

st.write(transliterate(noun), transliterate(linga[noun]))
df = nountable(noun,linga[noun])
df.set_index('', inplace=True)
st.write(df.to_markdown())

x='राम'
y='रामम्'

labels = ["प्रथमा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","संबोधन"]

user_inputs = []
for i in range(len(labels)):
    user_inputs.append(st.text_input(labels[i], ""))

cvibhaktis = tests['राम'].split('##')

for i in range(len(labels)):
    orig = ' '.join(cvibhaktis[i].split('#'))
    user = ' '.join(user_inputs[i].split())
    if orig != user:
        st.write("Mismatch in ",labels[i]," actual: ",orig, " user: ", user,
        " ",len(orig)," ",len(user), orig.encode(), user.encode())
    else:
        st.write(labels[i], " matches!")
