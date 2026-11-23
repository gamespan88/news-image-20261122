# Content for "THE WORLD IN ONE DAY" — Sunday 22 November 2026.
# Every story is dated to that one day (UTC) or labelled FORECAST / CLAIM.

NUMBERS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or suppressed by air defence"),
    ("35%", "electricity goal for 2035, kept"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("50", "Wembanyama points, 19 rebounds"),
]

REGIONS = [
    ("EUROPE", 8, "#33526e"),
    ("MIDDLE EAST", 3, "#8a6d3b"),
    ("AMERICAS", 7, "#5b7553"),
    ("ASIA-PACIFIC", 5, "#7a4a56"),
    ("AFRICA", 4, "#a05c2c"),
    ("OCEANIA", 2, "#3f6d6a"),
    ("WORLD", 2, "#4a4a55"),
]

TIMELINE = ("01:00 HK polls open  ·  03:00 COP31 objections close  ·  "
            "05:11 Hamas seeks talks  ·  05:30 Verstappen wins Vegas  ·  "
            "06:00 COP31 approval due  ·  07:30 Approval slips again")

HEROES = [
    {
        "num": 1, "scene": "drones",
        "banner": "186 DRONES OVERNIGHT", "banner2": "161 DOWNED",
        "dateline": "KYIV REGION, UKRAINE · WAR", "chip": "REPORTED",
        "headline": "Russia fires 186 drones; Kyiv-region block destroyed",
        "summary": ("Air defences downed or suppressed 161 of 186 drones "
                    "(72 jet-powered) from eight directions. A five-storey block in "
                    "Dymer was destroyed — up to seven feared trapped, two injured, nine "
                    "evacuated. (Ukrainian Air Force via wires)"),
    },
    {
        "num": 2, "scene": "cop",
        "banner": "COP31: FINAL TEXT", "banner2": "NO FOSSIL FUELS",
        "dateline": "ANTALYA, TÜRKIYE · CLIMATE", "chip": "REPORTED",
        "headline": "Climate deal lands with no mention of fossil fuels",
        "summary": ("The final text \u201crecalls\u201d the Dubai pact whole, keeps the "
                    "55%-electricity-by-2035 goal, drops the $120bn adaptation target and "
                    "is the first to admit 1.5\u00b0C will be overshot. (Reuters, BBC, "
                    "The Guardian)"),
    },
    {
        "num": 3, "scene": "bahrain",
        "banner": "CLAIM VS DENIAL", "banner2": "2 RADARS?",
        "dateline": "MANAMA, BAHRAIN · IRAN", "chip": "CLAIM",
        "headline": "Iran claims two US radars hit; Bahrain denies it",
        "summary": ("The IRGC says it destroyed two Patriot radars on Saturday night. "
                    "Bahrain answered Sunday: the target was a civilian industrial site — "
                    "a fire, no injuries — and a violation of its sovereignty. "
                    "(Khaleej Times, Al Jazeera)"),
    },
]

# kind drives the mini scene strip icon.
CARDS = [
    {"num": 4, "kind": "vote", "dateline": "HONG KONG · VOTE",
     "headline": "HK elects its Election Committee",
     "text": "856 candidates, 723 seats. (SCMP)"},
    {"num": 5, "kind": "cricket", "dateline": "WELLINGTON · TEST",
     "headline": "India declare on 720/9 — a record in NZ",
     "text": "Rahul 156, Pant 128, Gill 98. (ESPN)"},
    {"num": 6, "kind": "f1", "dateline": "LAS VEGAS · F1",
     "headline": "Verstappen wins Las Vegas Grand Prix",
     "text": "From pole; Norris +0.639. (FIA)"},
    {"num": 7, "kind": "nba", "dateline": "SAN ANTONIO · NBA",
     "headline": "Wembanyama scores 50 as the Spurs roll on",
     "text": "114–91 v Pelicans, 19 reb. (Reuters)"},
    {"num": 8, "kind": "ship", "dateline": "FINLAND GULF · SEA",
     "headline": "Russian cargo ship Sparta II still burning",
     "text": "Finland leads the rescue. (Reuters)"},
    {"num": 9, "kind": "power", "dateline": "TEHRAN · ENERGY",
     "headline": "Iran begins rationing electricity",
     "text": "Rolling cuts, 2 hours a day. (Wires)"},
    {"num": 10, "kind": "health", "dateline": "BRASÍLIA · HEALTH",
     "headline": "Bolsonaro in intensive care in Brasília",
     "text": "Bowel obstruction; stable. (Reuters)"},
    {"num": 11, "kind": "cyber", "dateline": "WASHINGTON · CYBER",
     "headline": "FBI probes hack of its crime database",
     "text": "WA pauses gun-dealer checks. (AP)"},
    {"num": 12, "kind": "strike", "dateline": "BRUSSELS · TRAVEL",
     "headline": "Belgian controllers join Monday's strike",
     "text": "Most flights grounded. (Wires)"},
    {"num": 13, "kind": "poison", "dateline": "MANIPUR · LIQUOR",
     "headline": "Toxic-liquor toll in Manipur climbs to 19",
     "text": "600 in hospital, six held. (Xinhua)"},
    {"num": 14, "kind": "fire", "dateline": "CIKANDE · FIRE",
     "headline": "Candy-factory fire: 3 dead, 36 missing",
     "text": "Blaze tore through plant. (Detiknews)"},
    {"num": 15, "kind": "quake", "dateline": "JUNÍN · QUAKE",
     "headline": "Peru quake toll updated: 1 dead, 16 hurt",
     "text": "170 homes damaged in Junín. (Reuters)"},
]

BRIEFS = [
    (16, "Estonia shuts 5 Russia crossings 1 Dec (Reuters)"),
    (17, "Denmark expels a Russian attaché (Wires)"),
    (18, "Nepal PM Shah in Delhi on first visit (IANS)"),
    (19, "Somalia expels UAE ambassador (Wires)"),
    (20, "Sudan: RSF accused in W. Kordofan (Claim)"),
    (21, "Kenya discharges last Ebola patient (Wires)"),
    (22, "Melbourne: 70 years since '56 Olympics (ABC)"),
    (23, "Trump seeks 'permanent' Iran deal (Al Jazeera)"),
    (24, "Nvidia faces SEC accounting probe (Reports)"),
    (25, "Gold holds near $5,535 (Reuters)"),
    (26, "Bitcoin back above $60,000 (Market data)"),
    (27, "FORECAST: ATP final — Zverev v Alcaraz (Turin)"),
    (28, "FORECAST: Man Utd v Chelsea, Pochettino debut"),
    (29, "Hamas seeks urgent mediator talks (Al Jazeera)"),
    (30, "Nigeria boat capsizes: 24 dead (AP/Reuters)"),
    (31, "Snow strands ~1,500 in Fukushima village (dpa)"),
]

# (number, lon, lat) for the locator map.
PINS = [
    (1, 31, 49), (2, 30, 39), (3, 50, 26), (4, 114, 22), (5, 175, -41),
    (6, -115, 36), (7, -98, 29), (9, 51, 35), (10, -48, -16), (12, 4, 50),
    (13, 94, 24), (14, 106, -6), (15, -75, -12), (18, 77, 28),
    (30, 8, 6), (31, 140, 37),
]

DATE_CHECK = ("Left out as other days' news: the 400-drone, 110-missile barrage "
              "(Thu 19–Fri 20 Nov) · the 148-drone night and Kryvyi Rih double-tap "
              "(Fri–Sat) · \u2018El Chapo Isidro\u2019 captured (Fri) · Bayelsa boat, 24 dead "
              "(Fri) · BepiColombo's Mercury burn (Sat). Tonight's real count: 186 drones.")

SOURCES = ("Sources: Reuters, BBC, AP, Al Jazeera, The Guardian, Ukrinform, Kyiv Post, SCMP, "
           "ESPN/cricinfo, Detiknews, Xinhua and the day's wires named with each story. "
           "Pictures and map: original, drawn in code.")

CERTAINTY = ("CERTAINTY — REPORTED = carried by the day's wires · CLAIM = one side's account, "
             "labelled as such · FORECAST = still to happen when drawn")
