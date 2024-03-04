import discord
from discord.ext import commands
from main import client
import pokebase as pb
from cogs.getdata import inventory
from cogs.getdata import pokemon as pokemonDB

search = client.create_group('search', 'Search for stuff')

regions = {'I':'Kanto', 'II':'Johto', 'III':'Hoenn', 'IV':'Sinnoh', 'V':'Unova', 'VI':'Kalos', 'VII':'Alola', 'VIII':'Galar', 'IX':'Paldea'}

typecolours = { # for making the embed colour match the type
    'Normal':discord.Colour.light_grey(),
    'Fire':discord.Colour.red(),
    'Water':discord.Colour.from_rgb(0, 102, 191), #dark-ish blue
    'Electric':discord.Colour.yellow(),
    'Grass':discord.Colour.dark_green(),
    'Ice':discord.Colour.from_rgb(0, 223, 252), #light blue
    'Fighting':discord.Colour.dark_orange(),
    'Poison':discord.Colour.magenta(),
    'Ground':discord.Colour.from_rgb(173, 168, 87), #beige
    'Flying':discord.Colour.teal(),
    'Psychic':discord.Colour.nitro_pink(),
    'Bug':discord.Colour.green(),
    'Rock':discord.Colour.from_rgb(117, 96, 43), # darker beige
    'Ghost':discord.Colour.purple(),
    'Dragon':discord.Colour.blurple(),
    'Dark':discord.Colour.from_rgb(31, 16, 3), # very dark brown
    'Steel':discord.Colour.dark_grey(),
    'Fairy':discord.Colour.from_rgb(227, 134, 218) # light pink
}

class search(commands.Cog):

    def __init__(self, client):
        self.client = client

    def searchLocal(pokemon, form, db):

        string = ''

        pkmn = db[pokemon]

        # init forms
        if form != '': # create format NAME-FORM if form section is filled in
            pokemonwithform += '-'+form.lower()
        elif pkmn['hasforms']: # if pokemon has forms and form section is empty, tell user to specify
            for formname in pkmn['forms']:
                formErrorString += '- '+formname+'\n'
            return f'This pokemon has multiple forms.\n```{formErrorString}```\nPlease choose one and include it in the `form` section of the command. (Don\'t include the pokemon name in the form section)'


        # name
        if form == '':
            name = pokemon.capitalize()
        else:
            name = pokemon.capitalize() + ' (' + form + ')'
        string += 'Name: ' + name

        # types & embed colour
        first = pkmn['types'][0].capitalize()
        try:
            second = pkmn['types'][1].capitalize()
            type = first+'/'+second # format example: Fire/Water
        except IndexError:
            type = first
        typecolour = typecolours[first]
        string += '\nType: '+type

        # origin region
        string += '\nRegion: Eliccia'

        # origin gen
        string += '\nGen: X'

        # stats
        string += '\n\nBase stats:'
        for stat in pkmn['stats']:
            statname = pkmn['stats'][stat]['name'].capitalize()
            string += f"\n{statname}: {pkmn['stats'][stat]['number']}"

        # abilities
        string += '\n\nAbilities:'
        for ability in pkmn['abilities']:
            string+= '\n'+ability

        # sprites
        spriteurl = pkmn['sprite']

        # pokedex entry
        entry = pkmn['entry']

        # create embed
        embed = discord.Embed(
            title=f'Pokemon: {name}',
            description=string,
            color=typecolour
        )
        embed.set_image(url=spriteurl)
        embed.set_footer(text=entry)
        
        return embed

    @search.command(description='Search for a pokemon')
    async def pokemon(ctx, pokemon, form: discord.commands.Option(str, "form", required = False, default = '')): # type:ignore (for pylance to stop bugging me)
        pokemon = pokemon.lower()
        pokemonwithform = pokemon
        await ctx.respond('Loading...') # So that the command doesn't time-out when the API request takes a long time

        try:

            customPokemon = pokemonDB.read_info()
            if pokemon in customPokemon:
                embed = search.searchLocal(pokemon, form, customPokemon)
                await ctx.edit(content='', embed=embed)
                return

            # init forms
            if form != '':
                pokemonwithform += '-'+form.lower()

            pkmn = pb.pokemon(pokemonwithform)
            spec = pb.pokemon_species(pokemon)

            string = ''

            # name
            if form == '':
                name = pokemon.capitalize()
            else:
                name = pokemon.capitalize() + ' (' + form + ')'
            string += 'Name: ' + name

            # types & embed colour
            try: # ask user to specify one of the forms if multiple exist (causes attribute error otherwise)
                types = pkmn.types[0].type.name.capitalize()
            except AttributeError:
                formErrorString = ''
                for a in spec.varieties:
                    formErrorString += '- '+a.pokemon.name+'\n'
                await ctx.edit(content=f'This pokemon has multiple forms.\n```{formErrorString}```\nPlease choose one and include it in the `form` section of the command. (Don\'t include the pokemon name in the form section)')
                return

            typecolour = typecolours[types]        
            try:
                types += '/' + pkmn.types[1].type.name.capitalize()
            except IndexError:
                pass
            string += '\nType: '+types


            # origin region
            gen = spec.generation.name.replace('generation-', '').upper()
            region = regions[gen]
            string += '\n\nRegion: '+region

            # origin gen
            string += '\nGeneration: '+gen

            # stats
            string += '\n\nBase stats:'
            for a in pkmn.stats:
                statname = a.stat.name.replace('-', ' ').capitalize()
                string += f'\n{statname}: {a.base_stat}'

            # abilities
            string += '\n\nAbilities:'
            for a in pkmn.abilities:
                string += '\n'+a.ability.name.capitalize()

            # sprites
            spriteurl = pkmn.sprites.front_default

            # pokedex entry
            for a in spec.flavor_text_entries:
                if a.language.name == 'en':
                    entry = a.flavor_text

            # send final message with embed
            embed = discord.Embed(
                title=f'Pokemon: {name}',
                description=string,
                color=typecolour
            )
            embed.set_image(url=spriteurl)
            embed.set_footer(text=entry.replace('\n', ' '))

            await ctx.edit(content='', embed=embed)
            
        except AttributeError:
            await ctx.edit(content="That pokemon doesn't exist.")

def setup(client):
    client.add_cog(search(client))