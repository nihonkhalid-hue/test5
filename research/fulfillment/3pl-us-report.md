# MadeInAtlas: US 3PL shortlist (no minimums, no contract)

Date checked: 2026-10-07. Companion data: `3pl-us.csv` (same folder), one row for each of the 45 candidates.

## How this was researched (read first)

- **Network limits.** This cloud session's network policy blocked WebFetch **and** curl for: apps.shopify.com, trustpilot.com, fulfill.com, g2.com, capterra.com, bbb.org, cbp.gov, reddit.com, and every 3PL website tried. Only WebSearch worked.
- **What the numbers are.** Every figure below comes from what the search index shows of the provider's own page (or an official .gov page), with its URL and date. **None of it was read from the live page**, so confirm each figure in the written quote.
- **Reddit 30-day skill: not used.** It is not installed in this cloud session: it is not in the available skill list, and `~/.claude/skills` contains no Reddit skill. reddit.com is also blocked here, so the requested RSS route failed too. The Reddit column in the CSV says "blocked" for every row; no Reddit seller evidence was collected.
- **Royal MCP: not used.** It was not connected in this session, so the madeinatlas.com WooCommerce integration was not checked. Nothing was changed.
- **No CLAUDE.md.** The repo had no CLAUDE.md.
- **Review dates.** Merchant review scores come from search snippets of Shopify, G2, Capterra and BBB pages. Individual review dates were not visible.

## Result in one line

Of 45 candidates, 22 fail a hard filter and 17 could not be verified (pricing not published). Six pass or pass conditionally, and none of those passes is fully confirmed.

## Top 5

### 1. Fulfyld (Madison, AL)
- **Fees:** no setup fee, no platform fee, no long-term contract, no offboarding fee.
- **Minimum:** none published. Reviewers cite about 100 orders/month as a practical floor.
- **Storage (0–250 orders tier):** small bin $2.50, regular bin $4.00, XL bin $6.00, pallet $32 per month.
- **Receiving:** first 2 hours free at onboarding, then $40 per man-hour.
- **Per order:** all-in rate including postage, pick/pack and packaging averages $7.51 for a 4–12 oz parcel. 5 picks are free, then $0.50 per extra item.
- **Returns:** $3.50 for the first item, $0.50 for each extra item.
- **Other:** says it handles customs documentation; ships internationally, including Canada.
- **Risks:** very thin independent reputation: Clutch 5.0 (1 review), Shopify app 3.5/5 (4 reviews in the index; the listing now shows 0), BBB not accredited with 0 complaints. The site carries a lot of self-published comparison content.
- **Sources:** [pricing](https://www.fulfyld.com/3pl-fulfillment-pricing/), [contract](https://www.fulfyld.com/knowledge/does-fulfyld-have-minimum-contract-length/), [3plinsider](https://3plinsider.com/reviews/fulfyld), [BBB](https://www.bbb.org/us/al/madison/profile/fulfillment-services/fulfyld-0513-900281814)

### 2. eFulfillment Service (Traverse City, MI), conditional
- **For foreign sellers:** the best-documented process found. About half its clients are international, US citizenship isn't required, and it acts as consignee (but **not** importer of record).
- **WooCommerce:** native integration.
- **Contract:** month-to-month, with a 30-day refundable Test Drive.
- **Fees:** pick/pack $2.65 for the first unit plus $0.65 for each extra unit. Receiving $11.50 per half hour. Bin storage $0.45 (billing period ambiguous). No long-term storage surcharge.
- **Catch:** EFS's own site confirms a fixed recurring "comprehensive support fee". 3plinsider puts it at about **$23.50 a week (~$102 a month)** [VERIFY]. If confirmed, it fails the "no monthly fee" filter.
- **Reputation:** BBB A+, accredited since 2002 (1 complaint in 3 years, from an end customer). Shopify app 2.9/5 (3 reviews), G2 2.3/5 (4 reviews).
- **Red flags:** Shopify reviews describe an invoice at 4x the expected amount (the system double-charged shipments), and disputed inventory counts the merchant couldn't edit.
- **Sources:** [importing FAQ](https://www.efulfillmentservice.com/faq/importing-taxes/), [3plinsider](https://3plinsider.com/reviews/efulfillment-service), [Shopify reviews](https://apps.shopify.com/efulfillment-service-order-fulfillment-for-ecommerce/reviews), [BBB](https://www.bbb.org/us/mi/traverse-city/profile/fulfillment-services/efulfillment-service-inc-0372-17004552)

### 3. ShipBob, Growth Plan
- **Fees and terms:** no order minimum and no onboarding fee. Official WooCommerce app. Ships to Canada.
- **Receiving:** $40 for the first 2 hours, then $45/hour.
- **Storage:** bin $5, shelf $10, pallet $40 per month.
- **Limits:** under 400 orders/month, **at most 50 SKUs** (every size and colour counts as a SKU), and items under 23 kg.
- **Reputation:** Shopify 4.3/5 (286), G2 3.7/5 (122), Capterra 3.6/5 (107).
- **Red flags (BBB):** inventory lost while still being billed; stock not counted in for months; 264 returned units disposed of without permission; 8 weeks to release inventory to a client who was leaving.
- **Sources:** [Growth Plan](https://uk.shipbob.com/growth-plan/), [fees](https://support.shipbob.com/s/article/US-Fulfillment-Center-Additional-Services-Pricing), [BBB](https://www.bbb.org/us/il/chicago/profile/logistics/shipbob-0654-90005479/complaints)

### 4. Amazon Multi-Channel Fulfillment (MCF)
- **Fees and terms:** no minimum and no setup fee. You don't need to sell on Amazon. Official WooCommerce extension. Unbranded packaging.
- **Storage:** $0.78 per cubic foot per month from January to September, **$2.40 per cubic foot from October to December**.
- **Per order (small standard, 12–16 oz):** $8.66 for a 1-unit order including shipping, plus a 3.5% surcharge. A peak surcharge applies from 15 Oct 2026 to 14 Jan 2027.
- **Caveats:** Amazon won't act as importer of record, so cartons must arrive with customs cleared and duties paid. US addresses only [VERIFY].
- **Reputation:** official Shopify app 3.3/5 (56); connector apps 4.8–4.9/5 (350+ reviews each).
- **Sources:** [pricing](https://supplychain.amazon.com/mcf/pricing), [WooCommerce extension](https://woocommerce.com/products/woocommerce-amazon-fulfillment/)

### 5. Frankly Fulfillment (Ohio), unverified
- **Reported terms:** no setup fee, no monthly minimum, no software fee. Orders from $2.50. WooCommerce supported. 30-day trial.
- **Caveat:** all of this comes from a third-party listing, and there is no reputation data at all. It is mainly an FBA prep centre, so confirm it handles direct-to-consumer apparel.
- **Source:** [ecomcircles](https://ecomcircles.com/prep-centers/frankly-fulfillment/)

### Next options
- **Momentum Warehousing** (CA): no minimums, $3 per carton received. Storage is pallet-only at $49/month after 90 days, which is expensive for a few cartons.
- **Hexprep:** WooCommerce support not confirmed.

## Main failures (hard filter 1)

| 3PL | Why it fails |
|---|---|
| Fulfillrite | $399/month minimum + $59.99/month account fee |
| Simpl | $750/month minimum |
| ShipMonk | $250/month minimum |
| ShipCalm | $3,000/quarter minimum |
| Printful | $150/month minimum for your own products |
| Saltbox | $199/month membership |
| ShipGenie | $200 setup fee |
| ShipBots | monthly maintenance fee |
| ShipHype | $999/month account fee |
| Falcon | $1,500 setup fee and 4,000 orders/month |
| Shipfusion | 2,000+ orders/month and a setup fee |
| Red Stag | 200+ orders/month |
| ShipHero | 500 orders/month |
| Flexport | $5,000/month |
| Stord / Ware2Go | ~3,000+ orders/month |
| Whiplash | $250/month minimum |
| Fulfillment.com | 1,500 orders/month |

The full list is in the CSV.

## Import check (could block the plan)

1. **De minimis is gone.** It ended for all countries on [29 Aug 2025](https://www.federalregister.gov/documents/2025/08/05/2025-14897/suspending-duty-free-de-minimis-treatment-for-all-countries), and the suspension was made [indefinite on 24 Jun 2026](https://www.federalregister.gov/documents/2026/06/24/2026-12670/indefinite-suspension-of-the-de-minimis-exemption-for-merchandise-arriving-through-all-modes-other) for non-postal shipments. Every Aramex carton now needs a formal entry, or an informal one if it's worth $2,500 or less.
2. **Importer of record.** The 3PLs won't take this role (EFS says so [explicitly](https://www.efulfillmentservice.com/faq/importing-taxes/); Amazon won't either).
   - **Recommended setup:** MadeInAtlas LLC as importer of record using its EIN. Register with [CBP Form 5106](https://www.cbp.gov/trade/programs-administration/entry-summary/cbp-form-5106). Ship **DDP** with Aramex or use a licensed customs broker. List the 3PL as consignee only.
   - [VERIFY with a broker] that the foreign owner causes no issue, and whether a bond is needed for informal entries.
3. **US–Morocco Free Trade Agreement.** Qualifying apparel enters free of the normal duty, but only under the **yarn-forward** rule: the yarn must be spun in Morocco or the US, and every step after that too. The fibre can come from anywhere ([trade.gov](https://www.trade.gov/summary-morocco-fta-textiles), [USTR](https://ustr.gov/about-us/policy-offices/press-office/fact-sheets/archives/2004/july/us-morocco-free-trade-agreement-textile-and-app)).
   - **How to claim:** the entry uses the "MA" prefix on the tariff code.
   - **Proof of origin:** on request, the importer must provide a signed declaration covering materials, their origin and how the garment was made ([19 CFR 10 subpart M](https://www.ecfr.gov/current/title-19/chapter-I/part-10/subpart-M), [CBP FAQ](https://www.cbp.gov/trade/free-trade-agreements/morocco/faqs)).
   - **What doesn't qualify:** garments made from imported yarn, for example Turkish or Chinese yarn.
4. **New 12.5% tariff.** Since 24 Jul 2026, products of Morocco carry a **12.5% Section 301 tariff** ([USTR notice](https://www.federalregister.gov/documents/2026/07/28/2026-15181/notice-of-actions-in-section-301-investigations-of-acts-policies-and-practices-of-various-economies)). Secondary sources say goods qualifying under the trade agreement are not exempt. [VERIFY whether apparel is in the notice's Annex I/II exceptions.] Budget for it.

## Questions to ask each 3PL before sending stock

1. Will you accept small Aramex parcels from Morocco shipped DDP, with MadeInAtlas LLC as importer of record and you as consignee? What is the receiving fee per parcel or per hour?
2. Will you onboard a US LLC whose owner lives in Morocco? Which documents do you need?
3. Are there any recurring fees at zero orders (account, support, software, maintenance)? Please confirm in writing that there is no monthly minimum.
4. How many folded garments fit in one bin or shelf? Is each size or colour a separate location?
5. What is your receiving turnaround? How are count discrepancies handled, and who pays for lost inventory?
6. What are your fees for returns, relabelling and polybags? Is there a long-term storage surcharge?
7. If I leave: how much notice, what removal fees, and how many days until my stock ships? Do you ever hold inventory over a disputed invoice?
8. Do you ship to Canada? With which carrier, and on what duty terms?
9. Is the WooCommerce connection an official plugin or an API? Does it sync inventory and tracking automatically?
