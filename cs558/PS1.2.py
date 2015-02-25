__author__ = 'Isaac'

cyphertext = "Z LUNI R HLWED XBSX FRY VEP XBAW EENASE ACDP IMMW YG EHV PZZY GYK XBW XIYY EIRRCFK FJ CLW TVYWH: NI BGPU XBWWV XLMXYW NG FV WYDJ VZCVIEX NZEK EFD QVR UJI TVYSXVH YIYRP GDO"

def changeLetter(cypher,key):
    numkey = ord(key.upper()) -65
    return chr( ( (ord(cypher.upper()) - 65 -numkey ) % 26) + 65 )

count =0
list1={}
list2={}
list3={}
list4={}
list5={}

punc = [':', ' ', ',' , '.', '"', '-']
plainText=''
for letter in list(cyphertext):
    if letter not in punc:
        if count % 5 is 0:
            plainText += changeLetter(letter, 'R')
        elif count % 5 is 1:
            plainText += changeLetter(letter, 'E')
        elif count % 5 is 2:
            plainText += changeLetter(letter, 'U')
        elif count % 5 is 3:
            plainText += changeLetter(letter, 'S')
        elif count % 5 is 4:
            plainText += changeLetter(letter, 'E')
        count+=1
    else:
        plainText += letter



print(plainText)

cyphertext = 'ZPINIGMTRE'
key = "REUSE"
def decrypt(cyphertext, key):
    plainText =""
    count=0
    key = list(key)
    for letter in list(cyphertext):
        plainText += changeLetter(letter,key[count])
        count = (count +1) % len(key)
    return plainText
print(decrypt(cyphertext,key))