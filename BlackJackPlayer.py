import sys

class State:
    
    def __init__(self):
        self.has_pair = False
        self.dealer_card = 2
        self.total = 5
        self.reward = 1.0 # To be calculated
        self.has_ace = False
        self.bet = 1.0
    
    def hit(self):
        pass
    
    def stand(self):
        pass
    
    def split(self):
        pass
    
    def double(self):
        pass






if __name__ == "__main__":
    prob = sys.argv[1]


# Write to file in a specific format