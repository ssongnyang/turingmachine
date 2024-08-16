from verifier import Verifier
from itertools import product, combinations
from discord import ui, app_commands
from discord.ext import commands
import discord
import random
import collections.abc

class TuringMachineGame:
    class Player():
        def __init__(self, _client, test_count_total=0, code_generate_total=0):
            self.client: discord.Member=_client
            self.code=(0, 0, 0)
            self.test_count=0
            self.test_count_total=test_count_total
            self.code_generate_total=code_generate_total
            self.result: str
        
        def __eq__(self, other: discord.Member):
            return self.client.id==other.id
    
    
    successed_players: list[Player] = []
    failed_players: list[Player] = []
    scouting=True
    running=False
    roundpause=False
    
    difficulty: str = "쉬움"
    mode: str = "클래식"
    verifier_count: int = 4 
    
    verifiers_list: list[Verifier] = []
    verifiers_num_list: list[int] = []
    fake_verifiers_num_list: list[int] = []
    answer: tuple[int, int, int] = (0, 0, 0)
    
    def __init__(self, starter, _mode):
        self.starter: self.Player = starter
        self.players: list[self.Player] = [(self.Player(starter))]
        self.mode=_mode
        self.response: list[str] = []
    
    def is_player(self, player: discord.Member):
        for p in self.players:
            if p==player:
                return True
        return False
    
    def find_player(self, player: discord.Member):
        for i in range(self.player_num()):
            if self.players[i]==player:
                return i
        return False
    
    def add_player(self, player: discord.Member):
        if not self.is_player(player):
            self.players.append(self.Player(player))
            return True
        else: return False
        
    def del_player(self, player: discord.Member):
        for p in self.players:
            if p==player: 
                self.players.remove(player)
                return True
        return False
    
    def print_player_mention(self, between: str="\n"):
        string=""
        for p in self.players:
            string+=p.client.mention+between
        return string[:-len(between)]
    
    def is_successed_player(self, player: discord.Member):
        for p in self.successed_players:
            if p==player:
                return True
        return False
                
    def add_successed_player(self, player: Player):
        if not self.is_successed_player(player.client):
            self.successed_players.append(player)
            return True
        else: return False
        
    def is_failed_player(self, player: discord.Member):
        for p in self.failed_players:
            if p==player:
                return True
        return False
                
    def add_failed_player(self, player: discord.Member):
        if not self.is_failed_player:
            self.failed_players.append(self.Player(player))
            return True
        else: return False
            
    def print_successed_player(self, between: str = ", "):
        string=""
        for p in self.successed_players:
            string+=f"{p.client.mention}({p.code_generate_total}/{p.test_count_total})"+between
        return string[:-(len(between))]
    
    def print_failed_mention(self, between: str=", "):
        string=""
        for p in self.failed_players:
            string+=p.client.mention+between
        return string[:-len(between)]
    
    def next_round(self):
        for r in self.response:
            if r=="계속":
                r="코드 선정"
        for p in self.players:
            p.test_count=0
            
    def embed_color(self):
        if self.mode=="클래식":
            return 0x49d44c
        elif self.mode=="익스트림":
            return 0xfebd11
        
    def player_num(self):
        return len(self.players)

    
class TuringMachine(commands.Cog):
    all_comb = {(4, 2, 2), (1, 4, 4), (2, 2, 4), (5, 5, 1), (5, 2, 1), (1, 4, 2), (5, 5, 3), (5, 2, 3), (5, 5, 5), (3, 1, 4), (3, 2, 2), (4, 1, 5), (3, 1, 2), (2, 5, 3), (1, 2, 2), (2, 5, 1), (4, 1, 1), (1, 2, 4), (5, 3, 2), (1, 5, 5), (3, 2, 4), (4, 1, 3), (2, 5, 5), (1, 3, 5), (1, 5, 1), (3, 4, 5), (2, 3, 4), (1, 3, 3), (4, 3, 4), (5, 3, 4), (1, 5, 3), (1, 3, 1), (4, 3, 2), (3, 3, 1), (5, 1, 5), (3, 4, 1), (3, 3, 3), (3, 4, 3), (2, 3, 2), (3, 3, 5), (2, 4, 2), (5, 1, 1), (5, 4, 3), (5, 1, 3), (2, 4, 4), (4, 5, 2), (5, 4, 1), (4, 5, 4), (2, 1, 5), (4, 2, 5), (3, 5, 2), (2, 2, 3), (2, 1, 3), (5, 4, 5), (2, 2, 1), (4, 4, 5), (2, 1, 1), (4, 2, 1), (1, 1, 2), (5, 2, 4), (4, 4, 3), (4, 2, 3),
                (1, 1, 4), (3, 5, 4), (2, 2, 5), (4, 4, 1), (1, 4, 5), (5, 2, 2), (1, 4, 3), (5, 5, 2), (3, 1, 5), (1, 4, 1), (4, 1, 4), (5, 5, 4), (3, 1, 3), (3, 2, 3), (2, 5, 2), (1, 2, 1), (3, 1, 1), (3, 2, 1), (1, 2, 3), (5, 3, 3), (4, 1, 2), (1, 2, 5), (5, 3, 1), (1, 5, 4), (3, 2, 5), (2, 5, 4), (3, 4, 4), (1, 3, 4), (5, 3, 5), (2, 3, 5), (1, 3, 2), (4, 3, 5), (1, 5, 2), (4, 3, 3), (5, 1, 4), (2, 4, 1), (3, 4, 2), (2, 3, 1), (4, 3, 1), (3, 3, 2), (2, 4, 3), (2, 3, 3), (5, 4, 2), (3, 3, 4), (2, 4, 5), (4, 5, 1), (5, 1, 2), (4, 5, 3), (2, 1, 4), (3, 5, 3), (4, 5, 5), (2, 1, 2), (4, 2, 4), (1, 1, 1), (5, 4, 4), (3, 5, 1), (2, 2, 2), (1, 1, 3), (4, 4, 4), (1, 1, 5), (5, 2, 5), (3, 5, 5), (4, 4, 2)}

    creteria_count_lst = (2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 4, 2, 3, 3, 2,
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 3, 3, 3, 3, 3, 6, 9, 9, 6, 6, 6, 6, 6, 6, 9)

    verifier_type = [(1, 2, 3, 4), (5, 6, 7), (8, 9, 10, 20, 21, 45, 46, 47), (11, 12, 13), (14, 15, 34, 35, 42), (16, 17, 18), (19, 37, 38), (22, 24, 25), (28, 29, 30), 
                    23, 26, 27, 31, 32, 33, 36, 39, 40, 41, 43, 44, 48]

    verifier_description=[
        "이 검증기는 <:bluetriangle:1273289917723705405>와 1을 비교합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>와 3을 비교합니다.",
        "이 검증기는 :yellow_square:와 3을 비교합니다.",
        "이 검증기는 :yellow_square:와 4를 비교합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>가 짝수인지 혹은 홀수인지 검증합니다.",
        "이 검증기는 :yellow_square:가 짝수인지 혹은 홀수인지 검증합니다.",
        "이 검증기는 :purple_circle:가 짝수인지 혹은 홀수인지 검증합니다.",
        "이 검증기는 1이 몇 번 나타나는지 검증합니다.",
        "이 검증기는 3이 몇 번 나타나는지 검증합니다.",
        "이 검증기는 4가 몇 번 나타나는지 검증합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>와 :yellow_square:를 비교합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>와 :purple_circle:를 비교합니다.",
        "이 검증기는 :yellow_square:와 :purple_circle:를 비교합니다.",
        "이 검증기는 어떤 숫자가 가장 작은지 검증합니다.",
        "이 검증기는 어떤 숫자가 가장 큰지 검증합니다.",
        "이 검증기는 짝수와 홀수 중 어느 쪽이 더 많은지 검증합니다.",
        "이 검증기는 짝수가 몇 번 나타나는지 검증합니다.",
        "이 검증기는 모든 숫자의 합이 홀수인지 혹은 짝수인지 검증합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>와 :yellow_square:의 합을 6과 비교합니다.",
        "이 검증기는 반복되는 숫자가 있는지, 있다면 몇 번 반복되는지 검증합니다.",
        "이 검증기는 정확히 두 번만 반복되는 숫자가 있는지 검증합니다",
        "이 검증기는 세 숫자가 어떤 순서로 정렬되어 있는지 검증합니다.",
        "이 검증기는 모든 숫자의 합을 6과 비교합니다.",
        "이 검증기는 오름차순으로 연속되는 숫자가 몇 개인지 검증합니다.",
        "이 검증기는 오름차순이나 내림차순으로 연속되는 숫자가 몇 개인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 3보다 작은지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 4보다 작은지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 1인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 3인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 4인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 1보다 큰지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 3보다 큰지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 짝수인지 혹은 홀수인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 다른 숫자들보다 작거나 같은지 검증합니다.",
        "이 검증기는 특정한 색의 숫자가 다른 숫자들보다 크거나 같은지 검증합니다.",
        "이 검증기는 모든 숫자의 합이 어떤 숫자의 배수인지 검증합니다.",
        "이 검증기는 특정한 두 숫자의 합이 4인지 검증합니다.",
        "이 검증기는 특정한 두 숫자의 합이 6인지 검증합니다.",
        "이 검증기는 특정한 색의 숫자를 1과 비교합니다.",
        "이 검증기는 특정한 색의 숫자를 3과 비교합니다.",
        "이 검증기는 특정한 색의 숫자를 4와 비교합니다.",
        "이 검증기는 어떤 숫자가 가장 작은지 혹은 가장 큰지 검증합니다.",
        "이 검증기는 <:bluetriangle:1273289917723705405>를 다른 특정한 색의 숫자와 비교합니다.",
        "이 검증기는 :yellow_square:를 다른 특정한 색의 숫자와 비교합니다.",
        "이 검증기는 1 또는 3이 몇 번 나타나는지 검증합니다.",
        "이 검증기는 3 또는 4가 몇 번 나타나는지 검증합니다.",
        "이 검증기는 1 또는 4가 몇 번 나타나는지 검증합니다.",
        "이 검증기는 특정한 색의 숫자 두 개를 비교합니다."
    ]

    creteria_description=[
        ["파란색이 1입니다", "파란색이 1보다 큽니다"],
        ["파란색이 3보다 작습니다", "파란색이 3입니다", "파란색이 3보다 큽니다"],
        ["노란색이 3보다 작습니다", "노란색이 3입니다", "노란색이 3보다 큽니다"],
        ["노란색이 4보다 작습니다", "노란색이 4입니다", "노란색이 4보다 큽니다"],
        ["파란색이 짝수입니다", "파란색이 홀수입니다"],
        ["노란색이 짝수입니다", "노란색이 홀수입니다"],
        ["보라색이 짝수입니다", "보라색이 홀수입니다"],
        ["1이 없습니다", "1이 1번 나타납니다", "1이 2번 나타납니다"],
        ["3이 없습니다", "3이 1번 나타납니다", "3이 2번 나타납니다"],
        ["4가 없습니다", "4가 1번 나타납니다", "4가 2번 나타납니다"],
        ["파란색이 노란색보다 작습니다", "파란색이 노란색과 같습니다", "파란색이 노란색보다 큽니다"],
        ["파란색이 보라색보다 작습니다", "파란색이 보라색과 같습니다", "파란색이 보라색보다 큽니다"],
        ["노란색이 보라색보다 작습니다", "노란색이 보라색과 같습니다", "노란색이 보라색보다 큽니다"],
        ["파란색이 노란색과 보라색보다 작습니다", "노란색이 파란색과 보라색보다 작습니다", "보라색이 파란색과 노란색보다 작습니다"],
        ["파란색이 노란색과 보라색보다 큽니다", "노란색이 파란색과 보라색보다 큽니다", "보라색이 파란색과 노란색보다 큽니다"],
        ["짝수가 더 많습니다", "홀수가 더 많습니다"],
        ["짝수가 없습니다", "짝수가 한 번 나타납니다", "짝수가 두 번 나타납니다", "짝수가 세 번 나타납니다"],
        ["모든 숫자의 합이 짝수입니다.", "모든 숫자의 합이 홀수입니다."],
        ["파란색과 노란색의 합이 6보다 작습니다.", "파란색과 노란색의 합이 6입니다", "파란색과 노란색의 합이 6보다 큽니다"],
        ["세 번 반복되는 숫자가 있습니다", "두 번 반복되는 숫자가 있습니다", "반복되는 숫자가 없습니다"],
        ["반복되는 숫자가 없거나, 세 번 반복되는 숫자가 있습니다", "두 번 반복되는 숫자가 있습니다"],
        ["오름차순입니다", "내림차순입니다", "오름차순이나 내림차순이 아닙니다"],
        ["모든 숫자의 합이 6보다 작습니다", "모든 숫자의 합이 6입니다", "모든 숫자의 합이 6보다 큽니다"],
        ["오름차순으로 숫자 세 개가 연속됩니다", "오름차순으로 숫자 두 개가 연속됩니다", "오름차순으로 연속된 숫자가 없습니다"],
        ["오름차순이나 내림차순으로 연속된 숫자가 없습니다","오름차순이나 내림차순으로 숫자 두 개가 연속됩니다", "오름차순이나 내림차순으로 숫자 세 개가 연속됩니다"],
        ["파란색이 3보다 작습니다", "노란색이 3보다 작습니다", "보라색이 3보다 작습니다"],
        ["파란색이 4보다 작습니다", "노란색이 4보다 작습니다", "보라색이 4보다 작습니다"],
        ["파란색이 1입니다", "노란색이 1입니다", "보라색이 1입니다"],
        ["파란색이 3입니다", "노란색이 3입니다", "보라색이 3입니다"],
        ["파란색이 4입니다", "노란색이 4입니다", "보라색이 4입니다"],
        ["파란색이 1보다 큽니다", "노란색이 1보다 큽니다", "보라색이 1보다 큽니다"],
        ["파란색이 3보다 큽니다", "노란색이 3보다 큽니다", "보라색이 3보다 큽니다"],
        ["파란색이 짝수입니다", "노란색이 짝수입니다", "보라색이 짝수입니다", "파란색이 홀수입니다", "노란색이 홀수입니다", "보라색이 홀수입니다"],
        ["파란색이 노란색과 보라색보다 작거나 같습니다", "노란색이 파란색과 보라색보다 작거나 같습니다", "보라색이 파란색과 노란색보다 작거나 같습니다"],
        ["파란색이 노란색과 보라색보다 크거나 같습니다", "노란색이 파란색과 보라색보다 크거나 같습니다", "보라색이 파란색과 노란색보다 크거나 같습니다"],
        ["세 수의 합이 3의 배수입니다","세 수의 합이 4의 배수입니다", "세 수의 합이 5의 배수입니다"],
        ["파란색과 노란색의 합이 4입니다", "파란색과 보라색의 합이 4입니다", "노란색과 보라색의 합이 4입니다"],
        ["파란색과 노란색의 합이 6입니다", "파란색과 보라색의 합이 6입니다", "노란색과 보라색의 합이 6입니다"],
        ["파란색이 1입니다", "노란색이 1입니다", "보라색이 1입니다","파란색이 1보다 큽니다","노란색이 1보다 큽니다","보라색이 1보다 큽니다"],
        ["파란색이 3보다 작습니다", "노란색이 3보다 작습니다","노란색이 3보다 작습니다","파란색이 3입니다", "노란색이 3입니다", "보라색이 3입니다","파란색이 3보다 큽니다","노란색이 3보다 큽니다","보라색이 3보다 큽니다"],
        ["파란색이 4보다 작습니다", "노란색이 4보다 작습니다","노란색이 4보다 작습니다","파란색이 4입니다", "노란색이 4입니다", "보라색이 4입니다","파란색이 4보다 큽니다","노란색이 4보다 큽니다","보라색이 4보다 큽니다"],    
        ["파란색이 가장 작습니다", "노란색이 가장 작습니다", "보라색이 가장 작습니다", "파란색이 가장 큽니다", "노란색이 가장 큽니다", "보라색이 가장 큽니다"],
        ["파란색이 노란색보다 작습니다", "파란색이 노란색과 같습니다", "파란색이 노란색보다 큽니다","파란색이 보라색보다 작습니다", "파란색이 보라색과 같습니다", "파란색이 보라색보다 큽니다"],
        ["노란색이 파란색보다 작습니다", "노란색이 파란색과 같습니다", "노란색이 파란색보다 큽니다","노란색이 보라색보다 작습니다", "노란색이 보라색과 같습니다", "노란색이 보라색보다 큽니다"],
        ["1이 없습니다", "1이 1번 나타납니다", "1이 2번 나타납니다","3이 없습니다", "3이 1번 나타납니다", "3이 2번 나타납니다"],
        ["3이 없습니다", "3이 1번 나타납니다", "3이 2번 나타납니다","4가 없습니다", "4가 1번 나타납니다", "4가 2번 나타납니다"],
        ["1이 없습니다", "1이 1번 나타납니다", "1이 2번 나타납니다","4가 없습니다", "4가 1번 나타납니다", "4가 2번 나타납니다"],
        ["파란색이 노란색보다 작습니다","파란색이 보라색보다 작습니다","노란색이 보라색보다 작습니다","파란색이 노란색과 같습니다","파란색이 보라색과 같습니다","노란색이 보라색과 같습니다","파란색이 노란색보다 큽니다","파란색이 보라색보다 큽니다","노란색이 보라색보다 큽니다"]
        
    ]    
    
    games: dict[int, TuringMachineGame]=  { }

    tm_successPlayer=[]
    tm_failPlayer=[]
    
    def __init__(self, bot) -> None:
        self.bot=bot

 

    def decode(self, _verifier_num_lst: list[int]): #return: [([verifier, verifier, ...], (t, s, c)),([verifier, verifier, ...], (t, s, c)),([verifier, verifier, ...], (t, s, c)),...]
        
        def all_creteria_comb(_verifier_num_lst: list[int]):
            result=[]
            for i in _verifier_num_lst:
                lst_each=[]
                for j in range(0, self.creteria_count_lst[i-1]):
                    lst_each.append(j)
                result.append(lst_each)
            result=product(*result)
            return list(result)
        
        result: list[tuple[list[Verifier], tuple[int, int, int]]] = []
        creteria_combination=all_creteria_comb(_verifier_num_lst)
        verifier_count=len(_verifier_num_lst)
        for i in range(0, len(creteria_combination)):
            verifier_lst: list[Verifier] = []
            for j in range(0, verifier_count):
                verifier_lst.append(Verifier(_verifier_num_lst[j], creteria_combination[i][j]))
                
            s: set = self.all_comb.copy()
            for j in range(0, len(_verifier_num_lst)):
                s = s & verifier_lst[j].possibleComb()
                
            if len(s) == 1:
                crt=True
                for _i in range(0, verifier_count):
                    _s=self.all_comb.copy()
                    for _j in range(0, verifier_count):
                        if _i != _j:
                            _s = _s & verifier_lst[_j].possibleComb()
                    if s==_s: crt=False
                        
                if crt:
                    result.append((verifier_lst, s.pop()))
                    
        return result

    def select_verifier(self, channel_id: int): 
        result: list[int]=[]
        game: TuringMachineGame = self.games[channel_id]
        if game.difficulty=="쉬움":
            while(not bool(self.decode(result))):
                result=[]
                _verifier_type=list(range(1, 18))
                for i in range(game.verifier_count):
                    v=random.choice(_verifier_type)
                    result.append(v)
                    
        elif game.difficulty=="보통":
            while(not bool(self.decode(result))):
                result=[]
                _verifier_type=list(range(1, 26))
                for i in range(game.verifier_count):
                    v=random.choice(_verifier_type)
                    result.append(v)
                        
        else:
            while(not bool(self.decode(result))):
                result=[]
                _verifier_type=self.verifier_type.copy()
                for i in range(game.verifier_count):
                    v=random.choice(_verifier_type)
                    _verifier_type.remove(v)
                    if isinstance(v, collections.abc.Iterable):
                        _v=random.choice(v)
                        result.append(_v)
                    else:
                        result.append(v)

        result.sort()
        return result
  
    def select_fake_verifier(self, real_verifier: list[int], difficulty: str):
        limit=0
        if difficulty=="쉬움":  limit=17
        elif difficulty=="보통": limit=25
        else: limit=48
        l=list(range(1, limit+1))
        for n in real_verifier:
            l.remove(n)
        result=list(random.choice(list(combinations(l, len(real_verifier)))))
        random.shuffle(result)
        return result
    
    def verifier_embed_generater(self, _verifiers_num_list: list[int], mode: str):
        embed=discord.Embed(title="이번 게임에 사용할 검증기 카드", description="ㅤ", color=0x49d44c)
        embed.set_author(name=f"{mode} 모드, 검증기 개수: {len(_verifiers_num_list)}")
        alphabet="ABCDEF"
        for i in range(len(_verifiers_num_list)):
            embed.add_field(name=f"{alphabet[i]}. {self.verifier_description[_verifiers_num_list[i]-1]}", value="", inline=False)
        
        return embed
    
    def verifier_embed_generater_for_extreme(self, _verifiers_num_list: list[int], _fake_verifiers_num_list: list[int], mode):
        embed=discord.Embed(title="이번 게임에 사용할 검증기 카드", description="ㅤ", color=0xfebd11)
        embed.set_author(name=f"{mode} 모드, 검증기 개수: {len(_verifiers_num_list)}")
        alphabet="ABCDEF"
        for i in range(len(_verifiers_num_list)):
            if _verifiers_num_list[i]<_fake_verifiers_num_list[i]:
                embed.add_field(name=f"{alphabet[i]}. {self.verifier_description[_verifiers_num_list[i]-1]}", value="또는", inline=False)
                embed.add_field(name=f"{alphabet[i]}. {self.verifier_description[_fake_verifiers_num_list[i]-1]}", value="", inline=False)
            else:
                embed.add_field(name=f"{alphabet[i]}. {self.verifier_description[_fake_verifiers_num_list[i]-1]}", value="또는", inline=False)
                embed.add_field(name=f"{alphabet[i]}. {self.verifier_description[_verifiers_num_list[i]-1]}", value="", inline=False)
            embed.add_field(name="" , value="", inline=False)
        
        return embed

    def verifier_test_result_generator(self, result: bool, code: tuple, idx: int, verifier_alpha:str, verifiers_num_list: list[int]):
        resultstring=""
        if result:
            resultstring="참 :o:"
        else:
            resultstring="거짓 :x:"
        embed=discord.Embed(title=f"검증 결과: {resultstring}", description="ㅤ", color=0x49d44c)
        embed.add_field(name=f"검증기: {verifier_alpha.upper()}", value=self.verifier_description[verifiers_num_list[idx]-1], inline=False)
        embed.add_field(name="임시 코드:", value=f"{code[0]}{code[1]}{code[2]}", inline=False)
        
        return embed

    def verifier_test_result_generator_for_extreme(self, result:bool, code:tuple, idx:int, verifier_alpha:str, verifiers_num_list: list[int], fake_verifiers_num_list: list[int]):
        resultstring=""
        if result:
            resultstring="참 :o:"
        else:
            resultstring="거짓 :x:"
        
        embed=discord.Embed(title=f"검증 결과: {resultstring}", description="ㅤ", color=0xfebd11)
        if verifiers_num_list[idx]<fake_verifiers_num_list[idx]:
            embed.add_field(name=f"검증기: {verifier_alpha.upper()}", value=self.verifier_description[verifiers_num_list[idx]-1], inline=False)
            embed.add_field(name="  또는", value=self.verifier_description[fake_verifiers_num_list[idx]-1], inline=False)
        else:
            embed.add_field(name=f"검증기: {verifier_alpha.upper()}", value=self.verifier_description[[idx]-1], inline=False)
            embed.add_field(name="  또는", value=self.verifier_description[verifiers_num_list[idx]-1], inline=False)
        embed.add_field(name="임시 코드:", value=f"{code[0]}{code[1]}{code[2]}", inline=False)
        
        return embed

    def game_end_generator(self, id: int):
        game: TuringMachineGame = self.games[id]
        if "성공" in game.response:
            embed=discord.Embed(title="게임 종료", description=f"{game.print_successed_player()}이(가) 정답을 맞췄습니다.", color=game.embed_color())
        else:
            embed=discord.Embed(title="게임 종료", description="아무도 정답을 맞추지 못했습니다.")
        alpha="ABCDEF"
        for i in range(len(game.verifiers_list)):
            embed.add_field(name=alpha[i], value=self.creteria_description[game.verifiers_list[i].verifier_num-1][game.verifiers_list[i].creteria_num], inline=False)
        embed.set_author(name=f"정답 코드: {game.answer[0]}{game.answer[1]}{game.answer[2]}")
        
        return embed

    async def send_verifier_image(self, thread: discord.Thread, verifier_num_list: list[int], fake_verifier_num_list: list[int], mode: str):
        alpha="ABCDEF"
        for i in range(len(verifier_num_list)):
            if mode=="클래식":
                embed=discord.Embed(title=f"검증기 {alpha[i]}", color=0x49d44c)
                embed.set_image(url=f"https://turingmachine.info/images/criteriacards/KR/TM_GameCards_KR-{str(verifier_num_list[i]).zfill(2)}.png")
                await thread.send(embed=embed)
            elif mode=="익스트림":
                if verifier_num_list[i]<fake_verifier_num_list[i]:
                    embed=discord.Embed(title=f"검증기 {alpha[i]} 후보", color=0xfebd11)
                    embed.set_image(url=f"https://turingmachine.info/images/criteriacards/KR/TM_GameCards_KR-{str(verifier_num_list[i]).zfill(2)}.png")
                    await thread.send(embed=embed)
                    embed=discord.Embed(title=f"검증기 {alpha[i]} 후보", color=0xfebd11)
                    embed.set_image(url=f"https://turingmachine.info/images/criteriacards/KR/TM_GameCards_KR-{str(fake_verifier_num_list[i]).zfill(2)}.png")
                    await thread.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"검증기 {alpha[i]} 후보", color=0xfebd11)
                    embed.set_image(url=f"https://turingmachine.info/images/criteriacards/KR/TM_GameCards_KR-{str(fake_verifier_num_list[i]).zfill(2)}.png")
                    await thread.send(embed=embed)
                    embed=discord.Embed(title=f"검증기 {alpha[i]} 후보", color=0xfebd11)
                    embed.set_image(url=f"https://turingmachine.info/images/criteriacards/KR/TM_GameCards_KR-{str(verifier_num_list[i]).zfill(2)}.png")
                    await thread.send(embed=embed)

    @app_commands.command(name="튜링머신", description="새로운 튜링머신 게임을 모집합니다.\n(모드 기본값: 클래식)")    
    @app_commands.describe(mode="모드(클래식, 익스트림)")
    async def scout(self, itc: discord.Interaction, mode: str = "클래식"):
        id = itc.channel.id
        if id in self.games:
            await itc.response.send_message("이미 모집 중이거나 진행 중인 게임이 있습니다.", ephemeral=True)
            return
        self.games[id]=TuringMachineGame(itc.user, mode)
        game: TuringMachineGame = self.games[id]
        if game.running:
            await itc.response.send_message("이미 게임이 진행 중입니다.")
            return

        
        if not (mode=="클래식" or mode=="익스트림"):
            await itc.response.send_message("모드는 클래식, 익스트림 두 종류만 가능합니다.", ephemeral=True)
            return
        game.mode=mode
        game.scouting=True
        
        embed=discord.Embed(title="튜링 머신", description=f"{itc.user.mention}님이 새로운 튜링 머신 게임을 모집합니다.", color=game.embed_color())
        embed.add_field(name=f"모드", value=mode, inline=True)
        embed.add_field(name="검증기 개수", value=game.verifier_count, inline=True)
        embed.add_field(name="난이도", value=game.difficulty, inline=True,)
        embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
        
        async def participate(_itc: discord.Interaction):
            if game.add_player(_itc.user):
                embed.remove_field(3)
                embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                await _itc.message.edit(embed=embed)
                await _itc.response.send_message(f"{_itc.user.mention}님이 게임에 참여했습니다.")
            else:
                await _itc.response.send_message(f"{_itc.user.mention}님은 이미 게임에 참여해 있습니다.", ephemeral=True)
       
        async def get_out(_itc: discord.Interaction):
            if game.del_player(_itc.user):
                if game.player_num()==0:
                    await game_cancel(_itc)
                    return
                else:
                    embed.remove_field(3)
                    embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                    await _itc.message.edit(embed=embed)
                    await _itc.response.send_message(f"{_itc.user.mention}님이 게임 참여를 취소했습니다.")
            else:
                await _itc.response.send_message("현재 게임에 참여하고 있지 않습니다.", ephemeral=True)
                
        async def set_difficulty(_itc: discord.Interaction):
            select=ui.Select()
            
            async def set_difficulty_callback(__itc: discord.Interaction):
                game.difficulty=select.values[0]
                embed.remove_field(2)
                embed.insert_field_at(2, name="난이도", value=game.difficulty, inline=True)
                await _itc.message.edit(embed=embed)
                await __itc.response.send_message(f"난이도를 {game.difficulty}으로 설정했습니다")
                
            select.add_option(label="쉬움", value="쉬움", description="직관적인 검증기만 사용합니다.",emoji="😃")
            select.add_option(label="보통", value="보통", description="조금 더 다양한 검증기를 사용합니다.",emoji="😐")
            select.add_option(label="어려움", value="어려움", description="난해한 검증기가 여럿 등장합니다.",emoji="😠")
            select.callback=set_difficulty_callback
            
            view=ui.View()
            view.add_item(select)
            await _itc.response.send_message(view=view, ephemeral=True)
            
        async def set_verifier_count(_itc: discord.Interaction):
            select=discord.ui.Select()
            
            async def set_verifier_count_callback(__itc: discord.Interaction):
                game.verifier_count=int(select.values[0])
                embed.remove_field(1)
                embed.insert_field_at(1, name="검증기 개수", value=game.verifier_count, inline=True)
                await _itc.message.edit(embed=embed)
                await __itc.response.send_message(f"검증기 개수를 {game.verifier_count}개로 설정했습니다")
                
            select.add_option(label="4개", value=4, description="검증기 4개의 기준을 찾아내세요!", emoji="4️⃣")
            select.add_option(label="5개", value=5, description="검증기 5개의 기준을 찾아내세요!",emoji="5️⃣")
            select.add_option(label="6개", value=6, description="검증기 6개의 기준을 찾아내세요!",emoji="6️⃣")
            select.callback=set_verifier_count_callback
            
            view=discord.ui.View()
            view.add_item(select)
            await _itc.response.send_message(view=view, ephemeral=True)
            
        async def start(_itc:discord.Interaction):
            if game.starter!=_itc.user: await _itc.response.send_message("처음 모집한 사람만 게임을 시작할 수 있습니다.", ephemeral=True)
            else:
                game.verifiers_num_list=self.select_verifier(_itc.channel.id)
                game.fake_verifiers_num_list=self.select_fake_verifier(game.verifiers_num_list, game.difficulty)
                decode_result=self.decode(game.verifiers_num_list)
                if len(decode_result)>1:
                    decode_result=random.choice(decode_result)
                else: 
                    decode_result=decode_result[0]
                game.verifiers_list=decode_result[0]
                game.answer=decode_result[1]
                print(f"정답: {game.answer}")
                    
                game.response=["코드 선정"] * game.player_num()
                
                async def command_help_callback(__itc: discord.Interaction):
                    embed=discord.Embed(title="명령어 도움말", description="ㅤ", color=game.embed_color())
                    embed.add_field(name="/코드 <code>", value="임시 코드를 <code>로 설정합니다.", inline=False)
                    embed.add_field(name=f"/검증 <verifier> (A~{chr(game.verifier_count+64)})", value="선택한 검증기에 임시 코드를 검증합니다.\n한 라운드에 최대 3번까지 할 수 있습니다.", inline=False)
                    embed.add_field(name="/정답 <code>", value="정답을 알아냈다면, 정답 코드를 입력할 수 있습니다. \n 정답을 입력할 수 있는 기회는 게임 중 단 한 번입니다.", inline=False)
                    embed.add_field(name="/계속", value="정답을 알아내지 못한 것 같다면 이 선택을 할 수 있습니다.\n모두가 '계속'을 선택하면, 다음 라운드로 넘어갑니다.", inline=False)
                    await __itc.response.send_message(embed=embed, ephemeral=True)
                    
                btn_command_help=discord.ui.Button(style=discord.ButtonStyle.blurple, label="명령어 도움말", row=0)
                btn_command_help.callback=command_help_callback
                
                btn_game_cancel=discord.ui.Button(style=discord.ButtonStyle.red, label="게임 취소", row=0)
                btn_game_cancel.callback=game_cancel
                
                view=ui.View()
                view.add_item(btn_command_help)
                view.add_item(btn_game_cancel)
                
                if game.mode=="클래식":
                    await _itc.response.edit_message(embed=self.verifier_embed_generater(game.verifiers_num_list, game.mode), view=view)
                elif game.mode=="익스트림":
                    await _itc.response.edit_message(embed=self.verifier_embed_generater_for_extreme(game.verifiers_num_list, game.fake_verifiers_num_list, game.mode), view=view)
                game.scouting=False
                game.running=True
                
                msg = await _itc.original_response()
                thread = await msg.create_thread(name="검증기 이미지") 
                await self.send_verifier_image(thread, game.verifiers_num_list, game.fake_verifiers_num_list, game.mode)
                        
        async def game_cancel(_itc: discord.Interaction):
            game=self.games[_itc.channel.id]
            if game.starter==_itc.user:
                del self.games[_itc.channel.id]
                await _itc.response.send_message("모집을 취소합니다.")
                await _itc.message.delete()
            else:
                await _itc.response.send_message("처음 모집한 사람만 게임을 취소할 수 있습니다.", ephemeral=True)
                
                
        btn_participate=discord.ui.Button(style=discord.ButtonStyle.blurple, label="참가",row=0)
        btn_participate.callback = participate
        
        btn_get_out=discord.ui.Button(style=discord.ButtonStyle.gray, label="참가 취소", row=0)
        btn_get_out.callback = get_out
        
        btn_start=discord.ui.Button(style=discord.ButtonStyle.green, label="시작", row=0)
        btn_start.callback=start
        
        btn_game_cancel=discord.ui.Button(style=discord.ButtonStyle.red, label="게임 취소", row=0)
        btn_game_cancel.callback=game_cancel
        
        btn_count=discord.ui.Button(style=discord.ButtonStyle.primary, label="검증기 개수 변경",row=1)
        btn_count.callback = set_verifier_count
        
        btn_difficulty=discord.ui.Button(style=discord.ButtonStyle.primary, label="난이도 변경", row=1)
        btn_difficulty.callback = set_difficulty
        
        view=ui.View()
        view.add_item(btn_participate)
        view.add_item(btn_get_out)
        view.add_item(btn_game_cancel)
        view.add_item(btn_start)
        view.add_item(btn_count)
        view.add_item(btn_difficulty)
        
        await itc.response.send_message(embed=embed, view=view)

    @app_commands.command(name="코드", description="새로운 임시 코드를 설정합니다.")      
    @app_commands.describe(code="1~5의 숫자로 이루어진 세 자리 자연수")
    async def set_code(self, itc:discord.Interaction, code: int):
        try:
            game=self.games[itc.channel.id]
        except KeyError:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        if game.scouting:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        elif not game.is_player(itc.user):
            await itc.response.send_message("게임에 참여하고 있지 않습니다.", ephemeral=True)
            return
        elif game.is_failed_player(itc.user):
            await itc.response.send_message("당신은 탈락했습니다.", ephemeral=True)
            return
        elif game.response[game.find_player(itc.user)]=="성공":
            await itc.response.send_message("지금은 임시 코드를 설정할 수 없습니다.", ephemeral=True)
            return
        elif game.response[game.find_player(itc.user)]=="추리":
            await itc.response.send_message("한 라운드에 임시 코드를 여러 번 설정할 수 없습니다.", ephemeral=True)
            return
        else:
            class InvalidCodeError(Exception):
                pass
            try:
                t=code//100
                s=(code % 100)//10
                c=(code % 100) % 10
                if t<1 or s<1 or c<1 or t>5 or s>5 or c>5:
                    raise InvalidCodeError()
                p=game.players[game.find_player(itc.user)]
                p.code=(t, s, c)
                p.code_generate_total+=1
                p.test_count=0
                game.response[game.find_player(itc.user)]="추리"
                await itc.response.send_message(f"임시 코드를 {code}로 설정했습니다.", ephemeral=True)
                
            except InvalidCodeError:
                await itc.response.send_message("코드는 '1~5'의 숫자로 이루어진 세 자리 숫자여야 합니다.",ephemeral=True)
                return
                
    @app_commands.command(name="검증", description="선택한 검증기에 임시 코드를 검증합니다.")      
    @app_commands.describe(verifier="검증기 번호(A, B, C...)")
    async def test_code(self, itc: discord.Interaction, verifier: str):
        try:
            game=self.games[itc.channel.id]
        except KeyError:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        if game.scouting:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        elif not game.is_player(itc.user):
            await itc.response.send_message("게임에 참여하고 있지 않습니다.", ephemeral=True)
            return
        elif game.is_failed_player(itc.user):
            await itc.response.send_message("당신은 탈락했습니다.", ephemeral=True)
            return
        elif game.response[game.find_player(itc.user)]=="코드 선정":
            await itc.response.send_message("지금은 검증할 수 없습니다. 먼저 임시 코드를 설정해주세요.", ephemeral=True)
            return
        elif game.response[game.find_player(itc.user)]=="성공":
            await itc.response.send_message("지금은 임시 코드를 설정할 수 없습니다.", ephemeral=True)
            return
        else:
            if len(verifier)==1 and verifier.isalpha() and 0<=ord(verifier.lower())-97<game.verifier_count:
                test_card=verifier.lower()
                idx=ord(test_card)-97
                p=game.players[game.find_player(itc.user)]
                if p.test_count<3:
                    if game.mode=="클래식":
                        await itc.response.send_message(embed=self.verifier_test_result_generator(game.verifiers_list[idx].verifier_TF(p.code[0], p.code[1], p.code[2]), p.code, idx, verifier, game. verifiers_num_list), ephemeral=True)
                    elif game.mode=="익스트림":
                        await itc.response.send_message(embed=self.verifier_test_result_generator_for_extreme(game.verifiers_list[idx].verifier_TF(p.code[0], p.code[1], p.code[2]), p.code, idx, verifier, game.verifiers_num_list, game.fake_verifiers_num_list),ephemeral=True)
                    p.test_count+=1
                    p.test_count_total+=1
                else:
                    await itc.response.send_message("더 이상 이 임시 코드로 검증을 진행할 수 없습니다.", ephemeral=True)

            else: await itc.response.send_message(f"검증기를 정확히(A~{chr(game.verifier_count+64)}) 입력해주세요.", ephemeral=True)
              
    @app_commands.command(name="정답", description="정답 코드를 맞힙니다. 기회는 단 한 번입니다.")      
    @app_commands.describe(code="1~5의 숫자로 이루어진 세 자리 자연수")
    async def submit(self, itc: discord.Interaction, code: int):
        id=itc.channel.id
        try:
            game=self.games[id]
        except KeyError:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        if game.scouting:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        elif not game.is_player(itc.user):
            await itc.response.send_message("게임에 참여하고 있지 않습니다.", ephemeral=True)
            return
        elif game.is_failed_player(itc.user):
            await itc.response.send_message("당신은 탈락했습니다.", ephemeral=True)
            return
        elif game.response[game.find_player(itc.user)]=="코드 선정":
            await itc.response.send_message("지금은 정답을 제출할 수 없습니다. 먼저 임시 코드를 설정하고 검증해주세요.", ephemeral=True)
            return
        else:
            class InvalidCodeError(Exception):
                pass
            try:
                t=code//100
                s=(code % 100)//10
                c=(code % 100) % 10
                if t<1 or s<1 or c<1 or t>5 or s>5 or c>5:
                    raise InvalidCodeError()
                
            except InvalidCodeError:
                await itc.response.send_message("코드는 '1~5'의 숫자로 이루어진 세 자리 숫자여야 합니다.",ephemeral=True)
                return
            
            if (t, s, c)==game.answer:
                game.response[game.find_player(itc.user)]="성공"
                game.add_successed_player(game.players[game.find_player(itc.user)])
            else:
                game.response[game.find_player(itc.user)]="실패"
                game.add_failed_player(itc.user)
                
            if "추리" not in game.response:
                if "성공" in game.response:
                    await itc.response.send_message(embed=self.game_end_generator(id))
                    del self.games[itc.channel.id]
                elif "실패" in game.response and "계속" in game.response:
                    await itc.response.send_message(f"{game.print_failed_mention()}님이 탈락했습니다. 게임을 이어갑니다.\n다음 임시 코드를 설정해주세요.")
                    game.next_round()
                elif "실패" in game.response and "계속" not in game.response:
                    await itc.response.send_message(embed=self.game_end_generator(id))
                    del self.games[itc.channel.id]
                else:
                    await itc.response.send_message("모두가 정답을 알아내지 못했습니다. 게임을 이어갑니다.\n다음 임시 코드를 설정해주세요.")
                    game.next_round()
            else: 
                await itc.response.send_message("정답을 제출했습니다.\n아직 추리 중인 플레이어가 있으니 잠시 기다리거나, 어서 닦달하세요.", ephemeral=True)   
                
    @app_commands.command(name="계속", description="이번 라운드를 마치고 다음 라운드로 넘어갑니다.")
    async def nextround(self, itc: discord.Interaction):
        try:
            game=self.games[itc.channel.id]
        except IndexError:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        if game.scouting:
            await itc.response.send_message("지금은 게임 중이 아닙니다.", ephemeral=True)
            return
        elif not game.is_player(itc.user):
            await itc.response.send_message("게임에 참여하고 있지 않습니다.", ephemeral=True)
            return
        elif game.is_failed_player(itc.user):
            await itc.response.send_message("당신은 탈락했습니다.", ephemeral=True)
            return
        else:
            game.response[game.find_player(itc.user)]="계속"
            if "추리" not in game.response:
                if "성공" in game.response:
                    await itc.response.send_message(embed=self.game_end_generator(id))
                    del self.games[itc.channel.id]
                elif "실패" in game.response and "계속" in game.response:
                    await itc.response.send_message(f"{game.print_failed_mention()}님이 탈락했습니다. 게임을 이어갑니다.\n다음 임시 코드를 설정해주세요.")
                    game.next_round()
                elif "실패" in game.response and "계속" not in game.response:
                    await itc.response.send_message(embed=self.game_end_generator(id))
                    del self.games[itc.channel.id]
                else:
                    await itc.response.send_message("모두가 정답을 알아내지 못했습니다. 게임을 이어갑니다.\n다음 임시 코드를 설정해주세요.")
                    game.next_round()
            else: 
                await itc.response.send_message("아직 추리 중인 플레이어가 있습니다. 잠시 기다리거나, 어서 닦달하세요.", ephemeral=True)   
    
