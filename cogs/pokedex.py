'''
MIT License

Copyright (c) 2017 Cree-Py

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Import dependencies
import discord
from discord.ext import commands
import json
import aiohttp
import random

class Pokedex:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def pokemon(self, ctx):
        '''Base group for pokemon commands.'''
        await ctx.send("Pokemon commands:\n`-pokemon random` Get stats about a random pokemon.\n`-pokemon info <pokemon>` Get info about a pokemon. You can use the name or international pokedex ID.\n**Note:** A lot of the time the API response time is slow so please be patient.")
        
    @pokemon.command()
    async def random(self, ctx):
        '''Get stats about a random pokemon.'''
        await ctx.trigger_typing()
        num = random.randint(1, 721)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://pokeapi.co/api/v2/pokemon/{num}/') as resp:
                data = await resp.json()
                id = data['id']
                em = discord.Embed(color=discord.Color(value=0x00FF00))
                em.title = data['name'].title()
                em.set_thumbnail(url=data['sprites']['front_default'])
                em.add_field(name="Height", value=str(data['height']/10) + ' meters')
                em.add_field(name="Weight", value=str(data['weight']/10) + ' kilograms')
                j = 0
                abilities = ""
                for i in range(len(data['abilities'])):
                    abilities += data['abilities'][i]['ability']['name'].title().replace('-', ' ') + "\n"
                    j += 1
                if j == 1:
                    em.add_field(name="Ability", value=abilities)
                else:
                    em.add_field(name="Abilities", value=abilities)
                types = ""
                j = 0
                for i in range(len(data['types'])):
                    types += data['types'][i]['type']['name'].title().replace('-', ' ') + "\n"
                    j += 1
                if j == 1:
                    em.add_field(name="Type", value=types)
                else:
                    em.add_field(name="Types", value=types)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://pokeapi.co/api/v2/pokedex/national/') as resp:
                data = await resp.json()
                pokedex = data['pokemon_entries'][id-1]['pokemon_species']['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(pokedex) as resp:
                data = await resp.json()
                for i in range(len(data['flavor_text_entries'])):
                    if data['flavor_text_entries'][i]['language']['name'] == "en":
                        description = data['flavor_text_entries'][i]['flavor_text']
                        break
                    else:
                        pass       
                em.description=description
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://pokeapi.co/api/v2/pokemon/{num}/') as resp:
                data = await resp.json()
                moves = ""
                for i in range(len(data['moves'])):
                    if not i == 0:
                        moves += ", "
                    moves += data['moves'][i]['move']['name'].title().replace('-', ' ')
        em.add_field(name="Learnable Moves", value=moves)
        await ctx.send(embed=em)
        
    @pokemon.command()
    async def info(self, ctx, pokemon):
        '''Get stats about a pokemon. You can specify either its pokedex number or name.'''
        await ctx.trigger_typing()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/') as resp:
                    data = await resp.json()
                    id = data['id']
                    em = discord.Embed(color=discord.Color(value=0x00FF00))
                    em.title = data['name'].title()
                    em.set_thumbnail(url=data['sprites']['front_default'])
                    em.add_field(name="Height", value=str(data['height']/10) + ' meters')
                    em.add_field(name="Weight", value=str(data['weight']/10) + ' kilograms')
                    j = 0
                    abilities = ""
                    for i in range(len(data['abilities'])):
                        abilities += data['abilities'][i]['ability']['name'].title().replace('-', ' ') + "\n"
                        j += 1
                    if j == 1:
                        em.add_field(name="Ability", value=abilities)
                    else:
                        em.add_field(name="Abilities", value=abilities)
                    types = ""
                    j = 0
                    for i in range(len(data['types'])):
                        types += data['types'][i]['type']['name'].title().replace('-', ' ') + "\n"
                        j += 1
                    if j == 1:
                        em.add_field(name="Type", value=types)
                    else:
                        em.add_field(name="Types", value=types)
            async with aiohttp.ClientSession() as session:
                async with session.get('https://pokeapi.co/api/v2/pokedex/national/') as resp:
                    data = await resp.json()
                    pokedex = data['pokemon_entries'][id-1]['pokemon_species']['url']
            async with aiohttp.ClientSession() as session:
                async with session.get(pokedex) as resp:
                    data = await resp.json()
                    for i in range(len(data['flavor_text_entries'])):
                        if data['flavor_text_entries'][i]['language']['name'] == "en":
                            description = data['flavor_text_entries'][i]['flavor_text']
                            break
                        else:
                            pass       
                    em.description=description
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/') as resp:
                    data = await resp.json()
                    moves = ""
                    for i in range(len(data['moves'])):
                        if not i == 0:
                            moves += ", "
                        moves += data['moves'][i]['move']['name'].title().replace('-', ' ')
            em.add_field(name="Learnable Moves", value=moves)
            await ctx.send(embed=em)
        except:
            await ctx.send("That is not a valid pokemon name or pokedex number. Please check your spelling or note that no Gen 7 pokemon are included in pokeapi.")
            
    @pokemon.command()
    async def move(self, ctx, *, move=None):
        '''Get information about a pokemon move. Accepts name of the move or its pokeapi.co ID.'''
        if move is None:
            await ctx.send("Usage: `-pokemon move <name of the move or its pokeapi.co ID>`")
            return
        await ctx.trigger_typing()
        urlmove = move.lower().replace(' ', '-')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://pokeapi.co/api/v2/move/{urlmove}/') as resp:
                    data = await resp.json()
                    id = data['id']
                    em = discord.Embed(color=discord.Color(value=0x00FF00))
                    em.title = data['name'].title().replace('-', ' ')
                    em.add_field(name="Accuracy", value=data['accuracy'])
                    em.add_field(name="PP", value=data['pp'])
                    em.add_field(name="Priority", value=data['priority'])
                    em.add_field(name="Damage", value=data['power'])
                    em.add_field(name="Type", value=data['type']['name'].title())
                    for i in range(len(data['flavor_text_entries'])):
                        if data['flavor_text_entries'][i]['language']['name'] == "en":
                            description = data['flavor_text_entries'][i]['flavor_text']
                            break
                        else:
                            pass       
                    type = data['type']['name']
                    em.description=description.replace('\n', ' ')
                    em.set_thumbnail(url=f'https://remixweb.herokuapp.com/assets/{type}.png')
            await ctx.send(embed=em)
        except:
            await ctx.send("That is not a valid move name or ID. Please check your spelling or note that no Gen 7 moves are included in pokeapi.")

         
def setup(bot):
    bot.add_cog(Pokedex(bot))
