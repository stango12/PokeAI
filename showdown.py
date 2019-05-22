#some file to read the game state
import requests
from bs4 import BeautifulSoup
import asyncio
import websockets
import json
from constants import *

# URL = "https://play.pokemonshowdown.com/battle-gen7randombattle-897500568"

# r = requests.get(url = URL)
# plain_text = r.text 

# soup = BeautifulSoup(plain_text, 'html.parser')

# f = open("output.txt", "w")
# f.write(soup.get_text())
# f.close()

move_convert = json.load(open('move_convert.json'))
bot_name = "testBot218"
bot_pass = "testBot"

class PSClient:

    async def connectToPoke(self):
        #async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as websocket:
        self.websocket = await websockets.connect('ws://sim.smogon.com:8000/showdown/websocket')
        await self.websocket.send("asdf")
        test = ""
        msg = await self.websocket.recv()
        test = await self.websocket.recv()
        print(test[10:])
        resp = requests.post("https://play.pokemonshowdown.com/action.php?",
        		data = {
        			'act': 'login',
        			'name': bot_name,
        			'pass': bot_pass,
        			'challstr': test[10:]
        		})
        r = json.loads(resp.text[1:])
        a = r['assertion']
        await self.websocket.send("|/trn " + bot_name + ",0," + a)
        #await self.challenge_user("asdfqqq", "gen7randombattle")
        
        # await websocket.send("|/challenge asdfqqq, gen7randombattle")
        # async for msg in self.websocket:
        #     print("\n START \n")
        #     print(msg)
        #     print("-----FINISHED-----")
        #     await self.websocket.send(input())

    async def send_message(self, room, message1, message2=None):
        if message2:
            msg = room + '|' + message1 + '|' + message2
        else:
            msg = room + '|' + message1
        print("Sent: " + msg)
        await self.websocket.send(msg)

    async def read_message(self, amount=1, offset=0):
        message = []
        for i in range(offset):
            await self.websocket.recv()
        for i in range(amount):
            m = await self.websocket.recv()
            message.append(m)
        print("-----Recieved-----")
        print(message)
        return message

    #NOTE: If bot is p1(opponent is p2), turn is even number(starting at 2) else start at 3
    async def challenge_user(self, user, mode):
        await self.websocket.send("|/challenge " + user + ", " + mode)
        resp = await self.read_message(3, 11)
        self.battleID = resp[0].partition("\n")[0][1:]
        team_data = json.loads(resp[1].split("|")[2])
        self.turn_number = team_data['rqid']
        if self.turn_number % 2 == 0:
            self.my_number = 'p1'
            self.enemy_number = 'p2'
        else:
            self.my_number = 'p2'
            self.enemy_number = 'p1'
        self.my_team = await self.make_team(team_data)
        self.enemy_team = Team()
        #Get active pokemon data
        data = resp[2].split("\n")
        for d in data:
            if 'switch' in d:
                temp = d[13:]
                temp = temp[:temp.find('|')]
                if self.my_number + 'a' in d:
                    self.my_team.set_current(temp)
                else:
                    self.enemy_team.add_pokemon_name(temp)
                    self.enemy_team.set_current(temp)

        await self.print_team(self.my_team)
        print(self.my_team.get_current().name)
        print(self.enemy_team.get_current().name)

    async def make_team(self, team_json):
        t = Team()
        count = 0
        for p in team_json['side']['pokemon']:
            print(count)
            comma = p['details'].find(',')
            poke_name = p['details'][:comma].lower()
            if poke_name == 'darmanitan':
                poke_name = 'darmanitan-standard'
            elif 'silvally' in poke_name:
                poke_name = 'silvally'
            elif 'shaymin' == poke_name:
                poke_name += '-land'
            elif 'thundurus' in poke_name or 'tornadus' in poke_name or 'landorus' in poke_name:
                poke_name += -'therian'
            poke = Pokemon(poke_name.replace(' ', '-'), p['item'], p['ability'])
            for m in p['moves']:
                m = 'hiddenpower' if 'hiddenpower' in m else m
                poke.add_move(move_convert[m])
            t.add_pokemon(poke)
            count += 1
        return t
        
    #Main loop to decide action (do move or switch pokemon?)
    #NOTE: move number and pokemon number start at 1
    async def decide_action(self):
        return

    async def send_move(self, move):
        await self.websocket.send(self.battleID + "|/choose move " + str(move) + "|" + str(self.turn_number))
        self.turn_number += 2

    async def send_pokemon(self, pokemon):
        await self.websocket.send(self.battleID + "|/choose switch " + str(pokemon) + "|" + str(self.turn_number))
        self.turn_number += 2
        
    async def print_team(self, team_obj):
        team = team_obj.get_team()
        for p in team:
            print("")
            print(p.name + ":" + p.ability + "---" + p.item)
            print("-----Moves-----")
            for m in p.moves:
                print(m.name + ":" + m.type)

async def test():
    pokemonWS = PSClient()
    await pokemonWS.connectToPoke()
    await pokemonWS.challenge_user("asdfqqq", "gen7randombattle")

asyncio.get_event_loop().run_until_complete(test())

# testBot218
# testBot

# async def hello(url):
# 	async with websockets.connect(url) as websocket:
# 		async for message in websocket:
# 			print("\n START \n")
# 			print(message)
# 			await websocket.send(input())
# 			print("-----FINISHED-----")