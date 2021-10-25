# Projeto para aprender e destrinchar as funções da API para produzir alggo util e postar no GIT.
# Objetivos: 1- Consultar os pokemons, 2- escolher um time, 3- dizer as fraquesas do time.

import requests 
import json

class timePokemon:
    def __init__(self,*pokemon):
        self.time = list()
        self.consultaAncora = {'normal': '', 'fighting': '', 'flying': '', 'poison': '', 'ground': '', 'rock': '', 'bug': '', 'ghost': '', 'steel': '', 'fire': '', 'water': '', 'grass': '', 'electric': '', 'psychic': '', 'ice': '', 'dragon': '', 'dark': '', 'fairy': '', 'unknown': '', 'shadow': ''}
        
        for x in pokemon:
            self.newPokemon(x)
    def __str__(self):
        texto = 'Aqui esta seu time: \n'
        numb = 1
        for x in self.time:
            name = x['name'].capitalize()
            sp = "                                       "
            spc = len(name)
            Espacamento = 16
            if spc > Espacamento: spc = Espacamento
            name += sp[0:(Espacamento - spc)]
            try:
                tipos = x['tipo1'].capitalize() + "/" + x['tipo2'].capitalize()
            except:
                tipos = x['tipo1'].capitalize()
            texto += "{}- {} Tipo: {}\n".format(numb, name, tipos)
            numb +=1     
        return texto
    
    def newPokemon(self, pokemonName):
        if len(self.time) < 6:
            try:  #Tratar o erro caso o nome seja escrito errado
                self.time.append(changePokemon(pokemonName))
            except:
               return print("Grafia de: " + str(pokemonName) + " esta errada ou o pokemon não existe.")
        else:
            return print("Time cheio, ja exitem 6 pokemons")

    def ConsultaCinergiaTime(self):
        lib = self.LibConsultaCinergiaTime()
        texto = "Tabela de convergencia de dano:"
        for typ, poke in lib.items():
            texto += "{}: {}\n".format(typ.capitalize(), poke)
        return texto  
    def LibConsultaCinergiaTime(self):
        self.refreshConsultaAncora()
        for poke in self.time:
            self.UrlConsultaCinergia(poke["tipo1url"], poke["name"], refresh= False)
            try:
                self.UrlConsultaCinergia(poke["tipo2url"], poke["name"], refresh= False)
            except: 
                continue
        return self.consultaAncora   

    def UrlConsultaCinergia(self, urlTipo,pokeName, refresh = True):
        if refresh == True : self.refreshConsultaAncora()
        damage_relations = ((requests.get(urlTipo)).json())["damage_relations"]
        for scaleDamage, scaleDamageVelues in damage_relations.items():
            for nametype in scaleDamageVelues:
                nameType = nametype['name']
                self.consultaAncora[nameType] += "{} {}, ".format(pokeName.capitalize(), self.scaleDamageFriendly(scaleDamage))  
        return
    
    def refreshConsultaAncora(self):
        self.consultaAncora = {'normal': '', 'fighting': '', 'flying': '', 'poison': '', 'ground': '', 'rock': '', 'bug': '', 'ghost': '', 'steel': '', 'fire': '', 'water': '', 'grass': '', 'electric': '', 'psychic': '', 'ice': '', 'dragon': '', 'dark': '', 'fairy': '', 'unknown': '', 'shadow': ''}
    def scaleDamageFriendly(self,scaleDamage):
        scaleDamage = str(scaleDamage)
        if scaleDamage == "double_damage_from": return "(2x From)"
        if scaleDamage == "double_damage_to": return "(2x To)"
        if scaleDamage == "half_damage_from": return "(1/2x From)"
        if scaleDamage == "half_damage_to": return "(1/2x To)"
        if scaleDamage == "no_damage_from": return "(0x From)"
        if scaleDamage == "no_damage_to": return "(0x To)"
        return "!Dano não parametrizado: " + str(scaleDamage)
def changePokemon(pokemonName):
    request = requestPokemon(pokemonName)
    texto = dict()
    texto['name']= str(request['name'])
    listaTipos = request['types'] #['type']['name']) #typ == type'
    texto.update(typesPokemon(pokemonName))
    return texto 
def typesPokemon(pokemonName): #Retorna um dicionario com o tipo e url dele
    request = requestPokemon(pokemonName)
    t = 1
    texto = dict()
    for x in request['types']:  #dict.update(newvalues)
        txt = "tipo"+str(t)
        texto[txt] = x['type']['name']
        txt += "url"
        texto[txt] = x['type']['url']
        t +=1
    return texto
def requestPokemon(pokemonName):
    return (requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemonName.casefold().strip())).json()
#print(changePokemon("magikarp"))
red = timePokemon("magikarp",'diglett',"  FLygon  ",)
print(red) 
print(red.ConsultaCinergiaTime())



'''
        request = (requests.get("https://pokeapi.co/api/v2/type/")).json()
        for x in request["results"]:
            y = x['name']
            consultaAncora[y] = ''
            '''