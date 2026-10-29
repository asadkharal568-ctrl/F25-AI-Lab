class ClassroomAgent:
    def __init__(self):
        self.previous = None

    def act(self, temp, occupied):
        if not occupied:
            mode = "ECO"
        elif temp > 26:
            mode = "COOL"
        elif temp < 20:
            mode = "WARM"
        else:
            mode = "IDLE"
        send = mode != self.previous
        self.previous = mode
        return mode, send


print("Lab 2 - Stateful Classroom Agent Trace")
agent = ClassroomAgent()
for step, (temp, occupied, expected) in enumerate([
        (29, True, "COOL"),
        (29, True, "COOL"),
        (20, True, "IDLE"),
        (26, True, "IDLE"),
        (19, True, "WARM"),
        (29, False, "ECO")], 1):
    before = agent.previous
    mode, send = agent.act(temp, occupied)
    action = "Send command" if send else "No command"
    print(f"{step}. Before: {before} | Room: ({temp}, {occupied}) | Mode: {mode} | {action} | Correct: {mode == expected}")
