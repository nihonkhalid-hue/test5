# Coloring pages & books: niche, velocity and seasonality report

_Data collected 2026-10-25 (UTC). Read COVERAGE.md first: Etsy, Amazon, eBay, Payhip, Creative Fabrica and Ko-fi blocked direct access, so several signals come from third-party trackers and are labelled as such._

**Master table:** 2,214 product rows across 11 sources (gumroad 735, etsy 699, teacherspayteachers 511, amazon 139, itch.io 104, payhip 19, creativemarket 3, monsterone 1, templatemonster 1, baldhamster 1, tiktokshop 1).

## How to read the scores

Opportunity score (0–100), per niche:

```
Demand = 0.35·P(Etsy searches ÷ Etsy competing listings)   [RankHero keyword pages]
       + 0.25·P(median Etsy favorites per month, est.)    [RankHero favorites ÷ listing age estimated from listing ID]
       + 0.15·P(median reviews on Gumroad/TpT/Amazon rows)
       + 0.15·P(12-month search trend %)                   [RankHero Etsy trend + Google Trends YoY]
       + 0.10·P(number of marketplaces where the niche appears)
Opportunity = 100 · Demand · (1 − 0.5 · top3_shop_share)    [share of the niche's Etsy top listings held by its 3 biggest shops]
P(x) = percentile rank of x among niches; a missing input scores 0.5 (neutral). evidence_n = how many of the 4 data inputs were present.
```

Niches need at least 15 collected rows to be ranked. `general-coloring` (no theme in the title) and Amazon supplies are excluded.

## Top 20 niches by opportunity

| # | Niche | Score | Evidence | Rows | Mkts | Etsy searches/listing | Trend % | Median $ | Etsy fav/mo (est) | Top-3 shop share | Japan-fit share |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | fall-thanksgiving | 61.4 | 3/4 | 74 | 3 | 3.82 | – | 3.81 | 1.86 | 0.17 | 0 |
| 2 | christmas-winter | 56.5 | 3/4 | 153 | 5 | 3.93 | – | 4 | 0.92 | 0.17 | 0.01 |
| 3 | fantasy-fairy-dragon | 55.7 | 4/4 | 109 | 4 | 9.09 | -18 | 3.99 | 1.45 | 0.12 | 0 |
| 4 | kids-educational | 55.0 | 2/4 | 111 | 5 | – | – | 5 | 2.25 | 0.21 | 0 |
| 5 | spring-easter | 54.1 | 3/4 | 49 | 5 | 3.46 | – | 3.5 | 1.62 | 0.24 | 0 |
| 6 | animals | 52.7 | 4/4 | 94 | 6 | 6.87 | -18 | 3.99 | 0.82 | 0.13 | 0 |
| 7 | summer-beach | 49.6 | 3/4 | 38 | 4 | 2.79 | – | 3.95 | 1.42 | 0.16 | 0 |
| 8 | cozy-hygge | 49.4 | 4/4 | 74 | 3 | 0.58 | 44.6 | 6.33 | 5.48 | 0.14 | 0 |
| 9 | color-by-number | 48.1 | 3/4 | 34 | 3 | 3.14 | – | 4.78 | 12.26 | 0.67 | 0 |
| 10 | anime-manga | 43.6 | 4/4 | 208 | 6 | 1.43 | -19 | 5 | 1.84 | 0.23 | 0.86 |
| 11 | mega-bundle-plr | 42.9 | 2/4 | 48 | 2 | – | – | 5.39 | 4.06 | 0.23 | 0.04 |
| 12 | halloween-spooky | 42.9 | 3/4 | 214 | 5 | 0.36 | – | 4.99 | 1.86 | 0.16 | 0 |
| 13 | valentine | 41.1 | 3/4 | 26 | 3 | 2.86 | – | 4.97 | 1.04 | 0.25 | 0 |
| 14 | bold-and-easy | 38.3 | 4/4 | 73 | 6 | 0.01 | 0.4 | 4.99 | 4.76 | 0.32 | 0 |
| 15 | chibi-kawaii | 35.2 | 4/4 | 178 | 4 | 0.32 | 12.7 | 5.13 | 1.53 | 0.16 | 0.94 |
| 16 | girls-fashion-people | 31.6 | 2/4 | 25 | 3 | – | – | 8.99 | 1.67 | 0.75 | 0 |
| 17 | quotes-affirmations-faith | 27.4 | 3/4 | 53 | 3 | 0.25 | – | 4.99 | 1.93 | 0.32 | 0 |
| 18 | mandala-pattern | 26.1 | 4/4 | 111 | 3 | 0.57 | -18 | 4.89 | 0.37 | 0.15 | 0 |
| 19 | japan-culture | 25.8 | 2/4 | 70 | 3 | – | – | 3.97 | 1.75 | 0.75 | 0.87 |
| 20 | cottagecore-botanical | 23.5 | 4/4 | 89 | 6 | 0.04 | -25.5 | 3.92 | 1.25 | 0.16 | 0 |

Too few rows to rank (shown for reference): horror-gothic-dark (14 rows, score 32.2), food-sweets (12 rows, score 29.1), travel-landscape-city (11 rows, score 28.2), retro-gaming-pixel (7 rows, score 26.2), seasonal-generic (3 rows, score 24.3).


## Top 50 velocity listings (Etsy, favorites per month)

Velocity = favorites ÷ listing age in months. Etsy hid review counts, so favorites are the only per-listing engagement number available (from RankHero). Listing age is **estimated** from the Etsy listing ID, interpolated between 35 FindNiche anchors whose release date is known. Listings older than the earliest anchor are excluded because their age is only a lower bound.

| # | Title | Shop | Price | Favorites | Listed (est) | Velocity | Metric | Niche | IP risk | Link |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8,000+ Bold and Easy Coloring Pages Bundle / Kawaii Cozy Co… | VelnoraPrintsCo | 4.29 USD | 660 | 2026-05-15 | 123 | favorites_per_month | mega-bundle-plr | original anime-style (low) | [link](https://www.etsy.com/listing/4505144878) |
| 2 | Adult Colouring Book "Wild Wood" by Amanda Clark - Intricat… | earthangelsarts | 27.99 GBP | 4,051 | 2023-10-18 | 112 | favorites_per_month | fantasy-fairy-dragon | – | [link](https://www.etsy.com/listing/1591198337) |
| 3 | Toy Story Party Favors, Party Favor Mini Coloring Sheets & … | SmithCoEvents | 1.75 USD | 2,879 | 2024-06-18 | 102 | favorites_per_month | general-coloring | fan-art/trademark: toy story | [link](https://www.etsy.com/listing/1745377040) |
| 4 | Personalized Coloring Book for Kids / Custom Name Coloring … | MunchkinLaneShop | 14.38 USD | 16,436 | 2021-05-13 | 96.44 | reviews_per_month | fantasy-fairy-dragon | – | [link](https://www.etsy.com/listing/1004634776) |
| 5 | Spooky Cutie Coloring Book PDF, Cozy Gothic Coloring Pages | AltWorlds | 2.49 EUR | 780 | 2026-01-04 | 80.65 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4434937274) |
| 6 | 110 Disney Mystery Coloring Books Bundle / Printable Color … | SharpPixelCo | 260 MAD | 376 | 2026-05-21 | 72.81 | favorites_per_month | color-by-number | fan-art/trademark: disney | [link](https://www.etsy.com/listing/4509068467) |
| 7 | Coraline Color by Number PDF Coloring Book, Dark Horror Art… | HappyColorFR | 3 EUR | 169 | 2026-08-15 | 72.36 | favorites_per_month | horror-gothic-dark | fan-art/trademark: coraline | [link](https://www.etsy.com/listing/4555212834) |
| 8 | Fall Coloring Pages, Fall Coloring Book, Fall Coloring Shee… | ProudPracticalPrints | 2.8 USD | 917 | 2025-08-15 | 63.94 | favorites_per_month | fall-thanksgiving | – | [link](https://www.etsy.com/listing/4352680915) |
| 9 | Kawaii Coloring Pages / 50 Pages / Cute Coloring Pages / Fo… | PrintableDandelion | 4 USD | 2,186 | 2023-11-14 | 61.76 | favorites_per_month | chibi-kawaii | original anime-style (low) | [link](https://www.etsy.com/listing/1610553653) |
| 10 | Tiny Cats: Cute Coloring Book for Relaxing by Coco Wyo | CocoWyoColoring | 3.99 USD | 2,419 | 2023-06-12 | 59.74 | favorites_per_month | animals | – | [link](https://www.etsy.com/listing/1502329015) |
| 11 | Favorite Anime Mystery Coloring Book PDF – 52 Color by Numb… | HappyColorFR | 5 EUR | 100 | 2026-09-04 | 59.61 | favorites_per_month | anime-manga | original anime-style (low) | [link](https://www.etsy.com/listing/4565979421) |
| 12 | Honey Days: Cute and Cozy Coloring Book for Adults and Kids… | KomfiKatColoring | 9.99 USD | 123 | 2026-08-22 | 58.43 | favorites_per_month | bold-and-easy | – | [link](https://www.etsy.com/listing/4559165353) |
| 13 | Darkline Color by Number PDF – 40 Gothic Horror Coloring Pa… | HappyColorFR | 3.7 EUR | 126 | 2026-08-18 | 56.33 | favorites_per_month | horror-gothic-dark | – | [link](https://www.etsy.com/listing/4556798075) |
| 14 | Cozy Coloring Book Bundle, 2000+ Pages (PDF Download) | TRENDYCOLORING | 66 MAD | 496 | 2026-01-30 | 56.26 | favorites_per_month | mega-bundle-plr | – | [link](https://www.etsy.com/listing/4449681945) |
| 15 | Hobby Girl: Cute and Cozy Coloring Book for Adults and Kids… | KomfiKatColoring | 9.99 USD | 388 | 2026-03-16 | 52.89 | favorites_per_month | bold-and-easy | – | [link](https://www.etsy.com/listing/4472798201) |
| 16 | Disney Princesses Kawaii Coloring Book / 30+ Magical Cozy S… | CozyCornerStudiox | 3.99 EUR | 437 | 2026-01-26 | 48.84 | favorites_per_month | chibi-kawaii | fan-art/trademark: disney | [link](https://www.etsy.com/listing/4447467954) |
| 17 | 1000+ Adult Mandala Coloring Book coloring book Printable C… | TemplateMountain | 1.99 USD | 309 | 2026-03-29 | 44.73 | favorites_per_month | mandala-pattern | – | [link](https://www.etsy.com/listing/4479766443) |
| 18 | Glassy World: Cute Coloring Book for Relaxing by Coco Wyo | CocoWyoColoring | 3.99 USD | 1,694 | 2023-05-24 | 41.2 | favorites_per_month | general-coloring | – | [link](https://www.etsy.com/listing/1488962802) |
| 19 | Fantasy coloring book for adults digital magical coloring f… | QuirkyFindsPH | 393 PHP | 319 | 2026-03-03 | 41.09 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4465940254) |
| 20 | Spooky Cartoon Color by Number Book, 40 Halloween Character… | InkInfinityCrafts | 10 NZD | 59 | 2026-09-05 | 35.87 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4566563270) |
| 21 | Cozy Coloring Book Bundle / 2000+ Printable Coloring Pages … | VelvetAuraCoDesigns | 2.6 USD | 167 | 2026-06-03 | 35.26 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4515825146) |
| 22 | Cute Fairy Coloring Book Pages Cozy Fantasy Coloring Book E… | HappyStrokesbyArya | 180 PHP | 181 | 2026-05-16 | 33.97 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4506099855) |
| 23 | Folk Floral Coloring Pages Bundle / Boho Folk Art Designs +… | ThePaperNookShop | 11.84 USD | 198 | 2026-04-30 | 33.82 | favorites_per_month | cottagecore-botanical | – | [link](https://www.etsy.com/listing/4496820540) |
| 24 | Monster High Mystery Coloring Book PDF – 56 Color by Number… | HappyColorFR | 4.5 EUR | 66 | 2026-08-25 | 32.89 | favorites_per_month | color-by-number | – | [link](https://www.etsy.com/listing/4560580206) |
| 25 | 24 Food Color by Number Pages for Adults / Procreate, Print… | OuramdColoring | 12.48 USD | 82 | 2026-08-07 | 31.55 | favorites_per_month | food-sweets | – | [link](https://www.etsy.com/listing/4551143057) |
| 26 | Mix Anime Cartoons: Mystery Color By Number Printable Color… | 1DigitalUniverse | 5.8 USD | 36 | 2026-09-20 | 31.27 | favorites_per_month | anime-manga | original anime-style (low) | [link](https://www.etsy.com/listing/4574620624) |
| 27 | Kids Bible Verse Coloring Pages, Kid's Bible Coloring Pages… | ProudPracticalPrints | 2.3 USD | 482 | 2025-06-29 | 30.34 | favorites_per_month | quotes-affirmations-faith | – | [link](https://www.etsy.com/listing/4327744032) |
| 28 | Cozy Cottage Coloring Book / Cute Fantasy Coloring Book for… | BusyBreePrints | 15 USD | 438 | 2025-07-24 | 29.07 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4340854974) |
| 29 | Cozy corners coloring pages, 38 charming home scenes to hel… | MagicalTimeShop | 10.52 USD | 211 | 2026-03-15 | 28.64 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4472240872) |
| 30 | Cozy Coloring Bundle – 160+ Pages of Cute, Comforting Color… | CremeoTinta | 12.44 USD | 57 | 2026-08-25 | 28.41 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4560621426) |
| 31 | Deep Little Things Spooky Cute Coloring Book – 40-Page Prin… | JoyfulColorCo | 3.59 USD | 156 | 2026-05-11 | 28.4 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4503240763) |
| 32 | Patchwork Magic Spooky Coloring Book, 15 Bold and Easy Colo… | YourColorBookArt | 3 USD | 56 | 2026-08-24 | 27.46 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4560342423) |
| 33 | 10,000,000+ Coloring Pages Bundle Plr Mrr / 100,000+ Colori… | ZenovaVibe | 1.49 USD | 1,019 | 2026-05-24 | 27.44 | reviews_per_month | mega-bundle-plr | – | [link](https://www.etsy.com/listing/4510687031) |
| 34 | 200 Kawaii Coloring Pages: Bold & Easy Designs (8.5x11") (P… | Kalawastu | 95,000 IDR | 679 | 2024-10-01 | 27.38 | favorites_per_month | chibi-kawaii | original anime-style (low) | [link](https://www.etsy.com/listing/1801677675) |
| 35 | Care Bears 2 Mystery Color By Number Book , Bisounours 2 / … | DreamsparkDigitals | 4 EUR | 91 | 2026-07-14 | 26.86 | favorites_per_month | animals | – | [link](https://www.etsy.com/listing/4537769843) |
| 36 | Cozy Colo Disney - Instants Secrets, Coloring Book Printabl… | ItsGigil | 4.5 USD | 66 | 2026-08-09 | 26.06 | favorites_per_month | cozy-hygge | fan-art/trademark: disney | [link](https://www.etsy.com/listing/4551796471) |
| 37 | LIVRE COLORIAGE DARKLINE - pdf hq / dark horror color by nu… | pixelandcolors | 7 EUR | 104 | 2026-06-25 | 25.91 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4527506587) |
| 38 | 50 page Kids Color By Number Printable Book – Animals, Trea… | FlickerandStck | 4 USD | 148 | 2026-05-02 | 25.56 | favorites_per_month | animals | – | [link](https://www.etsy.com/listing/4497875699) |
| 39 | Honeybutter & Co. Coloring Book Vol. 1 - Premium Cardstock … | HoneybutterColoring | 22 USD | 202 | 2026-02-22 | 25.06 | favorites_per_month | kids-educational | – | [link](https://www.etsy.com/listing/4461613692) |
| 40 | Cozy Coloring Book: Burnout Girl Moments for Stress Relief | MomoNookColoring | 2.97 EUR | 89 | 2026-06-30 | 23.12 | favorites_per_month | cozy-hygge | – | [link](https://www.etsy.com/listing/4530399906) |
| 41 | A Heartwarming Coloring Book — A Cute Fairytale World - Jap… | pomadour24 | 14 USD | 155 | 2026-04-02 | 22.87 | favorites_per_month | japan-culture | original anime-style (low) | [link](https://www.etsy.com/listing/4481876772) |
| 42 | Dark Romance Coloring Pages, Smut Coloring Pages, Romantasy… | AuburnRowDesign | 2.5 USD | 59 | 2026-08-05 | 22.14 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4549795633) |
| 43 | Kawaii Coloring Pages • 3-Page Printable Set • Cute Food, B… | Buttonmags | 2.8 GBP | 236 | 2025-11-22 | 21.29 | favorites_per_month | chibi-kawaii | original anime-style (low) | [link](https://www.etsy.com/listing/4409823629) |
| 44 | Whimsigoth Witches Bold and Easy Coloring Book / Printable … | CozyArtLab | 250 TRY | 62 | 2026-07-28 | 21.18 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4545260576) |
| 45 | Fantasy Creatures Coloring Book Bundle / 26 Printable Color… | GalanaStudio | 2.19 USD | 95 | 2026-06-09 | 20.93 | favorites_per_month | fantasy-fairy-dragon | – | [link](https://www.etsy.com/listing/4518792250) |
| 46 | 100 Smutty Coloring Sheets, Spicy Book Club, Adult Coloring… | BookishRealmsLLC | 5 USD | 579 | 2024-07-06 | 20.93 | favorites_per_month | general-coloring | – | [link](https://www.etsy.com/listing/1755182055) |
| 47 | Bold and Easy Folk Art Coloring Pages Printable, Cottagecor… | HappyCreateStudio | 3.89 USD | 166 | 2026-02-20 | 20.43 | favorites_per_month | bold-and-easy | – | [link](https://www.etsy.com/listing/4460462245) |
| 48 | The Apothecary Diaries Anime Coloring Book / 45 Pages + 10 … | momopages | 3.2 EUR | 53 | 2026-08-07 | 20.39 | favorites_per_month | anime-manga | original anime-style (low) | [link](https://www.etsy.com/listing/4550910050) |
| 49 | Barbie Color by Number Coloring Book PDF – 10 Mystery Color… | MysteriaColor | 5 USD | 22 | 2026-09-21 | 19.67 | favorites_per_month | color-by-number | fan-art/trademark: barbie | [link](https://www.etsy.com/listing/4575130070) |
| 50 | Spooky house coloring book, 37 cozy halloween coloring page… | MagicalTimeShop | 6.3 USD | 54 | 2026-08-01 | 19.31 | favorites_per_month | halloween-spooky | – | [link](https://www.etsy.com/listing/4547452449) |

### Other velocity signals

**Amazon** (ASINsight third-party monthly unit estimates; Amazon itself returned a CAPTCHA). `sales_per_day_est = monthly_sales_est ÷ 30.4`.

| Title | Monthly sales (est) | Price | Reviews | Link |
|---|---|---|---|---|
| Flycatcher Smart Sketcher 2.0 Projector, Drawing and Tracing Projecto… | 40,000 | 108 | 2,100 | [link](https://www.amazon.com/dp/B08TCD1RTK) |
| Crayola Bluey Color Wonder Coloring Set, 18 Bluey Coloring Pages, Tod… | 30,000 | 5.54 | 50,800 | [link](https://www.amazon.com/dp/B09HR1Q6DP) |
| Soucolor Sketch Book 9" x 12", 100 Sheets Kids Art Sketchbook Drawing… | 20,000 | 8.99 | 10,000 | [link](https://www.amazon.com/dp/B0B19J9FZM) |
| 9" x 12" Sketch Book, 2-Pack 50 Sheets Spiral Bound Art Sketchbook No… | 10,000 | 9.99 | 2,300 | [link](https://www.amazon.com/dp/B0DF77698M) |
| 9" x 12" Sketch Book, 2-Pack 50 Sheets Spiral Bound Art Sketchbook, A… | 10,000 | 11.99 | 1,500 | [link](https://www.amazon.com/dp/B0DF77698M) |
| Melissa & Doug Water Wow! Mess Free Coloring Book, Reusable Water-Rev… | 10,000 | 5.99 | 4,200 | [link](https://www.amazon.com/dp/B01LYCJ3ND) |
| Soucolor 9" x 12" Sketch Book, 100 Sheets Top Spiral Bound Sketchbook… | 10,000 | 9.99 | 9,500 | [link](https://www.amazon.com/dp/B0B19J9FZM) |
| 9" x 12" Sketch Book, 2-Pack 50 Sheets Spiral Bound Art Sketchbook, A… | 10,000 | 11.99 | 2,000 | [link](https://www.amazon.com/dp/B0DF77698M) |
| ZMLM Scratch Paper Art-Crafts Gift: 2 Pack Rainbow Notebooks Supplies… | 9,000 | 9.99 | 10,500 | [link](https://www.amazon.com/dp/B08HMHWXWG) |
| 9" x 12" Sketch Book, 2-Pack 50 Sheets Spiral Bound Art Sketchbook, A… | 9,000 | 9.99 | 2,200 | [link](https://www.amazon.com/dp/B0DF77698M) |
| Cupkin Animal Habitats Coloring & Sticker Activity Book / 500+ Sticke… | 8,000 | 16.98 | 6,700 | [link](https://www.amazon.com/dp/B098PMWSVS) |
| Crayola Color Wonder Mess Free Coloring Activity Set (30+ Pcs), Trave… | 8,000 | 14.09 | 18,200 | [link](https://www.amazon.com/dp/B01MA68J0O) |
| Animals Habitat 500+ Kids Sticker Book by Cupkin Toddler Airplane Tra… | 8,000 | 16.98 | 6,600 | [link](https://www.amazon.com/dp/B098PMWSVS) |
| CUPKIN Animals Habitat 500+ Kids Sticker Book Toddler Airplane Travel… | 8,000 | 16.98 | 6,200 | [link](https://www.amazon.com/dp/B098PMWSVS) |
| 9" x 12" Sketch Book, 2-Pack 50 Sheets Spiral Bound Art Sketchbook, A… | 8,000 | 9.99 | 2,000 | [link](https://www.amazon.com/dp/B0DF77698M) |

**Gumroad: most-rated coloring products.** Gumroad shows no listing dates, so this is total ratings, not velocity.

| Title | Creator | Price | Ratings | Sales shown | Link |
|---|---|---|---|---|---|
| FREE anime brushset! | ~Attki~ | 0 | 2,231 | NOT FETCHED | [link](https://attki.gumroad.com/l/animebasic) |
| Crazy Space - Coloring Pages by Gal Shir | Gal Shir | 4.99 | 1,164 | NOT SHOWN | [link](https://galshir.gumroad.com/l/crazy-space) |
| The Complete Guide to Anime Studies  | oridays | 0 | 1,013 | NOT FETCHED | [link](https://oridays.gumroad.com/l/animestudy) |
| Free Jelly Style Brushes for Procreate | Di | 0 | 649 | NOT FETCHED | [link](https://dibrushes.gumroad.com/l/free_jelly) |
| The Quintessential Thick Pencil Brush for Procreate | Nicole  | 0 | 641 | NOT FETCHED | [link](https://fossilforager.gumroad.com/l/wiklCa) |
| Matt's Sketching Procreate brush set  version 1.1 | Mateusz Urbanowicz | 0 | 639 | NOT FETCHED | [link](https://mateusz-urbanowicz.gumroad.com/l/srJcA) |
| 3D Paper Christmas Trees | Hattifant | 0 | 526 | NOT FETCHED | [link](https://hattifant.gumroad.com/l/xCmgr) |
| Azzylum's 2021 Brush Set for Procreate  | Azzylum | 0 | 517 | NOT FETCHED | [link](https://azzylum.gumroad.com/l/sYEUh) |
| Kaleidocycles Series - PATTERNS I | Hattifant | 4 | 377 | NOT FETCHED | [link](https://hattifant.gumroad.com/l/LJEfq) |
| Sailor Moon Coloring Book Pages (x6) | Jen Bartel | 0 | 362 | NOT SHOWN | [link](https://jenbartel.gumroad.com/l/xdUpE) |
| +31 Free Low Content Book and Coloring Book Interior Templa… | ShinyWords | 0 | 362 | NOT SHOWN | [link](https://shinywords.gumroad.com/l/free-bundle) |
| Peggy Chung Art's Procreate Brushes v01 | Gadget-Bot Shop | 0 | 360 | NOT FETCHED | [link](https://gadgetbot.gumroad.com/l/kBQSd) |
| Procreate MEGAPACK XXL: 2000+ Premium Brushes incl. FREE Li… | GeorgBrush.club / 2000+ … | 15 | 348 | NOT FETCHED | [link](https://georgvw.gumroad.com/l/procreate) |
| Spring KALEIDOCYCLE - a Paper Toy | Hattifant | 0 | 341 | NOT FETCHED | [link](https://hattifant.gumroad.com/l/MBzON) |
| FREE Anime Hair brushpack! | ~Attki~ | 0 | 341 | NOT FETCHED | [link](https://attki.gumroad.com/l/VgUuZ) |
| FREE Procreate Color Swatches: 37+ Palettes for Painting an… | GeorgBrush.club / 2000+ … | 0 | 319 | NOT SHOWN | [link](https://georgvw.gumroad.com/l/procreate_colors) |
| Eyes Painting Tutorial | oridays | 0 | 287 | NOT FETCHED | [link](https://oridays.gumroad.com/l/eyestutorial) |
| Free Procreate Outline Brushes for easy Coloring & Handlett… | liliyth | 0 | 276 | NOT SHOWN | [link](https://liliyth.gumroad.com/l/outlinebrushes) |
| Hungry Caterpillar Cut and Paste Book Craft Kids Activity | alittlepinchofperf | 3 | 257 | NOT FETCHED | [link](https://alpp2.gumroad.com/l/tnqTL) |
| Coloring Pages! | Geneva B makes things | 0 | 213 | NOT SHOWN | [link](https://gdbee.gumroad.com/l/pxWab) |

**Gumroad products that publicly show a sales count:**

| Title | Creator | Price | Sales shown | Link |
|---|---|---|---|---|
| Joey's Color Palettes | Joey Carlino | 0 | 18,503 | [link](https://joeycarlino.gumroad.com/l/Ujsavq) |
| Christmas Activity PLR Bundle / Colouring Party Games / Wor… | Epro Essentials | 0 | 2,196 | [link](https://eproessentials.gumroad.com/l/ChristmasActivityPLRBundle) |
| F*ck Off, I'm Coloring (free pages) | James Alexander | 0 | 1,548 | [link](https://jamesalexander.gumroad.com/l/f-off-sample) |
| Very Lucky Coloring Zine | veryluckyclover | 0 | 1,344 | [link](https://veryluckyclover.gumroad.com/l/coloringzine1) |
| The Road Rage Coloring Book (free pages) | James Alexander | 0 | 1,342 | [link](https://jamesalexander.gumroad.com/l/road-rage-coloring-book-sample) |
| World Regional Maps Printable PDF Coloring Book: Blank Outl… | J Bruce Jones | 5 | 973 | [link](https://bjdesign.gumroad.com/l/WorldRegionalMaps) |
| HIPAINT 🌈 Kopix Starter Set - 10+ Digital Color Markers | Mysha Kawaii | 0 | 917 | [link](https://mysharts.gumroad.com/l/amdidp) |
| Procreate Brushes VOL.6 / Watercolor | Olguioo | 16 | 778 | [link](https://olguioo.gumroad.com/l/pidwdu) |
| 30 Pop Art Earth Day Coloring Pages (4 FREE SAMPLES) | Creativetacos | 0 | 605 | [link](https://freestylecreatives.gumroad.com/l/popartearthdaycoloring) |
| COLORING MARKER Brush Set - Get Realistic Coloring Marker T… | Dotstruction Studio | 0 | 477 | [link](https://dotstruction.gumroad.com/l/ColoringMarkerBrushSet) |
| Canada and the Canadian Provinces and Territories Printable… | J Bruce Jones | 5 | 244 | [link](https://bjdesign.gumroad.com/l/NZsQs) |
| 1000+ Coloring Pages Mega Bundle – 13 High-Demand Categorie… | Eagle Putts | 3.95 | 189 | [link](https://eagleputts.gumroad.com/l/1000ColoringPagesMegaBundleHighDemandCategoriesPrintableDigital) |
| Mega Bundle: 12,600+ Printable Coloring Pages for Kids & Ad… | Character Art | 0 | 138 | [link](https://eschaibi.gumroad.com/l/coloring) |
| Color Me "Winter Wonderland"  | nashi | 0 | 125 | [link](https://nashi.gumroad.com/l/hQlat) |
| Medusa Spooktacular Chibi Coloring Page Freebie | YamPuff | 0 | 122 | [link](https://yampuff.gumroad.com/l/medusa) |

**Teachers Pay Teachers: most-reviewed coloring products** (kids and classroom demand):

| Title | Price | Rating | Reviews | Link |
|---|---|---|---|---|
| Sight Word Practice Mystery Coloring Pages : Back to School & Fall Ar… | 21 | 4.82 | 10,925 | [link](https://www.teacherspayteachers.com/Product/Sight-Word-Practice-Mystery-Coloring-Pages-Back-to-School-Fall-Art-Activities-592311) |
| Kindergarten December Fun Christmas Craft Morning Work Coloring Pages… | 8.5 | 4.89 | 10,167 | [link](https://www.teacherspayteachers.com/Product/Kindergarten-December-Fun-Christmas-Craft-Morning-Work-Coloring-Pages-Sight-Word-992594) |
| Kindergarten Summer Packet End of Year Review Coloring Page Fun Activ… | 10 | 4.9 | 8,908 | [link](https://www.teacherspayteachers.com/Product/Kindergarten-Summer-Packet-End-of-Year-Review-Coloring-Page-Fun-Activities-Craft-699193) |
| Addition & Subtraction Coloring Pages - Back to School, Fall Math Art… | 21 | 4.83 | 8,684 | [link](https://www.teacherspayteachers.com/Product/Addition-Subtraction-Coloring-Pages-Back-to-School-Fall-Math-Art-Activity-450593) |
| February Kindergarten Valentines Day Craft Coloring Pages Sight Words… | 8.5 | 4.9 | 7,664 | [link](https://www.teacherspayteachers.com/Product/February-Kindergarten-Valentines-Day-Craft-Coloring-Pages-Sight-Words-CVC-Search-1044631) |
| Fractions NO PREP Packet Math Coloring Sheets Pages Color by Number C… | 6 | 4.87 | 5,975 | [link](https://www.teacherspayteachers.com/Product/Fractions-NO-PREP-Packet-Math-Coloring-Sheets-Pages-Color-by-Number-Code-Games-1309186) |
| Kindergarten October Halloween Fun Activity Packet Math Coloring Page… | 8.5 | 4.91 | 5,344 | [link](https://www.teacherspayteachers.com/Product/Kindergarten-October-Halloween-Fun-Activity-Packet-Math-Coloring-Pages-Calendar-1457962) |
| Kindergarten November Fall Thanksgiving Coloring Pages Activities Tur… | 8.5 | 4.89 | 5,231 | [link](https://www.teacherspayteachers.com/Product/Kindergarten-November-Fall-Thanksgiving-Coloring-Pages-Activities-Turkey-Craft-1494299) |
| Kindergarten January Winter Craft Coloring Page Place Value Sight Wor… | 8.5 | 4.9 | 4,911 | [link](https://www.teacherspayteachers.com/Product/Kindergarten-January-Winter-Craft-Coloring-Page-Place-Value-Sight-Word-Worksheet-1598299) |
| May 1st Grade End of Year Activities Spring Worksheets Fractions Colo… | 8.5 | 4.91 | 4,722 | [link](https://www.teacherspayteachers.com/Product/May-1st-Grade-End-of-Year-Activities-Spring-Worksheets-Fractions-Color-by-Number-1818893) |

## Title words that recur among top-velocity and most-rated listings

cozy (37), cute (27), color (22), bundle (21), easy (20), bold (19), relaxing (18), spooky (15), number (14), procreate (14), kawaii (12), fall (12), free (12), activity (11), stress (11), relief (11), art (11), halloween (11), mystery (9), png (9), party (8), mandala (8), anime (7), fantasy (7), summer (7), brushes (7), dark (6), autumn (6), gift (6), thanksgiving (6), disney (5), horror (5), magical (5), scenes (5), dragon (5), teens (5), craft (5), gothic (4), coco (4), girl (4)

## Seasonality calendar

Google Trends (5-year weekly; index 0–100; monthly averages). `list_by` = 6 weeks before the start of the peak month, the middle of the 4–8 week indexing window.

| Term | Geo | Peak | 2nd | Trough | YoY % | 5-yr % | List by | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| adult coloring | WW | Dec | Nov | Jun | 22.1 | 68.6 | 2026-10-20 | 44 | 46 | 43 | 43 | 43 | 37 | 37 | 41 | 41 | 39 | 48 | 57 |
| bold and easy coloring | WW | Dec | Feb | Jul | 0.4 | – | 2026-10-20 | 18 | 25 | 2 | 16 | 18 | 14 | 13 | 16 | 21 | 16 | 21 | 26 |
| coloring book | WW | Dec | Nov | Jun | 14.3 | 97.2 | 2026-10-20 | 42 | 44 | 4 | 39 | 39 | 37 | 38 | 42 | 43 | 41 | 46 | 52 |
| coloring pages | WW | Nov | Dec | Jul | -15.5 | 9.3 | 2026-09-20 | 64 | 67 | 67 | 66 | 64 | 57 | 52 | 55 | 61 | 66 | 72 | 69 |
| cozy coloring | WW | Dec | Oct | Jul | 44.6 | – | 2026-10-20 | 24 | 25 | 25 | 21 | 2 | 19 | 19 | 25 | 28 | 28 | 26 | 31 |
| kawaii coloring | WW | May | Mar | Oct | 12.7 | 116 | 2027-03-20 | 4 | 42 | 43 | 43 | 48 | 43 | 38 | 39 | 41 | 36 | 38 | 4 |

Etsy search seasonality (RankHero monthly Etsy searches, Sep 2025 – Aug 2026). Volumes are coarse buckets, so only clear peaks are listed:

List-by dates already in the past (before 2026-10-25) mean: list immediately for this season's peak.

| Etsy keyword | Peak month(s) | Trough | 12-mo trend % | List by |
|---|---|---|---|---|
| coloring pages | Jan/Mar/Apr/May/Sep/Oct/Nov | Jun/Jul | -18 | evergreen |
| coloring pages printable | Jan/Mar/Apr/May/Jun/Nov | Oct | – | evergreen |
| adult coloring pages | Jan | Feb/Jun/Jul/Aug/Sep/Dec | – | 2026-11-20 |
| coloring book pdf | Jan | May/Jun/Jul/Aug/Sep | -19 | 2026-11-20 |
| cozy coloring pages | Jan | Jun | – | 2026-11-20 |
| anime coloring pages | Jan/Mar/Apr/May | Jul/Nov | – | 2026-11-20 |
| cute coloring pages | Jan/Mar | Jul | – | 2026-11-20 |
| cottagecore coloring | Jan/Mar/May | Jul/Sep | -18 | 2026-11-20 |
| procreate coloring pages | Jan | Apr/May/Jun/Jul | – | 2026-11-20 |
| coloring page | Jan/Mar/Apr/May/Oct/Nov | Jun/Jul | -18 | evergreen |
| coloring sheets | Jan/Mar/Apr/May | Jun/Jul/Aug | – | 2026-11-20 |
| printable coloring pages | Jan/Mar/Apr/May/Jun/Nov | Oct | – | evergreen |
| cozy coloring book | Jan/Nov/Dec | Jun/Oct | – | 2026-11-20 |
| mandala coloring pages | Jan/Mar/Apr/May/Sep/Oct/Nov | Jul | -18 | evergreen |
| fairy coloring pages | Jan/Feb/Mar/Apr/May/Jun/Jul/Aug/Sep/Oct/Nov | Dec | – | evergreen |
| cat coloring pages | Jan | Jul/Aug/Dec | -18 | 2026-11-20 |
| dragon coloring pages | Jan/Feb/Mar/Apr/May/Sep/Oct/Nov | Jun/Jul/Aug/Dec | -18 | evergreen |
| mushroom coloring pages | Jan/Mar/Apr/Sep/Oct | Jun/Jul/Aug/Dec | -33 | evergreen |
| gothic coloring pages | Jan/Mar/Aug/Sep/Oct/Nov | Feb/Apr/May/Jun/Jul/Dec | – | evergreen |
| botanical coloring pages | Jan | Oct/Nov/Dec | – | 2026-11-20 |
| animal coloring pages | Jan/Feb/Mar/Apr/May/Sep/Nov | Dec | -18 | evergreen |
| color by number | Jan | Jun/Jul/Aug | – | 2026-11-20 |
| retro coloring pages | Jan/Mar/Jul/Sep | Feb/Apr/May/Jun/Aug/Oct/Nov/Dec | – | 2026-11-20 |
| y2k coloring pages | Jan/Feb/Mar/Apr/May/Sep/Oct/Dec | Jul | – | evergreen |
| chibi coloring pages | Jan/Mar/May/Sep/Oct/Nov | Feb/Apr/Jun/Jul/Aug/Dec | – | evergreen |
| coloring pages for adults | Jan | Feb/Jun/Jul/Aug/Dec | -19 | 2026-11-20 |
| stress relief coloring | Jan/Apr | Jun/Jul/Aug | – | 2026-11-20 |
| mandala coloring book | Jan/Feb/Jul/Dec | Mar/Apr/May/Jun/Aug/Sep/Oct/Nov | – | 2026-11-20 |
| quote coloring pages | Jan/Mar/Apr/Sep/Oct/Nov | Jun/Jul/Dec | – | evergreen |
| procreate coloring | Jan/Dec | Jul/Aug | – | 2026-11-20 |
| digital coloring pages | Jan/Oct | Jun/Jul/Aug | – | 2026-11-20 |
| coloring bookmarks | Jan | Jul/Dec | – | 2026-11-20 |
| princess coloring pages | Jan/Feb/Mar/Apr/May/Jun/Jul/Aug/Sep | Oct/Nov/Dec | – | evergreen |
| unicorn coloring pages | Jan/Mar/Apr/May/Sep | Oct | -18 | evergreen |
| dinosaur coloring pages | Jan/Feb/Mar/Apr/May/Jun/Sep/Oct/Nov | Jul/Aug/Dec | -18 | evergreen |
| food coloring pages | Jan/Mar/Apr/May/Nov | Dec | – | evergreen |
| coloring book | Feb/Mar/Nov | Apr/May/Jun/Jul | – | 2026-12-21 |
| bold and easy coloring book | Feb | Apr/May/Jun | – | 2026-12-21 |
| kawaii coloring pages | Mar | Oct | – | 2027-01-18 |
| manga coloring | Mar | Jul/Sep | -19 | 2027-01-18 |
| fantasy coloring | Mar/Oct | Jun/Sep | -33 | 2027-01-18 |
| valentines coloring pages | Mar | Jul | – | 2027-01-18 |
| easter coloring pages | Mar | Jul/Aug/Sep | – | 2027-01-18 |
| floral coloring pages | Apr/May | Oct/Dec | – | 2027-02-18 |
| mermaid coloring pages | May/Jun/Jul/Aug | Oct | 22 | 2027-03-20 |
| summer coloring pages | May/Jun | Nov/Dec | – | 2027-03-20 |
| ocean coloring pages | May | Nov/Dec | – | 2027-03-20 |
| japan coloring book | Aug/Sep | Oct | – | 2027-06-20 |
| grayscale coloring | Sep | May/Jul | – | 2027-07-21 |
| coloring bundle | Sep | Feb/May/Jun | – | 2027-07-21 |
| fall coloring pages | Sep | Feb/Jun | – | 2027-07-21 |
| bible coloring pages | Sep | Dec | – | 2027-07-21 |
| kawaii food coloring | Sep/Oct | Aug | – | 2027-07-21 |
| mandala coloring | Oct | Jul/Aug | -18 | 2027-08-20 |
| halloween coloring pages | Oct | Feb/Apr | – | 2027-08-20 |
| spooky cute coloring | Oct | Apr/May/Jun | – | 2027-08-20 |
| halloween coloring book | Oct | Jan/Feb | – | 2027-08-20 |
| witch coloring pages | Oct | Jun/Dec | – | 2027-08-20 |
| spooky coloring pages | Oct | Dec | – | 2027-08-20 |
| goodnotes coloring | Nov | Jan/Feb/Mar/Apr/May/Jun/Jul/Aug/Sep/Oct/Dec | – | 2026-09-20 |
| cute coloring book | Nov/Dec | Apr/May/Jun/Jul/Aug/Sep | – | 2026-09-20 |
| christmas coloring book | Nov/Dec | Apr/Jun | – | 2026-09-20 |
| grayscale coloring pages | Nov/Dec | Jun/Aug/Sep | – | 2026-09-20 |
| thanksgiving coloring pages | Nov | May | – | 2026-09-20 |
| kawaii coloring | Nov | Aug | – | 2026-09-20 |
| bold and easy coloring | Dec | Jun | – | 2026-10-20 |
| christmas coloring pages | Dec | Apr/May/Jun | – | 2026-10-20 |
| adult coloring book | Dec | Apr/May/Jun | – | 2026-10-20 |
| anime coloring book | Dec | Feb/Apr/May/Jun | – | 2026-10-20 |
| kawaii coloring book | Dec | Oct | – | 2026-10-20 |
| coloring book for adults | Dec | Apr/May/Jun | – | 2026-10-20 |
| christmas coloring sheets | Dec | Apr/May/Jun | – | 2026-10-20 |

### Month-by-month launch calendar

| Month to publish | What to list |
|---|---|
| Jan | Valentine's (peaks early Feb); spring/Easter prep; evergreen New-Year self-care, cozy and mindful sets |
| Feb | Easter/spring pages (Easter Apr 5 2027); start spring kawaii and garden sets |
| Mar | Summer/beach and ocean sets; Mother's Day gift bundles |
| Apr | Summer kids activity packs (school-holiday demand Jun–Aug) |
| May | Back-to-school classroom sets (TpT peaks Aug–Sep) |
| Jun | Halloween and spooky-cute, early: Etsy shoppers start in Aug–Sep |
| Jul | Halloween main launch; fall/autumn and cozy-season sets |
| Aug | Thanksgiving/fall; Christmas and advent sets; gift bundles |
| Sep | Christmas/winter main launch (Google 'coloring' terms peak Nov–Dec) |
| Oct | Last call for Christmas; New-Year self-care and mindful sets for the Jan bump |
| Nov | Valentine's and winter-cozy; Jan 'adult coloring' resolution demand |
| Dec | Spring and Easter prep; evergreen anime/kawaii drops when competition is busy with holidays |

## Price ladder (USD; non-USD converted at fixed approximate rates)

| Marketplace | Tier | n | 25th pct | Median | 75th pct | Share free |
|---|---|---|---|---|---|---|
| amazon | 10-30 pages | 4 | 16.98 | 16.98 | 16.98 | 0 |
| amazon | 50+ pages | 12 | 5.89 | 9.99 | 11.99 | 0 |
| amazon | unknown size | 33 | 9.99 | 11.99 | 16.99 | 0 |
| etsy | 10-30 pages | 29 | 2.19 | 3.99 | 8.09 | 0 |
| etsy | 2-9 pages | 5 | 3.95 | 5.4 | 7 | 0 |
| etsy | 31-49 pages | 15 | 3.79 | 5.4 | 9.99 | 0 |
| etsy | 50+ pages | 51 | 3.24 | 4.79 | 10.99 | 0 |
| etsy | PLR/resell mega bundle | 15 | 2.1 | 3.5 | 5.39 | 0 |
| etsy | procreate | 11 | 3.99 | 4 | 12.48 | 0 |
| etsy | single sheet | 65 | 1.75 | 2.25 | 2.99 | 0 |
| etsy | unknown size | 476 | 2.5 | 3.83 | 6 | 0 |
| gumroad | 10-30 pages | 15 | 0 | 3 | 5 | 0.27 |
| gumroad | 2-9 pages | 12 | 3 | 4 | 5.99 | 0.25 |
| gumroad | 31-49 pages | 8 | 0 | 3.76 | 6 | 0.38 |
| gumroad | 50+ pages | 17 | 0 | 5 | 9.99 | 0.29 |
| gumroad | PLR/resell mega bundle | 27 | 0 | 4.99 | 17 | 0.3 |
| gumroad | goodnotes | 5 | 0 | 7.99 | 8.99 | 0.4 |
| gumroad | procreate | 114 | 0 | 7.2 | 13 | 0.32 |
| gumroad | single sheet | 52 | 0 | 0 | 1.39 | 0.69 |
| gumroad | unknown size | 476 | 0 | 5 | 12 | 0.26 |
| itch.io | single sheet | 8 | 2.99 | 2.99 | 12.99 | 0 |
| itch.io | unknown size | 60 | 2.49 | 4.99 | 6.99 | 0 |
| payhip | unknown size | 5 | 2.99 | 3.64 | 5.99 | 0.2 |
| teacherspayteachers | 10-30 pages | 8 | 4 | 4.75 | 6.49 | 0 |
| teacherspayteachers | 2-9 pages | 3 | 0 | 1 | 3 | 0.33 |
| teacherspayteachers | 31-49 pages | 7 | 4 | 4 | 4 | 0 |
| teacherspayteachers | 50+ pages | 16 | 7.99 | 13.38 | 21 | 0 |
| teacherspayteachers | single sheet | 16 | 1 | 1.5 | 3.33 | 0 |
| teacherspayteachers | unknown size | 450 | 3 | 4 | 5.9 | 0.01 |

## Formats and bundles

- **gumroad**: NOT SHOWN 434, PDF 185, Procreate 114, PNG 16, JPG 6, GoodNotes 6, SVG 2, paperback 1
- **etsy**: PDF 441, NOT SHOWN 248, PNG 26, JPG 11, Procreate 11, SVG 5, paperback 3, GoodNotes 1
- **payhip**: NOT SHOWN 19
- **amazon**: NOT SHOWN 124, paperback 14, PDF 1
- **teacherspayteachers**: NOT SHOWN 430, PDF 81, PNG 1
- **itch.io**: NOT SHOWN 99, PDF 4, PNG 1
- **gumroad bundles vs single sets** (median ratings): bundle 3 vs non-bundle 3 (n = 134 / 582)
- **etsy bundles vs single sets** (median favorites): bundle 44 vs non-bundle 36 (n = 115 / 550)

## Cross-marketplace overlap (niches present on 3+ sources)

| Niche | Sources | Breakdown | Score |
|---|---|---|---|
| animals | 6 | etsy:38; gumroad:29; teacherspayteachers:18; amazon:6; itch.io:2; payhip:1 | 52.7 |
| anime-manga | 6 | gumroad:62; itch.io:54; teacherspayteachers:48; etsy:42; payhip:1; baldhamster:1 | 43.6 |
| bold-and-easy | 6 | gumroad:25; etsy:22; teacherspayteachers:20; payhip:3; amazon:2; tiktokshop:1 | 38.3 |
| cottagecore-botanical | 6 | gumroad:39; etsy:38; amazon:7; payhip:2; itch.io:2; teacherspayteachers:1 | 23.5 |
| christmas-winter | 5 | teacherspayteachers:67; etsy:42; gumroad:40; amazon:2; itch.io:2 | 56.5 |
| kids-educational | 5 | gumroad:47; teacherspayteachers:24; etsy:21; amazon:13; itch.io:6 | 55.0 |
| spring-easter | 5 | gumroad:21; etsy:17; teacherspayteachers:8; creativemarket:2; amazon:1 | 54.1 |
| halloween-spooky | 5 | teacherspayteachers:92; gumroad:60; etsy:59; amazon:2; templatemonster:1 | 42.9 |
| fantasy-fairy-dragon | 4 | etsy:64; gumroad:40; itch.io:4; monsterone:1 | 55.7 |
| summer-beach | 4 | etsy:25; gumroad:6; teacherspayteachers:6; amazon:1 | 49.6 |
| chibi-kawaii | 4 | etsy:81; teacherspayteachers:52; gumroad:41; payhip:4 | 35.2 |
| horror-gothic-dark | 4 | gumroad:5; etsy:4; itch.io:4; amazon:1 | 32.2 |
| retro-gaming-pixel | 4 | gumroad:4; etsy:1; amazon:1; teacherspayteachers:1 | 26.2 |
| fall-thanksgiving | 3 | teacherspayteachers:41; etsy:24; gumroad:9 | 61.4 |
| cozy-hygge | 3 | etsy:42; gumroad:31; creativemarket:1 | 49.4 |
| color-by-number | 3 | teacherspayteachers:22; etsy:10; gumroad:2 | 48.1 |
| valentine | 3 | etsy:16; gumroad:5; teacherspayteachers:5 | 41.1 |
| girls-fashion-people | 3 | gumroad:14; amazon:7; etsy:4 | 31.6 |
| travel-landscape-city | 3 | etsy:5; amazon:4; gumroad:2 | 28.2 |
| quotes-affirmations-faith | 3 | gumroad:32; etsy:19; teacherspayteachers:2 | 27.4 |
| mandala-pattern | 3 | etsy:42; gumroad:41; teacherspayteachers:28 | 26.1 |
| japan-culture | 3 | teacherspayteachers:45; gumroad:13; etsy:12 | 25.8 |

## Newcomer test

Count of listings under 12 months old (actual or ID-estimated age) that already have 50+ reviews. Etsy hides reviews and Gumroad, TpT and Amazon show no dates, so I also count young Etsy listings with 100+ favorites as a proxy.

| Niche | Listings < 12 mo | of which 50+ reviews | of which 100+ favorites (proxy) |
|---|---|---|---|
| cozy-hygge | 28 | 0 | 5 |
| bold-and-easy | 10 | 0 | 5 |
| mega-bundle-plr | 9 | 2 | 4 |
| color-by-number | 8 | 0 | 3 |
| halloween-spooky | 16 | 0 | 3 |
| mandala-pattern | 14 | 0 | 3 |
| anime-manga | 6 | 0 | 2 |
| chibi-kawaii | 22 | 0 | 2 |
| horror-gothic-dark | 3 | 0 | 2 |
| kids-educational | 6 | 0 | 1 |
| animals | 7 | 0 | 1 |
| japan-culture | 3 | 0 | 1 |
| cottagecore-botanical | 2 | 0 | 1 |
| fall-thanksgiving | 5 | 0 | 0 |
| christmas-winter | 16 | 0 | 0 |
| fantasy-fairy-dragon | 6 | 0 | 0 |
| spring-easter | 5 | 0 | 0 |
| summer-beach | 2 | 0 | 0 |
| girls-fashion-people | 2 | 0 | 0 |
| food-sweets | 3 | 0 | 0 |
| quotes-affirmations-faith | 2 | 0 | 0 |

## Anime / manga / kawaii / cozy Japan / retro gaming

| Segment | Rows | Sources | Median $ | Median Gumroad ratings | Median Etsy favorites | Etsy fav/mo (est) | Fan-art rows | Women-lean share |
|---|---|---|---|---|---|---|---|---|
| anime/manga | 176 | 6 | 4.99 | 10.5 | 51.5 | 1.84 | 12 | 0.29 |
| kawaii/chibi | 133 | 5 | 5.71 | 3 | 33 | 1.43 | 2 | 0.74 |
| japan-culture/retro | 67 | 3 | 3.35 | 0 | 43 | 1.31 | 0 | 0.16 |
| cozy-japan | 31 | 3 | 4.31 | 0 | 37.5 | 2.25 | 1 | 0.97 |
| retro-gaming/pixel | 12 | 5 | 4.99 | 2 | 53 | 3.34 | 1 | 0.33 |

Etsy keyword demand for these terms (RankHero):

| Keyword | Monthly Etsy searches | Competing listings | Searches/listing | Trend | Median price |
|---|---|---|---|---|---|
| kawaii coloring pages | 18,100 | 33,399 | 0.54 | – | $3 |
| anime coloring pages | 27,100 | 11,685 | 2.32 | – | $3.99 |
| manga coloring | 3,600 | – | – | Search interest dropped 19% between October 2025 and Septem… | $4.45 |
| japanese coloring pages | 530 | – | – | – |  |
| anime coloring book | 4,400 | 8,289 | 0.53 | – | $3.74 |
| kawaii coloring book | 2,400 | 23,935 | 0.1 | – | $3 |
| chibi coloring pages | 1,300 | – | – | – |  |
| japan coloring book | 590 | – | – | – |  |
| kawaii coloring | 1,000 | – | – | – |  |
| kawaii food coloring | 210 | – | – | – | $3.29 |

Kupkaike (third-party, live Etsy count): anime colouring books: crowded, 2,273 relevant listings, median $4.99, 52% under $5, 67 shops in top 100


Top listings in this segment (IP-risk flag: `fan-art/trademark` means the title names a trademarked character or brand; `original anime-style` means a generic style with low risk):

| Segment | Source | Title | $ | Ratings/Reviews | Favorites | Velocity | IP risk | Link |
|---|---|---|---|---|---|---|---|---|
| kawaii/chibi | amazon | $3.99 · ★ 4.7 Units/sold 10K 2 B0DF77698M $11.99 · ★ 4… | – | – | – | 9,000 monthly_sales_est_thirdparty | fan-art/trademark: kpop demon | [link](https://www.amazon.com/dp/B09PGVGCH5) |
| kawaii/chibi | amazon | Crayola Kpop Demon Hunters Art Case (40+pcs), Coloring… | 24.99 | 108 | – | 7,000 monthly_sales_est_thirdparty | fan-art/trademark: kpop demon | [link](https://www.amazon.com/dp/B0GH2KKKR6) |
| anime/manga | gumroad | FREE anime brushset! | 0 | 2,231 | – | –  | original anime-style (low) | [link](https://attki.gumroad.com/l/animebasic) |
| anime/manga | gumroad | The Complete Guide to Anime Studies  | 0 | 1,013 | – | –  | original anime-style (low) | [link](https://oridays.gumroad.com/l/animestudy) |
| anime/manga | gumroad | FREE Anime Hair brushpack! | 0 | 341 | – | –  | original anime-style (low) | [link](https://attki.gumroad.com/l/VgUuZ) |
| retro-gaming/pixel | amazon | Kalysky 3Pack Mystery Mosaics Color By Number Coloring… | 16.99 | 42 | – | 200 monthly_sales_est_thirdparty | original anime-style (low) | [link](https://www.amazon.com/dp/B0G1M3298G) |
| kawaii/chibi | gumroad | 85 Kawaii Coloring Book Keywords | 0 | 155 | – | –  | original anime-style (low) | [link](https://paulmarles.gumroad.com/l/YUNALy) |
| cozy-japan | etsy | 8,000+ Bold and Easy Coloring Pages Bundle / Kawaii Co… | 4.29 | NOT SHOWN | 660 | 123 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4505144878) |
| anime/manga | gumroad | Free Anime Soft Style Brushes for Procreate, Soft Draw… | 0 | 121 | – | –  | original anime-style (low) | [link](https://dibrushes.gumroad.com/l/freeanime) |
| anime/manga | gumroad | FREE Procreate Lineart Portrait Brushes for Anime Eyes… | 0 | 114 | – | –  | original anime-style (low) | [link](https://cozybrushery.gumroad.com/l/anime_lineart) |
| anime/manga | gumroad | Procreate 8 FREE Soft Dreamy Pastel Paradise Brushes, … | 0 | 101 | – | –  | original anime-style (low) | [link](https://cozybrushery.gumroad.com/l/softpasteldream) |
| anime/manga | itch.io | Anime Backgrounds | – | 87 | – | –  | original anime-style (low) | [link](https://noranekogames.itch.io/yumebackground) |
| anime/manga | gumroad | Paint Tool Sai inspired Dream, 33 Dynamic Comic, Anime… | 0 | 77 | – | –  | original anime-style (low) | [link](https://cozybrushery.gumroad.com/l/saibrushes) |
| kawaii/chibi | etsy | Kawaii Coloring Pages / 50 Pages / Cute Coloring Pages… | 4 | NOT SHOWN | 2,186 | 61.76 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/1610553653) |
| anime/manga | gumroad | Free Anime Soft Style Brushes for Procreate, Soft Draw… | 0 | 60 | – | –  | original anime-style (low) | [link](https://staspro1.gumroad.com/l/freeanimestyle) |
| anime/manga | etsy | Favorite Anime Mystery Coloring Book PDF – 52 Color by… | 5.4 | NOT SHOWN | 100 | 59.61 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4565979421) |
| cozy-japan | etsy | Disney Princesses Kawaii Coloring Book / 30+ Magical C… | 4.31 | NOT SHOWN | 437 | 48.84 favorites_per_month | fan-art/trademark: disney | [link](https://www.etsy.com/listing/4447467954) |
| anime/manga | gumroad | Free Gleaming Marmalade Brush Set in Anime Style for P… | 0 | 32 | – | –  | original anime-style (low) | [link](https://staspro1.gumroad.com/l/freemarmalade) |
| anime/manga | etsy | Mix Anime Cartoons: Mystery Color By Number Printable … | 5.8 | NOT SHOWN | 36 | 31.27 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4574620624) |
| kawaii/chibi | etsy | 200 Kawaii Coloring Pages: Bold & Easy Designs (8.5x11… | 95,000 | NOT SHOWN | 679 | 27.38 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/1801677675) |
| anime/manga | gumroad | FREE Procreate Manga Brushes: Manga Master Studio, Lin… | 0 | 27 | – | –  | original anime-style (low) | [link](https://cozybrushery.gumroad.com/l/mangacomic) |
| kawaii/chibi | gumroad | Kawaii Creator Brush Pack for Procreate: 500 Stamp Bru… | 15 | 27 | – | –  | original anime-style (low) | [link](https://beejaydel.gumroad.com/l/kawaii) |
| anime/manga | gumroad | Basic Brush Set for Manga Studio 5 - Clip Studio Paint | 0 | 25 | – | –  | original anime-style (low) | [link](https://robertmarzullo.gumroad.com/l/ZtdUi) |
| anime/manga | gumroad | Anime brushset(basic)! | 3.3 | 24 | – | –  | original anime-style (low) | [link](https://attki.gumroad.com/l/fullanimebrushes) |
| kawaii/chibi | teacherspayteachers | FREE Thanksgiving Turkey Day Kawaii Coloring page | – | 24 | – | –  | original anime-style (low) | [link](https://www.teacherspayteachers.com/Product/FREE-Thanksgiving-Turkey-Day-Kawaii-Coloring-page-5057110) |
| japan-culture/retro | etsy | A Heartwarming Coloring Book — A Cute Fairytale World … | 14 | NOT SHOWN | 155 | 22.87 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4481876772) |
| anime/manga | gumroad | Tsukepen Manga & Anime Procreate Brush Set  | 0.99 | 22 | – | –  | original anime-style (low) | [link](https://tsukepen.gumroad.com/l/FjXKJ) |
| kawaii/chibi | etsy | Kawaii Coloring Pages • 3-Page Printable Set • Cute Fo… | 3.56 | NOT SHOWN | 236 | 21.29 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4409823629) |
| anime/manga | etsy | The Apothecary Diaries Anime Coloring Book / 45 Pages … | 3.46 | NOT SHOWN | 53 | 20.39 favorites_per_month | original anime-style (low) | [link](https://www.etsy.com/listing/4550910050) |
| anime/manga | gumroad | Cute Kawaii Anime Girls Coloring Pages for Adults - In… | 0 | 20 | – | –  | original anime-style (low) | [link](https://cozybrushery.gumroad.com/l/animecoloring) |

## Do NOT enter (saturated or dominated)

- **color-by-number**: top-3 shops hold 0.67 of its 10 Etsy top listings
- **mega-bundle-plr**: race to the bottom: $1–7 for 10,000+ resell-rights pages floods the low end
- **japan-culture**: top-3 shops hold 0.75 of its 12 Etsy top listings
- **cottagecore-botanical**: search trend -25.5%
- **Fan art of trademarked characters** (Sanrio, Pokémon, Ghibli, Disney, KPop Demon Hunters and similar): rows with this flag show demand but carry takedown risk on your own site. Sell original anime-style characters instead.
- **Broad head terms** ('coloring pages', 'coloring book', 'adult coloring pages'): huge search volume, but 400k+ Etsy listings target them. Use them as secondary tags only.

## Recommendations for your shop (anime / kawaii / cozy Japan / retro / J-pop; mostly women buyers)

Derived from the tables above. See REPORT data files for the numbers behind each point.

1. **Cozy + kawaii Japan is the best fit, and its search demand is growing.** Google Trends 'cozy coloring' is +44.6% YoY and 'kawaii coloring' +12.7% YoY (+116% over 5 years). 'Coloring pages' itself is −15.5%. Among the Japan segments, cozy-japan has the highest estimated Etsy favorites per month and a 97% women-lean share. Traditional publishers are moving in (Union Square's *Cozy Colo: Kawaii Japan*, Coco Wyo's Cozy series, Dover's *Dream of Chibis*), which shows demand but also coming competition. Build original chibi/kawaii characters in Japanese settings (konbini, sento, sakura, cafes, bento, shrines, train stations).
2. **Mystery color-by-number is the strongest velocity format.** New 2026 Etsy listings ('Favorite Anime Mystery Coloring Book – 52 Color by Number Pages', 'Darkline'/'Coraline' gothic color-by-number, a Disney mystery bundle) gain 55–75 favorites a month. The Disney and Coraline ones are fan art. An **original** anime or kawaii mystery color-by-number book fits your audience and avoids the IP risk. Caveat: Etsy's generic color-by-number shelf is concentrated (3 shops hold 67% of its top listings, see 'Do NOT enter'). So go for the anime/kawaii *mystery* angle on your own site, not generic color-by-number on Etsy.
3. **Anime as a head term is crowded and slipping.** Etsy 'anime/manga coloring' searches are about −19% over 12 months. Kupkaike rates 'anime colouring books' as crowded: 2,273 relevant Etsy listings, median $4.99, 52% under $5. Don't compete on 'anime coloring pages' alone. Use anime as the style and a cozy, spooky-cute or mystery color-by-number angle as the hook.
4. **Use bold-and-easy and 'cute & cozy' as style modifiers, not as the niche.** 'Bold and easy' has high favorites velocity (4.8/mo median) but a very low Etsy search-to-listing ratio (0.01): thousands of near-identical bundles. 'Cozy', 'cute', 'bold', 'easy' and 'relaxing' are the most frequent words in top-velocity titles, so put them in titles and tags.
5. **Seasonal drops pay when listed early.** Fall/Thanksgiving, Christmas and Easter have the best Etsy search-per-listing ratios. Christmas list-by dates have already passed for 2026 (aim for the Dec peak with a kawaii advent or cozy-winter set listed **now**). Next: Valentine's (list by about Dec 21), then spring/Easter kawaii (list by about Feb 18). Spooky-cute Halloween peaks in Oct, so list by mid-Aug 2027.
6. **Price ladder for your own site:** single sheets $1.50–3; 10–30 page packs $4–6 (Etsy median $3.99); 50+ page books $7–12 (Etsy p75 $10.99, Amazon median $9.99 for print). Procreate versions sell for more on Gumroad (median $7.20 for a Procreate set vs $5 general). Offer a PDF + Procreate + GoodNotes bundle as the premium tier.
7. **Retro gaming / pixel is thin but promising.** Only 12 rows, but it has the highest favorites per month among the Japan segments (3.3). Test a small original pixel/retro-console set before investing.
8. **Avoid:** fan art (Sanrio, Pokémon, Ghibli, Disney, KPop Demon Hunters); PLR mega-bundles ($1–5 for thousands of pages); broad head terms; mandala and cottagecore/botanical (searches down 18–25% and low search per listing).
