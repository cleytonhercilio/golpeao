"""
GolPeão — Seed de Dados: Copa do Mundo FIFA 2026
48 Seleções | 12 Grupos | 104 Jogos
Fonte: Sorteio FIFA — 5 de dezembro de 2024, Washington D.C.

Horários em UTC. Brasília = UTC-3.
"""

from datetime import datetime, timezone

# ============================================================
# TIMES — 48 Seleções com código ISO-2 para flagcdn.com
# ============================================================
# Formato: (id, name_pt, name_en, iso_code, group, confederation)
# Grupos confirmados no sorteio de 5/dez/2024

TEAMS = [
    # ── GRUPO A — Sede: México ────────────────────────────────
    (1,  "México",              "Mexico",               "mx",     "A", "CONCACAF"),
    (2,  "Coreia do Sul",       "South Korea",          "kr",     "A", "AFC"),
    (3,  "África do Sul",       "South Africa",         "za",     "A", "CAF"),
    (4,  "República Tcheca",    "Czech Republic",       "cz",     "A", "UEFA"),

    # ── GRUPO B — Sede: Canadá ────────────────────────────────
    (5,  "Canadá",              "Canada",               "ca",     "B", "CONCACAF"),
    (6,  "Qatar",               "Qatar",                "qa",     "B", "AFC"),
    (7,  "Suíça",               "Switzerland",          "ch",     "B", "UEFA"),
    (8,  "Bósnia e Herzegovina","Bosnia and Herzegovina","ba",    "B", "UEFA"),

    # ── GRUPO C — Sede: EUA ───────────────────────────────────
    (9,  "Brasil",              "Brazil",               "br",     "C", "CONMEBOL"),
    (10, "Marrocos",            "Morocco",              "ma",     "C", "CAF"),
    (11, "Haiti",               "Haiti",                "ht",     "C", "CONCACAF"),
    (12, "Escócia",             "Scotland",             "gb-sct", "C", "UEFA"),

    # ── GRUPO D — Sede: EUA ───────────────────────────────────
    (13, "Estados Unidos",      "United States",        "us",     "D", "CONCACAF"),
    (14, "Paraguai",            "Paraguay",             "py",     "D", "CONMEBOL"),
    (15, "Austrália",           "Australia",            "au",     "D", "AFC"),
    (16, "Turquia",             "Turkey",               "tr",     "D", "UEFA"),

    # ── GRUPO E — Sede: EUA ───────────────────────────────────
    (17, "Alemanha",            "Germany",              "de",     "E", "UEFA"),
    (18, "Curaçao",             "Curaçao",              "cw",     "E", "CONCACAF"),
    (19, "Costa do Marfim",     "Ivory Coast",          "ci",     "E", "CAF"),
    (20, "Equador",             "Ecuador",              "ec",     "E", "CONMEBOL"),

    # ── GRUPO F — Sede: EUA/Canadá ────────────────────────────
    (21, "Holanda",             "Netherlands",          "nl",     "F", "UEFA"),
    (22, "Japão",               "Japan",                "jp",     "F", "AFC"),
    (23, "Suécia",              "Sweden",               "se",     "F", "UEFA"),
    (24, "Tunísia",             "Tunisia",              "tn",     "F", "CAF"),

    # ── GRUPO G — Sede: EUA ───────────────────────────────────
    (25, "Bélgica",             "Belgium",              "be",     "G", "UEFA"),
    (26, "Egito",               "Egypt",                "eg",     "G", "CAF"),
    (27, "Irã",                 "Iran",                 "ir",     "G", "AFC"),
    (28, "Nova Zelândia",       "New Zealand",          "nz",     "G", "OFC"),

    # ── GRUPO H — Sede: EUA/México ────────────────────────────
    (29, "Espanha",             "Spain",                "es",     "H", "UEFA"),
    (30, "Cabo Verde",          "Cape Verde",           "cv",     "H", "CAF"),
    (31, "Arábia Saudita",      "Saudi Arabia",         "sa",     "H", "AFC"),
    (32, "Uruguai",             "Uruguay",              "uy",     "H", "CONMEBOL"),

    # ── GRUPO I — Sede: EUA/Canadá ────────────────────────────
    (33, "França",              "France",               "fr",     "I", "UEFA"),
    (34, "Senegal",             "Senegal",              "sn",     "I", "CAF"),
    (35, "Noruega",             "Norway",               "no",     "I", "UEFA"),
    (36, "Iraque",              "Iraq",                 "iq",     "I", "AFC"),

    # ── GRUPO J — Sede: EUA ───────────────────────────────────
    (37, "Argentina",           "Argentina",            "ar",     "J", "CONMEBOL"),
    (38, "Argélia",             "Algeria",              "dz",     "J", "CAF"),
    (39, "Áustria",             "Austria",              "at",     "J", "UEFA"),
    (40, "Jordânia",            "Jordan",               "jo",     "J", "AFC"),

    # ── GRUPO K — Sede: EUA/México ────────────────────────────
    (41, "Portugal",            "Portugal",             "pt",     "K", "UEFA"),
    (42, "Rep. Dem. do Congo",  "DR Congo",             "cd",     "K", "CAF"),
    (43, "Uzbequistão",         "Uzbekistan",           "uz",     "K", "AFC"),
    (44, "Colômbia",            "Colombia",             "co",     "K", "CONMEBOL"),

    # ── GRUPO L — Sede: EUA/Canadá ────────────────────────────
    (45, "Inglaterra",          "England",              "gb-eng", "L", "UEFA"),
    (46, "Croácia",             "Croatia",              "hr",     "L", "UEFA"),
    (47, "Gana",                "Ghana",                "gh",     "L", "CAF"),
    (48, "Panamá",              "Panama",               "pa",     "L", "CONCACAF"),
]

# ============================================================
# JOGOS DA FASE DE GRUPOS — 36 jogos (3 por grupo × 12 grupos)
# ============================================================
# Formato: (match_number, home_id, away_id, group, venue, scheduled_utc, stage)
# home_id / away_id = índice em TEAMS (1-based)
# scheduled_utc: datetime UTC aproximado (horários ET convertidos para UTC)
# Fonte: USA Today / NBC Sports (confirmados pela FIFA em dez/2025)

GROUP_STAGE_FIXTURES = [
    # ── GRUPO A ──────────────────────────────────────────────
    # Rodada 1
    (1,  1,  3,  "A", "Estadio Azteca, Cidade do México",    datetime(2026, 6, 11, 20, 0, tzinfo=timezone.utc)),
    (2,  2,  4,  "A", "Estadio Akron, Guadalajara",           datetime(2026, 6, 12,  3, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (17, 1,  4,  "A", "Estadio Azteca, Cidade do México",    datetime(2026, 6, 18, 18, 0, tzinfo=timezone.utc)),
    (18, 3,  2,  "A", "Estadio Akron, Guadalajara",           datetime(2026, 6, 18, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3 (simultâneos)
    (33, 1,  2,  "A", "Estadio Azteca, Cidade do México",    datetime(2026, 6, 26, 22, 0, tzinfo=timezone.utc)),
    (34, 4,  3,  "A", "Estadio Akron, Guadalajara",           datetime(2026, 6, 26, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO B ──────────────────────────────────────────────
    # Rodada 1
    (3,  5,  8,  "B", "BMO Field, Toronto",                  datetime(2026, 6, 12, 20, 0, tzinfo=timezone.utc)),
    (4,  6,  7,  "B", "Levi's Stadium, San Francisco",       datetime(2026, 6, 13,  3, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (19, 5,  7,  "B", "BMO Field, Toronto",                  datetime(2026, 6, 19, 18, 0, tzinfo=timezone.utc)),
    (20, 8,  6,  "B", "Levi's Stadium, San Francisco",       datetime(2026, 6, 19, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (35, 5,  6,  "B", "BMO Field, Toronto",                  datetime(2026, 6, 27, 22, 0, tzinfo=timezone.utc)),
    (36, 7,  8,  "B", "Levi's Stadium, San Francisco",       datetime(2026, 6, 27, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO C ──────────────────────────────────────────────
    # Rodada 1
    (5,  9,  12, "C", "Gillette Stadium, Boston",            datetime(2026, 6, 13, 21, 0, tzinfo=timezone.utc)),
    (6,  10, 11, "C", "Lumen Field, Seattle",                datetime(2026, 6, 14,  2, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (21, 9,  11, "C", "Gillette Stadium, Boston",            datetime(2026, 6, 20, 18, 0, tzinfo=timezone.utc)),
    (22, 12, 10, "C", "Lumen Field, Seattle",                datetime(2026, 6, 20, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (37, 9,  10, "C", "Gillette Stadium, Boston",            datetime(2026, 6, 28, 22, 0, tzinfo=timezone.utc)),
    (38, 11, 12, "C", "Lumen Field, Seattle",                datetime(2026, 6, 28, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO D ──────────────────────────────────────────────
    # Rodada 1
    (7,  13, 14, "D", "SoFi Stadium, Los Angeles",           datetime(2026, 6, 13,  2, 0, tzinfo=timezone.utc)),
    (8,  15, 16, "D", "Estadio BBVA, Monterrey",             datetime(2026, 6, 14,  3, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (23, 13, 16, "D", "SoFi Stadium, Los Angeles",           datetime(2026, 6, 20, 22, 0, tzinfo=timezone.utc)),
    (24, 14, 15, "D", "Estadio BBVA, Monterrey",             datetime(2026, 6, 21,  2, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (39, 13, 15, "D", "SoFi Stadium, Los Angeles",           datetime(2026, 6, 27, 18, 0, tzinfo=timezone.utc)),
    (40, 16, 14, "D", "Estadio BBVA, Monterrey",             datetime(2026, 6, 27, 18, 0, tzinfo=timezone.utc)),

    # ── GRUPO E ──────────────────────────────────────────────
    # Rodada 1
    (9,  17, 18, "E", "NRG Stadium, Houston",                datetime(2026, 6, 14, 18, 0, tzinfo=timezone.utc)),
    (10, 19, 20, "E", "Lincoln Financial Field, Philadelphia",datetime(2026, 6, 14, 21, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (25, 17, 20, "E", "NRG Stadium, Houston",                datetime(2026, 6, 21, 18, 0, tzinfo=timezone.utc)),
    (26, 18, 19, "E", "Lincoln Financial Field, Philadelphia",datetime(2026, 6, 21, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (41, 17, 19, "E", "NRG Stadium, Houston",                datetime(2026, 6, 29, 22, 0, tzinfo=timezone.utc)),
    (42, 20, 18, "E", "Lincoln Financial Field, Philadelphia",datetime(2026, 6, 29, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO F ──────────────────────────────────────────────
    # Rodada 1
    (11, 21, 22, "F", "AT&T Stadium, Dallas",                datetime(2026, 6, 15,  0, 0, tzinfo=timezone.utc)),
    (12, 23, 24, "F", "Estadio BBVA, Monterrey",             datetime(2026, 6, 15,  3, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (27, 21, 24, "F", "AT&T Stadium, Dallas",                datetime(2026, 6, 22, 18, 0, tzinfo=timezone.utc)),
    (28, 23, 22, "F", "Estadio BBVA, Monterrey",             datetime(2026, 6, 22, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (43, 21, 23, "F", "AT&T Stadium, Dallas",                datetime(2026, 6, 30, 22, 0, tzinfo=timezone.utc)),
    (44, 24, 22, "F", "Estadio BBVA, Monterrey",             datetime(2026, 6, 30, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO G ──────────────────────────────────────────────
    # Rodada 1
    (13, 25, 27, "G", "Lumen Field, Seattle",                datetime(2026, 6, 15, 20, 0, tzinfo=timezone.utc)),
    (14, 26, 28, "G", "SoFi Stadium, Los Angeles",           datetime(2026, 6, 16,  2, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (29, 25, 28, "G", "Lumen Field, Seattle",                datetime(2026, 6, 22, 22, 0, tzinfo=timezone.utc)),
    (30, 27, 26, "G", "SoFi Stadium, Los Angeles",           datetime(2026, 6, 23,  2, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (45, 25, 26, "G", "Lumen Field, Seattle",                datetime(2026, 7,  1, 22, 0, tzinfo=timezone.utc)),
    (46, 28, 27, "G", "SoFi Stadium, Los Angeles",           datetime(2026, 7,  1, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO H ──────────────────────────────────────────────
    # Rodada 1
    (15, 29, 30, "H", "Mercedes-Benz Stadium, Atlanta",      datetime(2026, 6, 15, 17, 0, tzinfo=timezone.utc)),
    (16, 31, 32, "H", "Hard Rock Stadium, Miami",            datetime(2026, 6, 15, 23, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (31, 29, 32, "H", "Mercedes-Benz Stadium, Atlanta",      datetime(2026, 6, 23, 18, 0, tzinfo=timezone.utc)),
    (32, 30, 31, "H", "Hard Rock Stadium, Miami",            datetime(2026, 6, 23, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (47, 29, 31, "H", "Mercedes-Benz Stadium, Atlanta",      datetime(2026, 7,  2, 22, 0, tzinfo=timezone.utc)),
    (48, 32, 30, "H", "Hard Rock Stadium, Miami",            datetime(2026, 7,  2, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO I ──────────────────────────────────────────────
    # Rodada 1
    (49, 33, 34, "I", "MetLife Stadium, Nova York/NJ",       datetime(2026, 6, 16, 20, 0, tzinfo=timezone.utc)),
    (50, 35, 36, "I", "Gillette Stadium, Boston",            datetime(2026, 6, 16, 23, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (51, 33, 36, "I", "MetLife Stadium, Nova York/NJ",       datetime(2026, 6, 24, 18, 0, tzinfo=timezone.utc)),
    (52, 34, 35, "I", "Gillette Stadium, Boston",            datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (53, 33, 35, "I", "MetLife Stadium, Nova York/NJ",       datetime(2026, 7,  3, 22, 0, tzinfo=timezone.utc)),
    (54, 36, 34, "I", "Gillette Stadium, Boston",            datetime(2026, 7,  3, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO J ──────────────────────────────────────────────
    # Rodada 1
    (55, 37, 38, "J", "Arrowhead Stadium, Kansas City",      datetime(2026, 6, 17,  2, 0, tzinfo=timezone.utc)),
    (56, 39, 40, "J", "Levi's Stadium, San Francisco",       datetime(2026, 6, 17,  5, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (57, 37, 40, "J", "Arrowhead Stadium, Kansas City",      datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)),
    (58, 38, 39, "J", "Levi's Stadium, San Francisco",       datetime(2026, 6, 25,  2, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (59, 37, 39, "J", "Arrowhead Stadium, Kansas City",      datetime(2026, 7,  4, 22, 0, tzinfo=timezone.utc)),
    (60, 40, 38, "J", "Levi's Stadium, San Francisco",       datetime(2026, 7,  4, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO K ──────────────────────────────────────────────
    # Rodada 1
    (61, 41, 44, "K", "NRG Stadium, Houston",                datetime(2026, 6, 17, 18, 0, tzinfo=timezone.utc)),
    (62, 42, 43, "K", "Lincoln Financial Field, Philadelphia",datetime(2026, 6, 17, 21, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (63, 41, 43, "K", "NRG Stadium, Houston",                datetime(2026, 6, 25, 18, 0, tzinfo=timezone.utc)),
    (64, 44, 42, "K", "Lincoln Financial Field, Philadelphia",datetime(2026, 6, 25, 22, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (65, 41, 42, "K", "NRG Stadium, Houston",                datetime(2026, 7,  5, 22, 0, tzinfo=timezone.utc)),
    (66, 43, 44, "K", "Lincoln Financial Field, Philadelphia",datetime(2026, 7,  5, 22, 0, tzinfo=timezone.utc)),

    # ── GRUPO L ──────────────────────────────────────────────
    # Rodada 1
    (67, 45, 46, "L", "AT&T Stadium, Dallas",                datetime(2026, 6, 17, 21, 0, tzinfo=timezone.utc)),
    (68, 47, 48, "L", "BC Place, Vancouver",                 datetime(2026, 6, 18,  2, 0, tzinfo=timezone.utc)),
    # Rodada 2
    (69, 45, 48, "L", "AT&T Stadium, Dallas",                datetime(2026, 6, 25, 22, 0, tzinfo=timezone.utc)),
    (70, 46, 47, "L", "BC Place, Vancouver",                 datetime(2026, 6, 26,  2, 0, tzinfo=timezone.utc)),
    # Rodada 3
    (71, 45, 47, "L", "AT&T Stadium, Dallas",                datetime(2026, 7,  6, 22, 0, tzinfo=timezone.utc)),
    (72, 48, 46, "L", "BC Place, Vancouver",                 datetime(2026, 7,  6, 22, 0, tzinfo=timezone.utc)),
]

# ============================================================
# ROUND OF 32 (OITAVAS AMPLIADAS) — 16 jogos
# Times preenchidos após fase de grupos
# Formato: (match_number, match_label, venue, scheduled_utc)
# ============================================================
ROUND_OF_32_FIXTURES = [
    (73,  "2º Grupo A vs 2º Grupo B",         "SoFi Stadium, Los Angeles",             datetime(2026, 6, 28, 20, 0, tzinfo=timezone.utc)),
    (74,  "1º Grupo E vs 3º (A/B/C/D/F)",     "Gillette Stadium, Boston",              datetime(2026, 6, 29, 21, 30, tzinfo=timezone.utc)),
    (75,  "1º Grupo F vs 2º Grupo C",          "Estadio BBVA, Monterrey",              datetime(2026, 6, 29,  2, 0, tzinfo=timezone.utc)),
    (76,  "1º Grupo C vs 2º Grupo F",          "NRG Stadium, Houston",                 datetime(2026, 6, 29, 18, 0, tzinfo=timezone.utc)),
    (77,  "1º Grupo I vs 3º (C/D/F/G/H)",     "MetLife Stadium, Nova York/NJ",        datetime(2026, 6, 30, 22, 0, tzinfo=timezone.utc)),
    (78,  "2º Grupo E vs 2º Grupo I",          "AT&T Stadium, Dallas",                 datetime(2026, 6, 30, 18, 0, tzinfo=timezone.utc)),
    (79,  "1º Grupo A vs 3º (C/E/F/H/I)",     "Estadio Azteca, Cidade do México",     datetime(2026, 7,  1,  2, 0, tzinfo=timezone.utc)),
    (80,  "1º Grupo L vs 3º (E/H/I/J/K)",     "Mercedes-Benz Stadium, Atlanta",       datetime(2026, 7,  1, 17, 0, tzinfo=timezone.utc)),
    (81,  "1º Grupo D vs 3º (B/E/F/I/J)",     "Levi's Stadium, San Francisco",        datetime(2026, 7,  1,  1, 0, tzinfo=timezone.utc)),
    (82,  "1º Grupo G vs 3º (A/E/H/I/J)",     "Lumen Field, Seattle",                 datetime(2026, 7,  1, 21, 0, tzinfo=timezone.utc)),
    (83,  "2º Grupo K vs 2º Grupo L",          "BMO Field, Toronto",                   datetime(2026, 7,  2,  0, 0, tzinfo=timezone.utc)),
    (84,  "1º Grupo H vs 2º Grupo J",          "SoFi Stadium, Los Angeles",            datetime(2026, 7,  2, 20, 0, tzinfo=timezone.utc)),
    (85,  "1º Grupo B vs 3º (E/F/G/I/J)",     "BC Place, Vancouver",                  datetime(2026, 7,  2,  4, 0, tzinfo=timezone.utc)),
    (86,  "1º Grupo J vs 2º Grupo H",          "Hard Rock Stadium, Miami",             datetime(2026, 7,  3, 23, 0, tzinfo=timezone.utc)),
    (87,  "1º Grupo K vs 3º (D/E/I/J/L)",     "Arrowhead Stadium, Kansas City",       datetime(2026, 7,  4,  2, 30, tzinfo=timezone.utc)),
    (88,  "2º Grupo D vs 2º Grupo G",          "AT&T Stadium, Dallas",                 datetime(2026, 7,  3, 19, 0, tzinfo=timezone.utc)),
]

# ============================================================
# ROUND OF 16 — 8 jogos
# ============================================================
ROUND_OF_16_FIXTURES = [
    (89,  "Venc. Jogo 74 vs Venc. Jogo 77",   "Lincoln Financial Field, Philadelphia", datetime(2026, 7,  4, 22, 0, tzinfo=timezone.utc)),
    (90,  "Venc. Jogo 73 vs Venc. Jogo 75",   "NRG Stadium, Houston",                 datetime(2026, 7,  4, 18, 0, tzinfo=timezone.utc)),
    (91,  "Venc. Jogo 76 vs Venc. Jogo 78",   "Estadio BBVA, Monterrey",              datetime(2026, 7,  5, 22, 0, tzinfo=timezone.utc)),
    (92,  "Venc. Jogo 80 vs Venc. Jogo 83",   "Levi's Stadium, San Francisco",        datetime(2026, 7,  6,  2, 0, tzinfo=timezone.utc)),
    (93,  "Venc. Jogo 79 vs Venc. Jogo 82",   "Estadio Azteca, Cidade do México",     datetime(2026, 7,  6, 22, 0, tzinfo=timezone.utc)),
    (94,  "Venc. Jogo 81 vs Venc. Jogo 88",   "SoFi Stadium, Los Angeles",            datetime(2026, 7,  7,  2, 0, tzinfo=timezone.utc)),
    (95,  "Venc. Jogo 84 vs Venc. Jogo 86",   "Hard Rock Stadium, Miami",             datetime(2026, 7,  7, 22, 0, tzinfo=timezone.utc)),
    (96,  "Venc. Jogo 85 vs Venc. Jogo 87",   "Arrowhead Stadium, Kansas City",       datetime(2026, 7,  8,  2, 30, tzinfo=timezone.utc)),
]

# ============================================================
# QUARTAS DE FINAL — 4 jogos
# ============================================================
QUARTERFINAL_FIXTURES = [
    (97,  "Venc. Jogo 89 vs Venc. Jogo 90",   "MetLife Stadium, Nova York/NJ",        datetime(2026, 7,  9, 22, 0, tzinfo=timezone.utc)),
    (98,  "Venc. Jogo 91 vs Venc. Jogo 92",   "Lumen Field, Seattle",                 datetime(2026, 7, 10,  2, 0, tzinfo=timezone.utc)),
    (99,  "Venc. Jogo 93 vs Venc. Jogo 94",   "AT&T Stadium, Dallas",                 datetime(2026, 7, 10, 22, 0, tzinfo=timezone.utc)),
    (100, "Venc. Jogo 95 vs Venc. Jogo 96",   "SoFi Stadium, Los Angeles",            datetime(2026, 7, 11,  2, 0, tzinfo=timezone.utc)),
]

# ============================================================
# SEMIFINAIS — 2 jogos
# ============================================================
SEMIFINAL_FIXTURES = [
    (101, "Venc. Jogo 97 vs Venc. Jogo 98",   "Mercedes-Benz Stadium, Atlanta",       datetime(2026, 7, 14, 22, 0, tzinfo=timezone.utc)),
    (102, "Venc. Jogo 99 vs Venc. Jogo 100",  "Gillette Stadium, Boston",             datetime(2026, 7, 15, 22, 0, tzinfo=timezone.utc)),
]

# ============================================================
# 3º LUGAR + FINAL
# ============================================================
FINAL_FIXTURES = [
    (103, "3º Lugar: Perd. Jogo 101 vs Perd. Jogo 102", "Hard Rock Stadium, Miami",  datetime(2026, 7, 18, 22, 0, tzinfo=timezone.utc)),
    (104, "FINAL: Venc. Jogo 101 vs Venc. Jogo 102",    "MetLife Stadium, Nova York/NJ", datetime(2026, 7, 19, 21, 0, tzinfo=timezone.utc)),
]

# ============================================================
# STAGES MAPEADOS
# ============================================================
STAGE_NAMES = {
    "group":   "Fase de Grupos",
    "round32": "Oitavas de Final",
    "round16": "Round of 16",
    "qf":      "Quartas de Final",
    "sf":      "Semifinais",
    "third":   "Disputa de 3º Lugar",
    "final":   "Final",
}

# ============================================================
# SUMMARY
# ============================================================
def print_summary():
    total = (
        len(GROUP_STAGE_FIXTURES) +
        len(ROUND_OF_32_FIXTURES) +
        len(ROUND_OF_16_FIXTURES) +
        len(QUARTERFINAL_FIXTURES) +
        len(SEMIFINAL_FIXTURES) +
        len(FINAL_FIXTURES)
    )
    print(f"🏆 GolPeão — Copa do Mundo FIFA 2026")
    print(f"📋 Times: {len(TEAMS)}")
    print(f"⚽ Jogos fase de grupos: {len(GROUP_STAGE_FIXTURES)}")
    print(f"🏅 Round of 32: {len(ROUND_OF_32_FIXTURES)}")
    print(f"🎯 Round of 16: {len(ROUND_OF_16_FIXTURES)}")
    print(f"⚔️  Quartas: {len(QUARTERFINAL_FIXTURES)}")
    print(f"🔥 Semifinais: {len(SEMIFINAL_FIXTURES)}")
    print(f"🥇 Final + 3º: {len(FINAL_FIXTURES)}")
    print(f"📊 TOTAL DE JOGOS: {total}")

if __name__ == "__main__":
    print_summary()
