import sys

# Global dictionary from hash to ID[0-680]
# a = { id : State}
hash_to_id ={}
# id is the position of that state in the list

# List of all possible states
all_states = []
prob = 0.307

class State:
    
    def __init__(self, hp, mc, ace_count, nas, bet, dealer_card, blackjack='F', splitted_aces='F'):
        self.has_pair = hp
        self.mult_cards = mc # 1 or 2(haspair) or multiple
        self.ace_count = ace_count
        self.non_ace_sum = nas
        self.bet = bet
        self.dealer_card = dealer_card
        self.blackjack = blackjack
        self.splitted_aces = splitted_aces

        self.best_move = 'H'
        
        self.old_reward = 0.0
        self.final_reward = 0.0 # To be calculated

        # self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + str(self.ace_count) + "_" + str(self.non_ace_sum) + "_"  + str(self.bet) + "_" + str(self.dealer_card) + "_" + str(self.total)
        self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + str(self.ace_count) + "_" + str(self.non_ace_sum) + "_"  + str(int(self.bet)) + "_" + str(self.dealer_card) + "_" + self.blackjack + "_" + self.splitted_aces
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
        assert(self.has_pair == 'T')
        # What to return ?
        s = State('F', 'F', self.ace_count//2, self.non_ace_sum//2, self.bet, self.dealer_card, self.blackjack)
        
        # IN case of splitting aces can only be done once
        
        return(hash_to_id[s.hash])
    
    def double(self):
        pass

    # returns 
    # def transition(self, action):
    #     if action == 'H' :

# To save it in Policy.txt
def print_output():
    writeString = ""
    
    # ONLY for initial states

    # STATES 5 to 20
    for total in range(5, 20):
        writeString += str(total) + '\t'
        
        for dc in range(2, 11):
            s = State('F', 'T', 0, total, 1.0, dc, 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('F', 'T', 0, total, 1.0, 1, 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATES A2...A9
    for other in range(2, 10):
        writeString += 'A' + str(other) + '\t'

        for dc in range(2, 11):
            s = State('F', 'T', 1, other, 1.0, dc, 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('F', 'T', 0, other, 1.0, 1, 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATES 22, 33 .... 1010
    for p in range(2, 11):
        writeString += str(p) + str(p) + '\t'

        for dc in range(2, 11):
            s = State('T', 'T', 0, 2*p, 1.0, dc, 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('T', 'T', 0, 2*p, 1.0, 1, 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATE AA
    writeString += 'AA' + '\t'

    for dc in range(2, 11):
        s = State('T', 'T', 2, 0, 1.0, dc, 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move + ' '
    
    s = State('T', 'T', 2, 0, 1.0, 1, 'F')
    st = all_states[hash_to_id[s.hash]]
    writeString += st.best_move

    # writeString += '\n'

    with open("Policy.txt","w") as outfile:
        outfile.write(writeString)
        outfile.close()



def enumerate_all_states():

    id_ = 0
    global all_states, hash_to_id

    # for dc in range(1, 11):
    #     if dc == 1 :
    #         # Ace , deal with it specially (or not)
    #         pass
    #     else :
    #         pass

    # TODO : ENUMERATE all these states correctly :

    for splitted_aces in ['T', 'F']:
        for blackjack in ['T', 'F']:
            for bet in range(1, 3):
                for dc in range(1, 11):
                    # Dealer card 1 will be dealt specially 
                    for total in range(1, 22): # Total 21 is different from black jack state? 
                        s = State('F', 'T', 0,total, bet, dc, blackjack, splitted_aces)
                        all_states.append(s)
                        hash_to_id[s.hash] = id_
                        id_ += 1
                    
                    # Ace with other in 2 to 9
                    for other in range(2, 10):
                        s = State('F', 'T', 1, other, bet, dc, blackjack, splitted_aces)
                        all_states.append(s)
                        hash_to_id[s.hash] = id_
                        id_ += 1
                    
                    # Pair with 2 to 10
                    for p in range(2, 11):
                        s = State('T', 'T', 0, 2*p, bet, dc, blackjack, splitted_aces)
                        all_states.append(s)
                        hash_to_id[s.hash] = id_
                        id_ += 1

                    # Pair of aces 
                    s = State('T', 'T', 2, 0, bet, dc, blackjack, splitted_aces)
                    all_states.append(s)
                    hash_to_id[s.hash] = id_
                    id_ += 1

                    # Singular states
                    for card in range(1, 11):
                        s = State('T', 'F', 0 if card > 1 else 1, (card if card>1 else 0), bet, dc, blackjack, splitted_aces)
                        all_states.append(s)
                        hash_to_id[s.hash] = id_
                        id_ += 1

                    
                    # What's special in this state
                    # The blackjack state
                    s = State( 'F' , 'T', 'T', bet, dc, 10, blackjack, splitted_aces)
                    all_states.append(s)
                    hash_to_id[s.hash] = id_
                    id_ += 1

actions = ['H','S','P','D']
                    
def bellman_backup(eps,p):
    stop = False
    while(not stop):
        
        for st in all_states :
            best_reward = -100.0
            for act in actions:
                current_reward = 0.0
                if st.bet == 2 :
                    if act != 'S':
                        continue
                if act=='H':
                    for i in range(1,11):
                        ret_id = st.hit(i)
                        add_reward = 0.0
                        if (ret_id<0):
                            add_reward = float(ret_id)
                        else:
                            add_reward = float(all_states[ret_id].old_reward)
                        if(i==10):
                            current_reward = current_reward + p*add_reward
                        else:
                            oth_prob = (1.0 - p)/9.0
                            current_reward = current_reward + oth_prob*add_reward
                elif act=='S':
                    for i in range(1,11): # dealers other card 
                        add_reward = 0.0
                        mult_prob = (1.0 - p)/9.0
                        dealer_sum = 0
                        if(i==10):
                            mult_prob = p
                        if (i!=1):
                            if (st.dealer_card!=1):
                                dealer_sum = i + st.dealer_card
                            else :
                                dealer_sum = i + 11
                        else :
                            if(st.dealer_card!=1):
                                dealer_sum = st.dealer_card + 11
                            else:
                                dealer_sum = 12
                        if(dealer_sum>=17):
                            cur_score = st.get_score()
                            if cur_score == 21 :
                                if st.blackjack == 'T':
                                    if dealer_sum == 21 :  # dealer currently has 2 cards only so 21 implies blackjack
                                        add_reward = 0.0
                                    else :
                                        add_reward = 1.5 * float(st.bet)
                                else:
                                    if dealer_sum == 21 : # dealer currently has 2 cards only so 21 implies blackjack
                                        add_reward = -1.0 * float(st.bet)
                                    else :
                                        add_reward = float(st.bet)

                            elif cur_score >= 22 :
                                add_reward = float(-1*st.bet)
                            elif dealer_sum >= 22 :
                                add_reward = float(st.bet)
                            else :
                                if cur_score > dealer_sum :
                                    add_reward = float(st.bet)
                                elif cur_score < dealer_sum :
                                    add_reward = -1.0 * float(st.bet)
                                else:
                                    add_reward = 0.0
                        else :
                            pass # call recursive function

                        current_reward = current_reward + mult_prob*add_reward
                elif act=='P':
                    if (st.has_pair == 'F') :
                        current_reward = -100.0
                    elif (st.splitted_aces == 'T'):
                        current_reward = -100.0
                    else :
                        st_id = st.split()
                        current_reward = 2.0 * all_states[st_id].old_reward

                else: #double
                    if st.bet == 2 :
                        current_reward = -100.0
                    else :
                        st_id = st.double()
                        current_reward = all_states[st_id].old_reward

                if current_reward >= best_reward :
                    st.best_move = act
                best_reward = max(best_reward,current_reward)
            st.final_reward = best_reward
        
        max_val = 0.0
        for st in all_states:
            cur_diff = abs(st.final_reward - st.old_reward)
            max_val = max(max_val,cur_diff)
            st.old_reward = st.final_reward
            st.final_reward = 0.0
        if(max_val<eps):
            stop = True

if __name__ == "__main__":
    global prob
    prob = float(sys.argv[1])
    enumerate_all_states()
    bellman_backup(0.0000000001,prob)

# Write to file in a specific format
