import sys

# Global dictionary from hash to ID[0-680]
# a = { id : State}
hash_to_id ={}
# id is the position of that state in the list

# List of all possible states
all_states = []
prob = 0.307

class State:
    
    def __init__(self, hp, mc, ace_count, nas, bet, dealer_card):
        self.has_pair = hp
        self.mult_cards = mc # 1 or 2(haspair) or multiple
        self.ace_count = ace_count
        self.non_ace_sum = nas
        self.bet = bet
        self.dealer_card = dealer_card
        
        self.best_move = 'H'
        
        self.old_reward = 0.0
        self.final_reward = 0.0 # To be calculated

        # self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + str(self.ace_count) + "_" + str(self.non_ace_sum) + "_"  + str(self.bet) + "_" + str(self.dealer_card) + "_" + str(self.total)
        self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + str(self.ace_count) + "_" + str(self.non_ace_sum) + "_"  + str(self.bet) + "_" + str(self.dealer_card)
        # self.hash = 'F_F_1_2_5'
        self.id = -1
    
    def get_score(self):
        # returns the best score
        if self.ace_count == 0:
            return self.non_ace_sum
        else :
            score = self.non_ace_sum
            if(self.ace_count>1):
                score = score + self.ace_count - 1
            if(score+11>21):
                score = score + 1
            else:
                score = score + 11
            return score

    def get_hit_sum(self, card):
        # returns the best non bust score score
        
        if card > 1 :
            if self.ace_count == 0:
                return (self.non_ace_sum + card)
            else :
                pot_val = self.non_ace_sum + 1*(self.ace_count-1) + 11*1+ card
                return ((pot_val - 10) if pot_val > 21 else pot_val) # This may be bust or over 21

        else : # card is an ace 
            if self.ace_count == 0:
                pot_val = self.non_ace_sum + 11 
                return ((pot_val - 10) if pot_val > 21 else pot_val)
            else : # We also have an ace, but 2 aces can never be simultaneously be counted as 11 therefore our aces will all be 1
                pot_val = self.non_ace_sum + 1*(self.ace_count) + 11
                return ((pot_val - 10)if pot_val > 21 else pot_val) # This may be bust or over 21

    def hit(self, new_card):
        new_id = -1

        if new_card == 1 : # If the new card is an ace
            if self.ace_count > 0 : # We have aces (atmost 1 can be soft)
                pass
            else: # We don't have any aces
                pass
        else : # If the new card is a number not an ace
            if self.ace_count > 0 : # We have aces (atmost 1 can be soft)
                pass
            else: # We don't have any aces
                pass

        # if self.has_ace == 'F': 
        #     # Not an ace
        #     if new_card != 1 :
        #         if(self.total + new_card) > 21 :
        #             return -1 # Or bust state
        #         else :
        #             if self.mult_cards == 'T' :
        #                 s = State('F', 'F', 'T', self.bet, self.dealer_card, self.total+new_card)
        #             else : 
        #                 if (self.total == new_card):
        #                     s = State('T', 'F', 'T', self.bet, self.dealer_card, self.total+new_card)
        #                 else : 
        #                     s = State('F', 'F', 'T', self.bet, self.dealer_card, self.total+new_card)

        #     # New card is an ace
        #     else : 
        #         if(self.total + new_card) > 21 :
        #             return -1 # Or bust state
        #         else :
        #             if self.mult_cards == 'T' :
        #                     s = State('F', 'T', 'T', self.bet, self.dealer_card, self.total+new_card)
        #             else : 
        #                 if (self.total == new_card):
        #                     s = State('T', 'F', 'T', self.bet, self.dealer_card, self.total+new_card)
        #                 else : 
        #                     s = State('F', 'F', 'T', self.bet, self.dealer_card, self.total+new_card)
                


        new_id = hash_to_id[s.hash]        
        return new_id

    def stand(self):
        pass
    
    def split(self):
        pass
    
    def double(self):
        pass

    # returns 
    # def transition(self, action):
    #     if action == 'H' :


def enumerate_all_states():

    id_ = 0
    global all_states, hash_to_id

    # for dc in range(1, 11):
    #     if dc == 1 :
    #         # Ace , deal with it specially (or not)
    #         pass
    #     else :
    #         pass
    for bet in range(1, 3):
        for dc in range(1, 11):
            # Dealer card 1 will be dealt specially 
            for total in range(1, 22): # Total 21 is different from black jack state? 
                s = State('F', 'F', 'T', bet, dc, total)
                all_states.append(s)
                hash_to_id[s.hash] = id_
                id_ += 1
            
            # Ace with other in 2 to 9
            for other in range(2, 10):
                s = State('F', 'T', 'T', bet, dc, other)
                all_states.append(s)
                hash_to_id[s.hash] = id_
                id_ += 1
            
            # Pair with 2 to 10
            for p in range(2, 11):
                s = State('T', 'F', 'T', bet, dc, 2*p)
                all_states.append(s)
                hash_to_id[s.hash] = id_
                id_ += 1

            # Pair of aces 
            s = State('T', 'T', 'T', bet, dc, 1)
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1

            # What's special in this state
            # The blackjack state
            s = State( 'F' , 'T', 'T', bet, dc, 10)
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1

            # Singular states
            for card in range(1, 11):
                s = State('T', 'F', 'F', bet, dc, (card if card>1 else 0))
                all_states.append(s)
                hash_to_id[s.hash] = id_
                id_ += 1
        
if __name__ == "__main__":
    prob = float(sys.argv[1])
    enumerate_all_states()

# Write to file in a specific format