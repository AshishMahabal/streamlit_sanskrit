from logging import PlaceHolder
from numpy.lib.function_base import place
import streamlit as st
import random
import unicodedata
import string
import streamlit_modal as modal
import streamlit.components.v1 as components
from google.cloud import firestore
from google.oauth2 import service_account
import json
import datetime
import uuid
from collections import Counter
from collections import defaultdict

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

#st.title('शब्दखुूळ (तिनाक्षरी)')
st.image('shabdakhoool.png')
#st.sidebar.title("Word Length")

# toDisplay = st.sidebar.radio(
# 	"Options",
# 	["2", "3", "4","5"],
# 	index=1
# )

def def_value():
    return uuid.uuid4().hex

# Globals
wlen = 3
wordlist = ['मयत','मकडी','माकड','मगर','मंकड','कमळ','करीम','किस्त्रीम','मंगळ','मालती']

# 'ऱ' is mapped to 'र' in blues2
consonents = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 
              'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 
              'य', 'र', 'ल', 'ळ', 'व', 'श', 'ष', 'स', 'ह']

vowels = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ',  'ओ', 'औ', 
          '।', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ',  'े', 'ै',  'ो', 'ौ']

vowel_subs = {'अ':1, 'आ':2, 'इ':3, 'ई':4, 'उ':5, 'ऊ':6, 'ऋ':11, 'ए':7, 'ऐ':8,  'ओ':9, 'औ':10, 
          '।':1, 'ा':2, 'ि':3, 'ी':4, 'ु':5, 'ू':6, 'ृ':11,  'े':7, 'ै':8,  'ो':9, 'ौ':10}

vowel_revsub = {1:'अ', 2:'आ', 3:'इ', 4:'ई', 5:'उ', 6:'ऊ', 11:'ऋ', 7:'ए', 8:'ऐ',  9:'ओ', 10:'औ'}
mmdigits = {0:'०',1:'१',2:'२',3:'३',4:'४',5:'५',6:'६',7:'७',8:'८',9:'९',10:'१०', 
    11: '११', 12:'१२', 13:'५६',14:'९९',15:'१०१',16:'१७५७',17:'अनंत',18:'नंतर'}
#mdigits = {0:'०',1:'१',2:'२',3:'३',4:'४',5:'५'}
mdigits = defaultdict(def_value)
for i in range(19):
    mdigits[i] = mmdigits[i]
imunicode = {'R':'🟥','R':'❌','G':'🟩','G':'✅','B':'🟦','B':'🔵','Y':'🟨'}

# The following two functions are from the code Abhijit had found somewhere
# for his crossword effort
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

def get_greens(sclust, tclust):
    
    greens = []
    for i in range(len(sclust)):
        if sclust[i] == tclust[i]:
            greens.append(i)
            
    return greens

def vowel_structure(word):
    tclust = split_clusters(word)
    
    tblues = []

    for i in range(len(tclust)):
        # remove halant signs
        tcomps = [j for j in tclust[i] if j != '्']
        
        # check for match अ needs to be handled differently as it does not appear as a separate vowel
        # List the possible unicode vovel endings as 0-12 (akar being 0 and rukar being 12)
        # Plus actual vowels
            
        found_vowel = 0
        for j in tcomps:
            if j in vowels:
                tblues.append(str(vowel_subs[j]))
                found_vowel += 1
        if found_vowel == 0:
            tblues.append('1')
    
#    return list(set(blues))
    return tblues

def consonant_structure(word):
    '''
    Get consonant structure
    '''
    
    tclust = split_clusters(word)  
    c_struc = []
    for i in range(len(tclust)):

        tblues2 = []

        tcomps = [j for j in tclust[i] if j != '्']
            
        found_consonent = 0
        for j in tcomps:
            if j in consonents:
                tblues2.append(j)
                found_consonent += 1
        tblues2.append(found_consonent)
        l = len(tblues2)-1
        c_struc.append(get_mdigits(l))
        # if l in mdigits:
        #     c_struc.append(mdigits[l])
        # else:
        #     c_struc.append('∞')
    
    return c_struc

def get_blues2(sclust, tclust):
    '''
    greens will overwrite any overlapping blues the way we call them.
    This is for consonents, so used for both versions.
    '''
        
    blues2 = []
    supsblues2 = []
    suptblues2 = []
    for i in range(len(sclust)):
        sblues2 = []
        tblues2 = []

        scomps = [j for j in sclust[i] if j != '्'] # remove halant signs
        tcomps = [j for j in tclust[i] if j != '्']
        # check for match अ needs to be handled differently as it does not appear as a separate vowel
        # List the possible unicode vovel endings as 0-12 (akar being 0 and rukar being 12)
        # Plus actual vowels
        
        #print(scomps,tcomps)
        found_consonent = 0
        for j in scomps:
            if j in consonents:
                if j == 'ऱ':
                    j = 'र'
                sblues2.append(j)
                found_consonent += 1
        if found_consonent == 0:
            sblues2.append('')
        supsblues2.append(sblues2)
            
        found_consonent = 0
        for j in tcomps:
            if j in consonents:
                if j == 'ऱ':
                    j = 'र'
                tblues2.append(j)
                found_consonent += 1
                st.session_state['usedc'].append(j)
        if found_consonent == 0:
            tblues2.append('')
        suptblues2.append(tblues2)
    
        if set(sblues2).intersection(set(tblues2)):
            blues2.append(i)

        #st.write(supsblues2)
    
    return list(blues2),supsblues2,suptblues2
        
def score(secret,test):
    '''
    Add B, G, Y, R in that order the the scoring string
    '''
    
    sclust = split_clusters(secret)
    tclust = split_clusters(test)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen

    green_array = get_greens(sclust,tclust)
    # blue_array1,svowels, tvowels = get_blues(sclust,tclust)
    blue_array2,sconsonents, tconsonents = get_blues2(sclust,tclust)
    #blue_comb = sorted(set(blue_array1) | set(blue_array2))
    blue_comb = sorted(set(blue_array2))

    ss = 'X' * len(sclust)
    for s in blue_comb:
        ss = ss[:s] + 'B' + ss[s + 1:]
    for s in green_array: # This overwrite the B's
        ss = ss[:s] + 'G' + ss[s + 1:]

    if ss.count('X') > 1: # No yellows if only one is X (==Red)
        #newss = test_for_yellows(ss,svowels,tvowels,sconsonents,tconsonents)
        newss = test_for_yellows_conly(ss,sconsonents,tconsonents)
    else:
        newss = ss.replace('X','R')
        
    return newss

def test_for_yellows_conly(ss,sconsonents,tconsonents):
    '''
    This is for consonents only
    '''

    ysconsonents = []
    ytconsonents = []
    checklist = []
    # Check for and exclude G and B
    for i in range(len(sconsonents)):
        if ss[i] == 'X':
            ysconsonents.append(sconsonents[i])
            ytconsonents.append(tconsonents[i])
            checklist.append(i)
        else:
            ysconsonents.append(['']) # changed this from 0 for set union to work
            ytconsonents.append(['']) # changed this from 0 for set union to work
    
    # Now we have a possibly smaller string to work with
    ys = []
    accountedc = [] # this is for the consonants

    for i in checklist: # i is from test, so ytconsonants
        if ytconsonents[i] != ['']: # skip pure vowels
            for j in checklist: # j is from secret, so ysconsonants
                if j not in accountedc and (set(ytconsonents[i]) & set(ysconsonents[j])):
                    #print("found in union")
                    ys.append(i)
                    accountedc.append(j)
                    #print("appending %d to ys due to consonent match" % i)
    uniq_ys = set(ys)
    
    for i in checklist: # use word length here
        if i in uniq_ys:
            ss = ss[:i] + 'Y' + ss[i + 1:]
        else:
            ss = ss[:i] + 'R' + ss[i + 1:]
    
    return ss

# The following few functions are for the checkboxes/buttons

def notes2():
    #blacktext("*Notes:*")
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
    # blacktext("Enter a Marathi word of suggested length and hit tab or enter.")
    # blacktext("> The vowel shape indicates the vowels in the word e.g. अअआ could mean अकरा or बछडा etc.")
    # blacktext("> The consonant shape indicates number of consonants in each letter e.g. 012 indicates that\
    #     the first is a pure vowel, the second is a single consonant (with a vowel), and the\
    #     third is a two-consonant combo (with a vowel) e.g. अभद्र or आरक्त or अलिप्त.\
    #     Note that क्ष (= क् + ष) and ज्ञ (= ज् + ञ) are both conjuncts of size 2.")
    # blacktext("> Anusvar is not counted. If the code suggests a म, it could be मं\
    #     and if it suggests अ it could be अं.")
    # blacktext("> Visargas :, ardha-chandra ॅ, chandra-bindu ॅं, halant (्) are not in\
    #      the secret words.")
    # blacktext("%s Green: letter correct in position, consonant(s), and vowel." % imunicode['G'])
    # blacktext("%s Blue: at least one consonant matches at that position\
    #      e.g. का for क्षे (=क्+षे), प for पु, इ for ओ etc." %imunicode['B'])
    # blacktext("%s Yellow: at least one consonant matches at another position." % imunicode['Y'])
    # blacktext("%s Red: the consonant does not match any letter not already matched. Blue and Yellow take\
    #     precedence over Red, so the following is possible: the secret word is\
    #     कर्तव्य and you have guessed कातरी. The का gets a Blue because क matches, the त also gest\
    #     a Blue because it due to the त in र् + त् and finally the री gets a Red despite the \
    #      र् matching that in र्त because something has already matched the second position." % imunicode['R'])
    # blacktext("> When you get all Greens, you win.")
    #blacktext("More examples will be added under 'Details'.")
    #str1 = "शब्दातील व्यंजनांची संख्या - अक्षरांगणीक: `%s` (0: शुद्ध स्वर, 1: क..ह, 2: प्र त्र क्ष ज्ञ ष्ट, 3: ष्ट्य,त्त्व,..)" % ''.join(cshape)
    #blacktext(str1)

def todos():
    st.subheader("ToDos:")
    st.markdown("- Add items to this list")
    st.markdown("- Lots of features.")
    st.markdown("- Should map 'ऱ' to 'र'")
    st.markdown("- Compare input words against real words")
    st.markdown("- Trim word list")
    st.markdown("- Provide examples with markings")
    st.markdown("- ~~Counter changes when radio buttons clicked - avoid that~~")

def blacktext(text):
    mtext = "<font color='black'>%s</font>" % text
    st.markdown(mtext,unsafe_allow_html=True )

def whitetext(text):
    mtext = "<font color='white'>%s</font>" % text
    st.markdown(mtext,unsafe_allow_html=True )

def colortext(text,color):
    mtext = "<font color=%s>%s</font>" % (color,text)
    st.markdown(mtext,unsafe_allow_html=True )

def details():
    #whitetext("*Details:*")
    whitetext("जवळजवळ 4000 शब्दांच्या यादीतून एक शब्द विनाक्रम निवडला जातो. त्याचा घाट (स्वराकार आणि\
        व्यंजनसंख्या) सांगितली जाते.")
    whitetext("उदाहरणार्थ: 'बछडा'चा स्वराकार अअआ आणि व्यंजनसंख्या १११.")
    whitetext("'अप्सरा'चे अअआ आणि ०२१.")
    whitetext("शब्द शोधतांता कोणत्याही घाटाचे चालतात. अनेकदा मुद्दाम जोडाक्षरे वापरल्याने फायदा होतो (प्र, त्र वगैरे).")
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
    whitetext("४. %s %s %s च्या सानिध्यात %s फसवा ठरू शकतो. उदाहरणार्थ: समजा गुप्त शब्द आहे कर्तव्य आणि तुमचा प्रयत्न आहे कातरी.\
         का आणि क अर्धवट जुळतात म्हणून का ला मिळतो  %s. त ला देखिल मिळतो %s \
        कारण तो र् + त् मधील त शी जुळतो. शेवटच्या री ला मात्र त्याच र्त मधील र ला जुळूनही %s मिळतो \
        कारण र्त ला आधीच एक गुण बहाल झाला आहे (%s)." % (imunicode['G'], imunicode['B'], imunicode['Y'], imunicode['R'],imunicode['B'], imunicode['B'], imunicode['R'], imunicode['B']))
    #      र् matching that in र्त because something has already matched the second position.")
    #whitetext("When trying words, you do not have to stick to the given shape.\
        # In fact, it would often be advantageous to try additional consonants, and perhaps\
        # also words with different स्वराकार. Since each letter has a vowel and between 0 and 3\
        # (rarely 4) consonants, the seemly 3-letter words are equivalent to an English range\
        # of about 5 to 8 (e.g. उखाणा expands to उ + ख् + आ + ण् + आ for a total of 5 while\
        # पर्याप्त is 8 with प् + अ + र् + य् + आ + प् + त् + अ). By giving the स्वराकार the requirement\
        # of guessing letters is reduced by 3.")

    #whitetext("Normally it should be possible to get to the answer in 4 to 6 steps.")
    # whitetext("*Details:*")
    # whitetext("The list of secret words is about 4000 long. A random one is\
    #     presented along with its shape: what vowels are in each letter, and\
    #     how many consonants are in each.")
    # whitetext("Thus, if the word is बछडा, the स्वराकार is अअआ and the\
    #     व्यंजनसंख्या is १११. अप्सरा has the same स्वराकार (अअआ) but the\
    #     व्यंजनसंख्या is ०२१.")
    # whitetext("When trying words, you do not have to stick to the given shape.\
    #     In fact, it would often be advantageous to try additional consonants, and perhaps\
    #     also words with different स्वराकार. Since each letter has a vowel and between 0 and 3\
    #     (rarely 4) consonants, the seemly 3-letter words are equivalent to an English range\
    #     of about 5 to 8 (e.g. उखाणा expands to उ + ख् + आ + ण् + आ for a total of 5 while\
    #     पर्याप्त is 8 with प् + अ + र् + य् + आ + प् + त् + अ). By giving the स्वराकार the requirement\
    #     of guessing letters is reduced by 3.")
    # whitetext("Another trick is to use more common consonants early, sometimes combined into\
    #     common conjuncts like प्र and त्र.")
    # whitetext("Normally it should be possible to get to the answer in 4 to 6 steps.")

def reveal():
    t2put = colortext('%s' % st.session_state['secret'],'white')
    st.components.v1.html(t2put,width=50,height=50)
    #whitetext('`%s`' % st.session_state['secret'])
    #st.markdown('`%s`' % st.session_state['secret'])

def newplay():
    st.markdown("Not yet implemented.\nReload for now.")
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
        if len(st.session_state['mylist'])>1: 
            for i in range(1,len(st.session_state['mylist'])):
                col1, col2, col3 = st.columns([10,10,20])
                with col1: 
                    forcol1 = ''
                    forcol1 = forcol1 + '\n' + ''.join([imunicode[st.session_state['mylist'][i][1][j]] for j in range(len(st.session_state['mylist'][i][1]))])
                    st.write("%8s %s %s" % (forcol1,"  ",st.session_state['mylist'][i][0]))
                if i == len(st.session_state['mylist'])-1:
                    with col2:
                        if st.session_state['mylist'][i][1] != 'G' * len(split_clusters(secret)):
                        #with col2:
                            blab = 'खुलासा %s' % mdigits[i]
                            bkey = 'खुलासा %s' % st.session_state['gcount']
                            if st.button(blab,key=bkey):
                                with modal.container():
                                    explain(st.session_state['mylist'][i][1])
                        else:
                        #with col2:
                            st.text('तुम्ही जिंकलात')
                            #st.text_input('','',key=st.session_state['gcount'],disabled=True,placeholder='तुम्ही जिंकलात')
            
        if onemore:
            col1, col2 = st.columns([20,10])
            with col1:
                #oldprompt = 'मराठी शब्द टाईप करा'
                #prompt = "गुपितातील स्वरक्रम `%s` अक्षरांगणीक व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape']))
                prompt = "स्वरक्रम `%s` व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape']))
                myc2 = st.text_input('','',key=st.session_state['gcount'],placeholder=prompt)
        else:
            if st.session_state['balloons'] == 1:
                st.balloons()
                st.session_state['balloons'] = 0
            col1, col2 = st.columns([12, 16])
            # with col1:
            #     myc2 = st.text_input('','',key=st.session_state['gcount'],disabled=True,placeholder='तुम्ही जिंकलात: '+st.session_state['mylist'][-1][0])
            modalstr = ''
            for i in range(1,len(st.session_state['mylist'])):
                modalstr = modalstr + ''.join([imunicode[k] for k in st.session_state['mylist'][i][1]]) + '\n'
            with col1:
                st.write("दवंडी पिटा")
                st.code("शब्दखूुळ\n#%d %s/∞\n\n%s" % (st.session_state['nthword'],get_mdigits(len(st.session_state['mylist'])-1),modalstr))

        #st.code("copy to clipboard")
            myc2 = ''

    if myc2.strip():
        ttclust = split_clusters(myc2.strip())
        #st.write(ttclust)
        goodstr=1
        goodstr = check_validity(ttclust)
        # for j in range(len(ttclust)):    
        #     for k in range(len(ttclust[j])): # eliminates non devnag
        #         # 0900 should go
        #         # 094E to 095F should go
        #         # 0964 to 0971 should go
        #         # 0973 to 097F should go
        #         # Allowed: 2305..2383; 2400..2403; 2412 (check)
        #         if ord(ttclust[j][k]) < 2304 or ord(ttclust[j][k]) > 2431:
        #             goodstr = 0
        #     for k in range(len(consonant_structure(myc2.strip()))): # eliminates clusters with > 4 consonants
        #         if consonant_structure(myc2.strip())[k] not in ['०','१','२','३','४']:
        #             goodstr = 0
        if len(ttclust) != len(split_clusters(secret)):
            goodstr = 0
        if goodstr == 1:
            myc2score = score(secret,myc2.strip())
            st.session_state['mylist'].append([myc2.strip(),myc2score,0])

        st.session_state['gcount'] += 1
        placeholder.empty()
        depth += 1
        #st.write(goodstr,st.session_state['gcount'],depth)
        if goodstr !=0 and myc2score == 'G' * len(split_clusters(secret)):
                #st.write("तुम्ही जिंकलात!")
                write2firebase(st.session_state['sessionid'],st.session_state['mylist'])
                getinput(secret,imunicode,0,depth)
        else:
            getinput(secret,imunicode,1,depth)

def write2firebase(sid,inlist):
    #db = firestore.Client.from_service_account_json("firestore-key.json")
    key_dict = json.loads(st.secrets["textkey"])
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
    if n in mdigits:
        return mdigits[n]
    else:
        return '>१०'

def explain(theScore):
    scoreCount = Counter(theScore)
    isare = {0:'are', 1:'is', 2:'are', 3:'are'}
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

    # if scoreCount['G']>0:
    #     blacktext("There %s %d %s indicating that %d letter(s) match exactly" % (isare[scoreCount['G']],scoreCount['G'],imunicode['G'],scoreCount['G']))
    # if scoreCount['B']>0:
    #     blacktext("There %s %d %s indicating that %d letter(s) match partially" % (isare[scoreCount['B']],scoreCount['B'],imunicode['B'],scoreCount['B']))
    # if scoreCount['Y']>0:
    #     blacktext("There %s %d %s indicating that %d letter(s) match elsewhere (partially or fully - barring those already accounted by %s and %s)" % (isare[scoreCount['Y']],scoreCount['Y'],imunicode['Y'],scoreCount['Y'],imunicode['G'],imunicode['B']))
    # if scoreCount['R']>0:
    #     blacktext("There %s %d %s indicating that %d letter(s) do not match even partially (this could exclude certain partial matches accounted for by %s and %s)" % (isare[scoreCount['R']],scoreCount['R'],imunicode['R'],scoreCount['R'],imunicode['B'],imunicode['Y']))

def copyright():
    #components.html("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """)
    #st.components.v1.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,height=20,width=300)
    whitetext("*Copyright 2022* (All rights reserved.)")
    whitetext("Developed by Ashish Mahabal using Python + Streamlit (and pinch of CSS)")
    whitetext("Code suggestions/help: [Jay, Abhijit] Mahabal")
    whitetext("The code is research style - meaning it has many hidden features,\
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
            return 0
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

    secret_wordfile = "subwordslen%d.dat" % n
    
    st.session_state['gcount'] = 1
    st.session_state['mylist'] = ['a'] # we ignore the zeroth later
    st.session_state['usedc'] = ['X'] # we ignore the zeroth later
    st.session_state['usedv'] = ['X'] # we ignore the zeroth later

    if 'secret' not in st.session_state:
        # idl1 = random.choice(string.ascii_uppercase)
        # idl2 = random.choice(string.ascii_uppercase)
        # idn1 = str("%0d" % random.randint(0,100000))
        # st.session_state['sessionid'] = idl1+idl2+idn1
        st.session_state['balloons'] = 1
        st.session_state['sessionid'] = uuid.uuid4().hex
        words = open(secret_wordfile,'r').read().split('\n')
        nthword = random.randrange(len(words))
        #secret = random.sample(words,1)[0]
        secret = words[nthword]
        st.session_state['nthword'] = nthword
        #st.write(secret,nthword)
        st.session_state['secret'] = secret
        st.session_state['rsshape'] = [vowel_revsub[int(i)] for i in vowel_structure(secret)]
        st.session_state['cshape'] = consonant_structure(secret)
    secret = st.session_state['secret']

    col2, col1 = st.columns(2)
    with col1:
        if st.button('?'):
            with modal.container():
                notes2()
    with col2:
    #st.markdown("शोधायच्या शब्दातील स्वरक्रम `%s` अक्षरांगणीक व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape'])))
        st.markdown("शोधा: स्वरक्रम `%s` व्यंजने `%s`" % (''.join(st.session_state['rsshape']),''.join(st.session_state['cshape'])))



    # secret = 'प्रकाश'
    # secret = 'लर्त्रण'
    # secret = 'प्रसाद'


## Trying modal. May replace tipa and tapashil with this.

    # copts = []
    # opts = st.columns(6)
    # #copts.append(opts[0].button('?'))
    # copts.append(opts[1].button('तपशील'))
    # copts.append(opts[2].button('Copyright'))

    # if copts[0]:
    #     with modal.container():
    #         notes2()

    # if copts[1]:
    #     with modal.container():
    #         details()

    # if copts[2]:
    #     with modal.container():
    #         copyright()
###############

    depth = 0
    getinput(secret,imunicode,1,depth)

    usedc = set(st.session_state['usedc'])
    usedv = set(st.session_state['usedv'])
    usedc.remove('X')
    usedv.remove('X')
    untriedc = set(consonents).difference(usedc)
    untriedv = set(vowels).difference(usedv)

    st.write("`वापरलेली` आणि न वापरलेली व्यंजने: ")
    uandunusedcl = ''
    for c in consonents:
        if c in untriedc:
            uandunusedcl += '%s ' % c
        else:
            uandunusedcl += '`%s` ' % c
# The following caused a bug when a letter was split across 30.
# Letting it naturally wrap.
    # st.markdown(uandunusedcl[:30])
    # st.markdown(uandunusedcl[30:])
    st.markdown(uandunusedcl)


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

    # with col3:
    #     if st.button('Copyright'):
    #         with modal.container():
    #             copyright()

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

#mainfunc(int(toDisplay))
#placeholder0 = st.empty()

#with placeholder0.container():
mainfunc(wlen)

