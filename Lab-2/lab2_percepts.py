"""Smart classroom target-mode agent; outputs are simulated, no hardware is controlled."""
class ClassroomAgent:
    def act(self,temp,occupied):
        if not occupied: return "ECO"
        if temp>26: return "COOL"
        if temp<20: return "WARM"
        return "IDLE"
if __name__=="__main__":
    agent=ClassroomAgent()
    for step,p in enumerate([(29,True),(29,True),(20,True),(26,True),(19,True),(29,False)],1):
        print(step,p,"target mode",agent.act(*p))
