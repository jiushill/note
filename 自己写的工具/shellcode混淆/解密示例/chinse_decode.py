import binascii
import base64
import string
data=open("test.txt",'r',encoding='utf-8').read()
payload = ['王', '神', '乱', '邪', '舒', '屈', '死', '暗', '乱', '魔', '刃', '寂', '亡', '希', '圣', '善', '何', '安', '圻', '欣', '饕', '餮',
           '早', '奴', '隶', '缰', '剑', '口', '屠', '戮', '斩', '光', '明', '佐', '助', '鸣', '人', '囚', '徒', '自', '暗', '裔', '杀', '总',
           '终', '源', '狱', '地', '轨', '鬼', '核', '抛']
pd = {}
zmu = string.ascii_letters
for u in range(0, len(zmu)):
    pd[zmu[u]] = payload[u]
pd['='] = '卍'
pd['0'] = '~'
pd['1'] = '!'
pd['2'] = '@'
pd['3'] = '#'
pd['4'] = '$'
pd['5'] = '%'
pd['6'] = '^'
pd['7'] = '&'
pd['8'] = '*'
pd['9'] = '('
pd['0'] = ')'

j=""
w=""

print(pd)
for v in data:
    if v in pd.values():
        j+=str(list(pd.keys())[list(pd.values()).index('{}'.format(v))]).replace('h','O')

d=bytes.decode(base64.b64decode(j))
print(bytes.decode(binascii.unhexlify(d),encoding='utf-8'))