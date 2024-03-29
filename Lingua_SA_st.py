import pandas as pd
import streamlit as st
from SA import sandhi, transliterate, vibhakti
import random
import numpy as np
import os
import random
import json

st.title('Let us do some Sanskrit')
st.sidebar.title("Options")

toDisplay = st.sidebar.radio(
	"Choose",
	["Nouns", "Verbs", "Prahelika", "Subhashitani","SuktayaH"],
	index=2
)
# these elements need to be distinct. Use this later for vikaran and purush pratya.
तिङ् = {} # तिप्‍तस्‍झिसिप्‍थस्‍थमिब्‍वस्‍मस्‍ताताञ्झथासाथाम्‍ध्‍वमिड्वहिमहिङ्
तिङ्['परस्मै'] = "तिप्#तस्#झि#सिप्#थस्#थ#मिप्#वस्#मस्".split('#')
तिङ्['आत्मने'] = "त#आताम्#झ#थास्#आथाम्#ध्वम्#इट्#वहि#महिङ्".split('#')

purush = ['प्रथम','मध्यम','उत्तम']

with open("verbs.json", "rb") as f:
    verbs = json.loads(f.read())

vachanas = ['एक','द्वि','बहु']
sup = ["स् (सु)","औ"," अस् (जस्)","स् (सु) ","औ ","अस् (जस्) ","अम्","औट्","अस् (शस्)","आ (टा)",'भ्याम्','भिस्',
    'ए (ङे)','भ्याम् ','भ्यस्', 'अस् (ङसि)','भ्याम्  ','भ्यस् ','अस् (ङस्)','ओस्','आम् ','इ (ङि)','ओस् ','सु (सुप्)']

emojis = [':sunglasses:',':smile:',':smiley:',':heart:',':grin:',':triumph:',
    ':star:',':musical_note:']

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
nouns['मति (स्त्री)'] = 'मतिः#मती#मतयः#हे मते#हे मती#हे मतयः#मतिम्#मती#मतीः#मत्या#मतिभ्याम्#मतिभिः#मतये/मत्यै#मतिभ्याम्#मतिभ्यः#\
मतेः/मत्याः#मतिभ्याम्#मतिभ्यः#मतेः/मत्याः#मत्योः#मतीनाम्#मतौ/मत्याम्#मत्योः#मतिषु'
nouns['नदी (स्त्री)'] = 'नदी#नद्यौ#नद्यः#हे नदि#हे नद्यौ#हे नद्यः#नदीम्#नद्यौ#नदीः#नद्या#नदीभ्याम्#नदीभिः#नद्यै#नदीभ्याम्#नदीभ्यः#\
नद्याः#नदीभ्याम्#नदीभ्यः#नद्याः#नद्योः#नदीनाम्#नद्याम्#नद्योः#नदीषु'
nouns['पितृ (पु)'] = 'पिता#पितरौ#पितरः#हे पितः#हे पितरौ#हे पितरः#पितरम्#पितरौ#पितॄन्#\
पित्रा#पितृभ्याम्#पितृभिः#पित्रे#पितृभ्याम्#पितृभ्यः#पितुः#पितृभ्याम्#पितृभ्यः#पितुः#पित्रोः#पितॄणाम्#पितरि#पित्रोः#पितृषु'
nouns['युष्मद् (त्रि)'] = 'त्वम्#युवाम्#यूयम्####त्वाम्#युवाम्#युष्मान्#त्वया#युवाभ्याम्#युष्माभिः#तुभ्यम्#युवाभ्याम्#युष्मभ्यम्#\
त्वत्#युवाभ्याम्#युष्मत्#तव#युवयोः#युष्माकम्#त्वयि#युवयोः#युष्मासु'
nouns['अस्मद् (त्रि)'] = 'अहम्#आवाम्#वयम्####माम्/मा#आवाम्/नौ#अस्मान्/नः#मया#आवाभ्याम्#अस्माभिः#मह्यम्/मे#आवाभ्याम्/नौ#अस्मभ्यम्/नः#\
मत्#आवाभ्याम्#अस्मत्#मम/मे#आवयोः/नौ#अस्माकम्/नः#मयि#आवयोः#अस्मासु'
nouns['तद् (पु)'] = 'स:#तौ#ते####तम्#तौ#तान्#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'
nouns['तद् (स्त्री)'] = 'सा#ते#ताः####ताम्#ते#ताः#तया#ताभ्याम्#ताभिः#तस्यै#ताभ्याम्#ताभ्यः#तस्याः#ताभ्याम्#ताभ्यः#तस्याः#तयोः#तासाम्#तस्याम्#तयोः#तासु'
nouns['तद् (न)'] = 'तत्#ते#तानि####तत्#ते#तानि#तेन#ताभ्याम्#तैः#तस्मै#ताभ्याम्#तेभ्यः#तस्मात्#ताभ्याम्#तेभ्यः#तस्य#तयोः#तेषाम्#तस्मिन्#तयोः#तेषु'
nouns['भवत् (पु)'] = 'भवान्#भवन्तौ#भवन्तः#हे भवन्#हे भवन्तौ#हे भवन्तः#भवन्तम्#भवन्तौ#भवतः#भवता#भवद्भ्याम्#भवद्भिः#भवते#भवद्भ्याम्#भवद्भ्यः#भवतः#\
भवद्भ्याम्#भवद्भ्यः#भवतः#भवतोः#भवताम्#भवति#भवतोः#भवत्सु'
nouns['भवत् (स्त्री)'] = 'भवती#भवत्यौ#भवत्यः#हे भवति#हे भवत्यौ#हे भवत्यः#भवतीम्#भवत्यौ#भवत्यः#भवत्या#भवतीभ्याम्#भवतीभिः#\
भवत्यै#भवतीभ्याम्#भवतीभ्यः#भवत्याः#भवतीभ्याम#भवतीभ्यः#भवत्याः#भवत्योः#भवतीनाम्#भवत्याम्#भवत्योः#भवतीषु'
nouns['किम् (पु)'] = 'कः#कौ#के####कम्#कौ#कान्#केन#काभ्याम्#कैः#कस्मै#काभ्याम्#केभ्यः#कस्मात्#काभ्याम्#केभ्यः#\
कस्य#कयोः#केषाम्#कस्मिन्#कयोः#केषु'
nouns['किम् (स्त्री)'] = 'का#के#काः####काम्#के#काः#कया#काभ्याम्#काभिः#कस्यै#काभ्याम्#काभिः#कस्याः#काभ्याम्#काभ्यः#\
कस्याः#कयोः#कासाम्#कस्याम्#कयोः#कासु'
nouns['किम् (न)'] = 'किम्#के#कानि####किम्#के#कानि#केन#काभ्याम्#कैः#कस्मै#काभ्याम्#केभ्यः#कस्मात्#काभ्याम्#केभ्यः#\
कस्य#कयोः#केषाम्#कस्मिन्#कयोः#केषु'

# Following were before strip/split
# nouns['माला (स्त्री)'] = 'माला#माले#मालाः#हे माले#हे माले#हे मालाः#मालाम्#माले#मालाः#मालया#मालाभ्याम्#मालाभिः#मालायै#मालाभ्याम्#मालाभ्यः#मालायाः#मालाभ्याम्#मालाभ्यः#मालायाः#मालयोः#मालानाम्#मालायाम्#मालयोः#मालासु'
# nouns['देव (पु)'] = 'देवः#देवौ#देवाः#हे देव#हे देवौ#हे देवाः#देवम्#देवौ#देवान्#देवेन#देवाभ्याम्#देवैः#देवाय#देवाभ्याम्#देवेभ्यः#देवात्#देवाभ्याम्#देवेभ्यः#देवस्य#देवयोः#देवानाम्#देवे#देवयोः#देवेषु'
# nouns['मुनि (पु)'] = 'मुनिः#मुनी#मुनयः#हे मुने#हे मुनी#हे मुनयः#मुनिम्#मुनी#मुनीन्#मुनिना#मुनिभ्याम्#मुनिभिः#मुनये#मुनिभ्याम्#मुनिभ्यः#मुनेः#मुनिभ्याम्#मुनिभ्यः#मुनेः#मुन्योः#मुनीनाम्#मुनौ#मुन्योः#मुनिषु'
# nouns['रात्रि (स्त्री)'] = 'रात्रिः#रात्री#रात्रयः#हे रात्रे#हे रात्रे#हे रात्रयः#रात्रिम्#रात्री#रात्रीः#रात्र्या#रात्रिभ्याम्#रात्रिभिः#रात्रये/रात्र्यै#रात्रिभ्याम्#रात्रिभ्यः#रात्रेः/रात्र्याः#रात्रिभ्याम्#रात्रिभ्यः#रात्रेः/रात्र्याः#रात्र्योः#रात्रीणाम्#रात्रौ/रात्र्याम्#रात्र्योः#रात्रिषु'
# nouns['नगरी (स्त्री)'] = 'नगरी#नगर्यौ#नगर्यः#हे नगरि#हे नगर्यौ#हे नगर्यः#नगरीम्#नगर्यौ#नगरीः#नगर्या#नगरीभ्याम्#नगरीभिः#नगर्यै#नगरीभ्याम्#नगरीभ्यः#नगर्याः#नगरीभ्याम्#नगरीभ्यः#नगर्याः#नगर्योः#नगरीणाम्#नगर्याम्#नगर्योः#नगरीषु'
# nouns['भानु (पु)'] = 'भानुः#भानू#भानवः#हे भानो#हे भानू#हे भानवः#भानुम्#भानू#भानून्#भानुना#भानुभ्याम्#भानुभिः#भानवे#भानुभ्याम्#भानुभ्यः#भानोः#भानुभ्याम्#भानुभ्यः#भानोः#भान्वोः#भानूनाम्#भानौ#भान्वोः#भानुषु'
# nouns['नेतृ (पु)'] = 'नेता#नेतारौ#नेतारः#हे नेतः#हे नेतारौ#हे नेतारः#नेतारम्#नेतारौ#नेतॄन्#नेत्रा#नेतृभ्याम्#नेतृभिः#नेत्रे#नेतृभ्याम्#नेतृभ्यः#नेतुः#नेतृभ्याम्#नेतृभ्यः#नेतुः#नेत्रोः#नेतॄणाम्#नेतरि#नेत्रोः#नेतृषु'
# nouns['पति (पु)'] = 'पतिः#पती#पतयः#हे पते#हे पती#हे पतयः#पतिम्#पती#पतीन्#पत्या#पतिभ्याम्#पतिभिः#पत्ये#पतिभ्याम्#पतिभ्यः#पत्युः#पतिभ्याम्#पतिभ्यः#पत्युः#पत्योः#पतीनाम्#पत्यौ#पत्योः#पतिषु'
# nouns['धेनु (स्त्री)'] = 'धेनुः#धेनू#धेनवः#हे धेनो#हे धेनू#हे धेनवः#धेनुम्#धेनू#धेनूः#धेन्वा#धेनुभ्याम्#धेनुभिः#धेनवे/धेन्वै#धेनुभ्याम्#धेनुभ्यः#धेनोः/धेन्वाः#धेनुभ्याम्#धेनुभ्यः#धेनोः/धेन्वाः#धेन्वोः#धेनूनाम्#धेनौ/धेन्वाम्#धेन्वोः#धेनुषु'

nouns['माला (स्त्री)'] = 'माला#माले#मालाः#हे माले#हे माले#हे मालाः#मालाम्#माले#मालाः#मालया#मालाभ्याम्#मालाभिः#मालायै#मालाभ्याम्#मालाभ्यः#मालायाः#मालाभ्याम्#मालाभ्यः#मालायाः#मालयोः#मालानाम्#मालायाम्#मालयोः#मालासु'
nouns['देव (पु)'] = 'देवः#देवौ#देवाः#हे देव#हे देवौ#हे देवाः#देवम्#देवौ#देवान्#देवेन#देवाभ्याम्#देवैः#देवाय#देवाभ्याम्#देवेभ्यः#देवात्#देवाभ्याम्#देवेभ्यः#देवस्य#देवयोः#देवानाम्#देवे#देवयोः#देवेषु'
nouns['मुनि (पु)'] = 'मुनिः#मुनी#मुनयः#हे मुने#हे मुनी#हे मुनयः#मुनिम्#मुनी#मुनीन्#मुनिना#मुनिभ्याम्#मुनिभिः#मुनये#मुनिभ्याम्#मुनिभ्यः#मुनेः#मुनिभ्याम्#मुनिभ्यः#मुनेः#मुन्योः#मुनीनाम्#मुनौ#मुन्योः#मुनिषु'
nouns['रात्रि (स्त्री)'] = 'रात्रिः#रात्री#रात्रयः#हे रात्रे#हे रात्रे#हे रात्रयः#रात्रिम्#रात्री#रात्रीः#रात्र्या#रात्रिभ्याम्#रात्रिभिः#रात्रये/रात्र्यै#रात्रिभ्याम्#रात्रिभ्यः#रात्रेः/रात्र्याः#रात्रिभ्याम्#रात्रिभ्यः#रात्रेः/रात्र्याः#रात्र्योः#रात्रीणाम्#रात्रौ/रात्र्याम्#रात्र्योः#रात्रिषु'
nouns['नगरी (स्त्री)'] = 'नगरी#नगर्यौ#नगर्यः#हे नगरि#हे नगर्यौ#हे नगर्यः#नगरीम्#नगर्यौ#नगरीः#नगर्या#नगरीभ्याम्#नगरीभिः#नगर्यै#नगरीभ्याम्#नगरीभ्यः#नगर्याः#नगरीभ्याम्#नगरीभ्यः#नगर्याः#नगर्योः#नगरीणाम्#नगर्याम्#नगर्योः#नगरीषु'
nouns['भानु (पु)'] = 'भानुः#भानू#भानवः#हे भानो#हे भानू#हे भानवः#भानुम्#भानू#भानून्#भानुना#भानुभ्याम्#भानुभिः#भानवे#भानुभ्याम्#भानुभ्यः#भानोः#भानुभ्याम्#भानुभ्यः#भानोः#भान्वोः#भानूनाम्#भानौ#भान्वोः#भानुषु'
nouns['नेतृ (पु)'] = 'नेता#नेतारौ#नेतारः#हे नेतः#हे नेतारौ#हे नेतारः#नेतारम्#नेतारौ#नेतॄन्#नेत्रा#नेतृभ्याम्#नेतृभिः#नेत्रे#नेतृभ्याम्#नेतृभ्यः#नेतुः#नेतृभ्याम्#नेतृभ्यः#नेतुः#नेत्रोः#नेतॄणाम्#नेतरि#नेत्रोः#नेतृषु'
nouns['पति (पु)'] = 'पतिः#पती#पतयः#हे पते#हे पती#हे पतयः#पतिम्#पती#पतीन्#पत्या#पतिभ्याम्#पतिभिः#पत्ये#पतिभ्याम्#पतिभ्यः#पत्युः#पतिभ्याम्#पतिभ्यः#पत्युः#पत्योः#पतीनाम्#पत्यौ#पत्योः#पतिषु'
nouns['धेनु (स्त्री)'] = 'धेनुः#धेनू#धेनवः#हे धेनो#हे धेनू#हे धेनवः#धेनुम्#धेनू#धेनूः#धेन्वा#धेनुभ्याम्#धेनुभिः#धेनवे/धेन्वै#धेनुभ्याम्#धेनुभ्यः#धेनोः/धेन्वाः#धेनुभ्याम्#धेनुभ्यः#धेनोः/धेन्वाः#धेन्वोः#धेनूनाम्#धेनौ/धेन्वाम्#धेन्वोः#धेनुषु'
nouns['वधू (स्त्री)'] = 'वधूः#वध्वौ#वध्वः#हे वधूः#हे वध्वौ#हे वध्वः#वधूम्#वध्वौ#वधूः#वध्वा#वधूभ्याम्#वधूभिः#वध्वै#वधूभ्याम्#वधूभ्यम्#वध्वाः#वधूभ्याम्#वधूभ्यः#वध्वाः#वध्वोः#वधूनाम्#वध्वाम्#वध्वोः#वधूषु'
nouns['मातृ (स्त्री)'] = 'माता#मातरौ#मातरः#हे माता#हे मातरौ#हे मातरः#मातरम्#मातरौ#मातॄ#मात्रा#मातृभ्याम्#मातृभिः#मात्रे#मातृभ्याम्#मातृभ्यः#मातुः#मातृभ्याम्#मातृभ्यः#मातुः#मात्रोः#मातॄणाम्#मातरि#मात्रोः#मातृषु'
nouns['स्त्री (स्त्री)'] = 'स्त्री #स्त्रियौ #स्त्रियः#हे स्त्री#हे स्त्रियौ#हे स्त्रियः#स्त्रियम्, स्त्रीम् #स्त्रियौ #स्त्रियः, स्त्रीः#स्त्रिया#स्त्रीभ्याम् #स्त्रीभिः#स्त्रियै#स्त्रीभ्याम् #स्त्रीभ्यः#स्त्रियाः#स्त्रीभ्याम् #स्त्रीभ्यः#स्त्रियाः#स्त्रियोः #स्त्रीणाम्#स्त्रियाम्#स्त्रियोः #स्त्रीषु'
nouns['विपद् (स्त्री)'] = 'विपत्#विपदौ #विपदः#हे विपत्#हे विपदौ#हे विपदः#विपदम्#विपदौ #विपदः#विपदा#विपद्भ्याम् #विपद्भिः#विपदे#विपद्भ्याम् #विपद्भ्यः#विपदः#विपद्भ्याम् #विपद्भ्यः#विपदः#विपदोः #विपदाम्#विपदि#विपदोः #विपत्सु'
nouns['दिश् (स्त्री)'] = 'दिक्#दिशौ #दिशः#हे दिक्#हे दिशौ#हे दिशः#दिशम्#दिशौ #दिशः#दिशा#दिग्भ्याम्#दिग्भ्यः#दिशे#दिग्भ्याम्#दिग्भ्यः#दिशः#दिग्भ्याम्#दिग्भ्यः#दिशः#दिशोः#दिशाम्#दिशि#दिशोः#दिक्षु'
nouns['वारि (न)'] = 'वारि#वारिणि#वारीणि#हे वारि#हे वारिणि#हे वारीणि#वारि#वारिणि#वारीणि#वारिणा#वारिभ्याम्#वारिभिः#वारिणे#वारिभ्याम्#वारिभ्यः#वारिणः#वारिभ्याम्#वारिभ्यः#वारिणः#वारिणोः#वारीणाम्#वारिणि#वारिणोः#वारिषु'
nouns['अक्षि (न)'] = 'अक्षि#अक्षिणी#अक्षिणी#हे अक्षि, अक्षे#हे अक्ष्णी#हे अक्षीणि#अक्षि#अक्षिणी#अक्षिणी#अक्ष्णा#अक्षिभ्याम्#अक्षिभिः#अक्ष्णे#अक्षिभ्याम्#अक्षिभ्यः#अक्ष्णः#अक्षिभ्याम्#अक्षिभ्यः#अक्ष्णः#अक्ष्णोः#अक्ष्णाम्#अक्ष्णि, अक्षणि#अक्ष्णोः#अक्षिषु'
nouns['मधु (न)'] = 'मधु#मधुनी#मधूनि#हे मधु, मधो#हे मधुनी#हे मधूनि#मधु#मधुनी#मधूनि#मधुना#मधुभ्याम्#मधुभिः#मधुने#मधुभ्याम्#मधुभ्यः#मधुनः#मधुभ्याम्#मधुभ्यः#मधुनः#मधुनोः#मधूनाम्#मधुनि#मधुनोः#मधुषु'

nouns['वाच् (स्त्री)'] = 'वाक् / वाग्#वाचौ#वाचः#हे वाक् / वाग्#हे वाचौ#हे वाचः#वाचम्#वाचौ#वाचः#वाचा#वाग्भ्याम्#वाग्भिः#वाचे#वाग्भ्याम्#वाग्भ्यः#वाचः#वाग्भ्याम्#वाग्भ्यः#वाचः#वाचोः#वाचाम्#वाचि#वाचोः#वाक्षु'
nouns['आशिष् (स्त्री)'] = 'आशीः#आशिषौ#आशिषः#हे आशीः#हे आशिषौ#हे आशिषः#आशिषम्#आशिषौ#आशिषः#आशिषा#आशीर्भ्याम्#आशीर्भिः#आशिषे#आशीर्भ्याम्#आशीर्भ्यः#आशिषः#आशीर्भ्याम्#आशीर्भ्यः#आशिषः#आशिषोः#आशिषाम्#आशिषि#आशिषोः#आशीःषु / आशीष्षु'
nouns['इदम् (स्त्री)'] = 'इयम्#इमे#इमाः####एनाम् / इमाम्#एने / इमे#एनाः / इमाः#एनया / अनया#आभ्याम्#आभिः#अस्यै#आभ्याम्#आभ्यः#अस्याः#आभ्याम्#आभ्यः#अस्याः#एनयोः / अनयोः#आसाम्#अस्याम्#एनयोः / अनयोः#आसु'
nouns['नामन् (न)'] = 'नाम#नाम्नी / नामनी#नामानि#हे नाम / नामन्#हे नाम्नी / नामनी#हे नामानि#नाम#नाम्नी / नामनी#नामानि#नाम्ना#नामभ्याम्#नामभिः#नाम्ने#नामभ्याम्#नामभ्यः#नाम्नः#नामभ्याम्#नामभ्यः#नाम्नः#नाम्नोः#नाम्नाम्#नाम्नि / नामनि#नाम्नोः#नामसु'
nouns['धनुष् (न)'] = 'धनुः#धनुषी#धनूंषि#हे धनुः#हे धनुषी#हे धनूंषि#धनुः#धनुषी#धनूंषि#धनुषा#धनुर्भ्याम्#धनुर्भिः#धनुषे#धनुर्भ्याम्#धनुर्भ्यः#धनुषः#धनुर्भ्याम्#धनुर्भ्यः#धनुषः#धनुषोः#धनुषाम्#धनुषि#धनुषोः#धनुष्षु'
nouns['मनस् (न)'] = 'मनः#मनसी#मनांसि#हे मनः#हे मनसी#हे मनांसि#मनः#मनसी#मनांसि#मनसा#मनोभ्याम्#मनोभिः#मनसे#मनोभ्याम्#मनोभ्यः#मनसः#मनोभ्याम्#मनोभ्यः#मनसः#मनसोः#मनसाम्#मनसि#मनसोः#मनस्सु'
nouns['इदम् (न)'] = 'इदम्#इमे#इमानि####इदम्#इमे#इमानि#एनेन / अनेन#आभ्याम्#एभिः#अस्मै#आभ्याम्#एभ्यः#अस्मात्#आभ्याम्#एभ्यः#अस्य#एनयोः / अनयोः#एषाम्#अस्मिन्#एनयोः / अनयोः#एषु'
nouns['जगत् (न)'] = 'जगत् / जगद्#जगती#जगन्ति#हे जगत् / जगद्#हे जगती#हे जगन्ति#जगत् / जगद्#जगती#जगन्ति#जगता#जगद्भ्याम्#जगद्भिः#जगते#जगद्भ्याम्#जगद्भ्यः#जगतः#जगद्भ्याम्#जगद्भ्यः#जगतः#जगतोः#जगताम्#जगति#जगतोः#जगत्सु'
nouns['अश्रु (न)'] = 'अश्रु#अश्रुणी#अश्रूणि#हे अश्रो#हे अश्रुणी#हे अश्रूणि#अश्रु#अश्रुणी#अश्रूणि#अश्रुणा#अश्रुभ्याम्#अश्रुभिः#अश्रुणे#अश्रुभ्याम्#अश्रुभ्यः#अश्रुणः#अश्रुभ्याम्#अश्रुभ्यः#अश्रुणः#अश्रुणोः#अश्रूणाम्#अश्रुणि#अश्रुणोः#अश्रुषु'
nouns['कर्तृ (न)'] = 'कर्तृ#कर्तृणी#कर्तॄणि#हे कर्तः#हे कर्तृणी#हे कर्तॄणि#कर्तृ#कर्तृणी#कर्तॄणि#कर्त्रा / कर्तृणा#कर्तृभ्याम्#कर्तृभिः#कर्त्रे / कर्तृणे#कर्तृभ्याम्#कर्तृभ्यः#कर्तुः / कर्तृणः#कर्तृभ्याम्#कर्तृभ्यः#कर्तुः / कर्तृणः#कर्त्रोः / कर्तृणोः#कर्तॄणाम्#कर्तरि / कर्तृणि#कर्त्रोः / कर्तृणोः#कर्तृषु'
nouns['सम्पद् (स्त्री)'] = 'सम्पत् / सम्पद्#सम्पदौ#सम्पदः#हे सम्पत् / सम्पद्#हे सम्पदौ#हे सम्पदः#सम्पदम्#सम्पदौ#सम्पदः#सम्पदा#सम्पद्भ्याम्#सम्पद्भिः#सम्पदे#सम्पद्भ्याम्#सम्पद्भ्यः#सम्पदः#सम्पद्भ्याम्#सम्पद्भ्यः#सम्पदः#सम्पदोः#सम्पदाम्#सम्पदि#सम्पदोः#सम्पत्सु'

nouns['श्वश्रू (स्त्री)'] = 'श्वश्रूः#श्वश्र्वौ#श्वश्र्वः#हे श्वश्रु#हे श्वश्र्वौ#हे श्वश्र्वः#श्वश्रूम्#श्वश्र्वौ#श्वश्रूः#श्वश्र्वा#श्वश्रूभ्याम्#श्वश्रूभिः#श्वश्र्वै#श्वश्रूभ्याम्#श्वश्रूभ्यः#श्वश्र्वाः#श्वश्रूभ्याम्#श्वश्रूभ्यः#श्वश्र्वाः#श्वश्र्वोः#श्वश्रूणाम्#श्वश्र्वाम्#श्वश्र्वोः#श्वश्रूषु'
nouns['एक (स्त्री)'] = 'एकः######एकम्###एकेन###एकस्मै###एकस्मात् / एकस्माद्###एकस्य###एकस्मिन्##'
nouns['द्वि/द्व (स्त्री)'] = '#द्वौ######द्वौ###द्वाभ्याम्###द्वाभ्याम्###द्वाभ्याम्###द्वयोः###द्वयोः#'
nouns['त्रि (स्त्री)'] = '##त्रयः######त्रीन्###त्रिभिः###त्रिभ्यः###त्रिभ्यः###त्रयाणाम्###त्रिषु'
nouns['इदम् (स्त्री)'] = 'अयम्#इमौ#इमे####एनम् / इमम्#एनौ / इमौ#एनान् / इमान्#एनेन / अनेन#आभ्याम्#एभिः#अस्मै#आभ्याम्#एभ्यः#अस्मात्#आभ्याम्#एभ्यः#अस्य#एनयोः / अनयोः#एषाम्#अस्मिन्#एनयोः / अनयोः#एषु'

sarvanouns = {}
sarvanouns[''] = ''
sarvanouns['युष्मद् (त्रि)'] = nouns['युष्मद् (त्रि)']
sarvanouns['अस्मद् (त्रि)'] = nouns['अस्मद् (त्रि)']
sarvanouns['तद् (पु)'] = nouns['तद् (पु)']
sarvanouns['तद् (स्त्री)'] = nouns['तद् (स्त्री)']
sarvanouns['तद् (न)'] = nouns['तद् (न)']

labels = ["प्रथमा","संबोधन","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी"]


devnouns = list(nouns.keys())
#st.write(devnouns)
sarvadevnouns = list(sarvanouns.keys())

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

def verblisttable(verb='अस्',pada='परस्मै',lakaara='लट्'):
    पुरुष = ['प्रथम','मध्यम','उत्तम']
    tdata = np.reshape(verbs[verb][pada][lakaara].split('#'), (3,3))
    df = pd.DataFrame(tdata,columns=['एकवचन','द्विवचन','बहुवचन'])
    df['पुरुष'] = पुरुष
    df = df.set_index('पुरुष')
    return df

def fornouns():

    copts = []
    opts = st.columns(3)
    copts.append(opts[0].checkbox('Notes',value='True'))
    copts.append(opts[1].checkbox('Quiz'))
    copts.append(opts[2].checkbox('Show'))
    #copts.append(opts[3].selectbox('Select noun1',devnouns))

    if copts[2]:
        sarvadevnoun = st.selectbox(
        'Select sarvanaam',
        sarvadevnouns,)
        #format_func=showdev)

    devnoun = st.selectbox(
        'Select noun',
        devnouns,)
        #format_func=showdev)

    if copts[0]:
        st.subheader("Notes:")
        st.write("For the set of nouns in the drop down menu, you can see their forms\
        and/or quiz yourself about them. I created these especially to ensure I get the\
        hrasv/dirgha and halant correct for various nouns. I will add more nouns, and\
        features. Currently for the forms you get right, you will see emojis displayed\
        near those forms.")
        st.write("Conjuncts do not show up well on Safari.")
        st.write("In devnagari mode, use H for visarga sign.")
        st.write("स्वौजसमौट्छष्टाभ्याम्भिस्ङेभ्याम्भ्यस्ङसिभ्याम्भ्यस्ङसोसाङ्ङ्योस्सुप् (4.1.2")
        st.write("सुँ-औ-जस्-अम्-औट्-शस्-टा-भ्याम्-भिस्-ङे-भ्याम्-भ्यस्-ङसिँ-भ्याम्-भ्यस्-ङस्-ओस्-आम्-ङि-ओस्-सुप्")

    if copts[1]: # quiz
        st.subheader('Noun quiz')
        st.write("Please complete the following for ",devnoun)
        
        vibhaktis = []
        cvibhaktis = nouns[devnoun].split('#')
        #cvibhaktis = list(map(lambda it: it.strip(), cvibhaktis))
        cvibhaktis = [item.strip() for item in cvibhaktis]

        corrects = 0
        for i in range(len(labels)):
            cols = st.columns(7)
            vibhaktis.append(cols[0].write(labels[i]))
            for j in range(3):
                vibhaktis.append(cols[j*2+1].text_input(sup[i*3+j],""))
                if '/' in cvibhaktis[i*3+j]:
                    posscvibhaktis = cvibhaktis[i*3+j].split('/')
                    if cvibhaktis[i*3+j] == vibhaktis[i*7+j*2+1].strip():
                        vibhaktis.append(cols[j*2+2].write(random.choice(emojis)))
                        corrects += 1
                    elif posscvibhaktis[1]+'/'+posscvibhaktis[0] == vibhaktis[i*7+j*2+1].strip():
                        vibhaktis.append(cols[j*2+2].write(random.choice(emojis)))
                        corrects += 1
                    elif posscvibhaktis[0] == vibhaktis[i*7+j*2+1].strip():
                        vibhaktis.append(cols[j*2+2].write(random.choice(emojis) + '(' + posscvibhaktis[1] + ')'))
                        corrects += 0.5
                    elif posscvibhaktis[1] == vibhaktis[i*7+j*2+1].strip():
                        vibhaktis.append(cols[j*2+2].write(random.choice(emojis) + '(' + posscvibhaktis[0] + ')'))
                        corrects += 0.5
                    else:
                        vibhaktis.append(cols[j*2+2].write(''))
                else:
                #lab = str(i*3+j+1)
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
        
    if copts[2]: # show
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



def forverbs():
    copts = []
    opts = st.columns(3)
    copts.append(opts[0].checkbox('Notes',value='True'))
    copts.append(opts[1].checkbox('Quiz'))
    copts.append(opts[2].checkbox('Show'))
    #copts.append(opts[3].selectbox('Select noun1',devnouns))

    vopts = []
    sopts = st.columns(3)
    vopts.append(sopts[0].selectbox(
        'Select verb',
        list(verbs.keys()),)
    )
    verb = vopts[0]
    vopts.append(sopts[1].selectbox('Select pada',verbs[verb]['pada']))
    #st.write(verbs[verb]['pada'])
    pada = vopts[1]
    vopts.append(sopts[2].selectbox('Select lakaar',list(verbs[verb][pada].keys())))
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
            cols = st.columns(7)
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
        st.subheader('Verbtable')
        st.write(verb,' धातु (गण ',गण,') ',pada,'पद ',lakaara,'लकार selected')
        df = verblisttable(verb,pada,lakaara)
        st.write(df.to_markdown())


if toDisplay == "Prahelika":
    prahelikas = open('prahelika.list','r').read().split(',')
    rchoice = random.sample(prahelikas,1)[0].strip()[1:-1]
    st.subheader("a random prahelika")
    st.write(rchoice)
    #st.stop()
elif toDisplay == "Subhashitani":
    subhashitas = open('subhashitani.list','r').read().split(',')
    rchoice = random.sample(subhashitas,1)[0].strip()[1:-1]
    st.subheader("a random subhashita")
    st.write(rchoice)
elif toDisplay == "SuktayaH":
    suktayah = open('suktayah.list','r').read().split(',')
    rchoice = random.sample(suktayah,1)[0].strip()[1:-1]
    st.subheader("a random sukti")
    st.write(rchoice)
elif toDisplay == "Nouns":
    fornouns()
elif toDisplay == "Verbs":
    forverbs()
