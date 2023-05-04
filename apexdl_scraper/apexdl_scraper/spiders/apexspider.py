import scrapy
from .data_apex import heroes_list, weapons_list, map_list


class ApexspiderSpider(scrapy.Spider):
    name = "apexspider"
    allowed_domains = ["apexlegends.fandom.com"]
    start_urls = ["http://apexlegends.fandom.com/"]

    def parse(self, response):
    
        for hero in heroes_list:
            hero_url = 'https://apexlegends.fandom.com/wiki/' + hero
            
            
            yield response.follow(hero_url, callback=self.parse_hero)

        
        for weapon in weapons_list:
            weapon_url = 'https://apexlegends.fandom.com/wiki/' + weapon
            
            yield response.follow(weapon_url, callback= self.parse_weapons)   
            
        for maps in map_list:
            map_url = 'https://apexlegends.fandom.com/wiki/' + maps
            
            yield response.follow(map_url, callback= self.parse_maps)   
            
    def parse_hero(self, response):
        
        name = response.css('th.infobox-header::text').get()
        image = response.css('td.infobox-centered a::attr(href)').get()
        real_name = response.css('th.infobox-row-name:contains("Real Name") + td.infobox-row-value::text').get()
        gender = response.css('tr.infobox-row th.infobox-row-name:contains("Gender") + td.infobox-row-value a::text').get()
        ages = response.css('tr.infobox-row th:contains("Age") + td::text').get()
        homeworld = response.css('tr.infobox-row th.infobox-row-name:contains("Homeworld") + td.infobox-row-value a::text').get()
        weight = response.css('tr.infobox-row th:contains("Weight") + td::text').get()
        height = response.css('tr.infobox-row th:contains("Height") + td::text').get()
        clas = response.css('tr.infobox-row td.infobox-row-value a:nth-child(2)::text').get()
        tactical_ability = response.xpath('//table[contains(@class, "infobox")]//tr[th/b/text()="Tactical Ability"]/td//a/text()').get()
        passive_ability = response.xpath('//table[contains(@class, "infobox")]//tr[th/b/text()="Passive Ability"]/td//a/text()').get()
        utlimate_ability = response.xpath('//table[contains(@class, "infobox")]//tr[th/b/text()="Ultimate Ability"]/td//a/text()').get()
        voice_actor = response.xpath("//tr[th/b[contains(text(), 'Voice Actor')]]/td[@class='infobox-row-value']/text()").get()
        
        
        yield {
        'heroes_name' : response.css('th.infobox-header::text').get().strip() if name else None,
        'image' : image if image else None,
        'real_name' : response.css('th.infobox-row-name:contains("Real Name") + td.infobox-row-value::text').get().strip() if real_name else None,
        'gender' : gender if gender else None,
        'ages' : response.css('tr.infobox-row th:contains("Age") + td::text').get().replace('\n','') if ages else None,
        'homeworld' : response.css('tr.infobox-row th.infobox-row-name:contains("Homeworld") + td.infobox-row-value a::text').get().strip() if homeworld else None,
        'weight' : response.css('tr.infobox-row th:contains("Weight") + td::text').get().replace('\n','') if weight else None,
        'height' : response.css('tr.infobox-row th:contains("Height") + td::text').get().replace('\n','') if height else None,
        'class' : clas if clas else None,
        'tactical_ability' : tactical_ability if tactical_ability else None,
        'passive_ability' : passive_ability if passive_ability else None,
        'utlimate_ability' : utlimate_ability if utlimate_ability else None,
        'voice_actor' : response.xpath("//tr[th/b[contains(text(), 'Voice Actor')]]/td[@class='infobox-row-value']/text()").get().replace('\n','') if voice_actor else None
        }
        
    def parse_weapons(self, response):
        
        name_weapon = response.xpath('//tbody[1]/tr/th[@class="infobox-header"]/text()').get()
        weapon_image = response.css('td.infobox-centered a::attr(href)').get()
        description = response.xpath('//td[contains(@class, "infobox-centered")]/i/text()').get()
        icon_weapon = response.xpath('//td[@class="infobox-row-value"]/span/a/img/@data-src').get()
        type_weapon = response.xpath('//th[b="Type"]/following-sibling::td/a/text()').get()
        ammo = response.xpath('//tr[@class="infobox-row"][th/b[contains(text(),"Ammo")]]/td/span/a/@data-src | //tr[@class="infobox-row"][th/b[contains(text(),"Ammo")]]/td/span/a/text()').get()
        fire_mode = response.xpath("//tr[@class='infobox-row'][th/b='Fire modes']/td/text()").get()
        manufacture1 = response.xpath('//tr[@class="infobox-row" and th[b="Manufacturer"]]//a[contains(@href, "/wiki/")]/text()').get()
        technical = response.xpath('//td[@class="infobox-row-value; invert-image"]/span[@style]/text() | //td[@class="infobox-row-value; invert-image"]/text()[normalize-space()][not(ancestor::span[@style])]').extract()
        
        yield {
            'weapon_name': response.xpath('//tbody[1]/tr/th[@class="infobox-header"]/text()').get().replace('\n','') if name_weapon else None,
            'weapon_images' : response.css('td.infobox-centered a::attr(href)').get() if weapon_image else None,
            'short_description': response.xpath('//td[contains(@class, "infobox-centered")]/i/text()').get().replace('\n','') if description else None,
            'icon_weapon': response.xpath('//td[@class="infobox-row-value"]/span/a/img/@data-src').get() if icon_weapon else None,
            'weapon_type': response.xpath('//th[b="Type"]/following-sibling::td/a/text()').get() if type_weapon else None, 
            'ammunition': response.xpath('//tr[@class="infobox-row"][th/b[contains(text(),"Ammo")]]/td/span/a/@data-src | //tr[@class="infobox-row"][th/b[contains(text(),"Ammo")]]/td/span/a/text()').get() if ammo else None,
            'fire_modes': response.xpath("//tr[@class='infobox-row'][th/b='Fire modes']/td/text()").get().replace('\n','') if fire_mode else None,
            'manufacture1': response.xpath('//tr[@class="infobox-row" and th[b="Manufacturer"]]//a[contains(@href, "/wiki/")]/text()').get() if manufacture1 else None,
            'technical': response.xpath('//td[@class="infobox-row-value; invert-image"]/span[@style]/text() | //td[@class="infobox-row-value; invert-image"]/text()[normalize-space()][not(ancestor::span[@style])]').extract() if technical else None  
        }
        
    def parse_maps(self, response):
        
        map_name =response.xpath("//meta[@property='og:title']/@content").get()
        map_field = response.xpath('//a/@href').getall()
        
        yield {
            'map': response.xpath("//meta[@property='og:title']/@content").get() if map_name else None,
            'gallery': [map_image for map_image in map_field if map_image.startswith('https://static')] if map_field else None
        }
        
        # for item in map_field:
        #     if item.startswith('https://static'):
        #         yield {: item}
                