import discord
from loveletter.card import Card

class LoveLetterPlayer:
    def __init__(self, itc: discord.Interaction):
        self.itc=itc
        self.client=itc.user
        self.id=itc.user.id
        self.card: list[Card]= []
        self.card_emoji_msg=None
        self.view_msg=None
        self.select_msg=None
        self.used_card: list[Card]= []
        self.protected: bool = False
        self.token: int = 0
        
        
    def __eq__(self, other):
        if type(other)==int:
            return self.id==other
        elif other==None:
            return False
        else:
            return self.id==other.id
    
    def find_card(self, card_num: int):
        for i in range(len(self.card)):
            if self.card[i]==card_num:
                return i
        return False
    
    def sort_card(self):
        if  len(self.card) >1 and self.card[0].num>self.card[1].num:
            self.card.reverse()
    
    def discard_card(self, card: Card | None = None):
        if card:
            for i in range(len(self.card)):
                if card.num==self.card[i].num:
                    self.card.pop(i)
                    return card
            return False
        else: 
            return self.card.pop()

    def show_card_emoji(self):
        result=""
        for c in self.card:
            result+=c.card_emoji()
        return result
    
    def shallow_copy(self):
        return [self][:][0]
        
        
        
            