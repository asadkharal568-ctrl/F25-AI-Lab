"""A* and UCS controlled comparison with heuristic audit."""
import heapq
GRAPH={"S":[("A",1),("B",4)],"A":[("C",2)],"B":[("G",5)],"C":[("G",3)],"G":[]}
H={"S":5,"A":4,"B":4,"C":2,"G":0}
TRUE_REMAINING={"S":6,"A":5,"B":5,"C":3,"G":0}

def informed_search(h):
    pq=[(h["S"],0,"S",["S"])]; best={"S":0}; processed=[]; expanded=0; rows=[]
    while pq:
        f,g,node,path=heapq.heappop(pq)
        if g!=best.get(node): continue
        processed.append((node,g,h[node],f))
        if node=="G": return path,g,processed,expanded
        expanded+=1
        for nxt,w in GRAPH[node]:
            ng=g+w
            if ng<best.get(nxt,float("inf")):
                best[nxt]=ng; heapq.heappush(pq,(ng+h[nxt],ng,nxt,path+[nxt]))
    return None,float("inf"),processed,expanded

def edge_sum(path):
    return sum(next(w for n,w in GRAPH[u] if n==v) for u,v in zip(path,path[1:]))
if __name__=="__main__":
    print("Heuristic audit: node | h | true remaining | admissible")
    for n in H: print(n,H[n],TRUE_REMAINING[n],H[n]<=TRUE_REMAINING[n],sep=" | ")
    print("Consistency checks:")
    for u,edges in GRAPH.items():
        for v,w in edges: print(f"{u}->{v}: {H[u]} <= {w}+{H[v]} = {w+H[v]} : {H[u]<=w+H[v]}")
    for label,h in (("A* supplied",H),("UCS h=0",{n:0 for n in H}),("A* overestimate h(C)=10",{**H,"C":10})):
        p,c,trace,expanded=informed_search(h)
        print("\n"+label,"path",p,"cost",c,"independent sum",edge_sum(p),"expanded",expanded)
        print("processed (node,g,h,f):",trace)
