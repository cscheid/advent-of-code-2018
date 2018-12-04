d = { 0: 1 }
current = 0
found = False
while not found:
    print("loop.")
    for v in l:
        current += v
        d[current] = d.get(current, 0) + 1
        if d[current] == 2:
            print("Found! %s" % current)
            found = True
            break
    
        
    
