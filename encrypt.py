import base64 

s1 = base64.encodestring('nanofab') 
s2 = base64.decodestring(s1) 
print s1,s2
 