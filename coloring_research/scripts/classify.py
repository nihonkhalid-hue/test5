"""Rule-based normalizers: niche, style, audience, Japan/anime fit, women lean, season, format, IP risk."""
import re

# (niche label, regex) checked in order; first match wins.
NICHES = [
    ("mega-bundle-plr", r"\bplr\b|\bmrr\b|resell|resale rights|commercial use|ready to sell|\d{1,3},\d{3}\+|\d{4,}\+ (coloring |colouring )?(pages|designs)|\b\d{1,3}k\+? (coloring )?pages"),
    ("anime-manga", r"anime|manga|shoujo|shojo|otaku|waifu"),
    ("chibi-kawaii", r"chibi|kawaii"),
    ("japan-culture", r"japan|japanese|kyoto|tokyo|geisha|kimono|ukiyo|yokai|samurai|bento|sushi|ramen|sakura|showa|city pop"),
    ("retro-gaming-pixel", r"pixel|video game|gamer|gaming|arcade|8[- ]bit|retro game|kawaii game"),
    ("halloween-spooky", r"halloween|spooky|ghost|witch|pumpkin|haunted|creepy cute|skeleton"),
    ("christmas-winter", r"christmas|xmas|santa|advent|holiday|winter|snowman|gingerbread|noel"),
    ("fall-thanksgiving", r"\bfall\b|autumn|thanksgiving|harvest"),
    ("spring-easter", r"easter|spring|bunny"),
    ("valentine", r"valentine"),
    ("summer-beach", r"summer|beach|tropical|ocean|sea life|underwater"),
    ("horror-gothic-dark", r"horror|gothic|goth\b|dark fantasy|macabre|victorian|creepy|skull|vampire|tarot|occult"),
    ("bold-and-easy", r"bold (and|&) easy|bold ?& ?easy|bold lines?|big (and|&) bold|simple large|large print|easy coloring|seniors|dementia"),
    ("cozy-hygge", r"cozy|cosy|hygge|comfy|snug|self[- ]care|cafe|book nook|cottage(?!core)"),
    ("cottagecore-botanical", r"cottagecore|mushroom|botanical|floral|flower|garden|fairy garden|plant"),
    ("mandala-pattern", r"mandala|zentangle|pattern|geometric|doodle art|stained glass|mosaic"),
    ("fantasy-fairy-dragon", r"fantasy|fairy|fairies|dragon|unicorn|mermaid|magical|mythical|enchanted|princess|elf"),
    ("animals", r"\bcats?\b|kitten|kitty|dogs?\b|puppy|animal|frog|capybara|axolotl|owl|bear|panda|fox|bird|horse|wildlife|farm|dinosaur|dino"),
    ("food-sweets", r"food|sweets|dessert|candy|cake|cupcake|snack|boba|fruit"),
    ("girls-fashion-people", r"\bgirls?\b|women|woman|fashion|portrait|people|beauty|lady|ladies"),
    ("quotes-affirmations-faith", r"quote|affirmation|bible|scripture|christian|faith|prayer|swear|sweary|motivational"),
    ("color-by-number", r"color by number|colour by number|color-by-number|mystery mosaic|by number"),
    ("travel-landscape-city", r"travel|landscape|landmark|city|cities|architecture|house|houses|village"),
    ("kids-educational", r"\bkids?\b|toddler|preschool|kindergarten|worksheet|classroom|alphabet|abc|educational|early finisher|activity"),
    ("seasonal-generic", r"season|four seasons|year round"),
]
NICHE_RE = [(n, re.compile(p, re.I)) for n, p in NICHES]


def niche(title, query=""):
    t = title or ""
    for n, rx in NICHE_RE:
        if rx.search(t):
            return n
    for n, rx in NICHE_RE:
        if query and rx.search(query):
            return n
    return "general-coloring"


def style(t):
    t = (t or "").lower()
    if re.search(r"bold (and|&) easy|bold lines?|big (and|&) bold|large print|simple", t): return "bold-easy"
    if re.search(r"grayscale|greyscale|grey scale|gray scale", t): return "grayscale"
    if re.search(r"kawaii|cute|chibi|cozy|cosy|adorable|sweet", t): return "cute"
    if re.search(r"realistic|photo|lifelike", t): return "realistic"
    if re.search(r"mandala|detailed|intricate|zentangle|stained glass|pattern", t): return "detailed"
    return "line-art"


def audience(t):
    t = (t or "").lower()
    kids = re.search(r"\bkids?\b|children|toddler|preschool|kindergarten|classroom|ages \d|boys|homeschool|worksheet", t)
    adult = re.search(r"adult|grown|seniors?|stress relief|relaxation|relaxing|mindful|for women|mature", t)
    teen = re.search(r"teen", t)
    if kids and adult: return "all"
    if adult: return "adult"
    if teen: return "teen"
    if kids: return "kids"
    return "all"


def japan_fit(t):
    t = (t or "").lower()
    if re.search(r"anime|manga|kawaii|chibi|japan|japanese|kyoto|tokyo|yokai|showa|city pop|j-pop|kpop|k-pop|pixel|video game|gamer|retro gam|sakura|bento|ramen|sushi|kimono", t):
        return "yes"
    if re.search(r"cute|cozy|cosy|spooky cute|creepy cute|fantasy girl|princess|cat|frog|capybara|axolotl|retro|y2k|witch", t):
        return "partial"
    return "no"


def women_lean(t, aud):
    t = (t or "").lower()
    if aud == "kids": return "no"
    if re.search(r"cozy|cosy|cute|kawaii|girl|women|woman|self[- ]care|cottagecore|floral|flower|fashion|mermaid|fairy|princess|hygge|witch|cafe|book nook|beauty|anime girl|chibi", t):
        return "yes"
    if re.search(r"truck|car|dinosaur|monster truck|sports|military|robot", t): return "no"
    return "unclear"


SEASONS = [("halloween", r"halloween|spooky|witch|pumpkin|ghost|haunted"), ("christmas", r"christmas|xmas|santa|advent|holiday|gingerbread"),
           ("winter", r"winter|snowman|snow"), ("fall-thanksgiving", r"\bfall\b|autumn|thanksgiving|harvest"),
           ("valentine", r"valentine"), ("easter-spring", r"easter|spring"), ("summer", r"summer|beach"),
           ("back-to-school", r"back to school")]


def season(t):
    for s, p in SEASONS:
        if re.search(p, t or "", re.I):
            return "seasonal", s
    return "evergreen", ""


def fmt(t, extra=""):
    s = f"{t} {extra}"
    found = []
    for name, p in [("Procreate", r"procreate"), ("GoodNotes", r"goodnotes|good notes"), ("PDF", r"\bpdf\b|printable|print at home|printables?"),
                    ("PNG", r"\bpng\b"), ("JPG", r"\bjpe?g\b"), ("SVG", r"\bsvg\b"), ("paperback", r"paperback|softcover|hardcover|spiral")]:
        if re.search(p, s, re.I):
            found.append(name)
    return "|".join(found) or "NOT SHOWN"


def page_count(t):
    m = re.search(r"(\d{1,3}(?:,\d{3})*|\d+)\s*\+?\s*(?:unique\s+|cute\s+|printable\s+|bold\s+|simple\s+|kawaii\s+|anime\s+|grayscale\s+|hand[- ]drawn\s+|adult\s+|mandala\s+|christmas\s+|halloween\s+)*(?:coloring\s+|colouring\s+|color\s+)?(?:pages?|sheets?|designs?|illustrations?|images?|pgs?)\b", t or "", re.I)
    if m:
        v = int(m.group(1).replace(",", ""))
        return v if v < 10_000_000 else ""
    return ""


def is_bundle(t, pc):
    return bool(re.search(r"bundle|mega ?pack|collection of|set of \d|\bpack\b", t or "", re.I)) or (isinstance(pc, int) and pc >= 50)


IP_TERMS = r"toy story|pixar|coraline|tim burton|nightmare before|lilo|encanto|moana|bluey|peppa|paw patrol|hello kitty|pokemon|pokémon|pikachu|sanrio|hello kitty|kuromi|my melody|cinnamoroll|pompompurin|ghibli|totoro|naruto|one piece|demon slayer|jujutsu|chainsaw man|dragon ball|sailor moon|spy x family|my hero academia|attack on titan|disney|mickey|stitch|frozen|bluey|barbie|mario|sonic|zelda|kirby|minecraft|roblox|fortnite|genshin|harry potter|hogwarts|taylor swift|eras tour|marvel|star wars|squishmallow|stranger things|wednesday addams|labubu|kpop demon|bts|blackpink"


def ip_risk(t):
    m = re.search(IP_TERMS, t or "", re.I)
    if m:
        return "fan-art/trademark: " + m.group(0).lower()
    if japan_fit(t) == "yes":
        return "original anime-style (low)"
    return ""
