import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti

st.title('Let us do some Sanskrit')
st.sidebar.header('Noun tables')

labels = ["प्रथमा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","संबोधन"]
vachanas = ['एक','द्वि','बहु']
sup = ["सु","औ","जस्","अम्","औट्","शस्","टा",'भ्याम्','भिस्','ङे','भ्याम् ','भ्यस्',
    'ङसि','भ्याम्  ','भ्यस् ','ङस्','ओस्','आम्','ङि','ओस् ','सुप्',"सु ","औ ","जस् "]

tests = {}
tests['rAma'] = 'राम:#रामौ#रामा:#रामम्#रामौ#रामान्#रामेण#रामाभ्याम्#रामै:#रामाय#रामाभ्याम्#रामेभ्य:#\
रामात्#रामाभ्याम्#रामेभ्य:#रामस्य#रामयो:#रामाणाम्#रामे#रामयो:#रामेषु#हे राम#हे रामौ#हे रामा:'
tests['ramA'] = 'रमा#रमे#रमा:#रमाम्#रमे#रमा:#रमया#रमाभ्याम्#रमाभि:#रमायै#रमाभ्याम्#रमाभ्या:#\
रमाया:#रमाभ्याम्#रमाभ्या:#रमाया:#रमयो:#रमाणाम्#रमायाम्#रमयो:#रमासु#हे रमे#हे रमे#हे रमा:'
tests['hari'] = 'हरि:#हरी#हरय:#हरिम्#हरी#हरीन्#हरिणा#हरिभ्याम्#हरिभि:#हरये#हरिभ्याम्#हरिभ्य:#\
हरे:#हरिभ्याम्#हरिभ्य:#हरे:#हर्यो:#हरीणाम्#हरौ#हर्यो:#हरिषु#हे हरे#हे हरी#हे हरय:'


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

if st.sidebar.checkbox('Show nountable'):
    st.write(transliterate(noun), transliterate(linga[noun]))
    df = nountable(noun,linga[noun])
    df.set_index('', inplace=True)
    st.write(df.to_markdown())

if st.sidebar.checkbox('Quiz nountable'):
    st.write("Please complete the following for ",noun)
    vibhaktis = []
    for i in range(8):
        cols = st.beta_columns(4)
        vibhaktis.append(cols[0].write(labels[i]))
        for j in range(3):
            vibhaktis.append(cols[j+1].text_input(sup[i*3+j],""))

    cvibhaktis = tests[noun].split('#')

    for i in range(len(labels)):
        for j in range(len(vachanas)):
            if cvibhaktis[i*3+j] != vibhaktis[i*4+j+1]:
                st.write("Mismatch in ",labels[i],vachanas[j])

if st.sidebar.checkbox('Debug'):
    for i in range(len(labels)):
        for j in range(len(vachanas)):
            if cvibhaktis[i*3+j] != vibhaktis[i*4+j+1]:
                st.write("Mismatch in ",labels[i], vachanas[j],
                " actual: ",cvibhaktis[i*3+j], " user: ", vibhaktis[i*3+j],)
