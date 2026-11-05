"""Rule-based normalizers for KDP products: segment, niche, interior, audience, Japan fit, women lean,
season, IP risk. Rules are applied to title + subtitle + category text; first match wins."""
import re

SEGMENTS = [
    ("coloring", r"colou?ring|color by number|colour by number|color-by-number"),
    ("puzzle", r"word ?search|word find|sudoku|crossword|cryptogram|kakuro|logic puzzle|brain ?teaser|brain games|puzzle book|puzzles? for|mazes? for adults|word puzzles|riddles?|trivia|dot[- ]to[- ]dot for adults|mad libs|word scramble|search[- ]a[- ]word|puzzle(s)?\b|would you rather|joke book|jokes for kids|this or that"),
    ("activity-kids", r"activity book|activity pad|sticker book|stickers? (book|activity)|mazes?|dot[- ]to[- ]dot|connect the dots|seek and find|hidden pictures|look and find|scissor skills|cut and paste|search and find|i spy|games? for kids|activities for kids"),
    ("art-instruction", r"how to draw|learn to draw|drawing (book|guide|for)|draw (anime|manga|cute|kawaii)|sketchbook|sketch book|drawing pad|manga drawing|anime drawing|calligraphy|lettering|watercolor (book|for beginners)|art (book|techniques)|zentangle"),
    ("workbook-education", r"workbook|handwriting|tracing|trace letters|letter tracing|cursive|phonics|preschool|pre-k|kindergarten|first grade|1st grade|2nd grade|math (practice|workbook)|multiplication|sight words|alphabet|abc|learn(ing)? to (read|write)|homeschool|test prep|study guide|practice (book|test)|flash cards|summer brain|spectrum|brain quest"),
    ("planner", r"planner|agenda|organizer|calendar|academic year|weekly (and|&) monthly|monthly planner|budget (book|planner)|bill (tracker|organizer)|meal planner|wedding planner"),
    ("logbook", r"log ?book|password (book|keeper|log|organizer)|internet address|record book|ledger|address book|guest book|tracker|blood (pressure|sugar)|mileage|reading log|recipe (book|journal|keeper) to write|blank recipe|maintenance log|inventory log|sign[- ]in"),
    ("journal", r"journal|diary|prompts|gratitude|devotional journal|prayer journal|guided|shadow work|affirmations? (book|journal)|5 minute|five minute|memory book|baby book|one line a day|q&a a day|question a day"),
    ("notebook", r"notebook|composition|college ruled|wide ruled|lined paper|graph paper|dot grid|blank book|blank pages|notepad|manuscript paper|staff paper|sheet music"),
    ("cookbook", r"cookbook|recipes?\b|cooking|baking|air fryer|instant pot|slow cooker|meal prep|crock ?pot|keto|mediterranean diet|anti[- ]inflammatory|vegan|smoothie|kitchen"),
    ("picture-book", r"picture book|board book|bedtime stor|little golden book|lift[- ]the[- ]flap|touch and feel|baby (touch|first)|read[- ]aloud|ages 0|ages 1-|ages 2-|ages 3-|toddlers? book|children's book about|kids book about|first words|pete the cat|dr\. seuss|eric carle"),
    ("fiction-romance", r"romance|romantasy|romantic|love story|billionaire|bratva|mafia|enemies to lovers|friends to lovers|fake dating|second chance|why choose|reverse harem|rom-?com|dark romance|smut|spicy|omegaverse|alpha|shifter|fae (romance|king)|court of|duke|earl|regency|hockey (romance)?|small town|cowboy|vampire romance|erotica|monster romance"),
    ("fiction-other", r"\bnovel\b|thriller|mystery|suspense|detective|murder|fantasy|science fiction|sci-fi|dystopian|horror|litrpg|gamelit|cultivation|progression|epic|saga|trilogy|book \d|series|volume \d|vol\. ?\d|\(.* book \d+\)|\bmanga\b|graphic novel|light novel|stories|tales|fiction|cozy mystery|chronicles"),
    ("nonfiction-selfhelp", r"self[- ]help|habits?|mindset|anxiety|healing|trauma|confidence|happiness|motivation|productivity|success|stoic|psychology|relationships?|boundaries|overthinking|therapy|mental health|personal growth|attachment|narcissis|manifest|law of attraction|adhd|self[- ]care|self[- ]love|wellness|meditation|mindfulness|burnout|parenting|leadership|money|finance|investing|business|marketing"),
]
SEG_RE = [(s, re.compile(p, re.I)) for s, p in SEGMENTS]
CAT_HINTS = [("coloring", r"coloring books"), ("puzzle", r"puzzles|word search|sudoku|crossword|games & activities|puzzles & games"),
             ("activity-kids", r"activity books|children's activity|children's games"), ("art-instruction", r"drawing|art instruction|study & teaching"),
             ("workbook-education", r"education|early learning|reference|study aids|test prep"), ("planner", r"calendars|time management|planners"),
             ("journal", r"journal writing|journaling|diaries"), ("cookbook", r"cookbooks|cooking|food & wine"),
             ("picture-book", r"children's books|picture books|baby|toddler"),
             ("fiction-romance", r"romance|romantasy"), ("fiction-other", r"fiction|fantasy|mystery|thriller|science fiction|horror|comics|manga|graphic novels|teen"),
             ("nonfiction-selfhelp", r"self-help|personal|psychology|health|business|parenting|religion|spirituality|christian|bible|biograph|history|sports|politics")]
CAT_RE = [(s, re.compile(p, re.I)) for s, p in CAT_HINTS]


def segment(title, cat=""):
    t = title or ""
    # fiction romance titles often only carry the series in parentheses; check category first for fiction
    for s, rx in SEG_RE:
        if rx.search(t):
            if s in ("fiction-other", "nonfiction-selfhelp") and cat:
                for s2, rx2 in CAT_RE:
                    if rx2.search(cat) and s2 in ("fiction-romance",): return s2
            return s
    for s, rx in CAT_RE:
        if cat and rx.search(cat): return s
    return "other"


NICHE_RULES = {
    "coloring": [("coloring-anime-manga-kawaii", r"anime|manga|kawaii|chibi|japan"), ("coloring-bold-easy", r"bold (and|&) easy|bold|simple|large print|big (and|&) easy"),
                 ("coloring-cozy", r"cozy|cosy|hygge|comfy|cottage|cafe|little|girl'?s? (season|day)|spooky cozy"), ("coloring-halloween", r"halloween|spooky|horror|creepy|gothic|witch"),
                 ("coloring-christmas", r"christmas|xmas|winter|santa|holiday"), ("coloring-mandala-pattern", r"mandala|pattern|stained glass|geometric|zentangle"),
                 ("coloring-swear-humor", r"swear|sweary|curse|f\*ck|funny|humor|sassy|sarcas|snarky|unhinged|shit|adulting"),
                 ("coloring-color-by-number", r"by number"), ("coloring-religious", r"bible|christian|scripture|faith|prayer|jesus"),
                 ("coloring-animals", r"animal|cat|dog|horse|bird|owl|dinosaur|ocean|sea|butterfl"), ("coloring-floral-nature", r"flower|floral|garden|botanical|nature|landscape"),
                 ("coloring-kids", r"kids|toddler|children|boys|girls ages|ages \d|preschool"), ("coloring-fantasy", r"fantasy|fairy|dragon|unicorn|mermaid|princess|magic")],
    "puzzle": [("puzzle-word-search-large-print", r"large print.*word|word.*large print"), ("puzzle-word-search", r"word ?search|word find|search[- ]a[- ]word"),
               ("puzzle-sudoku", r"sudoku"), ("puzzle-crossword", r"crossword"), ("puzzle-brain-games-seniors", r"seniors|dementia|brain games|memory"),
               ("puzzle-kids", r"kids|children|ages \d"), ("puzzle-trivia-riddles", r"trivia|riddle|quiz|would you rather|joke"), ("puzzle-mixed", r".")],
    "activity-kids": [("activity-sticker", r"sticker"), ("activity-mazes", r"maze"), ("activity-dot-to-dot", r"dot"), ("activity-seek-find", r"seek|find|i spy|hidden"),
                      ("activity-scissor-skills", r"scissor|cut"), ("activity-general", r".")],
    "journal": [("journal-gratitude", r"gratitude|thankful"), ("journal-prayer-faith", r"prayer|bible|faith|christian|devotion|scripture|god|jesus"),
                ("journal-shadow-work-healing", r"shadow work|healing|trauma|therapy|anxiety|mental"), ("journal-guided-prompts", r"guided|prompts|question|q&a|5 minute|five minute|one line"),
                ("journal-reading-book", r"reading|book (lover|journal)|bookish"), ("journal-kids-teens", r"kids|girls|boys|teen|children"),
                ("journal-memory-baby", r"baby|memory|grandma|grandpa|mom|dad"), ("journal-dream-manifest", r"dream|manifest|affirmation|law of attraction"),
                ("journal-anime-kawaii", r"anime|manga|kawaii|japan"), ("journal-general", r".")],
    "planner": [("planner-dated-2026-2027", r"2026|2027|2028|dated|18[- ]month|academic"), ("planner-budget-finance", r"budget|bill|finance|money|savings"),
                ("planner-meal-fitness", r"meal|fitness|workout|weight"), ("planner-teacher-student", r"teacher|student|lesson|homeschool"),
                ("planner-undated-general", r".")],
    "logbook": [("logbook-password", r"password|internet"), ("logbook-health", r"blood|sugar|pressure|medication|health"), ("logbook-recipe-blank", r"recipe"),
                ("logbook-reading", r"reading"), ("logbook-guest-address", r"guest|address"), ("logbook-other", r".")],
    "notebook": [("notebook-composition", r"composition|college ruled|wide ruled"), ("notebook-sketch-graph", r"graph|dot grid|blank|sketch"), ("notebook-music", r"music|staff|manuscript"),
                 ("notebook-anime-kawaii", r"anime|manga|kawaii|japan"), ("notebook-general", r".")],
    "workbook-education": [("workbook-handwriting-tracing", r"handwriting|tracing|trace|cursive|letter"), ("workbook-preschool-k", r"preschool|pre-k|kindergarten|toddler"),
                           ("workbook-math", r"math|multiplication|addition|subtraction|fraction"), ("workbook-reading-phonics", r"phonics|sight word|reading|spelling"),
                           ("workbook-test-prep", r"test|exam|study guide|prep"), ("workbook-other", r".")],
    "art-instruction": [("art-how-to-draw-anime-manga", r"anime|manga|chibi|kawaii"), ("art-how-to-draw-kids", r"kids|children"), ("art-sketchbook", r"sketchbook|sketch book|drawing pad"),
                        ("art-how-to-draw", r"draw"), ("art-other", r".")],
    "fiction-romance": [("romance-romantasy-fae", r"romantasy|fae|fantasy|court of|dragon|witch|magic|realm|crown|throne|empyrean"),
                        ("romance-dark-mafia", r"dark|mafia|bratva|cartel|stalker|captive|villain|obsess"), ("romance-sports-hockey", r"hockey|football|sports|baseball|soccer"),
                        ("romance-monster-scifi", r"monster|alien|orc|minotaur|scifi|sci-fi|omega"), ("romance-billionaire", r"billionaire|ceo|boss"),
                        ("romance-small-town-cowboy", r"small town|cowboy|ranch|christmas"), ("romance-other", r".")],
    "fiction-other": [("fiction-manga-graphic", r"manga|graphic novel|vol\.|volume"), ("fiction-cozy-mystery", r"cozy|cosy|mystery"), ("fiction-thriller-suspense", r"thriller|suspense|murder|killer|detective|crime"),
                      ("fiction-fantasy-scifi-litrpg", r"fantasy|litrpg|gamelit|cultivation|dragon|sci-?fi|science fiction|space|dungeon"), ("fiction-horror", r"horror|haunt|ghost"),
                      ("fiction-kids-middle-grade", r"dog man|diary of a|captain underpants|wimpy|kids|middle grade|ages \d"), ("fiction-other", r".")],
    "nonfiction-selfhelp": [("selfhelp-psychology-mental-health", r"anxiety|trauma|therapy|psychology|mental|overthinking|narcissis|attachment|adhd|healing"),
                            ("selfhelp-habits-productivity", r"habit|productivity|success|discipline|focus|stoic|mindset"), ("selfhelp-money-business", r"money|financ|invest|business|marketing|wealth"),
                            ("selfhelp-relationships-parenting", r"relationship|parent|marriage|love languages|dating|boundaries"),
                            ("selfhelp-spiritual-manifest", r"manifest|spirit|law of attraction|god|bible|christian|faith"), ("selfhelp-other", r".")],
    "cookbook": [("cookbook-diet-health", r"keto|diet|anti[- ]inflammatory|diabet|mediterranean|vegan|gluten|low carb|heart"), ("cookbook-appliance", r"air fryer|instant pot|slow cooker|crock|ninja|bread machine"),
                 ("cookbook-baking", r"bak|bread|dessert"), ("cookbook-kids", r"kids"), ("cookbook-japanese-asian", r"japan|ramen|bento|sushi|korean|asian|anime"), ("cookbook-other", r".")],
    "other": [("other-magazine", r"magazine|\| (january|february|march|april|may|june|july|august|september|october|november|december)|\b(19|20)\d\d\b.*issue|real simple|good housekeeping|better homes|woman's day|country living|hgtv|birds & blooms"),
              ("other-crafts-hobby-howto", r"knit|crochet|sew|quilt|embroider|craft|woodwork|garden|home|house|decor|interior|survival|off-grid|diy|stencil|origami|paper"),
              ("other-gift-humor-novelty", r"mini|kit|figure|gift|humor|funny|celebrating a special year|time traveling"),
              ("other-reference-collectibles", r"guide|coin|encyclopedia|dictionary|atlas|handbook|manual|bible of"), ("other-general", r".")],
    "picture-book": [("picture-book-bedtime-emotions", r"bedtime|feel|emotion|love you|kind"), ("picture-book-baby-board", r"baby|board|touch|first words"), ("picture-book-holiday", r"christmas|halloween|easter|valentine"), ("picture-book-other", r".")],
}


def niche(seg, title):
    for n, p in NICHE_RULES.get(seg, []):
        if re.search(p, title or "", re.I): return n
    return seg + "-general"


def interior(seg, title):
    t = (title or "").lower()
    if seg in ("notebook", "logbook", "planner") or (seg == "journal" and not re.search(r"guided|prompt|question|devotion", t)):
        content = "low-content"
    elif seg in ("coloring", "puzzle", "activity-kids", "workbook-education") or (seg == "journal"):
        content = "medium-content"
    else:
        content = "high-content"
    if seg == "picture-book" or re.search(r"full colou?r|color interior|premium color", t): ink = "color"
    elif seg in ("cookbook",): ink = "color-or-bw(unknown)"
    else: ink = "bw"
    return content + "/" + ink


def audience(title, cat=""):
    t = ((title or "") + " " + (cat or "")).lower()
    kids = re.search(r"\bkids?\b|children|toddler|preschool|kindergarten|ages \d|boys|baby|board book|grade|middle grade", t)
    teen = re.search(r"\bteens?\b|young adult|\bya\b", t)
    senior = re.search(r"seniors?|elderly|dementia|large print|alzheimer", t)
    adult = re.search(r"adults?|grown|women|men\b|stress relief|relaxation|mindful", t)
    if senior: return "seniors"
    if kids and not adult: return "kids"
    if teen and not adult: return "teens"
    if kids and adult: return "all-ages"
    return "adults"


def japan_fit(t):
    t = (t or "").lower()
    if re.search(r"anime|manga|kawaii|chibi|japan|japanese|kyoto|tokyo|yokai|showa|city pop|j-pop|k-pop|kpop|sakura|bento|ramen|sushi|kimono|shojo|shoujo|otaku|ghibli|pixel art|video game|gamer|retro gam|8[- ]bit", t):
        return "yes"
    if re.search(r"\bcute\b|cozy|cosy|spooky cute|retro|y2k|witch|cat\b|cats\b|frog|capybara|axolotl|fantasy girl|magical girl|pastel", t):
        return "partial"
    return "no"


def women_lean(t, seg, aud):
    t = (t or "").lower()
    if aud == "kids": return "no"
    if seg == "fiction-romance": return "yes"
    if re.search(r"women|woman|girl|ladies|mom\b|mother|cozy|cosy|cute|kawaii|self[- ]care|floral|flower|fashion|hygge|witch|cafe|beauty|sassy|bride|wedding|gratitude|affirmation|romance|romantasy|bookish|cottage", t):
        return "yes"
    if seg in ("journal", "planner", "coloring"): return "partial"
    return "no"


SEASONS = [("christmas", r"christmas|xmas|santa|advent|winter|snowman|gingerbread|holiday"), ("halloween", r"halloween|spooky|pumpkin|haunted"),
           ("new-year-planning", r"20(2[6-9])|dated|academic year|new year|18[- ]month"), ("valentine", r"valentine"), ("easter-spring", r"easter|spring"),
           ("fall-thanksgiving", r"\bfall\b|autumn|thanksgiving"), ("summer-back-to-school", r"summer|back to school|vacation|beach"),
           ("mothers-fathers-day", r"mother'?s day|father'?s day|for mom|for dad|grandma|grandpa"), ("graduation", r"graduat")]


def season(t):
    for s, p in SEASONS:
        if re.search(p, t or "", re.I): return "seasonal", s
    return "evergreen", "none"


IP = r"disney|pixar|marvel|star wars|pokemon|pokémon|pikachu|bluey|peppa|paw patrol|sanrio|hello kitty|kuromi|my melody|cinnamoroll|naruto|one piece|demon slayer|jujutsu|dragon ball|my hero academia|attack on titan|sailor moon|studio ghibli|ghibli|totoro|spy x family|chainsaw man|minecraft|roblox|fortnite|sonic|mario|nintendo|zelda|kirby|barbie|harry potter|hogwarts|taylor swift|swiftie|squishmallow|stitch|frozen|encanto|moana|spider-?man|batman|sesame|cocomelon|wednesday addams|stranger things|lord of the rings|bts|blackpink|kpop demon hunters|labubu|genshin|hatsune|miku|one punch|bleach|tokyo ghoul|haikyuu|jojo"


def ip_risk(t, publisher=""):
    t = (t or "").lower()
    m = re.search(IP, t)
    if not m: return "low"
    pub = (publisher or "").lower()
    licensed = re.search(r"viz|kodansha|yen press|seven seas|scholastic|golden|disney|random house|penguin|harper|simon|little, brown|bloomsbury|dark horse|udon|egmont|dk|studio fun|phidal|abrams|chronicle|insight|viz media", pub)
    return ("licensed-publisher (" + m.group(0) + ")") if licensed else ("HIGH: trademark term '" + m.group(0) + "'")
