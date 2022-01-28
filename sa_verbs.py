from logging import PlaceHolder
from numpy.lib.function_base import place
import streamlit as st
import random
import unicodedata

st.title('Marathi Wordle (length=3)')
#st.sidebar.title("Word Length")

# toDisplay = st.sidebar.radio(
# 	"Options",
# 	["2", "3", "4","5"],
# 	index=1
# )

wordlist = ['मयत','मकडी','माकड','मगर','मंकड','कमळ','करीम','किस्त्रीम','मंगळ','मालती']

consonents = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 
              'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 
              'य', 'र', 'ऱ', 'ल', 'ळ', 'व', 'श', 'ष', 'स', 'ह']
# Should map 'ऱ' to 'र' (todo)

vowels = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ',  'ओ', 'औ', 
          'ा', 'ि', 'ी', 'ु', 'ू', 'ृ',  'े', 'ै',  'ो', 'ौ']

vowel_subs = {'अ':1, 'आ':2, 'इ':3, 'ई':4, 'उ':5, 'ऊ':6, 'ऋ':11, 'ए':7, 'ऐ':8,  'ओ':9, 'औ':10, 
          'ा':2, 'ि':3, 'ी':4, 'ु':5, 'ू':6, 'ृ':11,  'े':7, 'ै':8,  'ो':9, 'ौ':10}

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


def get_blues(sclust, tclust):
    '''
    greens will overwrite any overlapping blues the way we call them.
    '''
    
    sblues = []
    tblues = []
    blues = []
    for i in range(len(sclust)):
        scomps = [j for j in sclust[i] if j != '्'] # remove halant signs
        tcomps = [j for j in tclust[i] if j != '्']
        # check for match अ needs to be handled differently as it does not appear as a separate vowel
        # List the possible unicode vovel endings as 0-12 (akar being 0 and rukar being 12)
        # Plus actual vowels
        
        #print(scomps,tcomps)
        found_vowel = 0
        for j in scomps:
            if j in vowels:
                sblues.append(vowel_subs[j])
                found_vowel += 1
        if found_vowel == 0:
            sblues.append(1)
            
        found_vowel = 0
        for j in tcomps:
            if j in vowels:
                tblues.append(vowel_subs[j])
                found_vowel += 1
        if found_vowel == 0:
            tblues.append(1)
    
    for i in range(len(sclust)):
        if sblues[i] == tblues[i]:
            blues.append(i)
    
#    return list(set(blues))
    return list(blues),sblues,tblues

def get_blues2(sclust, tclust):
    '''
    greens will overwrite any overlapping blues the way we call them.
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
                sblues2.append(j)
                found_consonent += 1
        if found_consonent == 0:
            sblues2.append('')
        supsblues2.append(sblues2)
            
        found_consonent = 0
        for j in tcomps:
            if j in consonents:
                tblues2.append(j)
                found_consonent += 1
        if found_consonent == 0:
            tblues2.append('')
        suptblues2.append(tblues2)
    
        #print(sblues2,tblues2)
        if set(sblues2).intersection(set(tblues2)):
            blues2.append(i)
    
#    return list(set(blues))
    return list(blues2),supsblues2,suptblues2

def test_for_yellows(ss,svowels,tvowels,sconsonents,tconsonents):
    #print(ss,svowels,tvowels,sconsonents,tconsonents)
    ysvowels = []
    ysconsonents = []
    ytvowels = []
    ytconsonents = []
    checklist = []
    for i in range(len(svowels)):
        if ss[i] == 'X':
            ysvowels.append(svowels[i])
            ysconsonents.append(sconsonents[i])
            ytvowels.append(tvowels[i])
            ytconsonents.append(tconsonents[i])
            checklist.append(i)
        else:
            ysvowels.append(0)
            ysconsonents.append(['']) # changed this from 0 for set union to work
            ytvowels.append(0)
            ytconsonents.append(['']) # changed this from 0 for set union to work
            
    #print(ss,ysvowels,ytvowels,ysconsonents,ytconsonents)
    #print(checklist)
    
    ys = []
    accountedv = [] # which of secret words letters already have a yellow
    accountedc = [] # this is for the consonants
    for i in checklist:
        #print(i)
        for j in checklist:
            if j not in accountedv and ytvowels[i] == ysvowels[j]:
                ys.append(i)
                accountedv.append(j)
                #print("appending %d to ys due to vowel match" % i)
                break # Now that you have already matched, don't match others

    for i in checklist:
        #print(i)
        for j in checklist:
            if ytconsonents[i] != ['']: # skip pure vowels
                if j not in accountedc and (set(ytconsonents[i]) & set().union(*ysconsonents)):
                    #print("found in union")
                    ys.append(i)
                    accountedc.append(i)
                    #print("appending %d to ys due to consonent match" % i)
    uniq_ys = set(ys)
    
    for i in checklist: # use word length here
        if i in uniq_ys:
            ss = ss[:i] + 'Y' + ss[i + 1:]
        else:
            ss = ss[:i] + 'R' + ss[i + 1:]
            
    #print(ss)
    
    return ss
        
def score(secret,test):
    '''
    Add B, G, Y, R in that order the the scoring string
    '''
    
    sclust = split_clusters(secret)
    tclust = split_clusters(test)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen

    green_array = get_greens(sclust,tclust)
    blue_array1,svowels, tvowels = get_blues(sclust,tclust)
    blue_array2,sconsonents, tconsonents = get_blues2(sclust,tclust)
    blue_comb = sorted(set(blue_array1) | set(blue_array2))

    ss = 'X' * len(sclust)
    for s in blue_comb:
        ss = ss[:s] + 'B' + ss[s + 1:]
    for s in green_array: # This overwrite the B's
        ss = ss[:s] + 'G' + ss[s + 1:]

    if ss.count('X') > 1: # No yellows if only one is X (==Red)
        newss = test_for_yellows(ss,svowels,tvowels,sconsonents,tconsonents)
    else:
        newss = ss.replace('X','R')
        
    return newss

def notes():
    st.subheader("Notes:")
    st.write("Choose word length on the left (only 3 RIGHT NOW).\
         Enter words with that length and hit tab. Advance to next fields yourself.\
         Minimal error checking exists for now.")
    st.write("Color code:")
    st.write("Green means that letter is correct (position, consonant, and vowel)")
    st.write("Blue means either consonant and vowel - or both - at that position match.")
    st.write("Yellow means either consonant or vowel - or both - at that position matches that of a letter in the code.")
    st.write("Red means neither consonant nor vowel is right at that position.")
    st.write("")

def todos():
    st.subheader("ToDos:")
    st.write("Add items to this list")
    st.write("Lots of features.")
    st.write("Should map 'ऱ' to 'र'")
    st.write("Compare input words against real words")
    st.write("Trim word list")
    st.write("Provide examples with markings")
    st.write("Counter changes when radio buttons clicked - avoid that")

def details():
    st.subheader("More details:")
    st.write("If the secret word is ...")

def reveal():
    st.subheader("The word is ... ")
    st.write(st.session_state['secret'])

def getinput(words,secret,totcols,im):
    
    placeholder = st.empty()
    with placeholder.container():

        if len(st.session_state['mylist'])>1: 
            for i in range(1,len(st.session_state['mylist'])):
                cols = st.columns(totcols)
                cols[0].write(st.session_state['mylist'][i][0])
                for j in range(len(st.session_state['mylist'][i][1])):
                    cols[j+1].image(im[st.session_state['mylist'][i][1][j]])
        myc2 = st.text_input('','',key=st.session_state['gcount'],placeholder='enter a Marathi word')

    if myc2:
        if myc2 in words:
            myc2score = score(secret,myc2.strip())
            st.session_state['mylist'].append([myc2,myc2score])
            if myc2score == 'G' * len(split_clusters(secret)):
                st.write("you win")

        st.session_state['gcount'] += 1
        placeholder.empty()
        getinput(words,secret,totcols,im)

def mainfunc(n):

    totcols = n+1
    wordfile = "wordslen%d.dat" % n
    
    #if 'gcount' not in st.session_state:
    st.session_state['gcount'] = 1
    st.session_state['mylist'] = ['a']

    if 'secret' not in st.session_state:
        words = open(wordfile,'r').read().split('\n')
        secret = random.sample(words,1)[0]
        st.session_state['secret'] = secret
        st.session_state['words'] = words
    secret = st.session_state['secret']
    words = st.session_state['words']

    copts = []
    opts = st.columns(4)
    
    #     copts.append(opts[1].checkbox('Reveal'))
    #     copts.append(opts[2].checkbox('Notes'))
    # else:
    
    copts.append(opts[0].checkbox('Notes'))
    copts.append(opts[1].checkbox('Todo'))
    copts.append(opts[2].checkbox('Details'))
    copts.append(opts[3].checkbox('Reveal'))
    

    if copts[0]:
        notes()
    if copts[1]:
        todos()
    if copts[2]:
        details()
    if copts[3]:
        reveal()
    
    
        

    im = {'R':'mwred.png','G':'mwgreen.png','B':'mwblue.png','Y':'mwyellow.png'}
    #cols = st.columns(totcols)

    getinput(words,secret,totcols,im)
    # st.write("test")
    # if st.button('New (not yet)'):
        
    #     st.session_state['gcount'] = 1
    #     st.session_state['mylist'] = ['a']
    #     secret = random.sample(words,1)[0]
    #     st.session_state['secret'] = secret
    #     placeholder.empty()
    #     getinput(words,secret,totcols,im)

#mainfunc(int(toDisplay))
mainfunc(3)


# if 'mylist' not in st.session_state:
#     st.session_state['mylist'] = ['a'] 
#     st.session_state['count'] = 1



