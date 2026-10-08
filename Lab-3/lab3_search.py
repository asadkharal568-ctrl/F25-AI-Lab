"""BFS, DFS, DLS, IDDFS and UCS on the lab's A-G graph."""
from collections import deque
import heapq
GRAPH={"A":["B","C"],"B":["D","E"],"C":["F"],"D":[],"E":["G"],"F":[],"G":[]}

def bfs(start,goal,graph=GRAPH):
    q=deque([(start,[start])]); seen={start}; order=[]; states=[]
    while q:
        node,path=q.popleft(); order.append(node)
        if node==goal: return path,order,states
        for nxt in graph.get(node,[]):
            if nxt not in seen:
                seen.add(nxt); q.append((nxt,path+[nxt]))
        states.append((node,[n for n,_ in q]))
    return None,order,states

def dfs(start,goal,graph=GRAPH):
    stack=[(start,[start])]; seen=set(); order=[]; states=[]
    while stack:
        node,path=stack.pop()
        if node in seen: continue
        seen.add(node); order.append(node)
        if node==goal: return path,order,states
        for nxt in reversed(graph.get(node,[])):
            if nxt not in seen: stack.append((nxt,path+[nxt]))
        states.append((node,[n for n,_ in reversed(stack)]))
    return None,order,states

def dls(start,goal,limit,graph=GRAPH):
    order=[]; cutoff=False
    def visit(node,path,depth):
        nonlocal cutoff
        order.append(node)
        if node==goal: return "FOUND",path
        if depth==limit:
            if graph.get(node,[]): cutoff=True
            return "CUTOFF" if graph.get(node,[]) else "FAILURE",None
        saw_cut=False
        for nxt in graph.get(node,[]):
            if nxt in path: continue
            status,result=visit(nxt,path+[nxt],depth+1)
            if status=="FOUND": return status,result
            if status=="CUTOFF": saw_cut=True
        return ("CUTOFF",None) if saw_cut else ("FAILURE",None)
    status,path=visit(start,[start],0)
    return status,path,order

def iddfs(start,goal,max_depth,graph=GRAPH):
    tries=[]
    for limit in range(max_depth+1):
        status,path,order=dls(start,goal,limit,graph); tries.append((limit,status,path,order))
        if status=="FOUND": return path,tries
        if status=="FAILURE": break
    return None,tries

WEIGHTED={"A":[("B",1),("C",2)],"B":[("D",2),("E",1)],"C":[("F",2),("G",10)],"D":[],"E":[("G",1)],"F":[],"G":[]}
def ucs(start,goal,graph=WEIGHTED):
    pq=[(0,start,[start])]; best={start:0}; order=[]
    while pq:
        cost,node,path=heapq.heappop(pq)
        if cost!=best.get(node): continue
        order.append(node)
        if node==goal: return path,cost,order
        for nxt,w in graph.get(node,[]):
            nc=cost+w
            if nc<best.get(nxt,float("inf")):
                best[nxt]=nc; heapq.heappush(pq,(nc,nxt,path+[nxt]))
    return None,float("inf"),order

def bfs_weighted_topology(start,goal,graph=WEIGHTED):
    """BFS minimizing hops on the same weighted topology (weights ignored)."""
    plain={u:[v for v,_ in edges] for u,edges in graph.items()}
    path,order,_=bfs(start,goal,plain)
    cost=sum(next(w for v,w in graph[u] if v==nxt) for u,nxt in zip(path,path[1:])) if path else float("inf")
    return path,cost,order

if __name__=="__main__":
    for algo,fn in (("BFS",bfs),("DFS",dfs)):
        p,o,_=fn("A","G"); print(algo,"path",p,"visit order",o)
    for lim in (1,2,3,4):
        s,p,o=dls("A","G",lim); print("DLS",lim,s,p,"order",o)
    for maximum in (1,2,3,4):
        p,tries=iddfs("A","G",maximum)
        print("IDDFS max",maximum,"attempts",[(l,s,path) for l,s,path,_ in tries],"result",p)
    bp,bc,bo=bfs_weighted_topology("A","G")
    print("BFS weighted topology",bp,"hops",len(bp)-1 if bp else None,"cost",bc,"processing",bo)
    path,cost,order=ucs("A","G")
    print("UCS weighted",path,"cost",cost,"processing",order,"independent sum",sum(next(w for n,w in WEIGHTED[u] if n==v) for u,v in zip(path,path[1:])))
    # Edge tests requested in manual
    print("start=goal",bfs("A","A")[0]); print("unreachable",bfs("A","Z")[0])
