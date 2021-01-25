import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti

st.title('Let us do some Sanskrit')
st.sidebar.header('Noun tables')

#labels = ["प्रथमा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","संबोधन"]
vachanas = ['एक','द्वि','बहु']
sup = ["सु","औ","जस्","सु ","औ ","जस् ","अम्","औट्","शस्","टा",'भ्याम्','भिस्','ङे','भ्याम् ','भ्यस्',
    'ङसि','भ्याम्  ','भ्यस् ','ङस्','ओस्','आम् ','ङि','ओस् ','सुप्']

tests = {}
tests['rAma'] = 'रामः#रामौ#रामाः#हे राम#हे रामौ#हे रामाः#रामम्#रामौ#रामान्#रामेण#रामाभ्याम्#रामैः#\
रामाय#रामाभ्याम्#रामेभ्यः#रामात्#रामाभ्याम्#रामेभ्यः#रामस्य#रामयोः#रामाणाम्#रामे#रामयोः#रामेषु'
tests['ramA'] = 'रमा#रमे#रमाः#हे रमे#हे रमे#हे रमाः#रमाम्#रमे#रमाः#रमया#रमाभ्याम्#रमाभिः#रमायै#रमाभ्याम्#रमाभ्याः#\
रमायाः#रमाभ्याम्#रमाभ्याः#रमायाः#रमयोः#रमाणाम्#रमायाम्#रमयोः#रमासु'
tests['phala'] = 'फलम्#फले#फलानि#हे फल#हे फले#हे फलानि#फलम्#फले#फलानि#फलेन#फलाभ्याम्#फलैः#फलाय#फलाभ्याम्#फलेभ्यः#\
फलात्#फलाभ्याम्#फलेभ्यः#फलस्य#फलयोः#फलानाम्#फले#फलयोः#फलेषु'
tests['hari'] = 'हरिः#हरी#हरयः#हे हरे#हे हरी#हे हरयः#हरिम्#हरी#हरीन्#हरिणा#हरिभ्याम्#हरिभिः#हरये#हरिभ्याम्#हरिभ्यः#\
हरेः#हरिभ्याम्#हरिभ्यः#हरेः#हर्योः#हरीणाम्#हरौ#हर्योः#हरिषु'
tests['bAlaka'] = 'बालकः#बालकौ#बालकाः#हे बालक#हे बालकौ#हे बालकाः#बालकम्#बालकौ#बालकान्#बालकेन#बालकाभ्याम्#बालकैः#\
बालकाय#बालकाभ्याम्#बालकेभ्यः#बालकात्#बालकाभ्याम्#बालकेभ्यः#बालकस्य#बालकयोः#बालकानाम्#बालके#बालकयोः#बालकेषु'
tests['guru'] = 'गुरुः#गुरू#गुरवः#हे गुरो#हे गुरू#हे गुरवः#गुरुम्#गुरू#गुरून्#गुरुणा#गुरुभ्याम्#गुरुभिः#गुरवे#गुरुभ्याम्#गुरुभ्यः#\
गुरोः#गुरुभ्याम्#गुरुभ्यः#गुरोः#गुर्वोः#गुरूणाम्#गुरौ#गुर्वोः#गुरुषु'
tests['nadI'] = 'नदी#नद्यौ#नद्यः#हे नदि#हे नद्यौ#हे नद्यः#नदीम्#नद्यौ#नदीः#नद्या#नदीभ्याम्#नदीभिः#नद्यै#नदीभ्याम्#नदीभ्यः#\
नद्याः#नदीभ्याम्#नदीभ्यः#नद्याः#नद्योः#नदीनाम्#नद्याम्#नद्योः#नदीषु'

labels = ["प्रथमा","संबोधन","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी"]

linga = {
        'rAma':'puM',
        'bAlaka':'puM',
        'phala':'napuMsaka',
        'ramA':'strI',
        'hari':'puM',
        'nadI':'strI',
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

if st.sidebar.checkbox('Show nountable'):
    st.write(transliterate(noun), transliterate(linga[noun]))
    df = nountable(noun,linga[noun])
    df.set_index('', inplace=True)
    st.write(df.to_markdown())

if st.sidebar.checkbox('Create nountable data'):
    df = nountable(noun,linga[noun])
    st.write("tests['",noun,"'] = ")
    st.write('#'.join([j for i in df.iloc[:,[1,2,3]].values.tolist() for j in i]))

# if st.sidebar.checkbox('Quiz nountable'):
#     st.write("Please complete the following for ",noun)
#     vibhaktis = []
#     for i in range(8):
#         cols = st.beta_columns(4)
#         vibhaktis.append(cols[0].write(labels[i]))
#         for j in range(3):
#             vibhaktis.append(cols[j+1].text_input(sup[i*3+j],""))

#     cvibhaktis = tests[noun].split('#')
#     #cvibhaktis = list(map(lambda it: it.strip(), cvibhaktis))
#     cvibhaktis = [item.strip() for item in cvibhaktis]

#     for i in range(len(labels)):
#         for j in range(len(vachanas)):
#             if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
#                 st.write("Mismatch in ",labels[i],vachanas[j])

# if st.sidebar.checkbox('Debug'):
#     for i in range(len(labels)):
#         for j in range(len(vachanas)):
#             if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
#                 st.write("Mismatch in ",labels[i], vachanas[j],
#                 " actual: ",cvibhaktis[i*4+j+1], " user: ", vibhaktis[i*4+j+1],)

# if st.sidebar.checkbox('Debug2'):
#     for i in range(len(labels)):
#         for j in range(len(vachanas)):
#             if cvibhaktis[i*4+j+1] != vibhaktis[i*4+j+1].strip():
#                 st.write("Mismatch in ",labels[i], vachanas[j],
#                 " actual: ",cvibhaktis[i*4+j+1].encode(), " user: ", vibhaktis[i*4+j+1].encode())

if st.sidebar.checkbox('Quiz nountable debug'):
    st.write("Please complete the following for ",noun)
    vibhaktis = []
    cvibhaktis = tests[noun].split('#')
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
                vibhaktis.append(cols[j*2+2].checkbox(lab,value=False,key=lab))
            else:
                vibhaktis.append(cols[j*2+2].checkbox(lab,value=True,key=lab))
                corrects += 1

    st.write(corrects,"/24 correct")