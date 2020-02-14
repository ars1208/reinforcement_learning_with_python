def V(s, gamma=0.99):
    V = R(s) + gamma * max_V_on_next_state(s)
    return V

def R(s):
    if s == "happy_end":
        return 1
    elif s == "bad_end":
        return -1
    else:
        return 0
