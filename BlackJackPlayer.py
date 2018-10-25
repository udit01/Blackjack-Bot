import sys

# Global dictionary from hash to ID[0-680]
# a = { id : State}
hash_to_id ={}
# id is the position of that state in the list

# List of all possible states
all_states = []

class State:
    
    def __init__(self, hp, mc, ha, nas, bet, dealer_card, blackjack='F', splitted_aces='F'):
        self.has_pair = hp
        self.mult_cards = mc # 1 or 2(haspair) or multiple
        self.has_ace = ha
        self.non_ace_sum = nas
        self.bet = bet
        self.dealer_card = dealer_card
        self.blackjack = blackjack
        self.splitted_aces = splitted_aces

        self.best_move = 'H'
        
        self.old_reward = 0.0
        self.final_reward = 0.0 # To be calculated

        # self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + str(self.ace_count) + "_" + str(self.non_ace_sum) + "_"  + str(self.bet) + "_" + str(self.dealer_card) + "_" + str(self.total)
        self.hash = (self.has_pair) + "_" + (self.mult_cards) + "_" + (self.has_ace) + "_" + str(self.non_ace_sum) + "_"  + str(int(self.bet)) + "_" + str(self.dealer_card) + "_" + self.blackjack + "_" + self.splitted_aces
        # self.hash = 'F_F_1_2_5'
        self.id = -1
    
    def get_score(self):
        # returns the best score
        if self.has_ace == 'F':
            return self.non_ace_sum
        else :
            score = self.non_ace_sum + 11
            return (score if score <= 21 else (score-10))

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
            if self.has_ace == 'T' : # We have aces (atmost 1 can be soft)
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    sum_ = self.non_ace_sum + 1 + 11 # as can ony count 1 ace as 11
                    if sum_ <= 21 : 
                        s = State('F', 'T', 'T', self.non_ace_sum+1, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                        new_id = hash_to_id[s.hash]        
                    else : 
                        sum_ -= 10 # Harden the ace
                        if sum_ <= 21 : 
                            s = State('F', 'T','T', self.non_ace_sum+1, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                            if s.hash not in hash_to_id :
                                print(self.hash)
                            new_id = hash_to_id[s.hash]        
                        else : # BUSTED 
                            return (-self.bet)
                else : # Single cards, potential blackjack?
                    # We have ace already, and a single card
                    s = State('T', 'T', 'T', 1, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                    new_id = hash_to_id[s.hash]        
            else: # We don't have any aces
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    sum_ = self.non_ace_sum + 11 
                    if sum_ <= 21 :
                        s = State('F', 'T', 'T', self.non_ace_sum, self.bet, self.dealer_card, self.blackjack, self.splitted_aces) 
                        new_id = hash_to_id[s.hash]        
                    else : 
                        sum_ -= 10
                        if sum_ <= 21 : 
                            s = State('F', 'T', 'T', self.non_ace_sum, self.bet, self.dealer_card, self.blackjack, self.splitted_aces) 
                            new_id = hash_to_id[s.hash]        
                        else : # BUSTED
                            return (-self.bet)
                else : # Single cards, potential blackjack?
                    if self.non_ace_sum == 10 : # BLACKJACK!
                        s = State('F', 'T', 'T', self.non_ace_sum, self.bet, self.dealer_card, 'T', self.splitted_aces) # Blackjack param
                        new_id = hash_to_id[s.hash]        
                    else : 
                        s = State('F', 'T', 'T', self.non_ace_sum, self.bet, self.dealer_card, self.blackjack, self.splitted_aces ) 
                        new_id = hash_to_id[s.hash]        
        else : # If the new card is a number not an ace
            if self.has_ace == 'T' : # We have aces (atmost 1 can be soft)
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    sum_ = self.non_ace_sum + new_card + 11
                    if sum_ <= 21 : 
                        s = State('F', 'T', 'T', self.non_ace_sum + new_card, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                        new_id = hash_to_id[s.hash]        
                    else : 
                        sum_ -= 10 # Hardening the ace
                        if sum_ <= 21 : 
                            s = State('F', 'T', 'T', self.non_ace_sum + new_card, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                            new_id = hash_to_id[s.hash]        
                        else : # BUSTED even after hardening
                            return (-self.bet)
                else : # Single cards, potential blackjack?
                    # We have a single ace card
                    if new_card == 10 : # A face card, threfore BLACKJACK!
                        s = State('F', 'T', 'T', self.non_ace_sum + new_card, self.bet, self.dealer_card, 'T', self.splitted_aces) # Blackjack param
                        if s.hash not in hash_to_id :
                            print(self.hash)
                        new_id = hash_to_id[s.hash]        
                    else : # OTHER CARD, therfore normal hit
                        s = State('F', 'T', 'T', self.non_ace_sum + new_card, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                        new_id = hash_to_id[s.hash]        
            else: # We don't have any aces
                if self.mult_cards == 'T' : # We have multiple cards so no blackjack
                    sum_ = self.non_ace_sum + new_card
                    if sum_ <= 21 : # Non bust
                        s = State('F', 'T', 'F', sum_, self.bet, self.dealer_card, self.blackjack, self.splitted_aces)
                        new_id = hash_to_id[s.hash]        
                    else : # BUSTED # MAKE A BUST STATE or return this
                        return (-self.bet)
                else : # Single card
                    # We don't have ace and ace didn't come
                    sum_ = self.non_ace_sum + new_card
                    if sum_ <= 21 : # Non bust
                        if self.non_ace_sum == new_card : # Pair made
                            s = State('T', 'T', 'F', sum_, self.bet, self.dealer_card, self.splitted_aces )
                            new_id = hash_to_id[s.hash]        
                        else :
                            s = State('F', 'T', 'F', sum_, self.bet, self.dealer_card, self.splitted_aces )
                            if s.hash not in hash_to_id :
                                print(self.hash)
                            new_id = hash_to_id[s.hash]        
                    else : # BUSTED # MAKE A BUST STATE or return this
                        return (-self.bet)

        new_id = hash_to_id[s.hash]        
        return new_id

    def stand(self):
        pass
    
    def split(self):
        assert(self.has_pair == 'T')
        # What to return ?
        if self.has_ace == 'T' :
            s = State('F', 'F', 'T', 0, self.bet, self.dealer_card, self.blackjack, 'T')
            if s.hash not in hash_to_id :
                print(self.hash)
            return(hash_to_id[s.hash])
        else :
            s = State('F', 'F', 'F', self.non_ace_sum//2, self.bet, self.dealer_card, self.blackjack, 'F')
            if s.hash not in hash_to_id :
                print(self.hash)
            return(hash_to_id[s.hash])
        # IN case of splitting aces can only be done once
        
    
    def double(self):
        assert(self.bet == 1)
        s = State(self.has_pair, self.mult_cards, self.has_ace, self.non_ace_sum, 2, self.dealer_card, self.blackjack, self.splitted_aces)
        return hash_to_id[s.hash]

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
            s = State('F', 'T', 'F', total, 1.0, dc, 'F', 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('F', 'T', 'F', total, 1.0, 1, 'F', 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATES A2...A9
    for other in range(2, 10):
        writeString += 'A' + str(other) + '\t'

        for dc in range(2, 11):
            s = State('F', 'T', 'T', other, 1.0, dc, 'F', 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('F', 'T', 'T', other, 1.0, 1, 'F', 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATES 22, 33 .... 1010
    for p in range(2, 11):
        writeString += str(p) + str(p) + '\t'

        for dc in range(2, 11):
            s = State('T', 'T', 'F', 2*p, 1.0, dc, 'F', 'F')
            st = all_states[hash_to_id[s.hash]]
            writeString += st.best_move + ' '
        
        s = State('T', 'T', 'F', 2*p, 1.0, 1, 'F', 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move

        writeString += '\n'

    # STATE AA
    writeString += 'AA' + '\t'

    for dc in range(2, 11):
        s = State('T', 'T', 'T', 1, 1.0, dc, 'F', 'F')
        st = all_states[hash_to_id[s.hash]]
        writeString += st.best_move + ' '
    
    s = State('T', 'T', 'T', 1, 1.0, 1, 'F', 'F')
    st = all_states[hash_to_id[s.hash]]
    writeString += st.best_move

    # writeString += '\n'

    with open("Policy.txt","w") as outfile:
        outfile.write(writeString)
        outfile.close()

def comp_hand_score(has_ace,non_ace_sum):
    if has_ace == 'F':
        return non_ace_sum
    score = 0
    if (non_ace_sum>10):
        score = non_ace_sum + 1
    else:
        score = non_ace_sum + 11
    return score

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

    choices = ['T', 'F']

    for hp in choices:
        for mc in choices:
            for ha in choices:
                for nas in range(0, 22):
                    for bet in range(1, 3):
                        for dc in range(1, 11):
                            for blackjack in choices:
                                for splitted_aces in choices:
                                    if hp == 'T' and mc == 'F' :
                                        continue
                                    if ha == 'F' and blackjack == 'T' :
                                        continue
                                    sc = comp_hand_score(ha,nas)
                                    if blackjack == 'T' and sc != 21 :
                                        continue
                                    if hp == 'T' and ha == 'T' and nas != 1 :
                                        continue
                                    if mc == 'F' and ha == 'T' and nas != 0 :
                                        continue
                                    if mc == 'F' and ha == 'F' and nas == 0 :
                                        continue
                                    if ha == 'F' and splitted_aces == 'T' :
                                        continue
                                    if ha == 'F' and hp == 'T' and nas == 0 :
                                        continue
                                    if ha == 'F' and hp == 'T' and (nas%2) == 1 :
                                        continue
                                    s = State(hp, mc, ha, nas, bet, dc, blackjack, splitted_aces)
                                    all_states.append(s)
                                    hash_to_id[s.hash] = id_
                                    id_ += 1

    # for splitted_aces in ['T', 'F']:
    #     for blackjack in ['T', 'F']:
    #         for bet in range(1, 3):
    #             for dc in range(1, 11):
    #                 # Dealer card 1 will be dealt specially 
    #                 for total in range(1, 22): # Total 21 is different from black jack state? 
    #                     s = State('F', 'T', 0,total, bet, dc, blackjack, splitted_aces)
    #                     all_states.append(s)
    #                     hash_to_id[s.hash] = id_
    #                     id_ += 1
                    
    #                 # Ace with other in 2 to 9
    #                 for other in range(2, 10):
    #                     s = State('F', 'T', 1, other, bet, dc, blackjack, splitted_aces)
    #                     all_states.append(s)
    #                     hash_to_id[s.hash] = id_
    #                     id_ += 1
                    
    #                 # Pair with 2 to 10
    #                 for p in range(2, 11):
    #                     s = State('T', 'T', 0, 2*p, bet, dc, blackjack, splitted_aces)
    #                     all_states.append(s)
    #                     hash_to_id[s.hash] = id_
    #                     id_ += 1

    #                 # Pair of aces 
    #                 s = State('T', 'T', 2, 0, bet, dc, blackjack, splitted_aces)
    #                 all_states.append(s)
    #                 hash_to_id[s.hash] = id_
    #                 id_ += 1

    #                 # Singular states
    #                 for card in range(1, 11):
    #                     s = State('T', 'F', 0 if card > 1 else 1, (card if card>1 else 0), bet, dc, blackjack, splitted_aces)
    #                     all_states.append(s)
    #                     hash_to_id[s.hash] = id_
    #                     id_ += 1

                    
    #                 # What's special in this state
    #                 # The blackjack state
    #                 s = State( 'F' , 'T', 'T', bet, dc, 10, blackjack, splitted_aces)
    #                 all_states.append(s)
    #                 hash_to_id[s.hash] = id_
    #                 id_ += 1
    
    return (id_)

actions = ['H','S','P','D']

expected_stand_reward = {}


def compute_stand_reward(pl_has_ace,pl_non_ace_score,dealer_has_ace,dealer_non_ace_score,player_blackjack,dealer_first_call,p,bet):
    global expected_stand_reward
    hash_str = str(pl_has_ace) + "_" + str(pl_non_ace_score) + "_" + str(dealer_has_ace) + "_" + str(dealer_non_ace_score) + "_" + str(player_blackjack) + "_" + str(dealer_first_call)
    if hash_str in expected_stand_reward :
        return expected_stand_reward[hash_str]
    add_reward = 0.0
    pl_score = comp_hand_score(pl_has_ace,pl_non_ace_score)
    dealer_score = comp_hand_score(dealer_has_ace,dealer_non_ace_score)

    if(dealer_score>=17):
        if pl_score == 21 :
            if player_blackjack == 'T':
                if dealer_score== 21 and dealer_first_call=='T' :  
                    add_reward = 0.0
                else :
                    add_reward = 1.5 * float(bet)
            else:
                if dealer_score == 21 and dealer_first_call=='T'  : 
                    add_reward = -1.0 * float(bet)
                elif dealer_score == 21 :
                    add_reward = 0.0
                else :
                    add_reward = float(bet)
        elif pl_score >= 22 :
            add_reward = float(-1*bet)
        elif dealer_score >= 22 :
            add_reward = float(bet)
        else :
            if pl_score > dealer_score :
                add_reward = float(bet)
            elif pl_score < dealer_score :
                add_reward = -1.0 * float(bet)
            else:
                add_reward = 0.0
    else :
        for i in range(1,11):
            cur_reward = 0.0
            mult_prob = (1.0 - p)/9.0
            if (i==10):
                mult_prob = p
            if (i!=1):
                cur_reward = compute_stand_reward(pl_has_ace,pl_non_ace_score,dealer_has_ace,dealer_non_ace_score+i,player_blackjack,'F',p,bet)
            else :
                if dealer_has_ace == 'T' :
                    cur_reward = compute_stand_reward(pl_has_ace,pl_non_ace_score,dealer_has_ace,dealer_non_ace_score+1,player_blackjack,'F',p,bet)
                else :
                    cur_reward = compute_stand_reward(pl_has_ace,pl_non_ace_score,'T',dealer_non_ace_score,player_blackjack,'F',p,bet)
            add_reward = add_reward + mult_prob*cur_reward

    expected_stand_reward[hash_str] = add_reward
    return add_reward

def bellman_backup(eps,p):
    stop = False
    cnt = 0
    while(not stop):
        cnt = cnt + 1 
        if cnt > 10000:
            break
        for st in all_states :
            best_reward = -100.0
            for act in actions:
                current_reward = 0.0
                if st.bet == 2 :
                    if act != 'S':
                        continue
                if st.blackjack == 'T':
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
                        if(i==10):
                            mult_prob = p
                        if (i!=1):
                            if (st.dealer_card!=1):
                                add_reward = compute_stand_reward(st.has_ace,st.non_ace_sum,'F',(i + st.dealer_card),st.blackjack,'T',p,st.bet)
                            else :
                                add_reward = compute_stand_reward(st.has_ace,st.non_ace_sum,'T',(i + 11),st.blackjack,'T',p,st.bet)
                        else :
                            if(st.dealer_card!=1):
                                add_reward = compute_stand_reward(st.has_ace,st.non_ace_sum,'T',(st.dealer_card + 11),st.blackjack,'T',p,st.bet)
                            else:
                                add_reward = compute_stand_reward(st.has_ace,st.non_ace_sum,'T',12,st.blackjack,'T',p,st.bet)
                        
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
                        for i in range(1,11):
                            ret_id = all_states[st_id].hit(i)
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
                        # current_reward = all_states[st_id].old_reward

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
    prob = float(sys.argv[1])
    enumerate_all_states()
    bellman_backup(0.00000001,prob)
    print_output()
# Write to file in a specific format
