from scrapy import Spider
from scrapy.http import Response


class PokemonSpider(Spider):
    name = "pokemon"

    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response: Response, **kwargs):
        for pokedex_entry in response.css("table[id='pokedex'] tbody tr"):
            pokedex_columns_entry = pokedex_entry.css("td")
            (
                id_column,
                name_column,
                type_column,
                total_stat_column,
                health_stat_column,
                attack_stat_column,
                defense_stat_column,
                special_attack_stat_column,
                special_defence_stat_column,
                speed_stat_column,
            ) = pokedex_columns_entry

            yield {
                "id": id_column.css("span::text").get(),
                "name": name_column.css("a::text").get(),
                "href": name_column.css("a::attr(href)").get(),
                "types": name_column.css("a::attr(href)").get(),
                "total": total_stat_column.css("::text").get(),
                "health": health_stat_column.css("::text").get(),
                "attack": attack_stat_column.css("::text").get(),
                "defence": defense_stat_column.css("::text").get(),
                "special_attack": special_attack_stat_column.css("::text").get(),
                "special_defence": special_defence_stat_column.css("::text").get(),
                "speed": speed_stat_column.css("::text").get(),
                "image": id_column.css("img::attr(src)").get(),
            }
