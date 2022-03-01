import random


for i in range(10):
    print(f'{random.choice([-1, 1])}, ', end='')

# print(*[x for x in dir(random) if x[0] != '_'])
# help('randint')