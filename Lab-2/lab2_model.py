"""Stateful classroom agent suppressing duplicate mode commands."""
class ClassroomAgent:
    def __init__(self): self.previous_mode=None
    def decide(self,temp,occupied):
        if not occupied: target="ECO"
        elif temp>26: target="COOL"
        elif temp<20: target="WARM"
        else: target="IDLE"
        send=target!=self.previous_mode
        previous=self.previous_mode
        self.previous_mode=target
        return previous,target,send

def run_trace():
    agent=ClassroomAgent()
    percepts=[(29,True),(29,True),(20,True),(26,True),(19,True),(29,False)]
    print("step | previous | percept | target | command")
    for i,p in enumerate(percepts,1):
        prev,target,send=agent.decide(*p)
        print(i,prev,p,target,"SEND" if send else "NO COMMAND",sep=" | ")
if __name__=="__main__": run_trace()
