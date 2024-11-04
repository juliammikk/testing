

def GCD(m,n):
    if n==0:
        return m  #includes case where both m and n are 0 (will return 0)
#    if m%n==0:
#       return n  #included in the recursive call because if that mod is zero it will be caught in if stat.
    return GCD(n, m%n)



def expmod1(a,n,m):
    return a**n%m

def expmod2(a,n,m):
    x=1
    for i in range(n):
        x = x * a % m
    return x

def expmod3(a,n,m):
     if n==0:
        return 1
     else:
         d=expmod3(a,n//2,m)
         if n%2==0:
             return d*d%m
         else:
             return d*d*a%m

print("I love you so much <3")

def probableprime(n):
    while True:
        if expmod3(2, n-1, n) == 1:
            return n
        n+=1




def insertSort(a, before):
    for i in range(1,len(a)):
        x = a[i]
        j=i-1
        while j>=0 and a[j]>x:
            a[j+1]=a[j]
            j-=1
        a[j+1]=x
    return a

def merge(b,c,before):
    x = len(b)+len(c)
    d = [None]*x
    i=j=0
    for k in range(0,x):
        if i == len(b):
           d[k]=c[j]
           j+=1
        elif j == len(c):
            d[k]=b[i]
            i+=1
        elif before(b[i],c[j]):
            d[k]=b[i]
            i+=1
        else:
            d[k]=c[j]
            j+=1
    return d


def mergeSort(A,m,n):
    if n-m==1:
        return [A[m]]
    else:
        p= (m+n)//2
        B=mergeSort(A,m,p)
        C=mergeSort(A,p,n)
        return merge(B,C,beforeInt)

def mergeSortAll(a):
    return mergeSort(a,0,len(a))

def beforeInt(a,b):
    if a<=b:
        return True
    return False




print(mergeSortAll([3,6,4,8]))


