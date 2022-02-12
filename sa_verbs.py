# Ashish Mahabal
# mahabal.ashish@gmail.com
# 12 Feb 2022
# V0.9

# Contributions from
# Abhijit Mahabal, Jay Mahabal, Anita Mahabal, Vidyullata (Anu) Mahabal
# Beta testing: Chaitali Parashare, Rohit Gawande

### Imports

import streamlit as st
import streamlit_modal as modal
import streamlit.components.v1 as components
from logging import PlaceHolder

import random
import unicodedata

from google.cloud import firestore
from google.oauth2 import service_account

import json
import datetime
import uuid

from collections import Counter
from collections import defaultdict


### Pinch of CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


### Image instead of unicode that breaks on iphones
#st.title('शब्दखुूळ (तिनाक्षरी)')
st.image('shabdakhoool.png')

### Future extension to allow words of other lengths
#st.sidebar.title("Word Length")
# toDisplay = st.sidebar.radio(
# 	"Options",
# 	["2", "3", "4","5"],
# 	index=1
# )

### We use this for firebase ids. No locations involved
def def_value():
    return uuid.uuid4().hex

# A few Globals
wlen = 3 # That is the length we currently use

# Used for quick tests
wordlist = ['मयत','मकडी','माकड','मगर','मंकड','कमळ','करीम','किस्त्रीम','मंगळ','मालती']

# 'ऱ' (r in तऱ्हा) is mapped to 'र' in blues2
consonants = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 
              'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 
              'य', 'र', 'ल', 'ळ', 'व', 'श', 'ष', 'स', 'ह']

vowels = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ',  'ओ', 'औ', 
          '।', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ',  'े', 'ै',  'ो', 'ौ']

vowel_subs = {'अ':1, 'आ':2, 'इ':3, 'ई':4, 'उ':5, 'ऊ':6, 'ऋ':11, 'ए':7, 'ऐ':8,  'ओ':9, 'औ':10, 
          '।':1, 'ा':2, 'ि':3, 'ी':4, 'ु':5, 'ू':6, 'ृ':11,  'े':7, 'ै':8,  'ो':9, 'ौ':10}

# This could perhaps be eliminated
vowel_revsub = {1:'अ', 2:'आ', 3:'इ', 4:'ई', 5:'उ', 6:'ऊ', 11:'ऋ', 7:'ए', 8:'ऐ',  9:'ओ', 10:'औ'}

# Use the following combo for long attempts. Includes something like an Easter egg
mmdigits = {0:'०',1:'१',2:'२',3:'३',4:'४',5:'५',6:'६',7:'७',8:'८',9:'९',10:'१०', 
    11: '११', 12:'१२', 13:'५६',14:'९९',15:'१०१',16:'१७५७',17:'अनंत',18:'नंतर'}
mdigits = defaultdict(def_value)
for i in range(len(mmdigits)):
    mdigits[i] = mmdigits[i]

### Current marking symbols. Later ones overwrite identical ones from before
### 🟨 does not seem to work on some devices
imunicode = {'R':'🟥','R':'❌','G':'🟩','G':'✅','B':'🟦','B':'🔵','Y':'🟨'}

# The following function is from a gist by Gareth Rees on stackoverflow
# https://stackoverflow.com/questions/6805311/combining-devanagari-characters
# Need to incorporate it better elsewhere in the program
def split_clusters_helper(s):
    """Generate the grapheme clusters for the string s. (Not the full
    Unicode text segmentation algorithm, but probably good enough for
    Devanagari.)
    """
    virama = u'\N{DEVANAGARI SIGN VIRAMA}'
    cluster = u''
    last = None
    for c in s:
        cat = unicodedata.category(c)[0]
        if cat == 'M' or cat == 'L' and last == virama:
            cluster += c
        else:
            if cluster:
                yield cluster
            cluster = c
        last = c
    if cluster:
        yield cluster

def split_clusters(s):
    return list(split_clusters_helper(s))

def splitc(word):
    return [i for i in word]

### These are part of the scoring functions

def get_greens(sclust, tclust):
    '''Report location of the greens'''
    greens = []
    for i in range(len(sclust)):
        if sclust[i] == tclust[i]:
            greens.append(i)
            
    return greens

def vowel_structure(word):
    '''
    Determine what vowel is in each letter
    The graphemes could be used more effectively here (unicodedata)
    '''

    tclust = split_clusters(word)
    tblues = []

    for i in range(len(tclust)): # a single vowel exists in each cluster
        tcomps = [j for j in tclust[i] if j != '्'] # remove halant signs
        
        # check for match अ needs to be handled differently as it does not appear as a separate vowel
        # List the possible unicode vovel endings as [1,11] (अ-कार being 1 and ऋ-कार being 11)
        # Plus actual vowels
            
        found_vowel = 0
        for j in tcomps:
            if j in vowels:
                tblues.append(str(vowel_subs[j]))
                found_vowel += 1
        if found_vowel == 0:
            tblues.append('1')
    
    return tblues

def consonant_structure(word):
    '''
    Get consonant structure i.e. how many consonants in each cluster
    Here too we could use unicodedata
    '''
    
    tclust = split_clusters(word)  
    c_struc = []
    for i in range(len(tclust)):

        tblues2 = []

        tcomps = [j for j in tclust[i] if j != '्'] # exclude halants
            
        found_consonant = 0
        for j in tcomps:
            if j in consonants:
                tblues2.append(j)
                found_consonant += 1 # There can be more than one consonant

        tblues2.append(found_consonant)
        l = len(tblues2)-1
        c_struc.append(get_mdigits(l))
    
    return c_struc

def get_blues2(sclust, tclust):
    '''
    Report location of the blues
    greens will overwrite any overlapping blues the way we call them.
    This is for consonants, so used for both versions.
    The function for vowels removed from this version
    '''
        
    blues2 = []
    supsblues2 = []
    suptblues2 = []
    for i in range(len(sclust)):
        sblues2 = []
        tblues2 = []

        scomps = [j for j in sclust[i] if j != '्'] # remove halant signs
        tcomps = [j for j in tclust[i] if j != '्']

        ### Some part below is repeatatious (here and in other functions)
        found_consonant = 0
        for j in scomps:
            if j in consonants:
                if j == 'ऱ':
                    j = 'र'
                sblues2.append(j)
                found_consonant += 1
        if found_consonant == 0:
            sblues2.append('')
        supsblues2.append(sblues2)
            
        found_consonant = 0
        for j in tcomps:
            if j in consonants:
                if j == 'ऱ':
                    j = 'र'
                tblues2.append(j)
                found_consonant += 1
                st.session_state['usedc'].append(j)
        if found_consonant == 0:
            tblues2.append('')
        suptblues2.append(tblues2)
    
        if set(sblues2).intersection(set(tblues2)):
            blues2.append(i)
    
    return list(blues2),supsblues2,suptblues2
        
def score(secret,test):
    '''
    Add B, G, Y, R in that order to the scoring string
    '''
    
    sclust = split_clusters(secret)
    tclust = split_clusters(test)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen (checked before)

    green_array = get_greens(sclust,tclust)
    # blue_array1,svowels, tvowels = get_blues(sclust,tclust) # The vowels version
    blue_array2,sconsonants, tconsonants = get_blues2(sclust,tclust)
    #blue_comb = sorted(set(blue_array1) | set(blue_array2)) # The vowels version
    blue_comb = sorted(set(blue_array2))

    ss = 'X' * len(sclust)
    for s in blue_comb:
        ss = ss[:s] + 'B' + ss[s + 1:]
    for s in green_array: # This overwrite the B's
        ss = ss[:s] + 'G' + ss[s + 1:]

    if ss.count('X') > 1: # No yellows if only one is X (==Red)
        #newss = test_for_yellows(ss,svowels,tvowels,sconsonants,tconsonants) # The vowels version
        newss = test_for_yellows_conly(ss,sconsonants,tconsonants)
    else:
        newss = ss.replace('X','R')
        
    return newss

def test_for_yellows_conly(ss,sconsonants,tconsonants):
    '''
    Return location of yellows (and reds)
    This is for consonants only
    '''

    ysconsonants = []
    ytconsonants = []
    checklist = []
    # Check for and exclude G and B
    for i in range(len(sconsonants)):
        if ss[i] == 'X':
            ysconsonants.append(sconsonants[i])
            ytconsonants.append(tconsonants[i])
            checklist.append(i)
        else:
            ysconsonants.append(['']) # changed this from 0 for set union to work
            ytconsonants.append(['']) # changed this from 0 for set union to work
    
    # Now we have a possibly smaller string to work with
    ys = []
    accountedc = [] # this is for the consonants

    for i in checklist: # i is from test, so ytconsonants
        if ytconsonants[i] != ['']: # skip pure vowels
            for j in checklist: # j is from secret, so ysconsonants
                if j not in accountedc and (set(ytconsonants[i]) & set(ysconsonants[j])):
                    #print("found in union")
                    ys.append(i)
                    accountedc.append(j) # j is now matched, so don't match it again
                    #print("appending %d to ys due to consonant match" % i)
    uniq_ys = set(ys)
    
    for i in checklist: # use word length here
        if i in uniq_ys:
            ss = ss[:i] + 'Y' + ss[i + 1:]
        else:
            ss = ss[:i] + 'R' + ss[i + 1:]
    
    return ss

# The following few functions are for the checkboxes/buttons

def tldr():
    blacktext("शब्द ओळखा (स्वर/व्यंजन)")
    blacktext("`अअआ`/`०११` = अकरा/अमका/..")
    blacktext("`अअआ`/`१११` = बंगला/बगळा/..")
    blacktext("`अअअ`/`११२` = समक्ष/सशक्त/..")
    blacktext("`उआई`/`०३१` = उत्क्रांती")
    blacktext("%s अचूक" % imunicode['G'])
    blacktext("%s किंचीत चूक" % imunicode['B'])
    blacktext("%s जागा चुकली" % imunicode['Y'])
    blacktext("%s चूक*" % imunicode['R'])
    blacktext("* तपशील पहा")

#### todos() not displayed currently
def todos():
    st.subheader("ToDos:")
    st.markdown("- Add items to this list")
    st.markdown("- Lots of features.")
    st.markdown("- Trim word list")
    st.markdown("- Provide examples with markings")

## What?
def blacktext(text):
    mtext = "<font color='black'>%s</font>" % text
    st.markdown(mtext,unsafe_allow_html=True )

def whitetext(text):
    mtext = "<font color='magenta'>%s</font>" % text
    st.markdown(mtext,unsafe_allow_html=True )

def colortext(text,color):
    mtext = "<font color=%s>%s</font>" % (color,text)
    st.markdown(mtext,unsafe_allow_html=True )

def details():
    whitetext("जवळजवळ 4000 शब्दांच्या यादीतून एक शब्द विनाक्रम निवडला जातो. त्याचा घाट (स्वराकार आणि\
        व्यंजनसंख्या) सांगितली जाते.")
    whitetext("उदाहरणार्थ: 'बछडा'चा स्वराकार अअआ आणि व्यंजनसंख्या १११.")
    whitetext("'अप्सरा'चे अअआ आणि ०२१.")
    whitetext("'अलिप्त'चे अइअ/०१२. व्यंजनांक ० म्हणजे शुद्ध स्वर.")
    whitetext("ष्ट्य,त्त्व वगैरेंचा व्यंजनांक ३ आहे.")
    whitetext("शब्द शोधतांना प्रयत्नशब्द कोणत्याही घाटाचे चालतात. अनेकदा मुद्दाम जोडाक्षरे वापरल्याने फायदा होतो (प्र, त्र वगैरे).")
    whitetext("4-6 प्रयत्नांत उत्तर मिळू शकतं.")
    whitetext("%s: अक्षर अचूक आहे (जागा, स्वर, आणि व्यंजन)." % imunicode['G'])
    whitetext("%s: अक्षरातील निदान एक व्यंजन याच जागी योग्य आहे (सगळी व्यंजने बरोबर असल्यास फरक अनुस्वाराचा किंवा स्वराचा असू शकतो).\
         उदाहरणार्थ: 'का'च्या ऐवजी क्षे (=क्+षे) वापरल्यास, किंवा 'प'च्या जागी पु, इ ऐवजी ओ इत्यादि" %imunicode['B'])
    whitetext("%s: अक्षरातील निदान एक व्यंजन इतर कोणत्यातरी जागी योग्य आहे." % imunicode['Y'])
    whitetext("%s: या जागी वापरलेले अक्षर चुकले आहे." % imunicode['R'])
    whitetext("%s %s %s %s या क्रमाने गुण दिले जातात, आणि एका स्थानाला एकच गुण मिळू शकतो." % (imunicode['G'], imunicode['B'], imunicode['Y'], imunicode['R']))
    whitetext("काही टिपा:")
    whitetext("१. अनुस्वार स्वरांमध्ये गणले जात नाहीत आणि व्यंजनांमध्येही नाही. \
        स्वरक्रमात अ असल्यास तो म असू शकेल किंवा मं (किंवा क, कं, ... आणि व्यंजनसंख्या शून्य असल्यास अ किंवा अं)")
    whitetext("२. क्ष (= क् + ष) आणि ज्ञ (= ज् + ञ) ही जोडाक्षरे आहेत.")
    whitetext("३. विसर्ग (:), अर्ध-चंद्र ( ॅ), चंद्र-बिंदू ( ॅं), हलन्त (्) गुप्त शब्दांच्या यादीत अंतर्भूत नाहीत.")
    whitetext("४. %s %s %s च्या सानिध्यात %s फसवा ठरू शकतो. उदाहरणार्थ: समजा गुप्तशब्द आहे कर्तव्य आणि तुमचा प्रयत्न आहे कातरी.\
         का आणि क अर्धवट जुळतात म्हणून का ला मिळतो  %s. त ला देखिल मिळतो %s \
        कारण तो र् + त् मधील त शी जुळतो. शेवटच्या री ला मात्र त्याच र्त मधील र ला जुळूनही %s मिळतो \
        कारण र्त ला आधीच एक गुण बहाल झाला आहे (%s)." % (imunicode['G'], imunicode['B'], imunicode['Y'], imunicode['R'],imunicode['B'], imunicode['B'], imunicode['R'], imunicode['B']))

def reveal():
    '''
    Show the answer
    May be take this out at some point?
    '''
    t2put = whitetext('%s' % st.session_state['secret'])
    st.components.v1.html(t2put,width=50,height=10) # Height doesn't seem to do much

def newplay():
    '''
    Because of the was the state works, this is non-trivial.
    Introduces a race condition with the second empty
    '''
    whitetext("Not yet implemented.\nReload for now.")
    # st.markdown("Another play")
    # del st.session_state['secret']
    # placeholder0.empty()
    #mainfunc(wlen)

def getinput(secret,imunicode,onemore,depth):
    '''
    This is the main function getting input and managing flow
    Has recursion
    '''
    
    placeholder = st.empty()
    with placeholder.container():
        if len(st.session_state['mylist'])>1: # If an entry that has been scored is present
            for i in range(1,len(st.session_state['mylist'])):
                col1, col2, col3 = st.columns([10,10,20]) # positioning is a painpoint
                with col1: 
                    forcol1 = ''
                    forcol1 = forcol1 + '\n' + ''.join([imunicode[st.session_state['mylist'][i][1][j]] for j in range(len(st.session_state['mylist'][i][1]))])
                    st.write("%8s %s %s" % (forcol1,"  ",st.session_state['mylist'][i][0]))
                if i == len(st.session_state['mylist'])-1:
                    with col2:
                        if st.session_state['mylist'][i][1] != 'G' * len(split_clusters(secret)):
                            blab = 'खुलासा %s' % mdigits[i]
                            bkey = 'खुलासा %s' % st.session_state['gcount']
                            if st.button(blab,key=bkey):
                                with modal.container(): # It is currently a modal
                                    explain(st.session_state['mylist'][i][1])
                        else:
                            st.text('तुम्ही जिंकलात')
            
        if onemore: # If victory has not been achieved
            col1, col2 = st.columns([20,10])
            with col1:
                prompt = "स्वरक्रम `%s` व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape']))
                myc2 = st.text_input('','',key=st.session_state['gcount'],placeholder=prompt)
        else:
            if st.session_state['balloons'] == 1: # This still causes some issues
                st.balloons()
                st.session_state['balloons'] = 0
            col1, col2 = st.columns([12, 16])
            modalstr = ''
            for i in range(1,len(st.session_state['mylist'])):
                modalstr = modalstr + ''.join([imunicode[k] for k in st.session_state['mylist'][i][1]]) + '\n'
            with col1: # शब्दखूुळ doesn't show properly everywhere
                st.write("दवंडी पिटा")
                st.code("शब्दखूुळ\n#%d %s/∞\n\n%s" % (st.session_state['nthword'],get_mdigits(len(st.session_state['mylist'])-1),modalstr))

            myc2 = ''

    if myc2.strip():
        ttclust = split_clusters(myc2.strip())

        goodstr=1 # This shouldn't be needed
        goodstr = check_validity(ttclust)
        if len(ttclust) != len(split_clusters(secret)):
            goodstr = 0
        if goodstr == 1:
            myc2score = score(secret,myc2.strip())
            st.session_state['mylist'].append([myc2.strip(),myc2score,0])

        st.session_state['gcount'] += 1
        placeholder.empty() # This empties stuff above. Streamlit state stuff
        depth += 1

        ### Record all words for the winners
        if goodstr !=0 and myc2score == 'G' * len(split_clusters(secret)):
                write2firebase(st.session_state['sessionid'],st.session_state['mylist'])
                getinput(secret,imunicode,0,depth)
        else:
            getinput(secret,imunicode,1,depth)

def write2firebase(sid,inlist):
    #db = firestore.Client.from_service_account_json("firestore-key.json") # local stuff
    key_dict = json.loads(st.secrets["textkey"]) # secret stored remotely
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="wordlemart")
    doc_ref = db.collection(u'plays').document(sid)
    setstr = {}
    setstr['attempts'] = []  
    for m in range(1,len(inlist)):
        attemptdict = {}
        attemptdict[u'input'] = inlist[m][0]
        attemptdict[u'score'] = inlist[m][1]
        attemptdict[u'indict'] = inlist[m][2]
        setstr['attempts'].append(attemptdict)
    timenow = datetime.datetime.now(datetime.timezone.utc)
    setstr[u'wintime'] = timenow
    doc_ref.set(setstr)

def get_mdigits(n):
    '''
    Good attempts last at most 10 tries
    '''
    if n in mdigits:
        return mdigits[n]
    else:
        return '>१०'

def explain(theScore):
    '''
    This should include actual letters for better support.
    Hopefully after a couple of games most people don't care about this help.
    '''

    scoreCount = Counter(theScore)

    blacktext("*खुलासा*")
    if scoreCount['G']>0:
        blacktext("%d %s %d अचूक" % (scoreCount['G'],imunicode['G'],scoreCount['G']))
    if scoreCount['B']>0:
        blacktext("%d %s %d किंचीत चूक" % (scoreCount['B'],imunicode['B'],scoreCount['B']))
    if scoreCount['Y']>0:
        blacktext("%d %s %d चूक जागा" % (scoreCount['Y'],imunicode['Y'],scoreCount['Y']))
    if scoreCount['R']>0:
        if scoreCount['G']>0 or scoreCount['B']>0 or scoreCount['Y']>0:
            blacktext("%d %s %d चूक*" % (scoreCount['R'],imunicode['R'],scoreCount['R']))
            blacktext("* तपशील पहा")
        else:
            blacktext("%d %s %d चूक" % (scoreCount['R'],imunicode['R'],scoreCount['R']))

def copyright():
    whitetext("*Copyright 2022* (All rights reserved.)")
    whitetext("Developed by Ashish Mahabal using Python + Streamlit (and pinch of CSS)")
    whitetext("Code suggestions/help: [Jay, Abhijit] Mahabal")
    whitetext("The code is research style - meaning it has many hidden features (that may seem like bugs),\
         and scope for future development e.g. providing synonyms and similar shaped words.")
    whitetext("Credits:")
    whitetext("Inspiration from Wordle. Wordnet's wordlist.")
    whitetext("Alpha-testers: [Abhijit, Anita, Jay, Anu] Mahabal ")
    whitetext("Beta-testers: Chaitali Parashare, Rohit Gawande")
    whitetext("We do not collect any personal or location data.")
    whitetext("Contact: [email](mailto:mahabal.ashish@gmail.com)|[twitter](https://twitter.com/aschig)")

# devnagari letter-set in unicode is assigned to the 0900-097F block (==2304-2431)
# https://unicode.org/charts/PDF/U0900.pdf
# Separate the characters into vovels, consonants, kanha-matra, halant, anusvara, visarga
# Use the unicodedata.category for this
vclust = [2309, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320,
    2321, 2322, 2323, 2324, 2400, 2401, 2418]
cclust = [i for i in range(2325,2362)]
kclust = [2366, 2367, 2368, 2369, 2370, 2371, 2372, 2373, 2374, 2375, 2376, 2377,
    2378, 2379, 2380, 2383, 2402, 2403]
hclust = [2381]
aclust = [2305, 2306]
viclust = [2307]

revclust = {}
for i in range(2304,2432):
    revclust[i] = 'n'   # Not allowed (the default)
for i in vclust:
    revclust[i] = 'v'   # vowel
for i in cclust:
    revclust[i] = 'c'   # consonant
for i in kclust:
    revclust[i] = 'k'   # kanha-matra (only one of these will be allowed)
for i in hclust:
    revclust[i] = 'h'   # halant
for i in aclust:
    revclust[i] = 'a'   # anusvara and chandarbindu
for i in viclust:
    revclust[i] = 'vi'  # visarga

def check_validity(in_clust):
    '''
    input: in_clust 
    output: 1 if all clusts good; 0 if any bad
    Rules:
    At most one kanha-matra
    one anusvara or one cb can combine with kanha-matra
    one visarga ok
    kanha-matra can not combine with vowels
    2304 to 2431 is the ord range allowed for devnag splits
    '''

    for j in range(len(in_clust)):
        clust_occ = {'v':0,'c':0,'k':0,'h':0,'a':0,'vi':0,'n':0}
        for k in range(len(in_clust[j])):
            if ord(in_clust[j][k]) < 2304 or ord(in_clust[j][k]) > 2431:
                #st.write("No!")
                return 0
            clust_occ[revclust[ord(in_clust[j][k])]] += 1
            #st.write(j,k,ord(in_clust[j][k]),in_clust[j][k])
        if clust_occ['n'] > 0:
            #st.write("disallowed character")
            return 0 # ideally, here and elsewhere, char type should also be returned
        if clust_occ['k'] > 1:
            #st.write("too many kanha-matra")
            return 0
        if clust_occ['a'] > 1:
            #st.write("too many anusvara/cb")
            return 0
        if clust_occ['vi'] > 1:
            #st.write("too many visargas")
            return 0
        if clust_occ['k'] > 0 and clust_occ['v'] > 0:
            #st.write("kanha-matra can not combine with pure vowels")
            return 0
        if clust_occ['c'] > 4:
            #st.write("too many consonants in one letter")
            return 0

    return 1

def mainfunc(n):
    '''
    Wrapper function
    '''

    secret_wordfile = "subwordslen%d.dat" % n # generic for lengths
    
    st.session_state['gcount'] = 1
    st.session_state['mylist'] = ['a'] # we ignore the zeroth later
    st.session_state['usedc'] = ['X'] # we ignore the zeroth later
    st.session_state['usedv'] = ['X'] # we ignore the zeroth later

    if 'secret' not in st.session_state:
        st.session_state['balloons'] = 1
        st.session_state['sessionid'] = uuid.uuid4().hex
        words = open(secret_wordfile,'r').read().split('\n')
        nthword = random.randrange(len(words))
        secret = words[nthword]
        st.session_state['nthword'] = nthword
        st.session_state['secret'] = secret
        st.session_state['rsshape'] = [vowel_revsub[int(i)] for i in vowel_structure(secret)]
        st.session_state['cshape'] = consonant_structure(secret)
    secret = st.session_state['secret']

    col2, col1 = st.columns(2)
    with col1:
        if st.button('?'):
            with modal.container():
                tldr()
    with col2:
        st.markdown("शोधा: स्वरक्रम `%s` व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape'])))

### Used for testing purposes
    # secret = 'प्रकाश'
    # secret = 'लर्त्रण'
    # secret = 'प्रसाद'

    depth = 0
    getinput(secret,imunicode,1,depth)

    usedc = set(st.session_state['usedc'])
    usedv = set(st.session_state['usedv'])
    usedc.remove('X')
    usedv.remove('X')
    untriedc = set(consonants).difference(usedc)

    ### This would be used in the harder version
    untriedv = set(vowels).difference(usedv)

    st.write("`वापरलेली` आणि न वापरलेली व्यंजने: ")
    uandunusedcl = ''
    for c in consonants:
        if c in untriedc:
            uandunusedcl += '%s ' % c
        else:
            uandunusedcl += '`%s` ' % c
    st.markdown(uandunusedcl)

# The following 4 should ideally be in a row
    col1, col2 = st.columns([10,4]) 
    with col1:
        if st.button('तपशील'):
            details()
    with col2:
        if st.button('उत्तर'):
            #with modal.container():
            reveal()

    col1, col2 = st.columns([10,4])
    with col1:
        if st.button('Copyright'):
            copyright()
    with col2:
        if st.button('नवी खेळी'):
            newplay()

    # The following is for window focus
    components.html(
        f"""
            <script>
                var input = window.parent.document.querySelectorAll("input[type=text]");
                for (var i = 0; i < input.length; ++i) {{
                    input[i].focus();
                }}
        </script>
        """,
        height=150
    )

# This was for trying the "new game button"
#mainfunc(int(toDisplay))
#placeholder0 = st.empty()
#with placeholder0.container():

mainfunc(wlen) # wlen is the global at the top