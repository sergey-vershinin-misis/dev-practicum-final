# Описание тегов можно получить на странице https://wiki.openstreetmap.org/wiki/Map_features#

OSM_TAG_CATEGORIES = (
    "sustenance",  # бары, кафе, пабы, рестораны, фаст-фуд, магазины мороженного, фуд-корты
    "education",  # школы (не только общеобразовательные), колледжи, детские садики,
    # библиотеки (не только книги), институты, университеты
    "fuel",  # заправочные станции для автомобилей
    "car_service",  # ремонт, шиномонтаж, автомойка
    "parking_space",  # парковочное пространство (несколько парковочных мест,
    # объединенных в группу)
    "atm",  # банкомат
    "bank",  # банк
    "bureau_de_change",  # обменный пункт
    "outpatient_medical_facilities",  # амбулаторные мед учреждения (поликлиники,
    # стоматология и т.п.)
    "inplace_medical_facilities",  # госпитали, хосписы и т.п.
    "pharmacy",  # аптеки
    "veterinary",  # ветеринарные клиники
    "entertainment",  # развлечения и искусство (кино, театры, концертные залы, выставки,
    # планетарии и т.п.)
    "entertainment_for_adults",  # ночные клубы, стриптиз
    "administrative_buildings",  # административные здания (суды, правительство и т.п.)
    "police",  # полицейский участок
    "fire_station",  # пожарная станция
    "post_office",  # почтова служба
    "grave_yard",  # кладбище
    "marketplace",  # рынок
    "monastery",  # монастырь
    "place_of_worship",  # храмы, мечети и т.п.
    "public_transport_stop_position",  # место остановки общественного транспорта
    "alcohol_shop",  # магазин, продающий алкогольные напитки
    "food_shop",  # продовольственные магазины (фрукты, овощи, бакалея, мясо, рыба и т.п.)
    "supermarket",  # супермаркет, универсам, главный магазин
    "mall",  # молл
    "wholesale",  # оптовый магазин (типа METRO Cash & Carry)
    "clothing_shop",  # магазин одежды, обуви и аксессуаров
    "discount_store",  # благотворительные магазины, секонд хэнд, фикс прайс
    "beauty_store",  # магазины health and beauty
    "hardware_store",  # строительство, товары для сада и дачи, ремонт
    "interior_store",  # мебель и интерьер
    "electronics_store",  # магазины электроники
    "sport_store",  # магазины спортивных товаров
    "auto_moto_store",  # авто-мото салон
    "car_parts_store",  # магазины авто и мото запчастей
    "hobbies_store",  # магазины, посвященные искусству, музыке, хобби
    "books_store",  # книжные магазины, журналы, подарки, комиксы
    # "other_type_store",  # прочие типы магазинов (см вики)
    "hotel",  # hostel, hotel, motel
    "museum",  # музей
)

OSM_TAGS = {
    # amenity
    # sustenance
    "bar": {
        "key": "amenity",
        "category": "sustenance",
    },
    "cafe": {
        "key": "amenity",
        "category": "sustenance",
    },
    "fast_food": {
        "key": "amenity",
        "category": "sustenance",
    },
    "food_court": {
        "key": "amenity",
        "category": "sustenance",
    },
    "pub": {
        "key": "amenity",
        "category": "sustenance",
    },
    "ice_cream": {
        "key": "amenity",
        "category": "sustenance",
    },
    "restaurant": {
        "key": "amenity",
        "category": "sustenance",
    },
    # amenity
    # education
    "college": {
        "key": "amenity",
        "category": "education",
    },
    "dancing_school": {
        "key": "amenity",
        "category": "education",
    },
    "driving_school": {
        "key": "amenity",
        "category": "education",
    },
    "first_aid_school": {
        "key": "amenity",
        "category": "education",
    },
    "kindergarten": {
        "key": "amenity",
        "category": "education",
    },
    "language_school": {
        "key": "amenity",
        "category": "education",
    },
    "library": {
        "key": "amenity",
        "category": "education",
    },
    "research_institute": {
        "key": "amenity",
        "category": "education",
    },
    "music_school": {
        "key": "amenity",
        "category": "education",
    },
    "school": {
        "key": "amenity",
        "category": "education",
    },
    "university": {
        "key": "amenity",
        "category": "education",
    },
    # amenity
    # transportation
    "fuel": {
        "key": "amenity",
        "category": "fuel",
    },
    "car_wash": {
        "key": "amenity",
        "category": "car_service",
    },
    "parking_space": {
        "key": "amenity",
        "category": "parking_space",
    },
    # amenity
    # financial
    "atm": {
        "key": "amenity",
        "category": "atm",
    },
    "bank": {
        "key": "amenity",
        "category": "bank",
    },
    "bureau_de_change": {
        "key": "amenity",
        "category": "bureau_de_change",
    },
    # amenity
    # healthcare
    "clinic": {
        "key": "amenity",
        "category": "outpatient_medical_facilities"
    },
    "dentist": {
        "key": "amenity",
        "category": "outpatient_medical_facilities"
    },
    "doctors": {
        "key": "amenity",
        "category": "outpatient_medical_facilities"
    },
    "hospital": {
        "key": "amenity",
        "category": "inplace_medical_facilities",
    },
    "nursing_home": {
        "key": "amenity",
        "category": "inplace_medical_facilities",
    },
    "pharmacy": {
        "key": "amenity",
        "category": "pharmacy",
    },
    "veterinary": {
        "key": "amenity",
        "category": "veterinary"
    },
    # amenity
    # entertainment, arts and culture
    "arts_centre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "cinema": {
        "key": "amenity",
        "category": "entertainment",
    },
    "community_centre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "conference_centre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "events_venue": {
        "key": "amenity",
        "category": "entertainment",
    },
    "exhibition_centre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "music_venue": {
        "key": "amenity",
        "category": "entertainment",
    },
    "planetarium": {
        "key": "amenity",
        "category": "entertainment",
    },
    "social_centre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "theatre": {
        "key": "amenity",
        "category": "entertainment",
    },
    "nightclub": {
        "key": "amenity",
        "category": "entertainment_for_adults",
    },
    "stripclub": {
        "key": "amenity",
        "category": "entertainment_for_adults",
    },
    # amenity
    # public service
    "courthouse": {
        "key": "amenity",
        "category": "administrative_buildings",
    },
    "townhall": {
        "key": "amenity",
        "category": "administrative_buildings",
    },
    "fire_station": {
        "key": "amenity",
        "category": "fire_station",
    },
    "police": {
        "key": "amenity",
        "category": "police",
    },
    "post_office": {
        "key": "amenity",
        "category": "post_office",
    },
    # amenity
    # others
    "grave_yard": {
        "key": "amenity",
        "category": "grave_yard",
    },
    "marketplace": {
        "key": "amenity",
        "category": "marketplace",
    },
    "monastery": {
        "key": "amenity",
        "category": "monastery",
    },
    "place_of_worship": {
        "key": "amenity",
        "category": "place_of_worship",
    },
    # public transport
    "stop_position": {
        "key": "public_transport",
        "category": "public_transport_stop_position",
    },
    # shop
    # food, beverages
    "alcohol": {
        "key": "shop",
        "category": "alcohol_shop",
    },
    "beverages": {
        "key": "shop",
        "category": "alcohol_shop",
    },
    "brewing_supplies": {
        "key": "shop",
        "category": "alcohol_shop",
    },
    "wine": {
        "key": "shop",
        "category": "alcohol_shop",
    },
    "bakery": {
        "key": "shop",
        "category": "food_shop",
    },
    "butcher": {
        "key": "shop",
        "category": "food_shop",
    },
    "cheese": {
        "key": "shop",
        "category": "food_shop",
    },
    "chocolate": {
        "key": "shop",
        "category": "food_shop",
    },
    "coffee": {
        "key": "shop",
        "category": "food_shop",
    },
    "confectionery": {
        "key": "shop",
        "category": "food_shop",
    },
    "convenience": {
        "key": "shop",
        "category": "food_shop",
    },
    "deli": {
        "key": "shop",
        "category": "food_shop",
    },
    "dairy": {
        "key": "shop",
        "category": "food_shop",
    },
    "farm": {
        "key": "shop",
        "category": "food_shop",
    },
    "frozen_food": {
        "key": "shop",
        "category": "food_shop",
    },
    "greengrocer": {
        "key": "shop",
        "category": "food_shop",
    },
    "health_food": {
        "key": "shop",
        "category": "food_shop",
    },
    "pasta": {
        "key": "shop",
        "category": "food_shop",
    },
    "pastry": {
        "key": "shop",
        "category": "food_shop",
    },
    "seafood": {
        "key": "shop",
        "category": "food_shop",
    },
    "spices": {
        "key": "shop",
        "category": "food_shop",
    },
    "tea": {
        "key": "shop",
        "category": "food_shop",
    },
    "water": {
        "key": "shop",
        "category": "food_shop",
    },
    "food": {
        "key": "shop",
        "category": "food_shop",
    },
    # shop
    # general store, department store, mall
    "department_store": {
        "key": "shop",
        "category": "mall",
    },
    "mall": {
        "key": "shop",
        "category": "mall",
    },
    "general": {
        "key": "shop",
        "category": "supermarket",
    },
    "supermarket": {
        "key": "shop",
        "category": "supermarket",
    },
    "wholesale": {
        "key": "shop",
        "category": "wholesale",
    },
    # shop
    # clothing, shoes, accessories
    "baby_goods": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "bag": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "boutique": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "clothes": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "fabric": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "fashion_accessories": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "jewelry": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "sewing": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "shoes": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "tailor": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "watches": {
        "key": "shop",
        "category": "clothing_shop",
    },
    "wool": {
        "key": "shop",
        "category": "clothing_shop",
    },
    # shop
    # discount store, charity
    "charity": {
        "key": "shop",
        "category": "discount_store",
    },
    "second_hand": {
        "key": "shop",
        "category": "discount_store",
    },
    "variety_store": {
        "key": "shop",
        "category": "discount_store",
    },
    # shop
    # health and beauty
    "beauty": {
        "key": "shop",
        "category": "beauty_store",
    },
    "chemist": {
        "key": "shop",
        "category": "beauty_store",
    },
    "cosmetics": {
        "key": "shop",
        "category": "beauty_store",
    },
    "erotic": {
        "key": "shop",
        "category": "beauty_store",
    },
    "hairdresser": {
        "key": "shop",
        "category": "beauty_store",
    },
    "hairdresser_supply": {
        "key": "shop",
        "category": "beauty_store",
    },
    "hearing_aids": {
        "key": "shop",
        "category": "beauty_store",
    },
    "herbalist": {
        "key": "shop",
        "category": "beauty_store",
    },
    "massage": {
        "key": "shop",
        "category": "beauty_store",
    },
    "medical_supply": {
        "key": "shop",
        "category": "beauty_store",
    },
    "nutrition_supplements": {
        "key": "shop",
        "category": "beauty_store",
    },
    "optician": {
        "key": "shop",
        "category": "beauty_store",
    },
    "perfumery": {
        "key": "shop",
        "category": "beauty_store",
    },
    # shop
    # do-it-yourself, household, building materials, gardening
    "agrarian": {
        "key": "shop",
        "category": "hardware_store",
    },
    "appliance": {
        "key": "shop",
        "category": "hardware_store",
    },
    "bathroom_furnishing": {
        "key": "shop",
        "category": "hardware_store",
    },
    "doityourself": {
        "key": "shop",
        "category": "hardware_store",
    },
    "electrical": {
        "key": "shop",
        "category": "hardware_store",
    },
    "energy": {
        "key": "shop",
        "category": "hardware_store",
    },
    "fireplace": {
        "key": "shop",
        "category": "hardware_store",
    },
    "florist": {
        "key": "shop",
        "category": "hardware_store",
    },
    "garden_centre": {
        "key": "shop",
        "category": "hardware_store",
    },
    "garden_furniture": {
        "key": "shop",
        "category": "hardware_store",
    },
    "gas": {
        "key": "shop",
        "category": "hardware_store",
    },
    "glaziery": {
        "key": "shop",
        "category": "hardware_store",
    },
    "groundskeeping": {
        "key": "shop",
        "category": "hardware_store",
    },
    "hardware": {
        "key": "shop",
        "category": "hardware_store",
    },
    "houseware": {
        "key": "shop",
        "category": "hardware_store",
    },
    "locksmith": {
        "key": "shop",
        "category": "hardware_store",
    },
    "paint": {
        "key": "shop",
        "category": "hardware_store",
    },
    "pottery": {
        "key": "shop",
        "category": "hardware_store",
    },
    "security": {
        "key": "shop",
        "category": "hardware_store",
    },
    # shop
    # furniture and interior
    "antiques": {
        "key": "shop",
        "category": "interior_store",
    },
    "bed": {
        "key": "shop",
        "category": "interior_store",
    },
    "candles": {
        "key": "shop",
        "category": "interior_store",
    },
    "carpet": {
        "key": "shop",
        "category": "interior_store",
    },
    "curtain": {
        "key": "shop",
        "category": "interior_store",
    },
    "doors": {
        "key": "shop",
        "category": "interior_store",
    },
    "flooring": {
        "key": "shop",
        "category": "interior_store",
    },
    "furniture": {
        "key": "shop",
        "category": "interior_store",
    },
    "household_linen": {
        "key": "shop",
        "category": "interior_store",
    },
    "interior_decoration": {
        "key": "shop",
        "category": "interior_store",
    },
    "kitchen": {
        "key": "shop",
        "category": "interior_store",
    },
    "lighting": {
        "key": "shop",
        "category": "interior_store",
    },
    "tiles": {
        "key": "shop",
        "category": "interior_store",
    },
    "window_blind": {
        "key": "shop",
        "category": "interior_store",
    },
    # shop
    # electronics
    "computer": {
        "key": "shop",
        "category": "electronics_store",
    },
    "electronics": {
        "key": "shop",
        "category": "electronics_store",
    },
    "hifi": {
        "key": "shop",
        "category": "electronics_store",
    },
    "mobile_phone": {
        "key": "shop",
        "category": "electronics_store",
    },
    "radiotechnics": {
        "key": "shop",
        "category": "electronics_store",
    },
    "telecommunication": {
        "key": "shop",
        "category": "electronics_store",
    },
    "vacuum_cleaner": {
        "key": "shop",
        "category": "electronics_store",
    },
    "printer_ink": {
        "key": "shop",
        "category": "electronics_store",
    },
    # shop
    # outdoors and sport, vehicles
    "atv": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "bicycle": {
        "key": "shop",
        "category": "sport_store",
    },
    "car": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "car_repair": {
        "key": "shop",
        "category": "car_parts_store",
    },
    "motorcycle_repair": {
        "key": "shop",
        "category": "car_parts_store",
    },
    "car_parts": {
        "key": "shop",
        "category": "car_parts_store",
    },
    "caravan": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "fishing": {
        "key": "shop",
        "category": "sport_store",
    },
    "surf": {
        "key": "shop",
        "category": "sport_store",
    },
    "golf": {
        "key": "shop",
        "category": "sport_store",
    },
    "hunting": {
        "key": "shop",
        "category": "sport_store",
    },
    "jetski": {
        "key": "shop",
        "category": "sport_store",
    },
    "motorcycle": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "outdoor": {
        "key": "shop",
        "category": "sport_store",
    },
    "scuba_diving": {
        "key": "shop",
        "category": "sport_store",
    },
    "ski": {
        "key": "shop",
        "category": "sport_store",
    },
    "snowmobile": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "sports": {
        "key": "shop",
        "category": "sport_store",
    },
    "swimming_pool": {
        "key": "shop",
        "category": "sport_store",
    },
    "trailer": {
        "key": "shop",
        "category": "auto_moto_store",
    },
    "tyres": {
        "key": "shop",
        "category": "car_parts_store",
    },
    # shop
    # art, music, hobbies
    "art": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "model": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "music": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "musical_instrument": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "photo": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "trophy": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "video": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "video_games": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "camera": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "collector": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "craft": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "frame": {
        "key": "shop",
        "category": "hobbies_store",
    },
    "games": {
        "key": "shop",
        "category": "hobbies_store",
    },
    # shop
    # stationery, gifts, books, newspapers
    "books": {
        "key": "shop",
        "category": "books_store",
    },
    "gift": {
        "key": "shop",
        "category": "books_store",
    },
    "lottery": {
        "key": "shop",
        "category": "books_store",
    },
    "newsagent": {
        "key": "shop",
        "category": "books_store",
    },
    "stationery": {
        "key": "shop",
        "category": "books_store",
    },
    "ticket": {
        "key": "shop",
        "category": "books_store",
    },
    "anime": {
        "key": "shop",
        "category": "books_store",
    },
    # shop
    # others
    # "bookmaker": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "copyshop": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "dry_cleaning": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "e-cigarette": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "funeral_directors": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "insurance": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "laundry": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "money_lender": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "outpost": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "party": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "pawnbroker": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "pest_control": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "pet": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "pet_grooming": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "pyrotechnics": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "religion": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "storage_rental": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "tobacco": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "toys": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "travel_agency": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # "weapons": {
    #     "key": "shop",
    #     "category": "other_type_store",
    # },
    # # tourism
    # "hostel": {
    #     "key": "tourism",
    #     "category": "hotel",
    # },
    # "hotel": {
    #     "key": "tourism",
    #     "category": "hotel",
    # },
    # "motel": {
    #     "key": "tourism",
    #     "category": "hotel",
    # },
    # "museum": {
    #     "key": "tourism",
    #     "category": "museum",
    # },
}
