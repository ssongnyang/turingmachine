from loveletter.loveletterplayer import LoveLetterPlayer
from loveletter.card import Card
from abc import *

class Result:
    valid_card_num=(1, 2, 3, 4, 5, 6, 7, 8)
    def __init__(self, user: LoveLetterPlayer, card: Card) -> None:
        self.user=user
        self.card=card
        
    @abstractmethod
    def result(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

class ResultMessage:
    def __init__(self, msg: str, ephemeral: bool = False) -> None:
        self.msg=msg
        self.ephemeral=ephemeral
        
class TargetResult(Result):
    valid_card_num=(1, 2, 3, 5, 6)
    def __init__(self, user: LoveLetterPlayer, card: Card, target: LoveLetterPlayer) -> None:
        super().__init__(user, card)
        self.target=target
        
    def result(self):
        return f"{self.user.client.mention}님이 {self.card.card_name()} 카드를 {self.target.client.mention}님에게 사용했습니다."
    
    def description(self):
        if self.card.num==1:
            return ResultMessage(f"{self.target.client.mention}님의 카드는 {self.target.card[0].card_name()}입니다.\n{self.target.client.mention}님은 탈락하지 않습니다.", True)
        if self.card.num==2:
            return ResultMessage(f"{self.target.client.mention}님의 카드는 {self.target.card[0].card_name()}입니다.", True)
        if self.card.num==3:
            return ResultMessage(f"{self.target.client.mention}님의 카드는 {self.target.card[0].card_name()}입니다.\n{self.target.client.mention}님은 탈락하지 않습니다.", True)
        if self.card.num==5:
            return ResultMessage(f"{self.target.client.mention}님은 카드를 버리고 새로 한 장을 뽑습니다.")
        if self.card.num==6:
            return ResultMessage(f"{self.user.client.mention}님과 {self.target.client.mention}님이 카드를 바꿉니다.")

class GuardResult(Result):
    valid_card_num=(1,)
    def __init__(self, user: LoveLetterPlayer, card: Card, target: LoveLetterPlayer, value: int) -> None:
        super().__init__(user, card)
        self.target=target
        self.value=value
        
    def result(self):
        return f"{self.user.client.mention}님이 {self.card.card_name()} 카드를 {self.target.client.mention}님에게 사용했습니다."
    
    def description(self):
        if self.card.num==1:
            return ResultMessage(f"\n\n{self.target.client.mention}님의 카드는 {Card(self.value).card_name()}(이)가 아니었습니다.")
        


class NontargetResult(Result):
    valid_card_num=(1, 2, 3, 4, 5, 6, 7, 8)
    def __init__(self, user: LoveLetterPlayer, card: Card) -> None:
        super().__init__(user, card)
        
    def result(self):
        return f"{self.user.client.mention}님이 {self.card.card_name()} 카드를 사용했습니다."
    
    def description(self):
        if self.card.num==4:
            return ResultMessage(f"\n\n{self.user.client.mention}님은 다음 턴까지 다른 카드의 효과를 받지 않습니다.")
        if self.card.num==7: 
            return ResultMessage("ㅤ")
        if self.card.num==8:
            return ResultMessage(f"\n\n{self.user.client.mention}님은 스스로 게임을 포기했습니다.")
        if self.card.num==5:
            return ResultMessage("\n\n카드가 더 이상 남아있지 않아 효과를 적용하지 않습니다.")
        else:
            return ResultMessage("\n\n대상으로 지정할 수 있는 사람이 없습니다.")
        
class KillResult(TargetResult):
    valid_card_num=(1, 3)
    def __init__(self, user: LoveLetterPlayer, card: Card, target: LoveLetterPlayer, killed: LoveLetterPlayer) -> None:
        super().__init__(user, card, target)
        self.killed=killed
        
    def result(self):
        return super().result()
    
    def description(self):
        if self.card.num==1:
            return ResultMessage(f"\n\n{self.target.client.mention}님의 카드는 {self.target.card[0].card_name()}이(가) 맞았습니다!\n\n{self.target.client.mention}님이 탈락했습니다.")
        if self.card.num==3:
            return ResultMessage(f"\n\n{self.killed.client.mention}님이 탈락했습니다.\n\n{self.killed.client.mention}님의 카드는 {self.killed.card[0].card_name()}입니다.")
        
class AccidentResult(TargetResult):
    valid_card_num=(5)
    def __init__(self, user: LoveLetterPlayer, card: Card, target: LoveLetterPlayer) -> None:
        super().__init__(user, card, target)
        
    
    def result(self):
        return f"{self.user.client.mention}님이 {self.card.card_name()} 카드를 {self.target.client.mention}님에게 사용했습니다."
    
    
    def description(self):
        return ResultMessage(f"그런데 이럴수가! {self.target.client.mention}님의 카드가 공주였습니다!\n{self.target.client.mention}님이 탈락했습니다")