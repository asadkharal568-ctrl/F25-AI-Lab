"""Transparent rule checker: all thresholds are synthetic lab assumptions."""
THRESHOLD=70
MIN_GPA=2.5
REQUIRED_CREDITS=12

def evaluate(score, documents_complete, gpa, credits):
    reasons=[]
    if not documents_complete: reasons.append("documents incomplete")
    if score < THRESHOLD: reasons.append(f"score below {THRESHOLD}")
    if gpa < MIN_GPA: reasons.append(f"GPA below {MIN_GPA:.1f}")
    if credits < REQUIRED_CREDITS: reasons.append(f"credits below {REQUIRED_CREDITS}")
    return ("Review" if not reasons else "Hold", "all synthetic checks passed" if not reasons else "; ".join(reasons))

cases=[
 ("pass",80,True,3.2,15,"Review"),
 ("GPA condition fails",80,True,2.4,15,"Hold"),
 ("credits condition fails",80,True,3.2,11,"Hold"),
 ("score boundary",70,True,2.5,12,"Review"),
]
print("case | inputs (score, complete, GPA, credits) | expected | actual | reason")
for name,score,complete,gpa,credits,expected in cases:
 actual,reason=evaluate(score,complete,gpa,credits)
 print(f"{name} | ({score}, {complete}, {gpa}, {credits}) | {expected} | {actual} | {reason}")
 assert actual==expected
