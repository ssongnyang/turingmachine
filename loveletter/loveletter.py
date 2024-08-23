import discord
from discord import ui, app_commands
from discord.ext import commands
import random

from loveletter.card import Card
from loveletter.result import *
from loveletter.loveletterplayer import LoveLetterPlayer



class LoveLetterGame():
    def __init__(self, players: list[LoveLetterPlayer], ban_knight: bool, thread: discord.Thread, win_condition: int) -> None:
        self.ban_knight=ban_knight
        self.turn: int=0
        self.members=players
        self.players = self.members[:]
        self.starter=self.players[0]
        self.thread=thread
        self.win_condition=win_condition
        
        
    def  player_num(self):
        return len(self.players)

    def previous_player(self):
            return self.players[(self.turn-1) % self.player_num()]
    
    def now_player(self):
        return self.players[self.turn % self.player_num()]
    
    
    def find_player(self, player: LoveLetterPlayer | int) -> LoveLetterPlayer:
        for p in self.players:
            if p==player:
                return p
    
    async def del_player(self, player: LoveLetterPlayer):
        for p in self.players:
            if p==player: 
                self.players.remove(player)
                if self.player_num()==len(self.members)-1:
                    self.starter=p
                return True
        return False
    
    def rearrange(self):
        f=False
        for p in self.members * 2:
            if p==self.starter:
                self.players.clear()
                f=True
            if f:
                self.players.append(p)
                if len(self.players)==len(self.members):
                    for p in self.players:
                        p.card.clear()
                        p.card_emoji_msg=None
                        p.view_msg=None
                        p.select_msg=None
                        p.used_card.clear()
                        p.protected= False
                    return
    
    def print_player_mention(self, between: str="\n"):
        string=""
        for p in self.members:
            string+=p.client.mention+between
        return string[:-len(between)]
    
    def create_cardlist(self, ban_knight: bool):
        result=[Card(1)]* 5 + [Card(2)] * 2 + [Card(4)] * 2 + [Card(5)] * 2 + [Card(6)] + [Card(7)] + [Card(8)]
        if not ban_knight:
            result+=[Card(3)] * 2
        random.shuffle(result)
        hidden=random.randint(0, len(result)-1)
        result.pop(hidden)
        return result
    
    async def start(self):
        try:
            for p in self.players:
                await p.itc.response.defer()
        except discord.errors.InteractionResponded:
            pass
            
            
        for p in self.members:
            if p.token==self.win_condition:
                embed=discord.Embed(title="러브레터", description=f"{p.client.mention}님이 우승하였습니다!\nㅤ\n게임을 종료합니다.", color=LoveLetter.embed_color)
                await self.thread.send(embed=embed)
                embed=discord.Embed(title="러브레터", description=f"{self.starter.client.mention}님이 새로운 러브레터 게임을 시작했습니다.\nㅤ\n{p.client.mention}님이 우승하였습니다!", color=LoveLetter.embed_color)
                embed.set_image(url=p.client.display_avatar.url)
                await p.itc.followup.edit_message(message_id=self.thread.id, embed=embed)
                await self.thread.edit(archived=True)
                return
        
        
        self.rearrange() #카드 클리어
        self.turn=0
        
        
        self.cardlist=self.create_cardlist(self.ban_knight)
        
        for p in self.players[1:]:
            await self.draw_card(p, card=True, selection=False)
        await self.draw_card(self.players[0], card=False, selection=False)
        await self.draw_card(self.players[0], card=True, selection=True)
        await self.update_embed(result = None, first=True)
    
    
    async def draw_card(self, player: LoveLetterPlayer, card: bool, selection: bool = True):
        try:
            player.card.append(self.cardlist.pop())
        except IndexError: ##카드를 다 뽑음
            self.update_embed_final()
            self.start()
            return
        print(player.client.display_name + "drawed")
        #player.sort_card()
        if card:
            await self.send_card(player)
        if selection:
            await self.send_selection(player, itc=player.itc)
    
    
     
            
            
    async def send_selection(self, user: LoveLetterPlayer, itc: discord.Interaction):
        card_select=ui.Select(placeholder="낼 카드를 선택하세요.")
        async def card_select_callback(itc: discord.Interaction):
            selected=int(card_select.values[0])
            if selected in (1, 2, 3, 5, 6):
                target_select=ui.Select(placeholder=f"{Card(selected).card_name()} 카드를 사용할 대상을 선택하세요.")
                if selected==5:
                    target_select.add_option(label=user.client.display_name, value=user.client.id)
                for p in self.players:
                    if p!=user and p.protected==False:
                        target_select.add_option(label=p.client.display_name, value=p.client.id)
                if len(target_select.options)==0: # 지목할 대상 없음
                    await self.update_embed(await self.use(user, Card(selected)))
                    if self.player_num()==1:
                        await self.start()
                        return 
                              
                async def target_select_callback(_itc: discord.Interaction):
                    target=self.find_player(int(target_select.values[0]))
                    if selected==1:
                        number_select=ui.Select(placeholder=f"{target.client.display_name}님이 갖고 있을 카드를 예측하세요.")
                        for i in range(2, 9):
                            number_select.add_option(label=f"{Card(i).card_name()} ({i})", value=i, description=Card(i).card_simple_description())
                        
                        async def number_select_callback(__itc: discord.Interaction):
                            value=int(number_select.values[0])
                            await self.update_embed(await self.use(user, Card(selected), target, value))
                            if self.player_num()==1:
                              await self.start()
                        
                        number_select.callback=number_select_callback
                        view=ui.View()
                        view.add_item(number_select)
                        await _itc.response.edit_message(view=view)
                        #await user.itc.followup.edit_message(message_id=user.select_msg.id, view=view)
                        #await user.select_msg.edit(view=view)
                        
                    else:
                        await self.update_embed(await self.use(user, Card(selected), target))
                        if self.player_num()==1:
                            await self.start()
                            
                target_select.callback=target_select_callback
                view=ui.View()
                view.add_item(target_select)
                await itc.response.edit_message(view=view)
                #await user.select_msg.edit(view=view)
                
            else: # selected in (4, 7, 8)
                await self.update_embed(await self.use(user, Card(selected)))
                if self.player_num()==1:
                    await self.start()
                
        if (Card(7) in user.card and Card(5) in user.card) or (Card(7) in user.card and Card(6) in user.card):
            card=Card(7)
            card_select.add_option(label=f"{card.card_name()} ({card.num})", value=card.num, description=card.card_simple_description())
        else:
            for card in set(user.card):
                card_select.add_option(label=f"{card.card_name()} ({card.num})", value=card.num, description=card.card_simple_description())
        card_select.callback=card_select_callback
        view=ui.View()
        view.add_item(card_select)
        
        user.select_msg = await user.itc.followup.send(view=view, ephemeral=True, wait=True)
        
        
        
    async def send_card(self, player: LoveLetterPlayer):
        if player.card_emoji_msg:
            await player.itc.followup.edit_message(message_id=player.card_emoji_msg.id, content=player.show_card_emoji())
        else: 
            player.card_emoji_msg = await player.itc.followup.send(player.show_card_emoji(), ephemeral=True)
    
    
    
    async def use(self, user: LoveLetterPlayer, card: Card, target: LoveLetterPlayer | None = None, value: int | None = None):
        user.discard_card(card)
        await user.select_msg.delete()
        if len(user.used_card)>0 and user.used_card[-1].num==4:
            user.protected=False
        user.used_card.append(card)
        if target == None:
            if card.num==4:
                user.protected=True
                return NontargetResult(user, card)
            elif card.num==7:
                return NontargetResult(user, card)
            elif card.num==8:
                await self.del_player(user)
                return NontargetResult(user, card)
            else:
                return NontargetResult(user, card)
        else:
            if card.num==1:
                if target.card[0].num==value:#탈락
                    await self.del_player(target)
                    return KillResult(user, card, target, target)
                else: #진행
                    return GuardResult(user, card, target, value)
            if card.num==2: # 진행
                return TargetResult(user, card, target)
            if card.num==3:
                if user.card[0].num>target.card[0].num: #탈락
                    await self.del_player(target)
                    return KillResult(user, card, target, target)
                elif user.card[0].num<target.card[0].num: #탈락
                    await self.del_player(user)
                    return KillResult(user, card, target, user)
                else: 
                    return NontargetResult(user, card)
            
            if card.num==5:
                if len(self.cardlist)==1:
                    return NontargetResult(user, card)
                elif target.discard_card().num==8: #탈락
                    await self.del_player(target)
                    return AccidentResult(user, card, target)
                else: 
                    await self.draw_card(target, card=True, selection=False)
                    return TargetResult(user, card, target)
            if card.num==6:
                temp=user.card.copy()
                user.card = target.card.copy()
                target.card=temp.copy()
                return TargetResult(user, card, target)



    async def update_embed_final(self):
        embed=discord.Embed(
        title="러브레터", 
        description="덱의 카드가 다 떨어져 게임이 종료되었습니다.",
        color=LoveLetter.embed_color
            )
        
        
        maxplayer=[self.players[0]]
        for p in self.players:
            if p.card[0].num>maxplayer[0].card[0].num:
                maxplayer=[p]
            elif p.card[0].num==maxplayer[0].card[0].num:
                maxplayer.append(p)
        embed.add_field(name=f"최고 숫자: {maxplayer[0].card[0].num}", value=f"{self.print_player_mention(", ")}님이 토큰 1개를 획득합니다.")
        for p in maxplayer:
            p.token+=1
        
        embed.add_field(name="플레이어", value=self.print_player_mention())    
        value=""
        for p in self.members:
            value+=f"{p.token}개\n"
        embed.add_field(name="토큰", value=value)
        value=""
        
        await self.embed_msg.edit(embed=embed)
        
        
    async def update_embed(self, result: ResultMessage | None = None, first: bool = False):
        embed=discord.Embed(
            title="러브레터", 
            color=LoveLetter.embed_color
            )
        if self.player_num()==1:
            self.players[0].token+=1
            embed.insert_field_at(0, name="", value=f"{self.players[0].client.mention}님이 토큰 1개를 획득합니다.", inline=False)
        else:
            if not first:
                await self.send_card(self.now_player())
                self.turn+=1
                await self.draw_card(self.now_player(), card=True, selection=True)
            embed.add_field(name="", value=f"{self.now_player().client.mention}님의 차례입니다.\nㅤ\n", inline=False)
            
        embed.add_field(name="플레이어", value=self.print_player_mention())
        value=""
        for p in self.members:
            value+=f"{p.token}개\n"
        embed.add_field(name="토큰", value=value)
        value=""
        for p in self.members:
            if p==self.now_player():
                value+="✅\n"
            else: value+="ㅤ\n"
        
        embed.add_field(name="현재 차례", value=value)
        embed.set_footer(text=f"턴: {self.turn+1}")
        
        
        
        
        
        if first:
            self.embed_msg = await self.thread.send(embed=embed)
        else:
            if result.description().ephemeral:
                embed.insert_field_at(0, name="", value=result.result(), inline=False)
                await self.previous_player().itc.followup.send(content=result.description().msg, ephemeral=True)
            else:
                embed.insert_field_at(0, name="", value=result.result()+"\n"+result.description().msg, inline=False)
            
            await self.embed_msg.edit(embed=embed)
        
        
        
    
class LoveLetterGameManager:
    
    scouting: bool = True
    running: bool = False
    
    def __init__(self, starter: LoveLetterPlayer) -> None:
        self.starter=starter
        self.players: list[LoveLetterPlayer] = [starter]
        self.win_condition: int = 5
        self.ban_knight= True
        
        self.thread=None
        self.root_msg=None
        

        
    
        
        
    
        
    async def start(self, itc: discord.Interaction):
        self.running = True
        
        self.thread = await self.root_msg.create_thread(name='게임 보기')
        
        self.round=LoveLetterGame(self.players, self.ban_knight, self.thread, self.win_condition)
        await self.round.start()
        
            
    def next_player(self):
        pass
        
    def find_player(self, player: discord.Member):
        for i in range(self.player_num()):
            if self.players[i]==player:
                return i
        return False
        
    
    
    def player_num(self):
        return len(self.players)
    
    def is_player(self, player: discord.Member):
        for p in self.players:
            if p==player:
                return True
        return False
    
    
    
    def add_player(self, player: discord.Interaction):
        if not self.is_player(player.user):
            self.players.append(LoveLetterPlayer(player))
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

    def ban_knight_str(self):
        if self.ban_knight: return "제외"
        else: return "포함"
    
    
    
class LoveLetter(commands.Cog):
    games: dict[int, LoveLetterGameManager] = {}
    embed_color=0x88001b
    
    def end_game(self, id: int):
        del(self.games[id])
    
    def __init__(self, bot):
        self.bot=bot



    @app_commands.command(name="러브레터", description="새로운 러브레터 게임을 모집합니다.")
    @app_commands.choices(승리조건=[
        app_commands.Choice(name='3개', value=3),
        app_commands.Choice(name='4개 (4인 적합)', value=4),
        app_commands.Choice(name='5개 (3인 적합)', value=5),
        app_commands.Choice(name='6개', value=6),
        app_commands.Choice(name='7개 (2인 적합)', value=7)
    ])
    @app_commands.choices(기사카드=[
        app_commands.Choice(name='포함', value=0),
        app_commands.Choice(name='제외', value=1),
    ])
    async def scout(self, itc: discord.Interaction, 승리조건: int, 기사카드: int):
        id = itc.channel.id
        if id in self.games:
            await itc.response.send_message("이미 모집 중이거나 진행 중인 게임이 있습니다.", ephemeral=True)
            return
        self.games[id]= LoveLetterGameManager(LoveLetterPlayer(itc))
        game: LoveLetterGameManager = self.games[id]
        if game.running:
            await itc.response.send_message( "이미 게임이 진행 중입니다.", ephemeral=True)
            return
        game.win_condition=승리조건
        game.ban_knight=bool(기사카드)
        embed=discord.Embed(title="러브레터", description=f"{itc.user.mention}님이 새로운 러브레터 게임을 모집합니다.", color=self.embed_color)
        embed.add_field(name="승리 조건", value=f"토큰 {game.win_condition}개", inline=True)
        embed.add_field(name="3번(기사) 카드", value=game.ban_knight_str(), inline=True,)
        embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
        
        async def participate(_itc: discord.Interaction):
            await _itc.response.defer()
            if game.add_player(_itc):
                embed.remove_field(2)
                embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                await _itc.message.edit(embed=embed)
            else:
                await _itc.response.send_message(f"{_itc.user.mention}님은 이미 게임에 참여해 있습니다.", ephemeral=True)
        
        async def get_out(_itc: discord.Interaction):
            if game.del_player(_itc.user):
                if game.player_num()==0:
                    await game_cancel(_itc)
                    return
                else:
                    embed.remove_field(2)
                    embed.add_field(name="현재 멤버", value=game.print_player_mention(), inline=True)
                    await _itc.message.edit(embed=embed)
                    await _itc.response.send_message("참여를 취소했습니다.", ephemeral=True)
            else:
                await _itc.response.send_message("현재 게임에 참여하고 있지 않습니다.", ephemeral=True)
         
        async def start(_itc: discord.Interaction):
            if game.starter!=_itc.user: 
                await _itc.response.send_message("처음 모집한 사람만 게임을 시작할 수 있습니다.", ephemeral=True)
                return
            
                
            async def card_help_callback(__itc: discord.Interaction):
                embed=discord.Embed(title="러브레터 카드 참조표", description="ㅤ", color=self.embed_color)
                for i in range(1, 9):
                    card=Card(i)
                    embed.add_field(name=f"{card.num} - {card.card_name()}", value=card.card_description(), inline=False)
                await __itc.response.send_message(embed=embed, ephemeral=True)
                
            btn_command_help=discord.ui.Button(style=discord.ButtonStyle.blurple, label="카드 종류", row=0)
            btn_command_help.callback=card_help_callback
            
            btn_game_cancel=discord.ui.Button(style=discord.ButtonStyle.red, label="게임 취소", row=0)
            btn_game_cancel.callback=game_cancel
            
            view=ui.View()
            view.add_item(btn_command_help)
            view.add_item(btn_game_cancel)
            
            game.scouting=False
            game.running=True
            
            embed=discord.Embed(title="러브레터", description=f"{game.starter.client.mention}님이 새로운 러브레터 게임을 시작했습니다.\nㅤ\n스레드에서 진행을 확인하세요.", color=self.embed_color)

            #msg = await _itc.original_response()
            #thread = await game.root_msg.create_thread(name="게임 보기") 
            #await thread.send("ㅇ")
            await _itc.response.defer()
            await _itc.followup.edit_message(message_id=_itc.message.id, embed=embed, view=view)
            await game.start(itc)
                        
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
        
        
        
        view=ui.View()
        view.add_item(btn_participate)
        view.add_item(btn_get_out)
        view.add_item(btn_game_cancel)
        view.add_item(btn_start)
        
        msg = await itc.response.send_message(embed=embed, view=view)
        async for msg in itc.channel.history(limit=1):
            game.root_msg=msg
                