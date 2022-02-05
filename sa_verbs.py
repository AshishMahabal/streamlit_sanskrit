from logging import PlaceHolder
from numpy.lib.function_base import place
import streamlit as st
import random
import unicodedata
import string
import streamlit_modal as modal
import streamlit.components.v1 as components

st.title('शब्दखुूळ (तिनाक्षरी)')
#st.sidebar.title("Word Length")

# toDisplay = st.sidebar.radio(
# 	"Options",
# 	["2", "3", "4","5"],
# 	index=1
# )

# Globals
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
mdigits = {0:'०',1:'१',2:'२',3:'३',4:'४',5:'५',6:'६',7:'७',8:'८',9:'९',10:'१०'}
imunicode = {'R':'🟥','G':'🟩','B':'🟦','Y':'🟨'}



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
    
    ys = []
    accountedc = [] # this is for the consonants

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
    
    return ss

# def cnote(imname,imwidth,textdes):
#     col1, col2 = st.columns([1,20])
#     with col1:
#         st.markdown(imname)
#     with col2:
#         st.markdown(textdes)

# The following few functions are for the checkboxes
def notes():
    st.subheader("Notes:")
    st.markdown("Enter a Marathi word of suggested length and hit tab or enter.")
    st.markdown("> The vowel shape indicates the vowels in the word e.g. `अअआ` could mean `अकरा` or `बछडा` etc.")
    st.markdown("> The consonant shape indicates number of consonants in each letter e.g. 012 indicates that\
        the first is a pure vowel, the second is a single consonant (with a vowel), and the\
        third is a two-consonant combo (with a vowel) e.g. `अभद्र` or `आरक्त` or `अलिप्त`.\
        Please note that `क्ष (= क् + ष)` and `ज्ञ (= ज् + ञ)` are both conjuncts of size 2.")
    st.markdown("> Everything is modulo an anusvar meaning where the codes above suggest a `म`, it could be `मं`\
        and where it suggests `अ` it could be `अं`.")
    st.markdown("> Visargas `:`, ardha-chandra `ॅ` and `ॉ`, chandra-bindu `ॅं` do not appear in\
         the secret words, nor are they halant (ending in `्`).")
    st.markdown("%s Green means that that letter is correct in all respects (position, consonant, and vowel." % imunicode['G'])
    st.markdown("%s Blue indicates that at least one consonant matches at that position\
         e.g. `क` for `क्षे (=क्+षे)`, `के` for `क्षे`, `प` for `पु`, `इ` for `ओ` etc." %imunicode['B'])
    st.markdown("%s Yellow reveals that at least one consonant at that position matches one at another position." % imunicode['Y'])
    st.markdown("%s Red suggests that that consonant may not match anything in the word. Blue and Yellow take\
        precedence over Red, so the following situation is possible: the secret word is\
        `कर्तव्य` and you have guessed `कातरी`. The `का` gives you a Blue because `क` matches, the `त` also gives\
        you a Blue because it matches the `त` in `र् + त्` and finally the `री` gives you a Red despite the \
        fact that the `र्` matches that in `र्त` because something has already matched the second position." % imunicode['R'])
    st.write("> When you get all Greens, you win.")
    st.write("More examples will be added under 'Details'.")

def todos():
    st.subheader("ToDos:")
    st.markdown("- Add items to this list")
    st.markdown("- Lots of features.")
    st.markdown("- Should map 'ऱ' to 'र'")
    st.markdown("- Compare input words against real words")
    st.markdown("- Trim word list")
    st.markdown("- Provide examples with markings")
    st.markdown("- ~~Counter changes when radio buttons clicked - avoid that~~")

def details():
    st.subheader("More details:")
    st.write("If the secret word is ...")

def reveal():
    st.subheader("The word is ... ")
    st.markdown('`%s`' % st.session_state['secret'])


def getinput(words,secret,totcols,imunicode,onemore,depth):
    '''
    This is the main function getting input and managing flow
    Has recursion
    '''
    
    
    placeholder = st.empty()
    with placeholder.container():

        if len(st.session_state['mylist'])>1: 
            for i in range(1,len(st.session_state['mylist'])):
                #cols = st.columns(totcols)
                # cols[0].write(st.session_state['mylist'][i][0])
                forcol1 = ''
                forcol1 = forcol1 + ''.join([st.session_state['mylist'][i][1][j] for j in range(len(st.session_state['mylist'][i][1]))])
                forcol1 = forcol1 + '\n' + ''.join([imunicode[st.session_state['mylist'][i][1][j]] for j in range(len(st.session_state['mylist'][i][1]))])
                #with cols[0]:
                st.write("%8s %s %s" % (forcol1,"  ",st.session_state['mylist'][i][0]))
                # with cols[1]:
                #     st.markdown(forcol1)
                # for j in range(len(st.session_state['mylist'][i][1])):
                #     #cols[j+1].image(im[st.session_state['mylist'][i][1][j]],width=50)
                #     tcolor = st.session_state['mylist'][i][1][j]
                #     with cols[j+1]:
                #         st.markdown("%s%s" % (imunicode[tcolor],tcolor))
        if onemore:
            col1, col2, col3 = st.columns([10,10,10])
            with col1:
        #st.image(imname, width=imwidth)
                myc2 = st.text_input('','',key=st.session_state['gcount'],placeholder='मराठी शब्द टाईप करा')
        else:
            st.balloons()
            col1, mid, col2 = st.columns([8,1,4])
            with col1:
                myc2 = st.text_input('','',key=st.session_state['gcount'],disabled=True,placeholder='तुम्ही जिंकलात: '+st.session_state['mylist'][-1][0])
            modalstr = ''
            # modal.open()
            # if modal.is_open():
            #     with modal.container():
            # with col2:
            #     st.write("Share")
            for i in range(1,len(st.session_state['mylist'])):
                modalstr = modalstr + ''.join([imunicode[k] for k in st.session_state['mylist'][i][1]]) + '\n'
            with col1:
                st.write("दवंडी पिटा")
                st.code("शब्दखूुळ\n%s %s/∞\n\n%s" % (secret,get_mdigits(len(st.session_state['mylist'])-1),modalstr))

        #st.code("copy to clipboard")
            myc2 = ''

    if myc2:
        #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
        if myc2 in words:
            #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
            #logfile = open("logdir/userlog.txt", "a")
            myc2score = score(secret,myc2.strip())
            st.session_state['mylist'].append([myc2,myc2score])
            # logfile.write("%s %s 1 %s %d %d\n" % (st.session_state['sessionid'],myc2,myc2score,len(st.session_state['mylist']),depth))
            # logfile.close()
            # if myc2score == 'G' * len(split_clusters(secret)):
            #     st.write("you win")
        else: # For now allowing all words
            ttclust = split_clusters(myc2.strip())
            goodstr=1
            for j in range(len(ttclust)):
                for k in range(len(ttclust[j])):
                    if ord(ttclust[j][k]) < 2304 or ord(ttclust[j][k]) > 2431:
                        goodstr = 0
            if len(ttclust) == len(split_clusters(secret)) and goodstr == 1:
                #logfile = open("logdir/"+st.session_state['sessionid']+".txt", "a")
                #logfile = open("logdir/userlog.txt", "a")
                myc2score = score(secret,myc2.strip())
                st.session_state['mylist'].append([myc2,myc2score])
                # logfile.write("%s %s 0 %s %d %d\n" % (st.session_state['sessionid'],myc2,myc2score,len(st.session_state['mylist']),depth))
                # logfile.close()
        st.session_state['gcount'] += 1
        placeholder.empty()
        depth += 1
        if myc2 in words and myc2score == 'G' * len(split_clusters(secret)):
                st.write("तुम्ही जिंकलात")
                logfile = open("logdir/userlog.txt", "a")
                for m in range(1,len(st.session_state['mylist'])):
                    logfile.write("%s %s 0 %s %d %d\n" % (st.session_state['sessionid'],st.session_state['mylist'][m][0],st.session_state['mylist'][m][1],len(st.session_state['mylist']),99))
                logfile.close()
                getinput(words,secret,totcols,imunicode,0,depth)
        else:
            getinput(words,secret,totcols,imunicode,1,depth)

def get_mdigits(n):
    if n in mdigits:
        return mdigits[n]
    else:
        return '>१०'

def mainfunc(n):
    '''
    Wrapper function
    '''

    #totcols = n+1
    # totcols = [3]
    # for i in range(n):
    #     totcols.append(1)
    # totcols.append(6)
    totcols = [4,7,20]
    wordfile = "wordslen%d.dat" % n
    secret_wordfile = "subwordslen%d.dat" % n
    
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
    
    cshape = consonant_structure(secret)
    st.markdown("शोधायच्या शब्दातील स्वरक्रम `%s` अक्षरांगणीक व्यंजने `%s`" % (''.join(rsshape),''.join(cshape)))
    #str1 = "शब्दातील व्यंजनांची संख्या - अक्षरांगणीक: `%s` (0: शुद्ध स्वर, 1: क..ह, 2: प्र त्र क्ष ज्ञ ष्ट, 3: ष्ट्य,त्त्व,..)" % ''.join(cshape)
    #st.markdown(str1)

    # secret = 'प्रकाश'
    # secret = 'लर्त्रण'

    copts = []
    opts = st.columns([4,4,4,12])
    copts.append(opts[0].checkbox('टिपा'))
    copts.append(opts[1].checkbox('तपशील'))
    copts.append(opts[2].checkbox('उत्तर'))
    #copts.append(opts[3].checkbox('बाकी'))

    # if st.checkbox('टिपा'):
    #     notes()
    # if st.checkbox('तपशील'):
    #     details()
    # if st.checkbox('उत्तर'):
    #     reveal()
    

    if copts[0]:
        notes()
    if copts[1]:
        details()
    if copts[2]:
        reveal()
    # if copts[3]:
    #     todos()

    depth = 0
    getinput(words,secret,totcols,imunicode,1,depth)

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
    st.markdown(uandunusedcl)

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
mainfunc(3)