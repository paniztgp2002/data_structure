def findmaxs(l) :
  #gets a list of numbers
  #exceptions ==> list with  :
  # 1) no item , 2) 1 item , 3) 2 items
  if len(l) == 0 :
          return None
  if len(l) == 1 :
    return l[0]
  if len(l) == 2 :
    if l[0] > l[1] :
    	return (l[0],l[1])
    else :
    	return (l[1],l[0])
    def max(low, high, seq):
     
     #low = list[0] , high = last index ==> (list[n])
        
        if low>=high:
            return seq[low],[]
        mid = low+(high-low)//2
        #________
        # x == first half largest item
        # a == list of items which are compared to x until now
        #________
        x,a = max(low, mid, seq)
        y,b = max(mid+1, high, seq)
        #_____
        # y == second half largest item
        # b  == list of items which compared to y until now
        #____
        if x>y:
            a.append(y)
            return x,a
        b.append(x)
        return y,b
        
     #_______
    # comp contains (largest item in the input list) and items which are compared to it
    comp = max(0,len(l)-1,l)
    #_______
    
    secmax = comp[1][0]
    #_______
    # this loop finds second largest item from the list of items which are compared to first largest item(comp)
    #complexity ==> log(n) 
    for i in comp[1]:
        if i>secmax:
            secmax = i
    return comp[0], secmax
  #______

#testing code ( YOU CAN GET AN INPUT INSTEAD)
print(findmaxs([3,9]))

