def my_generator(start=0, step=1):
  x = start
  while True:
    yield x
    x += step
    # print(f"Yielded {i}")

result = my_generator()

print(next(result)) # 1
print(next(result)) # 2
print(next(result)) # 3

# print(list(result))
print(my_generator())
