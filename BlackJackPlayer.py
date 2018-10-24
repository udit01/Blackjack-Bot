import sys

# Global dictionary from hash to ID[0-680]
# a = { id : State}
hash_to_id ={}
# id is the position of that state in the list

# List of all possible states
all_states = []
prob = 0.307

class State:
    
    def __init__(self, hp, ha, bet, dealer_card, total):
        # self.has_pair = 'F'
        self.has_pair = hp
        # self.has_ace = 'F'
        self.has_ace = ha
        # False -> 1 and True means ->2
        # self.bet = 1
        # self.dealer_card = 2
        # self.total = 5
        self.bet = bet
        self.dealer_card = dealer_card
        self.total = total
        
        self.best_move = 'H'
        
        self.old_reward = 0.0
        self.final_reward = 0.0 # To be calculated

        self.hash = (self.has_pair) + "_" + (self.has_ace) + "_" + str(self.bet) + "_" + str(self.dealer_card) + "_" + str(self.total)
        # self.hash = 'F_F_1_2_5'
        self.id = -1
    
    # def hit(self):
    #     pass
    
    # def stand(self):
    #     pass
    
    # def split(self):
    #     pass
    
    # def double(self):
    #     pass

    # returns 
    def transition(self, action):
        if action == 'H' :


def enumerate_all_states():

    id_ = 0
    global all_states, hash_to_id

    # for dc in range(1, 11):
    #     if dc == 1 :
    #         # Ace , deal with it specially (or not)
    #         pass
    #     else :
    #         pass
    
    for dc in range(1, 11):
        # Dealer card 1 will be dealt specially 
        for total in range(1, 22): # Total 21 is different from black jack state? 
            s = State('F', 'F', 1.0, dc, total)
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1
        
        # Ace with other in 2 to 9
        for other in range(2, 10):
            s = State('F', 'T', 1.0, dc, 11+other)
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1
        
        # Pair with 2 to 10
        for p in range(2, 11):
            s = State('T', 'F', 1.0, dc, 2*p)
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1

        # Pair of aces 
        s = State('T', 'T', 1.0, dc, 12)
        all_states.append(s)
        hash_to_id[s.hash] = id_
        id_ += 1

        # The blackjack state
        s = State( 'F' , 'T', 1.5, dc, 21)
        all_states.append(s)
        hash_to_id[s.hash] = id_
        id_ += 1
        
if __name__ == "__main__":
    prob = float(sys.argv[1])
    enumerate_all_states()

# Write to file in a specific format