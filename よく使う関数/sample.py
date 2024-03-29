N , M = map(int,input().split())
graph = [[] for _ in range(N)]
ans = [0] * N
visited = [False] * N

# グラフの受け取り
for _ in range(M):
    i, j = map(int,input().split())
    graph[i - 1].append(j)
    graph[j - 1].append(i)


# 深さ優先探索
def DFS(i):
    visited[i] = True
    for j in graph[i]:
        if visited[j - 1] == True:
            ans[j - 1] += 1
            continue
        DFS(j - 1)

# 鉄則本のDFS
# 深さ優先探索を行う関数（pos は現在位置、visited[x] は頂点 x が青色かどうかを表す真偽値）
def dfs(pos, G, visited):
    visited[pos] = True
    for i in G[pos]:
        if visited[i] == False:
            dfs(i, G, visited)

# Union Find経路圧縮あり、要素数指定なし(メインはこっちでいい気がする)
import collections
class UnionFind():
    def __init__(self):
        # unionfind経路圧縮あり,要素にtupleや文字列可,始めに要素数指定なし
        self.parents = dict()                                      # {子要素:親ID,}
        self.members_set = collections.defaultdict(lambda : set()) # keyが根でvalueが根に属する要素要素(tupleや文字列可)
        self.roots_set = set()                                     # 根の集合(tupleや文字列可)
        self.key_ID = dict()                                       # 各要素にIDを割り振る
        self.ID_key = dict()                                       # IDから要素名を復元する
        self.cnt = 0                                               # IDのカウンター

    def dictf(self,x): # 要素名とIDをやり取りするところ
        if x in self.key_ID:
            return self.key_ID[x]
        else:
            self.cnt += 1
            self.key_ID[x] = self.cnt
            self.parents[x] = self.cnt
            self.ID_key[self.cnt] = x
            self.members_set[x].add(x)
            self.roots_set.add(x)
            return self.key_ID[x]
 
    def find(self, x):
        ID_x = self.dictf(x)
        if self.parents[x] == ID_x:
            return x
        else:
            self.parents[x] = self.key_ID[self.find(self.ID_key[self.parents[x]])]
            return self.ID_key[self.parents[x]]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        if x == y:
            return
        for i in self.members_set[y]:
            self.members_set[x].add(i)
        self.members_set[y] = set()
        self.roots_set.remove(y)
        self.parents[y] = self.key_ID[x]

    def size(self, x):#xが含まれる集合の要素数
        return len(self.members_set[self.find(x)])

    def same(self, x, y):#同じ集合に属するかの判定
        return self.find(x) == self.find(y)

    def members(self, x):#xを含む集合の要素
        return self.members_set[self.find(x)]

    def roots(self):#根の要素
        return self.roots_set

    def group_count(self):#根の数
        return len(self.roots_set)

    def all_group_members(self):#根とその要素
        return {r: self.members_set[r] for r in self.roots_set}

# Union-Find 木
class unionfind:
    # n 頂点の Union-Find 木を作成
    # （ここでは頂点番号が 1-indexed になるように実装しているが、0-indexed の場合は par, size のサイズは n でよい）
    def __init__(self, n):
        self.n = n
        self.par = [ -1 ] * (n + 1) # 最初は親が無い
        self.size = [ 1 ] * (n + 1) # 最初はグループの頂点数が 1
        
    # 頂点 x の根を返す関数
    def root(self, x):
        # 1 個先（親）がなくなる（つまり根に到達する）まで、1 個先（親）に進み続ける
        while self.par[x] != -1:
            x = self.par[x]
        return x
        
    # 要素 u, v を統合する関数
    def unite(self, u, v):
        rootu = self.root(u)
        rootv = self.root(v)
        if rootu != rootv:
            # u と v が異なるグループのときのみ処理を行う
            if self.size[rootu] < self.size[rootv]:
                self.par[rootu] = rootv
                self.size[rootv] += self.size[rootu]
            else:
                self.par[rootv] = rootu
                self.size[rootu] += self.size[rootv]
                
    def members(self, x):
        roots = self.root(x)
        return [i for i in range(self.n) if self.root(i) == roots]
    #  要素 u と v が同一のグループかどうかを返す関数
    def same(self, u, v):
        return self.root(u) == self.root(v)

# エラトステネスのふるい(nが素数か判定)
# O(NloglogN)
def eratosthenes_sieve(n):
    is_prime = [True]*(n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, n + 1):
        if is_prime[p]:
            for q in range(2*p, n + 1, p):
                is_prime[q] = False
    return is_prime

# エラトステネスのふるい(x以下の素数列挙)
def sieve_of_eratosthenes(x):
    nums = [i for i in range(x+1)]
    root = int(pow(x,0.5))
    for i in range(2,root + 1):
        if nums[i] != 0:
            for j in range(i, x+1):
                if i*j >= x+1:
                    break
                nums[i*j] = 0
    primes = sorted(list(set(nums)))[2:]
    return primes

# 10進数をn進数に変換する関数
def Base_10_to_n(X, n):
    if X//n:
        return Base_10_to_n(X//n, n)+str(X % n)
    return str(X % n)

# a の b 乗を m で割った余りを返す関数(for文の30は条件によって変更する必要あり)
def Power(a, b, m):
	p = a
	Answer = 1
	for i in range(30):
		wari = 2 ** i
		if (b // wari) % 2 == 1:
			Answer = (Answer * p) % m # a の 2^i 乗が掛けられるとき
		p = (p * p) % m
	return Answer

# 幅優先探索(鉄則本A63)
import sys
from collections import deque
sys.setrecursionlimit(100000)
N , M = map(int,input().split())
# グラフ受け取り変数(1オリジン)
graph = [[] for _ in range(N+1)]
# -1で初期化
dist = [-1] * (N+1)
dist[1] = 0
Q = deque()
Q.append(1)

# グラフの受け取り(1オリジン受け取り)
for _ in range(M):
    i, j = map(int,input().split())
    graph[i].append(j)
    graph[j].append(i)

while len(Q) >= 1:
# 初めは1(スタート地点)
    pos = Q.popleft()
# スタート地点と連結している場所1つ1つに対してfor文を行う
    for i in graph[pos]:
# distに既に値が入ってた場合、-1以外が入っている。dist = -1を満たさない場合は上書きしてしまうから実行しない。
        if dist[i] == -1:
            dist[i] = dist[pos] + 1
            Q.append(i)
for i in range(1,N+1):
    print(dist[i])

# 長さNでnum番目の順列を求める
from collections import deque
def Permutation_N(N,num):
    remain_deque = deque()
    serial_num = list(range(1,N+1))
    ans = []
    for i in range(1,N+1):
        remain = num % i
        num = num // i
        remain_deque.appendleft(remain)
    for j in range(N):
        ind = remain_deque.popleft()
        ans.append(serial_num[ind])
        serial_num.pop(ind)
    return ans

# 順列が辞書順に何番目か調べる関数
from math import factorial #x!を計算
def index_of_permutation(L):
    index = 0  #0-indexed
    while len(L)> 1:
        a = len([l for l in L if l<L[0]])
        index = index + a * factorial(len(L) - 1)
        L = L[1:]
    return index

# ランレングス圧縮
def rle(s):
    n = len(s) #文字列の長さ
    ans = [] #圧縮後のリスト
    l = 0 #始点
    while l<n:
        r = l+1
        while r<n and s[l]==s[r]: #異なる文字になるまで進む
            r += 1
        ans.append((s[l], r-l)) #文字,連続する個数
        l = r #連続しなかった文字から探索を開始
    return ans
