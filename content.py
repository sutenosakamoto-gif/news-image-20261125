# Structured content for the 25 November 2026 world-news front page.
# Every fact below is drawn from SOURCES.md (S1-S35, D1-D11), verified
# against dated 25 Nov 2026 wire/official reporting. Certainty labels:
# CONFIRMED = 2+ outlets report the fact; OFFICIAL = on the record /
# official data; REPORTED = one outlet, sourced; CLAIM = one side's account.

MASTHEAD = "THE WORLD IN A DAY"
DATE_LINE = "WEDNESDAY 25 NOVEMBER 2026"
SUBHEAD = [
    "Houthis say they hit a Saudi refinery as Asia tumbles on a tariff threat,",
    "and the first Pakistani reaches China's space station",
]
REGION_LINE = (
    "33 STORIES  \u00b7  MIDDLE EAST 5  \u00b7  ASIA-PACIFIC 9  \u00b7  EUROPE 8  \u00b7  "
    "NORTH AMERICA 4  \u00b7  AFRICA 3  \u00b7  LATIN AMERICA 3  \u00b7  MARKETS 1"
)

# (number, region, certainty, headline, body lines, illustration chip)
LEADS = [
    (
        1, "MIDDLE EAST", "CLAIM",
        "Houthis say they hit Saudi refinery and Riyadh finance district",
        [
            "The Saudi-led coalition says it intercepted",
            "four drones at Ras Tanura. Houthis threaten",
            "Jeddah and all Saudi Red Sea ports.",
        ],
        "4 DRONES DOWN",
    ),
    (
        2, "MARKETS", "CONFIRMED",
        "Asia tumbles as tariff threat kills the AI rebound",
        [
            "MSCI Asia-Pacific ex-Japan -2.3%; Seoul -5.3%,",
            "Taiwan -5.1%, Nikkei -2.9%. New Section 301",
            "tariffs on 16 partners REPORTED as imminent.",
        ],
        "-2.3% MSCI ASIA",
    ),
    (
        3, "SCIENCE", "CONFIRMED",
        "Shenzhou-24 carries the first Pakistani to Tiangong",
        [
            "Muhammad Zeeshan Ali, 40, is the first Pakistani",
            "in orbit and the first foreign astronaut to",
            "visit China's station. Docked 03:56 UTC.",
        ],
        "1ST PAKISTANI IN ORBIT",
    ),
]

# (number, region, certainty, headline, body lines, chip)
MIDDLE = [
    (
        4, "MIDDLE EAST", "REPORTED",
        "Israeli strike kills Hamas official and family",
        ["Abuelouf, wife and 2 children killed; 2nd in 24 hrs."],
        "2ND IN 24 HRS",
    ),
    (
        5, "EUROPE", "CONFIRMED",
        "Ukraine drones hit two Russian refineries",
        ["Fires at Samara plants overnight; one dead."],
        "2 REFINERIES HIT",
    ),
    (
        6, "LATIN AMERICA", "CONFIRMED",
        "All Colombia hostages rescued in Cartagena",
        ["Forces storm Éxito supermarket; about 20 freed."],
        "20 FREED",
    ),
    (
        7, "ASIA-PACIFIC", "CONFIRMED",
        "China probes a fourth Politburo member",
        ["Chen Jining under graft probe; city pledges loyalty."],
        "4TH PROBE",
    ),
    (
        8, "NORTH AMERICA", "CONFIRMED",
        "Thanksgiving storms threaten Macy's parade",
        ["Balloon risk in 25–35 mph gusts; storm may form."],
        "81.5M TRAVELLING",
    ),
    (
        9, "ASIA-PACIFIC", "CONFIRMED",
        "Australia\u2013Solomon Islands sign security pact",
        ["Canberra named primary partner, replacing China."],
        "NEW SECURITY PACT",
    ),
    (
        10, "AFRICA", "CONFIRMED",
        "Ramaphosa wins bid to overturn \u2018Farmgate\u2019 report",
        ["Court sets aside panel report on constitution."],
        "FARMGATE CASE WON",
    ),
    (
        11, "EUROPE", "CONFIRMED",
        "EU proposes \u20ac50bn fund to lead in quantum",
        ["Buy-European rules to cut US and China reliance."],
        "\u20ac50BN FUND",
    ),
    (
        12, "EUROPE", "CONFIRMED",
        "Greeks strike over wages and services",
        ["Nationwide stoppage; third such action in weeks."],
        "NATIONWIDE STRIKE",
    ),
    (
        13, "ASIA-PACIFIC", "CONFIRMED",
        "Rescuers search for \u2018dozens\u2019 in Indonesian mine",
        ["Workers 100 m down in flooded Pongkor mine."],
        "DOZENS TRAPPED",
    ),
]

# (number, headline, short text) — one brief each, 20 items
ALSO = [
    (14, "N. Korea expels Swiss envoy", "48 hrs to leave; office shut."),
    (15, "Russian planes in Korea ADIZ", "Seoul scrambles jets; alert on."),
    (16, "Australian inflation 4.9%", "Core 3.8%, a two-year high."),
    (17, "Iran defiant over US blockade", "Prices held 3 months; CPI +88.7%."),
    (18, "Gulf bourses mixed", "Saudi -0.3%, Abu Dhabi +0.5%."),
    (19, "Jordan death sentence", "Court rules over 5 Nov stabbing."),
    (20, "Spain election: housing fight", "S\u00e1nchez vs Feij\u00f3o; vote Sunday."),
    (21, "German economy +0.1% in Q3", "Slightly below forecasts."),
    (22, "UK defence plan at risk", "~\u00a328.8bn costlier than planned."),
    (23, "UK warns firms of sabotage", "Officials cite Russian sabotage."),
    (24, "2030 World Cup final race", "Bernab\u00e9u vs 115,000-seat arena."),
    (25, "Miss Universe 2026: Barreto", "24 Nov local; first mother to win."),
    (26, "Australia's LGBTQ apology", "Apology for decades of bias."),
    (27, "Myanmar landmine toll worst", "1,891 hurt or killed in 2025."),
    (28, "Sahel drones change the war", "Cheap FPV drones erode air power."),
    (29, "Naspers earnings up 12%", "Driven by Tencent; EPS 240 cents."),
    (30, "Costa Rica's rope bridges", "Rope crossings as forests vanish."),
    (31, "US soldier sold secrets", "Secrets sold to Chinese buyers."),
    (32, "Abrego Garcia leaves for Spain", "Left voluntarily for Spain."),
    (33, "Fort Hood shooter seeks delay", "Asks for time to contest sentence."),
]

# (figure, caption) — THE DAY IN NUMBERS strip
NUMBERS = [
    ("-2.3%", "MSCI Asia-Pacific ex-Japan, Wed (Seoul -5.3%)"),
    ("4", "drones the coalition says it stopped at Ras Tanura"),
    ("20", "hostages freed in the Cartagena storming"),
    ("4.9%", "Australia's Oct inflation; core 3.8%, 2-yr high"),
    ("\u20ac50bn", "EU quantum equity fund proposed"),
    ("81.5m", "Americans travelling for Thanksgiving (AAA)"),
    ("1st", "Pakistani in orbit \u2014 first foreigner at Tiangong"),
]

# (time, label) — UTC timeline; DUE items carry no actuals
TIMELINE = [
    ("00:18 UTC", "Shenzhou-24 lifts off from Jiuquan"),
    ("~00:30 UTC", "Australia CPI released: 4.9%"),
    ("~02:00 UTC", "Solomons security pact signed"),
    ("03:56 UTC", "Shenzhou-24 docks with Tiangong"),
    ("Asian morning", "Markets tumble on tariff-threat reports"),
    ("Morning UTC", "Houthi claims; 4 drones intercepted"),
    ("~10:00 UTC", "Cartagena hostages freed"),
    ("13:30 UTC", "US PCE & GDP \u2014 DUE, not yet released"),
]

# DATE CHECK: (day label, text) — structured exclusion audit
DATE_CHECK = [
    ("24 NOV", "Huawei guilty on 10 of 12 counts (Brooklyn jury)"),
    ("24 NOV", "Shein agrees $100m FTC settlement"),
    ("24 NOV", "Senegal reinstated as 2025 AFCON winners (CAS)"),
    ("24 NOV", "UN: 47,000 women killed by partners in 2025 \u2014 figures published Tue"),
    ("24 NOV", "Putin's retaliation \u2018inevitable\u2019 threat (Tue); Samara strikes are Wed"),
    ("24 NOV", "Yesterday's leads: Nvidia rally, Hanoi blast, Zaporizhzhia attack"),
    ("24 NOV", "Riyadh tower strike: 11 wounded (Tue)"),
    ("24 NOV", "Pope Francis' private diary published"),
    ("23\u201324 NOV", "Burglary at William & Kate's Anmer Hall; 2 arrested"),
    ("24 NOV", "Unclassified CIA/ODNI system breached (NYT report)"),
]
NOT_YET = (
    "NOT YET: US PCE & GDP actuals (due 13:30 UTC) \u00b7 Spain vote 29 Nov \u00b7 "
    "OPEC+ 29 Nov \u00b7 Fed Dec decision \u00b7 Macy's balloons (Thu risk, not outcome)"
)

LEGEND = (
    "CONFIRMED = 2+ outlets report the fact  \u00b7  OFFICIAL = on the record / official data  "
    "\u00b7  REPORTED = one outlet, sourced  \u00b7  CLAIM = one side's account"
)
FOOTER_NOTE = (
    "Scenes are drawn illustrations, not photographs. Sources: Reuters, AP, AFP \u2014 "
    "full list in SOURCES.md. 33 stories, 7 regions."
)

# World-map pins: (story number, lon, lat, region colour key, label offset dx, dy)
REGION_COLOURS = {
    "MIDDLE EAST": (166, 30, 34),
    "ASIA-PACIFIC": (31, 78, 121),
    "EUROPE": (46, 107, 52),
    "NORTH AMERICA": (122, 74, 18),
    "AFRICA": (178, 106, 0),
    "LATIN AMERICA": (107, 63, 160),
    "MARKETS": (51, 51, 51),
}
PINS = [
    (1, 50.1, 26.6, "MIDDLE EAST", 16, -6),
    (2, 139.7, 35.7, "MARKETS", 10, -16),
    (3, 100.3, 39.8, "ASIA-PACIFIC", 12, -14),
    (4, 34.5, 31.5, "MIDDLE EAST", -16, 12),
    (5, 50.1, 53.2, "EUROPE", 12, -12),
    (6, -75.5, 10.4, "LATIN AMERICA", -14, -14),
    (7, 121.5, 31.2, "ASIA-PACIFIC", 12, 10),
    (8, -74.0, 40.7, "NORTH AMERICA", 12, -14),
    (9, 160.0, -9.6, "ASIA-PACIFIC", 10, 10),
    (10, 28.2, -25.7, "AFRICA", 12, -10),
    (11, 4.35, 50.85, "EUROPE", -18, -12),
    (12, 23.7, 38.0, "EUROPE", 12, 10),
    (13, 106.8, -6.6, "ASIA-PACIFIC", 12, 8),
    (14, 125.8, 39.0, "ASIA-PACIFIC", 12, -12),
    (15, 130.9, 37.5, "ASIA-PACIFIC", 12, 10),
    (16, 151.2, -33.9, "ASIA-PACIFIC", 12, -10),
    (17, 51.4, 35.7, "MIDDLE EAST", 14, -18),
    (18, 55.3, 25.2, "MIDDLE EAST", 16, 12),
    (19, 35.9, 31.95, "MIDDLE EAST", -18, -12),
    (20, -3.7, 40.4, "EUROPE", -16, -14),
    (21, 13.4, 52.5, "EUROPE", 10, -14),
    (22, -0.1, 51.5, "EUROPE", -20, 10),
    (23, -0.1, 51.5, "EUROPE", 16, 12),
    (24, -7.6, 33.6, "AFRICA", -8, 16),
    (25, -66.1, 18.5, "LATIN AMERICA", 12, -12),
    (26, 149.1, -35.3, "ASIA-PACIFIC", -14, -8),
    (27, 96.15, 16.8, "ASIA-PACIFIC", 12, 8),
    (28, -8.0, 12.6, "AFRICA", 14, -16),
    (29, 18.4, -33.9, "AFRICA", -14, -12),
    (30, -84.1, 9.9, "LATIN AMERICA", -14, 10),
    (31, -77.0, 38.9, "NORTH AMERICA", -14, 12),
    (32, -3.7, 40.4, "EUROPE", 14, 12),
    (33, -97.8, 31.1, "NORTH AMERICA", 12, 10),
]
