import math
ans = 0.0; 

for i in range(1,1001):
    ans += 1000/i;

print("total expected calls: ", ans, " so total time: ", ans/100); 
