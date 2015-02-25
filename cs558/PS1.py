__author__ = 'Isaac'


text = "THVVWCZTQ \
CZ WECQ YIAQQ LFN JCII IVAHZ WEV DCPPVHVZYV MVWJVVZ VZYHLOWCFZ AZD ANWEVZWCYAWCFZ \
WECQ RVQQATV CQ VZYHLOWVD JCWE A BVHL CZQVYNHV VZYHLOWCFZ QYEVRV CDVAIIL AZ \
VZYHLOWCFZ QYEVRV QEFNID AIIFJ FZIL ANWEFHCGVD OAHWCVQ JEF XZFJ WEV XVL WF HVAD \
WEV RVQQATV EFJVBVH LFN SNQW HVAD WEV RVQQATV JCWEFNW XZFJCZT WEV XVL EVZYV \
WEV VZYHLOWCFZ QYEVRV CQ CZQVYNHV "
wordlist = text.split(" ")

freq = {}

for word in wordlist:
    for letter in list(word):
        if letter in  freq:
            freq[letter] = freq[letter]+ 1
        else:
            freq[letter] = 1

import operator
sorted_x = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
print(sorted(freq))

total = ['E','T','A','O','I','N','S','R','H','L','D','C','M','F','P','G','W','Y','B','V','K','X','J','Q','Z']

print(freq)
print (sorted_x)
count =0
map={'A': 'A', 'B':'V', 'C': 'I','D':'D', 'E' :'H', 'F':'O', 'G':"Z", 'H': 'R','I': 'L', 'J':'W', 'K':'Q', 'L':'Y','M':'B', 'N':'U', 'O':'P', 'P':'F', 'Q':'S', 'R':'M','S':'J', 'T':'G', 'U':'T', 'V':'E', 'W':'T', 'X':'K', 'Y':'C', 'Z':'N' }

result =""

for word in wordlist:
    string =""
    for letter in list(word):
        string += map[letter]
    result += string + " "

print (result)



print(ord('A'.lower()) -96)

