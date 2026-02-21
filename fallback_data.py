"""
Sample data returned when the scraper is unavailable (e.g. no Chrome, blocked, errors).
Allows the frontend to show example output and explain what the server does.
"""

# 50 realistic-looking BMW i3 offers (French AutoScout24 style)
# Shape: list of {"url": str, "data": {"title": str, "model": str, "vendor_info": dict}}
FALLBACK_OFFERS = [
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-42-kwh-atelier-170-electrique-8a1b2c3d4e5f",
        "data": {
            "title": "BMW i3 120 Ah 42 kWh ATELIER 170",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Jean Dupont",
                "address": {"url": "https://maps.google.com/?q=Nimes", "text": "FR-30000 Nimes"},
                "company": "BMW NÎMES - AUTOSPHERE",
                "pro": True,
                "numbers": ["+33466123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-94ah-rex-connected-atelier-electrique-1b2c3d4e5f6a",
        "data": {
            "title": "BMW i3 170ch 94Ah REx +CONNECTED Atelier",
            "model": "Électrique/Essence 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Marie Martin",
                "address": {"url": "https://maps.google.com/?q=Bayonne", "text": "FR-64100 Bayonne"},
                "company": "BMW BAYONNE - AUTOSPHERE",
                "pro": True,
                "numbers": ["+33559123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-ilife-atelier-electrique-2c3d4e5f6a7b",
        "data": {
            "title": "BMW i3 170ch 120Ah iLife Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Pierre Bernard",
                "address": {"url": "https://maps.google.com/?q=Colmar", "text": "FR-68005 COLMAR"},
                "company": "BMW MINI COLMAR JMS AUTOMOBILE",
                "pro": True,
                "numbers": ["+33389123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-edition-360-atelier-3d4e5f6a7b8c",
        "data": {
            "title": "BMW i3 170ch 120Ah Edition 360 Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Sophie Leroy",
                "address": {"url": "https://maps.google.com/?q=Charleville", "text": "FR-08000 Charleville Mézières"},
                "company": "BMW PHILIPPE EMOND CHARLEVILLE MEZIERES",
                "pro": True,
                "numbers": ["+33324123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-berline-i01-lci-ilife-loft-4e5f6a7b8c9d",
        "data": {
            "title": "BMW i3 120Ah BERLINE I01 LCI iLife Loft",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Luc Fontaine",
                "address": {"url": "https://maps.google.com/?q=Saint-Andre", "text": "FR-01390 Saint-André-de-Corcy"},
                "company": "DRIVE ON",
                "pro": True,
                "numbers": ["+33478123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-60ah-urbanlife-atelier-5f6a7b8c9d0e",
        "data": {
            "title": "BMW i3 170 ch 60 Ah UrbanLife Atelier",
            "model": "Électrique/Essence 75 kW (102 Ch)",
            "vendor_info": {
                "name": "Claire Moreau",
                "address": {"url": "https://maps.google.com/?q=Lavau", "text": "FR-10150 LAVAU"},
                "company": "E-Motors France Troyes",
                "pro": True,
                "numbers": ["+33325123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-i3s-184-roadstyle-edition-6a7b8c9d0e1f",
        "data": {
            "title": "BMW i3 i3s 184 Roadstyle Edition",
            "model": "Electrique 135 kW (184 Ch)",
            "vendor_info": {
                "name": "Thomas Petit",
                "address": {"url": "https://maps.google.com/?q=Rambervillers", "text": "FR-88700 Rambervillers"},
                "company": "Rambervillers Automobiles",
                "pro": True,
                "numbers": ["+33329123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-360-electric-170-120ah-edition-7b8c9d0e1f2a",
        "data": {
            "title": "BMW i3 360 electric 170 120ah edition atelier bva",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Nathalie Roux",
                "address": {"url": "https://maps.google.com/?q=Tours", "text": "FR-37100 Tours"},
                "company": "EWIGO TOURS / SAS MLF AUTOMOBILES",
                "pro": True,
                "numbers": ["+33247123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120-ah-42-kwh-atelier-170-8c9d0e1f2a3b",
        "data": {
            "title": "BMW i3 120 Ah 42 kWh ATELIER 170",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "François Girard",
                "address": {"url": "https://maps.google.com/?q=Lescure", "text": "FR-81380 LESCURE D'ALBI"},
                "company": "SN DIFFUSION",
                "pro": True,
                "numbers": ["+33563123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-loft-9d0e1f2a3b4c",
        "data": {
            "title": "BMW i3 170ch 120Ah Loft",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Isabelle Lambert",
                "address": {"url": "https://maps.google.com/?q=Marignane", "text": "FR-13700 Marignane"},
                "company": "BMW MARIGNANE - AUTOSPHERE",
                "pro": True,
                "numbers": ["+33442123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-edition-windmill-atelier-0e1f2a3b4c5d",
        "data": {
            "title": "BMW i3 170ch 120Ah Edition WindMill Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Philippe Simon",
                "address": {"url": "https://maps.google.com/?q=Merignac", "text": "FR-33700 Merignac"},
                "company": "BMW MERIGNAC - AUTOSPHERE",
                "pro": True,
                "numbers": ["+33556123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-i01-170ch-rex-1f2a3b4c5d6e",
        "data": {
            "title": "BMW i3 (I01) 170CH (REX)",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Michel Dubois",
                "address": {"url": "https://maps.google.com/?q=La+Garde", "text": "FR-83130 La Garde"},
                "company": "EXCELLENCE AUTO 83",
                "pro": True,
                "numbers": ["+33494123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-windmil-120-2a3b4c5d6e7f",
        "data": {
            "title": "BMW i3 Windmil 120",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Catherine Blanc",
                "address": {"url": "https://maps.google.com/?q=Monaco", "text": "FR-98000 Monaco"},
                "company": "Particulier",
                "pro": False,
                "numbers": ["+33761234567"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-edition-windmill-lodge-3b4c5d6e7f8a",
        "data": {
            "title": "BMW i3 170ch 120Ah Edition WindMill Lodge",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "André Faure",
                "address": {"url": "https://maps.google.com/?q=Seynod", "text": "FR-74601 SEYNOD"},
                "company": "ARAVIS AUTOMOBILES",
                "pro": True,
                "numbers": ["+33450123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-ilife-atelier-chambourcy-4c5d6e7f8a9b",
        "data": {
            "title": "BMW i3 170ch 120Ah iLife Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Sébastien Mercier",
                "address": {"url": "https://maps.google.com/?q=Chambourcy", "text": "FR-78240 CHAMBOURCY"},
                "company": "BMW NEUBAUER CHAMBOURCY",
                "pro": True,
                "numbers": ["+33130123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-edition-windmill-beaucouze-5d6e7f8a9b0c",
        "data": {
            "title": "BMW i3 170ch 120Ah Edition WindMill Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Valérie Garnier",
                "address": {"url": "https://maps.google.com/?q=Beaucouze", "text": "FR-49000 Beaucouze"},
                "company": "BMW Dynamism Automobiles",
                "pro": True,
                "numbers": ["+33241123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-ilife-atelier-montlucon-6e7f8a9b0c1d",
        "data": {
            "title": "BMW i3 170ch 120Ah iLife Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Olivier Chevalier",
                "address": {"url": "https://maps.google.com/?q=Montlucon", "text": "FR-03100 MONTLUCON"},
                "company": "HELI MOTORS MONTLUCON",
                "pro": True,
                "numbers": ["+33470123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-ilife-atelier-la-garde-7f8a9b0c1d2e",
        "data": {
            "title": "BMW i3 170ch 120Ah iLife Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Christine Robin",
                "address": {"url": "https://maps.google.com/?q=La+Garde", "text": "FR-83130 LA GARDE"},
                "company": "BAVARIA MOTORS",
                "pro": True,
                "numbers": ["+33498123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-120ah-edition-360-lodge-8a9b0c1d2e3f",
        "data": {
            "title": "BMW i3 170ch 120Ah Edition 360 Lodge",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Patrick Gauthier",
                "address": {"url": "https://maps.google.com/?q=Cholet", "text": "FR-49302 CHOLET CEDEX"},
                "company": "CHARRIER SA",
                "pro": True,
                "numbers": ["+33241123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-s-120-ah-alu19-led-cam-9b0c1d2e3f4a",
        "data": {
            "title": "BMW i3 s (120 Ah) Alu19\" Led/Cam/Pdc/Gps/Bt",
            "model": "Electrique 135 kW (184 Ch)",
            "vendor_info": {
                "name": "Laurent Perrin",
                "address": {"url": "https://maps.google.com/?q=Lille", "text": "FR-59000 Lille"},
                "company": "Auto's Basile - Kuurne motors",
                "pro": True,
                "numbers": ["+33320123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-94ah-rex-atelier-0c1d2e3f4a5b",
        "data": {
            "title": "BMW i3 94Ah REx Atelier",
            "model": "Électrique/Essence 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Hélène Lemoine",
                "address": {"url": "https://maps.google.com/?q=Lyon", "text": "FR-69001 Lyon"},
                "company": "BMW Lyon Centre",
                "pro": True,
                "numbers": ["+33472123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-ilife-1d2e3f4a5b6c",
        "data": {
            "title": "BMW i3 120Ah iLife",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Denis Rousseau",
                "address": {"url": "https://maps.google.com/?q=Bordeaux", "text": "FR-33000 Bordeaux"},
                "company": "BMW Bordeaux Sud",
                "pro": True,
                "numbers": ["+33556123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-60ah-urban-2e3f4a5b6c7d",
        "data": {
            "title": "BMW i3 60 Ah Urban",
            "model": "Électrique 75 kW (102 Ch)",
            "vendor_info": {
                "name": "Martine Vincent",
                "address": {"url": "https://maps.google.com/?q=Strasbourg", "text": "FR-67000 Strasbourg"},
                "company": "BMW Strasbourg",
                "pro": True,
                "numbers": ["+33388123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-lodge-3f4a5b6c7d8e",
        "data": {
            "title": "BMW i3 120Ah Lodge",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Jean-Louis Andre",
                "address": {"url": "https://maps.google.com/?q=Marseille", "text": "FR-13001 Marseille"},
                "company": "BMW Marseille Est",
                "pro": True,
                "numbers": ["+33491123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-184ch-i3s-4a5b6c7d8e9f",
        "data": {
            "title": "BMW i3 184ch i3s",
            "model": "Electrique 135 kW (184 Ch)",
            "vendor_info": {
                "name": "Bernard Lefebvre",
                "address": {"url": "https://maps.google.com/?q=Toulouse", "text": "FR-31000 Toulouse"},
                "company": "BMW Toulouse Nord",
                "pro": True,
                "numbers": ["+33561123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-rex-94ah-5b6c7d8e9f0a",
        "data": {
            "title": "BMW i3 REx 94Ah",
            "model": "Électrique/Essence 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Monique Fournier",
                "address": {"url": "https://maps.google.com/?q=Nice", "text": "FR-06000 Nice"},
                "company": "BMW Nice Côte d'Azur",
                "pro": True,
                "numbers": ["+33493123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-world-6c7d8e9f0a1b",
        "data": {
            "title": "BMW i3 120Ah World",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Pierre-Marie David",
                "address": {"url": "https://maps.google.com/?q=Rennes", "text": "FR-35000 Rennes"},
                "company": "BMW Rennes",
                "pro": True,
                "numbers": ["+33299123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-60ah-rex-7d8e9f0a1b2c",
        "data": {
            "title": "BMW i3 60 Ah REx",
            "model": "Électrique/Essence 75 kW (102 Ch)",
            "vendor_info": {
                "name": "Anne-Sophie Henry",
                "address": {"url": "https://maps.google.com/?q=Nantes", "text": "FR-44000 Nantes"},
                "company": "BMW Nantes Atlantique",
                "pro": True,
                "numbers": ["+33240123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-atelier-8e9f0a1b2c3d",
        "data": {
            "title": "BMW i3 120Ah Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "François-Xavier Bonnet",
                "address": {"url": "https://maps.google.com/?q=Grenoble", "text": "FR-38000 Grenoble"},
                "company": "BMW Grenoble",
                "pro": True,
                "numbers": ["+33476123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-94ah-connected-9f0a1b2c3d4e",
        "data": {
            "title": "BMW i3 94Ah +Connected",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Cécile Marchand",
                "address": {"url": "https://maps.google.com/?q=Dijon", "text": "FR-21000 Dijon"},
                "company": "BMW Dijon",
                "pro": True,
                "numbers": ["+33380123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-windmill-120ah-0a1b2c3d4e5f",
        "data": {
            "title": "BMW i3 WindMill 120Ah",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Stéphane Colin",
                "address": {"url": "https://maps.google.com/?q=Reims", "text": "FR-51100 Reims"},
                "company": "BMW Reims",
                "pro": True,
                "numbers": ["+33326123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-edition-360-1b2c3d4e5f6a",
        "data": {
            "title": "BMW i3 Edition 360",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Nicolas Barbier",
                "address": {"url": "https://maps.google.com/?q=Amiens", "text": "FR-80000 Amiens"},
                "company": "BMW Amiens",
                "pro": True,
                "numbers": ["+33322123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-loft-120ah-2c3d4e5f6a7b",
        "data": {
            "title": "BMW i3 Loft 120Ah",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Sandrine Guerin",
                "address": {"url": "https://maps.google.com/?q=Caen", "text": "FR-14000 Caen"},
                "company": "BMW Caen",
                "pro": True,
                "numbers": ["+33231123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-urban-life-60ah-3d4e5f6a7b8c",
        "data": {
            "title": "BMW i3 Urban Life 60 Ah",
            "model": "Électrique 75 kW (102 Ch)",
            "vendor_info": {
                "name": "Romain Joly",
                "address": {"url": "https://maps.google.com/?q=Le+Mans", "text": "FR-72000 Le Mans"},
                "company": "BMW Le Mans",
                "pro": True,
                "numbers": ["+33243123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-phase2-4e5f6a7b8c9d",
        "data": {
            "title": "BMW i3 120Ah Phase 2",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Virginie Masson",
                "address": {"url": "https://maps.google.com/?q=Brest", "text": "FR-29200 Brest"},
                "company": "BMW Brest",
                "pro": True,
                "numbers": ["+33298123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-rex-120ah-5f6a7b8c9d0e",
        "data": {
            "title": "BMW i3 REx 120Ah",
            "model": "Électrique/Essence 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Laetitia Gaillard",
                "address": {"url": "https://maps.google.com/?q=Limoges", "text": "FR-87000 Limoges"},
                "company": "BMW Limoges",
                "pro": True,
                "numbers": ["+33555123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-s-edition-6a7b8c9d0e1f",
        "data": {
            "title": "BMW i3 S Edition",
            "model": "Electrique 135 kW (184 Ch)",
            "vendor_info": {
                "name": "Jérôme Roussel",
                "address": {"url": "https://maps.google.com/?q=Clermont-Ferrand", "text": "FR-63000 Clermont-Ferrand"},
                "company": "BMW Clermont",
                "pro": True,
                "numbers": ["+33473123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-42kwh-atelier-7b8c9d0e1f2a",
        "data": {
            "title": "BMW i3 42 kWh Atelier",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Benoît Michel",
                "address": {"url": "https://maps.google.com/?q=Angers", "text": "FR-49000 Angers"},
                "company": "BMW Angers",
                "pro": True,
                "numbers": ["+33241123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-94ah-atelier-rex-8c9d0e1f2a3b",
        "data": {
            "title": "BMW i3 94Ah Atelier REx",
            "model": "Électrique/Essence 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Corinne Bertrand",
                "address": {"url": "https://maps.google.com/?q=Besancon", "text": "FR-25000 Besançon"},
                "company": "BMW Besançon",
                "pro": True,
                "numbers": ["+33381123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-ilife-120-9d0e1f2a3b4c",
        "data": {
            "title": "BMW i3 iLife 120",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Dominique Arnaud",
                "address": {"url": "https://maps.google.com/?q=Perpignan", "text": "FR-66000 Perpignan"},
                "company": "BMW Perpignan",
                "pro": True,
                "numbers": ["+33468123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-berline-120ah-0e1f2a3b4c5d",
        "data": {
            "title": "BMW i3 Berline 120Ah",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Sylvie Legrand",
                "address": {"url": "https://maps.google.com/?q=Poitiers", "text": "FR-86000 Poitiers"},
                "company": "BMW Poitiers",
                "pro": True,
                "numbers": ["+33549123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-rex-1f2a3b4c5d6e",
        "data": {
            "title": "BMW i3 170ch REx",
            "model": "Électrique/Essence 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Marc Durand",
                "address": {"url": "https://maps.google.com/?q=Orleans", "text": "FR-45000 Orléans"},
                "company": "BMW Orléans",
                "pro": True,
                "numbers": ["+33238123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-windmill-atelier-2a3b4c5d6e7f",
        "data": {
            "title": "BMW i3 WindMill Atelier",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Christophe Nicolas",
                "address": {"url": "https://maps.google.com/?q=Rouen", "text": "FR-76000 Rouen"},
                "company": "BMW Rouen",
                "pro": True,
                "numbers": ["+33235123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-edition-3b4c5d6e7f8a",
        "data": {
            "title": "BMW i3 120Ah Edition",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Élodie Martinez",
                "address": {"url": "https://maps.google.com/?q=Mulhouse", "text": "FR-68100 Mulhouse"},
                "company": "BMW Mulhouse",
                "pro": True,
                "numbers": ["+33389123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-60ah-urban-atelier-4c5d6e7f8a9b",
        "data": {
            "title": "BMW i3 60 Ah Urban Atelier",
            "model": "Électrique 75 kW (102 Ch)",
            "vendor_info": {
                "name": "Bruno Fernandez",
                "address": {"url": "https://maps.google.com/?q=Annecy", "text": "FR-74000 Annecy"},
                "company": "BMW Annecy",
                "pro": True,
                "numbers": ["+33450123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-lodge-edition-5d6e7f8a9b0c",
        "data": {
            "title": "BMW i3 120Ah Lodge Edition",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Aurélie Petit",
                "address": {"url": "https://maps.google.com/?q=Avignon", "text": "FR-84000 Avignon"},
                "company": "BMW Avignon",
                "pro": True,
                "numbers": ["+33490123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-94ah-ilife-6e7f8a9b0c1d",
        "data": {
            "title": "BMW i3 94Ah iLife",
            "model": "Electrique 125 kW (170 Ch)",
            "vendor_info": {
                "name": "Gilles Leger",
                "address": {"url": "https://maps.google.com/?q=Pau", "text": "FR-64000 Pau"},
                "company": "BMW Pau",
                "pro": True,
                "numbers": ["+33559123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-170ch-94ah-7f8a9b0c1d2e",
        "data": {
            "title": "BMW i3 170ch 94Ah",
            "model": "Electrique 127 kW (173 Ch)",
            "vendor_info": {
                "name": "Fabienne Roy",
                "address": {"url": "https://maps.google.com/?q=Montpellier", "text": "FR-34000 Montpellier"},
                "company": "BMW Montpellier",
                "pro": True,
                "numbers": ["+33467123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-s-184ch-8a9b0c1d2e3f",
        "data": {
            "title": "BMW i3 S 184ch",
            "model": "Electrique 135 kW (184 Ch)",
            "vendor_info": {
                "name": "Renaud Blanc",
                "address": {"url": "https://maps.google.com/?q=Cannes", "text": "FR-06400 Cannes"},
                "company": "BMW Cannes",
                "pro": True,
                "numbers": ["+33493123456"],
            },
        },
    },
    {
        "url": "https://www.autoscout24.fr/offers/bmw-i3-120ah-world-atelier-9b0c1d2e3f4a",
        "data": {
            "title": "BMW i3 120Ah World Atelier",
            "model": "Electrique 126 kW (171 Ch)",
            "vendor_info": {
                "name": "Chantal Morel",
                "address": {"url": "https://maps.google.com/?q=Saint-Etienne", "text": "FR-42000 Saint-Étienne"},
                "company": "BMW Saint-Étienne",
                "pro": True,
                "numbers": ["+33477123456"],
            },
        },
    },
]


def get_fallback_offers():
    """Return sample offers when the scraper is unavailable. Use in API for fallback response."""
    return list(FALLBACK_OFFERS)
