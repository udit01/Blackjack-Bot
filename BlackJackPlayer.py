import sys

# Global dictionary from hash to ID[0-680]
# a = { id : State}
hash_to_id ={}
# id is the position of that state in the list

# List of all possible states
all_states = []
prob = 0.307

class State:
    
    def __init__(self, hp, mc, ace_count, nas, bet, dealer_card, blackjack='F'):
        self.has_pair = hp
        self.mult_cards = mc # 1 or 2(haspair) or multiple
        self.ace_count = ace_count
        self.non_ace_sum = nas
        self.bet = bet
        self.dealer_card = dealer_card
        self.blackjack = blackjack

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

    # def get_hit_sum(self, card):
    #     # returns the best non bust score score
        
    #     if card > 1 :
    #         if self.ace_count == 0:
    #             return (self.non_ace_sum + card)
    #         else :
    #             pot_val = self.non_ace_sum + 1*(self.ace_count-1) + 11*1+ card
    #             return ((pot_val - 10) if pot_val > 21 else pot_val) # This may be bust or over 21

    #     else : # card is an ace 
    #         if self.ace_count == 0:
    #             pot_val = self.non_ace_sum + 11 
    #             return ((pot_val - 10) if pot_val > 21 else pot_val)
    #         else : # We also have an ace, but 2 aces can never be simultaneously be counted as 11 therefore our aces will all be 1
    #             pot_val = self.non_ace_sum + 1*(self.ace_count) + 11
    #             return ((pot_val - 10)if pot_val > 21 else pot_val) # This may be bust or over 21

    def hit(self, new_card):
        new_id = -1

        if new_card == 1 : # If the new card is an ace
            if self.ace_count > 0 : # We have aces (atmost 1 can be soft)
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    if self.has_pair == 'T' : # We have a paired state
                        sum_ = self.non_ace_sum + self.ace_count + 11
                        if sum_ <= 21 : 
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card)
                        else : 
                            sum_ -= 11 # Harden the ace
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card)
                            else : # BUSTED 
                                return (-self.bet)
                    else : # We don't have a paired state
                        sum_ = self.non_ace_sum + self.ace_count + 11
                        if sum_ <= 21 : 
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card)
                        else : 
                            sum_ -= 11 # Harden the ace
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card)
                            else : # BUSTED 
                                return (-self.bet)
                else : # Single cards, potential blackjack?
                    if self.has_pair == 'T' : # We have a paired state
                        assert(False)
                        s = None
                    else : # We don't have a paired state
                        # We have ace already, and a single card
                        s = State('T', 'T', self.ace_count + 1, self.non_ace_sum, self.bet, self.dealer_card)
            else: # We don't have any aces
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    if self.has_pair == 'T' : # We have a paired state
                        sum_ = self.non_ace_sum + 11 
                        if sum_ <= 21 :
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card) 
                        else : 
                            sum_ -= 10
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card) 
                            else : # BUSTED
                                return (-self.bet)
                    else : # We don't have a paired state
                        sum_ = self.non_ace_sum + 11 
                        if sum_ <= 21 :
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card) 
                        else : 
                            sum_ -= 10
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card) 
                            else : # BUSTED
                                return (-self.bet)
                else : # Single cards, potential blackjack?
                    if self.has_pair == 'T' : # We have a paired state
                        assert(False)
                        s = None
                    else : # We don't have a paired state
                        if self.non_ace_sum == 10 : # BLACKJACK!
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card, 'T') # Blackjack param
                        else : 
                            s = State('F', 'T', self.ace_count+1, self.non_ace_sum, self.bet, self.dealer_card ) 
        else : # If the new card is a number not an ace
            if self.ace_count > 0 : # We have aces (atmost 1 can be soft)
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    if self.has_pair == 'T' : # We have a paired state
                        sum_ = self.non_ace_sum + new_card + 1*(self.ace_count-1) + 11*1
                        if sum_ <= 21 : 
                            s = State('F', 'T', self.ace_count, self.non_ace_sum+new_card, self.bet, self.dealer_card)
                        else : 
                            sum_ -= 10 # Hardening the ace
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count, self.non_ace_sum + new_card, self.bet, self.dealer_card)
                            else : # BUSTED even after hardening
                                return (-self.bet)
                    else : # We don't have a paired state
                        sum_ = self.non_ace_sum + new_card + 1*(self.ace_count-1) + 11*1
                        if sum_ <= 21 : 
                            s = State('F', 'T', self.ace_count, self.non_ace_sum+new_card, self.bet, self.dealer_card)
                        else : 
                            sum_ -= 10 # Hardening the ace
                            if sum_ <= 21 : 
                                s = State('F', 'T', self.ace_count, self.non_ace_sum + new_card, self.bet, self.dealer_card)
                            else : # BUSTED even after hardening
                                return (-self.bet)
                else : # Single cards, potential blackjack?
                    if self.has_pair == 'T' : # We have a paired state
                        assert(False)
                        s = None
                    else : # We don't have a paired state
                        # We have a single ace card
                        if new_card == 10 : # A face card, threfore BLACKJACK!
                            s = State('F', 'T', self.ace_count, self.non_ace_sum, self.bet, self.dealer_card, 'T') # Blackjack param
                        else : # OTHER CARD, therfore normal hit
                            s = State('F', 'T', self.ace_count, self.non_ace_sum+new_card, self.bet, self.dealer_card)
            else: # We don't have any aces
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    if self.has_pair == 'T' : # We have a paired state
                        sum_ = self.non_ace_sum + new_card
                        if sum_ <= 21 : # Non bust
                            s = State('F', 'T', 0, sum_, self.bet, self.dealer_card )
                        else : # BUSTED # MAKE A BUST STATE or return this
                            return (-self.bet)
                    else : # We don't have a paired state
                        sum_ = self.non_ace_sum + new_card
                        if sum_ <= 21 : # Non bust
                            s = State('F', 'T', 0, sum_, self.bet, self.dealer_card )
                        else : # BUSTED # MAKE A BUST STATE or return this
                            return (-self.bet)
                else : # Single card
                    if self.has_pair == 'T' : # We have a paired state
                        assert(False) # AS Impossible and should never come
                        s = None # Or make a dummy state ?
                    else : # We don't have a paired state
                        # We don't have ace and ace didn't come
                        sum_ = self.non_ace_sum + new_card
                        if sum_ <= 21 : # Non bust
                            if self.non_ace_sum == new_card : # Pair made
                                s = State('T', 'T', 0, sum_, self.bet, self.dealer_card )
                            else :
                                s = State('F', 'T', 0, sum_, self.bet, self.dealer_card )
                        else : # BUSTED # MAKE A BUST STATE or return this
                            return (-self.bet)

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

            # Singular states
            for card in range(1, 11):
                s = State('T', 'F', 'F', bet, dc, (card if card>1 else 0))
                all_states.append(s)
                hash_to_id[s.hash] = id_
                id_ += 1

            
            # What's special in this state
            # The blackjack state
            s = State( 'F' , 'T', 'T', bet, dc, 10, 'T')
            all_states.append(s)
            hash_to_id[s.hash] = id_
            id_ += 1
        
if __name__ == "__main__":
    global prob
    prob = float(sys.argv[1])
    enumerate_all_states()

# Write to file in a specific format