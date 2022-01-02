# hash table
# immutable dict 생성
# 지능형 Set
# Set 선언 최적화

# immutable dict
from types import MappingProxyType # 읽기전용 dictionary만들 수 있음

d = {'key1' : 'value1'}

# Read only
d_frozen = MappingProxyType(d)
print(d, id(d)) # {'key1': 'value1'} 140582107766656
print(d_frozen, id(d_frozen)) # {'key1': 'value1'} 140582107655472

# 수정
# d_frozen['key2'] = 'value2' # TypeError: 'mappingproxy' object does not support item assignment

# Set 선언
s1 = {} # <class 'dict'>
s2 = set() # <class 'set'>

s3 = {'Apple', 'Orange', 'Kiwi'}
s4 = frozenset({'Apple', 'Orange', 'Kiwi'})

s3.add('Melon')
# s4.add('Melon') # AttributeError: 'frozenset' object has no attribute 'add'

print()
print()

# 선언 최적화
# 바이트코드 -> 파이썬 인터프리터 실행

from dis import dis

print(dis('{10}'))
'''
1           0 LOAD_CONST               0 (10)
            2 BUILD_SET                1
            4 RETURN_VALUE
None
'''
print('--------------------')
print(dis('set([10])'))
'''
1           0 LOAD_NAME                0 (set)
            2 LOAD_CONST               0 (10)
            4 BUILD_LIST               1
            6 CALL_FUNCTION            1
            8 RETURN_VALUE
None
'''

# Conprehending set
from unicodedata import name

print({name(chr(i), '') for i in range(0, 256)}) # {'', 'LATIN CAPITAL LETTER Q',...
# 없는 값은 ''로 표시