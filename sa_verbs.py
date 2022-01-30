from logging import PlaceHolder
from numpy.lib.function_base import place
import streamlit as st
import random
import unicodedata
import string

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
          '।', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ',  'े', 'ै',  'ो', 'ौ']

vowel_subs = {'अ':1, 'आ':2, 'इ':3, 'ई':4, 'उ':5, 'ऊ':6, 'ऋ':11, 'ए':7, 'ऐ':8,  'ओ':9, 'औ':10, 
          '।':1, 'ा':2, 'ि':3, 'ी':4, 'ु':5, 'ू':6, 'ृ':11,  'े':7, 'ै':8,  'ो':9, 'ौ':10}

vowel_revsub = {1:'अ', 2:'आ', 3:'इ', 4:'ई', 5:'उ', 6:'ऊ', 11:'ऋ', 7:'ए', 8:'ऐ',  9:'ओ', 10:'औ'}

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
        
        #print(scomps,tcomps)
            
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
        # check for match अ needs to be handled differently as it does not appear as a separate vowel
        # List the possible unicode vovel endings as 0-12 (akar being 0 and rukar being 12)
        # Plus actual vowels
            
        found_consonent = 0
        for j in tcomps:
            if j in consonents:
                tblues2.append(j)
                found_consonent += 1
        tblues2.append(found_consonent)
        c_struc.append(str(len(tblues2)-1))
    
#    return list(set(blues))
    return c_struc

def get_blues(sclust, tclust):
    '''
    greens will overwrite any overlapping blues the way we call them.
    This is for vowels, so not used for the simpler version
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
                st.session_state['usedv'].append(j)
        if found_vowel == 0:
            tblues.append(1)
            st.session_state['usedv'].append('।')
    
    for i in range(len(sclust)):
        if sblues[i] == tblues[i]:
            blues.append(i)
    
#    return list(set(blues))
    return list(blues),sblues,tblues

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
                st.session_state['usedc'].append(j)
        if found_consonent == 0:
            tblues2.append('')
        suptblues2.append(tblues2)
    
        #print(sblues2,tblues2)
        if set(sblues2).intersection(set(tblues2)):
            blues2.append(i)
    
#    return list(set(blues))
    return list(blues2),supsblues2,suptblues2

def test_for_yellows(ss,svowels,tvowels,sconsonents,tconsonents):
    '''
    This is for the c and s version
    test_for_yellows_conly(ss,sconsonents,tconsonents) to be used for consonants
    '''
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
    #print(ss,svowels,tvowels,sconsonents,tconsonents)

    ysconsonents = []
    ytconsonents = []
    checklist = []
    for i in range(len(sconsonents)):
        if ss[i] == 'X':
            ysconsonents.append(sconsonents[i])
            ytconsonents.append(tconsonents[i])
            checklist.append(i)
        else:
            ysconsonents.append(['']) # changed this from 0 for set union to work
            ytconsonents.append(['']) # changed this from 0 for set union to work
            
    #print(ss,ysvowels,ytvowels,ysconsonents,ytconsonents)
    #print(checklist)
    
    ys = []
    accountedc = [] # this is for the consonants
    # for i in checklist:
    #     #print(i)
    #     for j in checklist:
    #         if j not in accountedv and ytvowels[i] == ysvowels[j]:
    #             ys.append(i)
    #             accountedv.append(j)
    #             #print("appending %d to ys due to vowel match" % i)
    #             break # Now that you have already matched, don't match others

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


def notes():
    st.subheader("Notes:")
    st.markdown("Enter a Marathi word of suggested length and hit tab or enter.")
    st.markdown("> The vowel shape indicates the vowels in the word e.g. अअआ could mean अकरा or बछडा etc.")
    st.markdown("> The consonant shape indicates number of consonants in each letter e.g. 012 indicates that\
        the first is a pure vowel, the second is a single consonant (with a vowel), and the\
        third is a two-consonant combo (with a vowel) e.g. अभद्र or आरक्त or अलिप्त.\
        ")
    st.markdown("Everything is modulo an anusvar meaning where the codes above suggest a म, it could be मं\
        and where it suggests अ it could be अं.")
    st.markdown("> - Green means that that letter is correct in all respects (position, consonant, and vowel.")
    st.markdown("> - Blue indicates that at least one consonant matches at that position\
         e.g. क for क्षे (=क्+शे), के for क्षे, प for पु, इ for ओ etc.")  
    st.markdown("> -  Yellow reveals that at least one consonant at that position matches one at another position.\
        ")
    st.markdown("> - Red suggests that that consonant may not match anything in the word. Blue and Yellow take\
        precedence over Red, so the following situation is possible: the secret word is\
        कर्तव्य and you have guessed कातरी. The का gives you a Blue because क matches, the त also gives\
        you a Blue because it matches the त in र् + त् and finally the री gives you a Red despite the \
        fact that the र् matches that in र्त because something has already matched the second position.")
    # st.write("Enter a Marathi word of suggested length and hit tab or enter. The words are\
    #     checked against a longer list of possible word (yet likely incomplete).")
    # st.write("Color code:")
    # st.write("Green means that letter is correct (position, consonant, and vowel)\
    #      e.g. क्षे for क्षे, स for स etc. If the secret is 'प्रकाश' and your guess is 'आकाश'\
    #      you will get greens for the second and third places.")
    # st.write("Blue means either consonant and vowel - or both - at that position match\
    #      e.g. क for क्षे (=क्+शे), के for क्षे, प for पु, इ for ओ etc. If the secret is 'भविष्य'\
    #      and your guess is 'भरीत', you will get a green for the first (full match)\
    #      and a blue for the last (the akar matches).")
    # st.write("Yellow means either consonant or vowel - or both - at that position matches\
    #      that of a letter in the code at another position\
    #      e.g. क for क्षे (=क्+शे), के for क्षे, प for पु, इ for ओ etc.\
    #      Blue takes precedence over yellow i.e. if you get a blue in one position because\
    #      of a partial match, you will not get a yellow for it no matter what. Thus if\
    #      the secret is 'भविष्य' and the guess is 'निर्भय', no greens because no perfect match,\
    #      then a blue for the third because they are both akar, and yellows for first and\
    #      second because ikar of नि matches that of वि and akar of र्भ matches that of भ.")
    # st.write("Red means neither consonant nor vowel is right at that position.\
    #      That is for all positions that are not green, blue, or red. ")
    st.write("When you get all Greens, you win.")
    st.write("More examples will be added under 'Details'.")

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

def getinput(words,secret,totcols,im,onemore):
    
    placeholder = st.empty()
    with placeholder.container():

        if len(st.session_state['mylist'])>1: 
            for i in range(1,len(st.session_state['mylist'])):
                cols = st.columns(totcols)
                cols[0].write(st.session_state['mylist'][i][0])
                for j in range(len(st.session_state['mylist'][i][1])):
                    cols[j+1].image(im[st.session_state['mylist'][i][1][j]],width=50)
        if onemore:
            myc2 = st.text_input('','',key=st.session_state['gcount'],placeholder='enter a Marathi word')
        else:
            myc2 = st.text_input('','',key=st.session_state['gcount'],disabled=True,placeholder='You win with: '+st.session_state['mylist'][-1][0])
            st.balloons()

    if myc2:
        #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
        if myc2 in words:
            #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
            logfile = open("logdir/userlog.txt", "a")
            myc2score = score(secret,myc2.strip())
            st.session_state['mylist'].append([myc2,myc2score])
            logfile.write("%s %s 1 %s\n" % (st.session_state['sessionid'],myc2,myc2score))
            logfile.close()
            # if myc2score == 'G' * len(split_clusters(secret)):
            #     st.write("you win")
        else: # For now allowing all words
            if len(split_clusters(myc2.strip())) == len(split_clusters(secret)):
                #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
                logfile = open("logdir/userlog.txt", "a")
                myc2score = score(secret,myc2.strip())
                st.session_state['mylist'].append([myc2,myc2score])
                logfile.write("%s %s 0 %s\n" % (st.session_state['sessionid'],myc2,myc2score))
                logfile.close()
        st.session_state['gcount'] += 1
        placeholder.empty()
        if myc2 in words and myc2score == 'G' * len(split_clusters(secret)):
                st.write("you win")
                getinput(words,secret,totcols,im,0)
        else:
            getinput(words,secret,totcols,im,1)


def mainfunc(n):

    totcols = n+1
    wordfile = "wordslen%d.dat" % n
    secret_wordfile = "subwordslen%d.dat" % n
    
    #if 'gcount' not in st.session_state:
    st.session_state['gcount'] = 1
    st.session_state['mylist'] = ['a'] # we ignore the zeroth later
    st.session_state['usedc'] = ['X'] # we ignore the zeroth later
    st.session_state['usedv'] = ['X'] # we ignore the zeroth later

    if 'secret' not in st.session_state:
        idl1 = random.choice(string.ascii_uppercase)
        idl2 = random.choice(string.ascii_uppercase)
        idn1 = str("%0d" % random.randint(0,100000))
        st.session_state['sessionid'] = idl1+idl2+idn1
        words = open(secret_wordfile,'r').read().split('\n')
        secret = random.sample(words,1)[0]
        words = open(wordfile,'r').read().split('\n') # all words now
        st.session_state['secret'] = secret
        st.session_state['words'] = words
    secret = st.session_state['secret']
    words = st.session_state['words']
    sshape = vowel_structure(secret)
    rsshape = []
    for i in sshape:
        rsshape.append(vowel_revsub[int(i)])
    st.markdown("Vowel shape for the word is ")
    st.markdown(''.join(rsshape))
    st.markdown("Consonants in each letter are ")
    cshape = consonant_structure(secret)
    # for i in cshape:
    #     c_struc = consonant_structure(secret)
    st.markdown(''.join(cshape))
    #st.markdown(c_struc)
    st.markdown(st.session_state['sessionid'])
    #secret = 'प्रकाश'

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

    getinput(words,secret,totcols,im,1)
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
usedc = set(st.session_state['usedc'])
usedv = set(st.session_state['usedv'])
usedc.remove('X')
usedv.remove('X')
untriedc = set(consonents).difference(usedc)
untriedv = set(vowels).difference(usedv)
# if '।' not in usedv:
#     untriedv.add('।')
st.write("Untried consonents: ")

unusedcl = []
for c in consonents:
    if c in untriedc:
        unusedcl.append(c)
st.markdown(unusedcl)

# unusedvl = []
# st.write("Untried vowels: ")
# for v in vowels:
#     if v in untriedv:
#         unusedvl.append(v)
# st.markdown(unusedvl)

usedcl = []
st.write("Tried consonents: ")
for c in consonents:
    if c in usedc:
        usedcl.append(c)
st.markdown(usedcl)

# usedvl = []
# st.write("Tried vowels: ")
# for v in vowels:
#     if v in usedv:
#         usedvl.append(v)
# st.markdown(usedvl)


# if 'mylist' not in st.session_state:
#     st.session_state['mylist'] = ['a'] 
#     st.session_state['count'] = 1



