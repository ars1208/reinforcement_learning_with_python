def V(s, gamma=0.99):
    V = R(s) + gamma * max_V_on_next_state(s)
    return V
    
