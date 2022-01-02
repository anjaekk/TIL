# hash table
# Dict Advanced
# Setdefault

# 해시테이블(hash table): key에 value 저장
# key값을 해싱 함수 -> 해쉬 주소 -> key에 대한 value 참조


t1 = (10, 20, (30, 40, 50))
t2 = (10, 20, [30, 40, 50])

print(hash(t1)) # 465510690262297113
# print(hash(t2)) # TypeError: unhashable type: 'list'

# Dict Setdefault
# key 중복 source
source =(('k1', 'val1'), 
        ('k1', 'val2'),
        ('k2', 'val3'),
        ('k2', 'val4'),
        ('k2', 'val5'))

new_dict1 = {}
new_dict2 = {}

# No user Setdefault
for k, v in source:
    if k in new_dict1:
        new_dict1[k].append(v)
    else:
        new_dict1[k] = [v]
print(new_dict1) # {'k1': ['val1', 'val2'], 'k2': ['val3', 'val4', 'val5']}


# Use Setdefault
for k, v in source:
    new_dict2.setdefault(k, []).append(v)
print(new_dict2) # {'k1': ['val1', 'val2'], 'k2': ['val3', 'val4', 'val5']}

# 주의
new_dict3 = {k: v for k, v in source}
print(new_dict3) # {'k1': 'val2', 'k2': 'val5'}