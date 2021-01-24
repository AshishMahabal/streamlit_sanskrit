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
tests['ramA'] = 'प्रथमा#रमा#रमे#रमाः#द्वितीया#रमाम्#रमे#रमाः#तृतीया#रमया#रमाभ्याम्#रमाभिः#चतुर्थी#रमायै#रमाभ्याम्#रमाभ्याः#\
पंचमी#रमायाः#रमाभ्याम्#रमाभ्याः#षष्ठी#रमायाः#रमयोः#रमाणाम्#सप्तमी#रमायाम्#रमयोः#रमासु#संबोधन#हे रमे#हे रमे#हे रम'
tests['phala'] = 'प्रथमा#फलम्#फले#फलानि#द्वितीया#फलम्#फले#फलानि#तृतीया#फलेन#फलाभ्याम्#फलैः#\
चतुर्थी#फलाय#फलाभ्याम्#फलेभ्यः#पंचमी#फलात्#फलाभ्याम्#फलेभ्यः#षष्ठी#फलस्य#फलयोः#फलानाम्#सप्तमी#फले#फलयोः#फलेषु#संबोधन#हे फल#हे फले#हे फलान'
tests['hari'] = 'प्रथमा#हरिः#हरी#हरयः#द्वितीया#हरिम्#हरी#हरीन्#तृतीया#हरिणा#हरिभ्याम्#हरिभिः#चतुर्थी#हरये#हरिभ्याम्#हरिभ्यः#\
पंचमी#हरेः#हरिभ्याम्#हरिभ्यः#षष्ठी#हरेः#हर्योः#हरीणाम्#सप्तमी#हरौ#हर्योः#हरिषु#संबोधन#हे हरे#हे हरी#हे हरय'
tests['rAma'] = 'प्रथमा#रामः#रामौ#रामाः#द्वितीया#रामम्#रामौ#रामान्#तृतीया#रामेण#रामाभ्याम्#रामैः#\
चतुर्थी#रामाय#रामाभ्याम्#रामेभ्यः#पंचमी#रामात्#रामाभ्याम्#रामेभ्यः#षष्ठी#रामस्य#रामयोः#रामाणाम्#सप्तमी#रामे#रामयोः#रामेषु#संबोधन#हे राम#हे रामौ#हे राम'
tests['bAlaka'] = 'प्रथमा#बालकः#बालकौ#बालकाः#द्वितीया#बालकम्#बालकौ#बालकान्#तृतीया#बालकेन#बालकाभ्याम्#बालकैः#\
चतुर्थी#बालकाय#बालकाभ्याम्#बालकेभ्यः#पंचमी#बालकात्#बालकाभ्याम्#बालकेभ्यः#षष्ठी#बालकस्य#बालकयोः#बालकानाम्#सप्तमी#बालके#बालकयोः#बालकेषु#संबोधन#हे बालक#हे बालकौ#हे बालकाः'
tests['guru'] = 'प्रथमा#गुरुः#गुरू#गुरवः#द्वितीया#गुरुम्#गुरू#गुरून्#तृतीया#गुरुणा#गुरुभ्याम्#गुरुभिः#\
चतुर्थी#गुरवे#गुरुभ्याम्#गुरुभ्यः#पंचमी#गुरोः#गुरुभ्याम्#गुरुभ्यः#षष्ठी#गुरोः#गुर्वोः#गुरूणाम्#सप्तमी#गुरौ#गुर्वोः#गुरुषु#संबोधन#हे गुरो#हे गुरू#हे गुरव'

linga = {
        'rAma':'puM',
        'bAlaka':'puM',
        'phala':'napuMsaka',
        'ramA':'strI',
        'hari':'puM',
        'nadi':'strI',
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

if st.sidebar.checkbox('Create nountable data'):
    df = nountable(noun,linga[noun])
    st.write("tests['",noun,"'] = ")
    st.write('#'.join([j for i in df.values.tolist() for j in i]))

if st.sidebar.checkbox('Quiz nountable'):
    st.write("Please complete the following for ",noun)
    vibhaktis = []
    for i in range(8):
        cols = st.beta_columns(4)
        vibhaktis.append(cols[0].write(labels[i]))
        for j in range(3):
            vibhaktis.append(cols[j+1].text_input(sup[i*3+j],""))

    cvibhaktis = tests[noun].split('#')
    #cvibhaktis = list(map(lambda it: it.strip(), cvibhaktis))
    cvibhaktis = [item.strip() for item in cvibhaktis]

    for i in range(len(labels)):
        for j in range(len(vachanas)):
            if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
                st.write("Mismatch in ",labels[i],vachanas[j])

if st.sidebar.checkbox('Debug'):
    for i in range(len(labels)):
        for j in range(len(vachanas)):
            if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
                st.write("Mismatch in ",labels[i], vachanas[j],
                " actual: ",cvibhaktis[i*4+j+1], " user: ", vibhaktis[i*4+j+1],)

if st.sidebar.checkbox('Debug2'):
    for i in range(len(labels)):
        for j in range(len(vachanas)):
            if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
                st.write("Mismatch in ",labels[i], vachanas[j],
                " actual: ",cvibhaktis[i*4+j+1].encode(), " user: ", vibhaktis[i*4+j+1].encode())
