import pandas as pd
import streamlit as st

import random
import numpy as np
import os
import random
import json

import unicodedata

st.title('Marathi Wordle')
st.sidebar.title("Word Length")

toDisplay = st.sidebar.radio(
	"Options",
	["2", "3", "4"],
	index=1
)

wordlist = ['मयत','मकडी','माकड','मगर','मंकड','कमळ','करीम','किस्त्रीम','मंगळ','मालती']

consonents = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 
              'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 
              'य', 'र', 'ऱ', 'ल', 'ळ', 'व', 'श', 'ष', 'स', 'ह']
# Should map 'ऱ' to 'र'

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

def get_greens(secret_word, test_word):
    sclust = split_clusters(secret_word)
    tclust = split_clusters(test_word)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen
    
    greens = []
    for i in range(len(sclust)):
        if sclust[i] == tclust[i]:
            greens.append(i)
            
    return greens


def get_blues(secret_word, test_word):
    '''
    arguments provided with greens already removed
    indexing will have to be properly accounted for
    '''
    
    sclust = split_clusters(secret_word)
    tclust = split_clusters(test_word)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen
        
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

def get_blues2(secret_word, test_word):
    '''
    arguments provided with greens already removed
    indexing will have to be properly accounted for
    OR do it separately afterwards
    '''
    
    sclust = split_clusters(secret_word)
    tclust = split_clusters(test_word)
    if len(sclust)!=len(tclust):
        print("mismatched length")   # This should not happen
        
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
        if ytconsonents[i] != ['']: # skip pure vowels
            if j not in accountedc and (set(ytconsonents[i]) & set().union(*ysconsonents)):
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
            
    #print(ss)
    
    return ss
        
def score(secret,test):
    
    green_array = get_greens(secret,test)
    blue_array1,svowels, tvowels = get_blues(secret,test)
    blue_array2,sconsonents, tconsonents = get_blues2(secret,test)
    blue_comb = sorted(set(blue_array1) | set(blue_array2))

    ss = 'XXX' # should be word length
    ss = 'X' * len(split_clusters(secret))
    for s in blue_comb:
        ss = ss[:s] + 'B' + ss[s + 1:]
    for s in green_array:
        ss = ss[:s] + 'G' + ss[s + 1:]
    #print(ss, i)
    if ss.count('X') > 1:
        newss = test_for_yellows(ss,svowels,tvowels,sconsonents,tconsonents)
    else:
        newss = ss.replace('X','R')
        
    return newss

def twos():
    return

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
    st.write("Lots of features.")

def details():
    st.subheader("More details:")
    st.write("If the secret word is ...")

def reveal():
    st.subheader("The word is ... ")
    st.write(st.session_state['secret'])

def threes():

    # column_names = ["1", "2", "3"]
    # df = pd.DataFrame(columns = column_names)

    # secret = 'काळीज'
    # secret = wordlist[8]
    
    if 'secret' not in st.session_state:
        words = open('subthrees.dat','r').read().split('\n')
        secret = random.sample(words,1)[0]
        st.session_state['secret'] = secret
    secret = st.session_state['secret']
    #st.write(secret)

    copts = []
    opts = st.columns(4)
    copts.append(opts[0].checkbox('Notes',value='True'))
    copts.append(opts[1].checkbox('Todo'))
    copts.append(opts[2].checkbox('Details'))
    copts.append(opts[3].checkbox('Reveal'))

    #st.subheader("Notes:")
    if copts[0]:
        notes()
    if copts[1]:
        todos()
    if copts[2]:
        details()
    if copts[3]:
        reveal()
    #st.write("For the ... forms.")
    
    im = {'R':'mwred.png','G':'mwgreen.png','B':'mwblue.png','Y':'mwyellow.png'}

    corrects = 0
    for i in range(10):
        cols = st.columns(4)

        myc = cols[0].text_input('Guess %s' % str(i+1),'')

        if myc:
            foo = score(secret,myc.strip())
            # # The HTML rendering does not work properly
            # df = pd.DataFrame([[foo[i] for i in range(len(foo))]])
            # s = df.style.applymap(background_color)
            # cols[1].write(st.dataframe(s))
            for i in range(len(foo)):
                cols[i+1].image(im[foo[i]])
            #cols[1].write(foo)  # Original - works
            if foo == 'G' * len(split_clusters(secret)):
                st.write("you win")


def fours():
    return

def background_color(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    #color = 'red' if val == 'मा' else 'black'
    #is_max = s == s.max()

    if val == 'G':
        retcol = 'background-color: green'
    if val == 'B':
        retcol = 'background-color: blue'
    if val == 'Y':
        retcol = 'background-color: yellow'
    if val == 'R':
        retcol = 'background-color: red'

    return retcol

unsafe_allow_html=True
if toDisplay == "2":
    twos()
elif toDisplay == "3":
    threes()
elif toDisplay == "4":
    fours()


############################

# Some styling code from here: https://pandas.pydata.org/pandas-docs/version/0.25.1/user_guide/style.html


def color_wrong_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val == 'मा' else 'black'
    return 'color: %s' % color

# df = pd.DataFrame([['म्हा','ता','रा'],['मा','णू','स']])

# #s = df.style.applymap(color_wrong_red)
# s = df.style.applymap(background_color)
# #s
# st.dataframe(s)

