import streamlit as st
from SA import sandhi, vibhakti, transliterate
import pandas as pd

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

df = nountable('ramA','strI')
df.set_index('', inplace=True)
st.write(df.to_markdown())