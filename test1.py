n = int(input())
t = int(input())
s = 0
r = t

for _ in range(n):
    a, b = map(int, input().split())
    s += a
    r = min(s + t, r + b)

print(r)