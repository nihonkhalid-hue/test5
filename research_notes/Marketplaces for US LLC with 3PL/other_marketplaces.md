# US Marketplaces (besides Amazon/Walmart) for a Moroccan-owned US single-member LLC using a US 3PL (PrepPrime)

Research date: 2026-10-10. Method: web search. Direct page fetches failed with DNS errors for etsy.com, community.ebay.com and valueaddedresource.net, so some official-page content is taken from search-result summaries of those pages. Most non-official sources are LLC-formation, agency or SaaS vendors with an incentive to sell services. They are flagged as such below.

## 1. Which marketplaces are realistically open to a foreign-owned US LLC (EIN, Mercury, no SSN/ITIN, Moroccan IP)? A ranked view

### Takeaway
Rough order of ease, from the evidence found: (1) Etsy and eBay, which are open but have known identity and tax verification friction; (2) your own Shopify store, where the problem is payments, not the store, because Shopify Payments US wants an SSN/ITIN, so Stripe direct or PayPal are used instead; (3) curated or juried channels such as Uncommon Goods, Chairish and NOVICA, which are fit-driven rather than KYC-driven; (4) Temu Local and Wayfair, which are possible but unclear for foreign owners; (5) TikTok Shop US, Target Plus and SHEIN, which are effectively closed (they need a US representative with US ID and SSN/ITIN, an invitation, or $5M revenue). Faire is unclear for a Moroccan brand.

### Cited Findings

**eBay US (business account under the LLC)**
- For registered businesses, eBay asks for identification of beneficial owners, officers, directors or account managers, plus the EIN, business address and phone. If automated checks fail, eBay may ask for a photo of a valid ID. — [eBay export: bank account payouts](https://export.ebay.com/en/first-steps/how-to-create-seller-account/bank-account/)
- eBay's tax FAQ says that without a TIN, or with a W-8 certifying foreign status, payouts can be put on hold and backup withholding may apply. This implies that a W-8 path exists. — [eBay 1099-K & Tax Withholding FAQs](https://www.ebay.com/sellercenter/resources/changes-to-ebay-and-your-1099-k)
- An eBay community thread from an LLC with non-US owners reports that automatic verification would not pass and the account was blocked. An earlier moderator reply said a name and SSN/TIN for the officer or owner contact is still needed for identity, even with an EIN. — [eBay Community: Verification of Business Account for LLC with Non-US Owners](https://community.ebay.com/t5/Selling/Verification-of-Business-Account-for-LLC-with-Non-US-Owners/m-p/33781566/highlight/true); [eBay Community: EIN instead of SSN](https://community.ebay.com/t5/Ask-a-Mentor/Ein-instead-ssn/td-p/33281246)
- Another thread asks whether running a US LLC from Pakistan is allowed, which shows that operating from abroad is a common worry. — [eBay Community thread](https://community.ebay.com/forum/selling-57920/topic/us-llc-owned-by-non-us-resident-%C3%A2-is-operating-from-pakistan-allowed-157139/)
- A third-party blog (not official) says international sellers cannot open a US business account directly. This conflicts with eBay's W-8 language above. — summarized in search results from [flowlister.com](https://flowlister.com/blog/ebay-business-account/)

**Etsy**
- Etsy's help center says that with a non-US bank account you must verify the bank after your first sale (usually 30 days to start, 60 days to finish) or the shop is suspended. — [Etsy Help: Update and verify bank account](https://help.etsy.com/hc/en-us/articles/115015775908-How-to-Update-and-Verify-Your-Bank-Account-for-Etsy-Payments-Deposits)
- Etsy's seller verification page says a single-member LLC may be a disregarded entity and points users to the IRS letter ("sole mbr"). — [Etsy Help: Verify seller information](https://help.etsy.com/hc/en-us/articles/360001980067-How-to-Verify-Your-Seller-Information-for-Etsy-Payments)
- LLC vendors (biased) say that a non-US owner of a US LLC can open a shop with an EIN, a US bank and a selfie-plus-ID check of beneficial owners, and that Etsy checks the entity name and EIN against IRS records. — [MyStateLLC: Etsy KYC with Wyoming LLC](https://www.mystatellc.com/llc/marketplace/etsy/wyoming); [Monezzi](https://monezzi.com/open-etsy-seller-account)
- A non-US LLC owner on Etsy's forum reports being stuck in a tax-verification loop. A reply says new EINs can take weeks to appear in the IRS database. — [Etsy Community: Tax Verification Loop (Non-US LLC)](https://community.etsy.com/t5/Technical-Issues/Stuck-in-a-Tax-Verification-Loop-Non-US-LLC/td-p/149009213)

**TikTok Shop US**
- Agency and blog sources agree that TikTok Shop US needs a US Primary Business Representative with US government ID and SSN/ITIN. A non-US person can be verified only as the Ultimate Beneficial Owner (25%+) with a foreign passport. A real US address is required, and virtual offices or PO boxes may be auto-blocked. — [Clemta](https://clemta.com/blog/how-to-start-tiktok-shop-us-non-resident); [cfointl](https://cfointl.com/insights/us-llc-for-tiktok-shop-sellers/); [Avenue US](https://avenueus.com/blog/us-llc-for-tiktok-shop-sellers); [NCP/nvinc](https://nvinc.com/tiktok-shop-verified-seller/); agency video [TikTok @scottjletourneau](https://www.tiktok.com/@scottjletourneau/video/7486170842280414510)
- One source notes a mismatch: TikTok asks for a W-9, but a foreign-owned disregarded SMLLC would normally give a W-8BEN. — [cfointl](https://cfointl.com/insights/us-llc-for-tiktok-shop-sellers/)

**Shopify + Shop app (own site; traffic from Google and Meta)**
- Shopify community and staff answers say Shopify Payments US requires a full SSN/ITIN from the owner even when the business has an EIN (Terms §B-3). Non-residents also report approval followed by suspension. — [Shopify Community: SSN required for non-US resident](https://community.shopify.com/t/ssn-required-in-shopify-payments-for-non-us-resident-account/286532); [Shopify Payments for foreign-owned US LLC](https://community.shopify.com/t/shopify-payments-for-foreign-owned-us-llc/306063); [non-resident with LLC and EIN, no SSN](https://community.shopify.com/t/shopify-payments-for-non-us-resident-have-llc-and-ein-dont-have-ssn/39626)
- One 2026 article says Shopify Payments US is rejecting non-resident sellers. The source is NCP, a vendor. — [nvinc: Shopify Payments US rejecting non-residents (2026)](https://nvinc.com/shopify-payments-us-is-rejecting-non-resident-sellers/)
- Forum users treat Stripe direct as the workaround for non-residents. Its current eligibility rules were not verified. — [Shopify Community thread](https://community.shopify.com/t/how-to-ue-shopify-payments-being-a-non-us-resident/123101)

**Temu US Local Seller Program**
- Launched March 2024. A ShipStation and GeekSeller guide says any US-registered business or US resident can register at seller.temu.com. — [ShipStation](https://www.shipstation.com/blog/temus-local-seller-program-a-shipstation-sellers-guide/); [GeekSeller](https://www.geekseller.com/blog/temu-now-officially-open-to-u-s-local-sellers/)
- A 2026 guide lists the requirements as EIN, W-9, US business bank and government ID. — [SellerGains](https://sellergains.com/blog/temu-seller-requirements/)
- A formation vendor (biased) claims that without a local director holding an SSN, applications are often flagged or rejected. — [FlatFeeCorp](https://flatfeecorp.com/articles/temu-global-store-local-entity-requirements-non-resident-sellers-compliance-guide)

**SHEIN Marketplace US**
- Recent guides say new US sellers must be US-based businesses with at least $5M in annual revenue that ship from US operations. Older 2024 guides said $2M. Documents include incorporation papers, W-9 or W-8BEN-E, a trademark certificate and a logo. Individuals are not supported. — [Marpipe](https://www.marpipe.com/blog/shein-marketplace-explained); [Linnworks](https://www.linnworks.com/blog/shein-marketplace-guide/); [CedCommerce](https://cedcommerce.com/blog/how-to-sell-on-shein-a-sellers-guide/)

**Target Plus (and Mirakl)**
- Target Plus is invite-only or curated, although some sources mention a public application. Requirements cited are a registered US entity, inventory in the US, a US bank, W-9 and EIN, 24-hour dispatch, GS1 barcodes and price parity. It is now reachable through Mirakl Connect, but connecting does not grant admission. — [BellaVix](https://www.bellavix.com/target-plus-marketplace-explained-invite-only-requirements-fulfillment-standards-and-whether-your-brand-is-ready/); [ChannelEngine](https://support.channelengine.com/hc/en-us/articles/19136507076765-Target-Plus-marketplace-guide); [RetailBoss on Mirakl Connect](https://retailboss.co/mirakl-connect-adds-target-plus-to-its-seller-platform/); [eplaybooks](https://www.eplaybooks.com/post/target-plus-marketplace)

**Wayfair**
- Wayfair's own site describes the supplier program for the US, Canada and UK. — [sell.wayfair.com](https://sell.wayfair.com/)
- Third-party guides disagree on whether the supplier application is self-serve or invitation-only. They cite $1M to $2M product liability insurance and a need to ship from a warehouse or 3PL in the selling region, which a US 3PL meets. Review time is cited as 1 to 4 weeks. — [Spreetail](https://www.spreetail.com/blog/how-to-sell-on-wayfair); [WizCommerce](https://wizcommerce.com/blog/how-to-sell-on-wayfair-wholesaler-onboarding-guide/); [Medium: Wayfair international registration](https://medium.com/@crossbordertrade/wayfair-international-seller-registration-process-5ca71b46d4f3)

**Faire (wholesale)**
- Faire+ (large-retailer orders) requires a $2M certificate of insurance naming Faire, plus GTIN, weight, dimensions and Made-in data. It is available to select brands only. — [Faire support](https://www.faire.com/support/articles/53978627639067)
- Commission figures conflict: either 15% plus a $10 new-customer fee and processing, or 25% on first orders and 15% on reorders. Faire Direct (brand-referred retailers) is 0% in both versions. — [Craftybase](https://craftybase.com/blog/how-to-sell-on-faire-wholesale-guide); [adtribute](https://www.adtribute.io/directory/faire)
- Faire's list of supported locations covers the US, UK and EU countries among others. Morocco was not listed. — [Faire: not located in available countries](https://www.faire.com/support/articles/360016111311)
- Moroccan-goods brands already appear on Faire, for example the "marocMaroc" brand page and a "marocco" wholesale discovery page. — [Faire marocMaroc](https://www.faire.com/brand/b_426fyd5kx2); [Faire discover](https://www.faire.com/discover/marocco)

**Chairish, 1stDibs, NOVICA, Uncommon Goods, Michaels MakerPlace**
- Chairish's official commissions: Consignor 40%; Professional 30%; Premium 25% on vintage and 30% on new or made-to-order items. — [Chairish support](https://support.chairish.com/hc/en-us/articles/44165603442321-Chairish-Selling-Plans-Commission-Rate-Overview)
- Chairish and 1stDibs both carry many Moroccan rugs (1stDibs shows about 4,240 Moroccan rug listings), and a Marrakech-based maker sells on 1stDibs. — [1stDibs Moroccan rugs](https://www.1stdibs.com/furniture/rugs-carpets/origin/moroccan/); [Chairish Moroccan rugs](https://www.chairish.com/collection/rugs/moroccan)
- Uncommon Goods: makers apply only through its "Submit Your Product" form, and buyers reach out if interested. — [Uncommon Goods support](https://support.uncommongoods.com/hc/en-us/articles/49417644394139-How-do-I-submit-a-product-for-consideration)
- NOVICA welcomes international applicants, but the page found covers wholesale buyers, not artisan onboarding. — [NOVICA wholesale FAQ](https://www.novica.com/wholesale/faq/)
- Michaels MakerPlace sign-up starts with a free Michaels account and is aimed at small businesses and crafters. The separate Michaels Marketplace for brands and resellers asks for an LLC or corporation. — [Michaels MakerPlace](https://www.michaels.com/makerplace); [Michaels Marketplace](https://www.michaels.com/marketplace)

**Walmart (for context only)**
- Walmart reportedly needs a US entity taxed as a corporation or partnership, not a disregarded SMLLC, and geo-checks the applicant's IP. — [nvinc (vendor)](https://nvinc.com/which-entity-is-best-to-sell-on-walmart/)

### Inferences
- **Ranking for this seller's profile (inferred):**
  1. **Etsy.** It fits handmade Moroccan goods best. It is open to a US LLC with EIN and a US bank. The risk is IRS-match and ID verification delays.
  2. **eBay.** It is open, with a W-8 path, but foreign-owner verification failures are documented. eBay International Shipping or eBay export from Morocco is a fallback.
  3. **Shopify plus Google free listings and Meta.** The store is easy to open. The blocker is Shopify Payments. Expect Stripe direct or PayPal as the processor. The Shop app and Shopify's Google and Meta channels may depend on Shopify Payments or Shop Pay, which is unverified.
  4. **Chairish, 1stDibs and Uncommon Goods.** These are juried and commission-heavy, but strong for premium rugs, lamps and vintage-style items.
  5. **Wayfair and Temu Local.** Both are possible with a US 3PL. Wayfair needs liability insurance. Temu's foreign-owner treatment is unclear.
  6. **Faire.** It suits wholesale to boutiques, but Moroccan-brand eligibility is uncertain. Listing as a US-based brand that ships from the US 3PL may help, but this is unverified.
  7. **TikTok Shop US, Target Plus and SHEIN.** These are effectively not available without a US representative with an SSN, an invitation, or $5M revenue.
- Logging in from a Moroccan IP is a documented risk on Walmart. It is plausible but undocumented as a risk for the other platforms.

### Gaps
- No official or reliable information was found on these points:
  - Kaiyo, Mercari, Poshmark, Newegg, Bonanza and OnBuy requirements for foreign-owned LLCs
  - Kohl's, Macy's, Nordstrom, Home Depot and Lowe's marketplace entry rules
  - Tundra alternatives
  - The current Wayfair "Partner Home" program for small suppliers specifically
  - 1stDibs seller fees and international onboarding
  - Google Merchant Center and Meta Shops requirements
- Fees for Etsy, eBay, Temu and TikTok were not verified in this pass and should come from the official fee pages.
- No Reddit threads came up in search, so there is no organic forum evidence on approval ease. The Etsy and eBay community threads are the only peer evidence.
- 3PL integration (PrepPrime connectors to Etsy, eBay, Shopify and others) was not researched.

## 2. Etsy's July 2026 DDP rule for non-US sellers: does shipping from a US 3PL avoid it?

### Takeaway
Since July 9, 2026, Etsy requires DDP on orders shipped from outside the US to US buyers for the order to keep Etsy Purchase Protection. Shipping from a US 3PL appears to fall outside the rule because it is tied to where the shipment comes from, but no source explicitly confirms a US-warehouse exemption.

### Cited Findings
- The Etsy Seller Handbook says DDP is required on US-bound orders to qualify for Etsy Purchase Protection from July 9, 2026. Penalties include losing protection and being charged for tariffs or collection fees that buyers incur. UPS and FedEx are among the DDP carriers. — [Etsy Seller Handbook: Navigating Evolving Global Tariff Policies](https://www.etsy.com/il-en/seller-handbook/article/navigating-evolving-global-tariff-policies/1355662653395)
- The handbook frames the rule as covering shipments from outside the US, with exceptions only where DDP services are unavailable. — [Etsy Seller Handbook](https://www.etsy.com/il-en/seller-handbook/article/navigating-evolving-global-tariff-policies/1355662653395); [Etsy Help: Managing International Shipments](https://help.etsy.com/hc/en-us/articles/360001987487-Information-for-Managing-International-Shipments)
- The rule was announced June 9, 2026 by Etsy VP James Ossman. It is tied to the end of the US $800 de minimis exemption. — [Value Added Resource](https://www.valueaddedresource.net/etsy-requires-ddp-shipping-us-tariffs/); [Shopifreaks](https://www.shopifreaks.com/etsy-will-require-non-us-sellers-to-prepay-us-tariffs-and-bake-duties-into-item-prices-starting-in-july/)
- One report (Patreon, unverified) says Etsy also quietly made DDP shipping to the US a search-ranking factor. — [Patreon post](https://www.patreon.com/posts/etsy-changed-to-141479532)

### Inferences
- If inventory is imported in bulk (with duties paid at entry) and orders ship domestically from PrepPrime with the shop's ship-from origin set to the US, the parcel-level DDP rule should not apply. Search ranking could still treat the shop as non-US if the shop location is Morocco. Setting the shop and ship-from location to the US under the LLC is likely the cleaner setup. This is inference, not confirmed.

### Gaps
- Etsy has published nothing explicit on non-US-owned shops that ship from US warehouses. Confirm with Etsy Seller Support.

## 3. Cross-border programs (selling without a US LLC)

### Takeaway
Only partial evidence was found. Etsy and eBay accept Moroccan-resident sellers directly, but Etsy now requires DDP on direct US shipments. Faire does not list Morocco as a supported location.

### Cited Findings
- Etsy lets non-US banks receive payouts, subject to verification after the first sale. — [Etsy Help](https://help.etsy.com/hc/en-us/articles/115015775908-How-to-Update-and-Verify-Your-Bank-Account-for-Etsy-Payments-Deposits)
- eBay runs export.ebay.com onboarding for non-US sellers. — [eBay export](https://export.ebay.com/en/first-steps/how-to-create-seller-account/bank-account/)
- One NCP article argues that non-residents often do not need a US LLC unless a platform requires a W-9 or the country lacks processor access. The source is a vendor. — [nvinc](https://nvinc.com/us-llc-non-resident-ecommerce-sellers/)

### Gaps
- Whether Morocco is a supported country for Etsy Payments and eBay Managed Payments was not confirmed in this pass.
- Cross-border options for NOVICA artisans, 1stDibs and Chairish international dealers were not confirmed.

## 4. Tax flag: does inventory at a US 3PL create a US trade or business (ECI)?

### Takeaway
This is genuinely unsettled and depends on the facts. The IRS says that income from a US trade or business selling inventory is ECI. Practitioners disagree on whether 3PL storage alone, without a dependent agent or a fixed place of business, creates a US trade or business. Get professional advice.

### Cited Findings
- IRS: if a US trade or business sells inventory, the income is clearly ECI. The activity must be "considerable, continuous and regular." — [IRS: Effectively connected income](https://www.irs.gov/eci)
- An ABA Tax Lawyer article (Spring 2026) notes that for some inventory sales a US fixed place of business is also required for ECI. — [ABA: Reforming ECI rules](https://www.americanbar.org/groups/taxation/resources/tax-lawyer/2026-spring/reforming-effectively-connected-income-rules)
- A consultancy blog says inventory in US fulfillment centers generally makes profit ECI under IRC §§864/871/882. — [terms.law](https://terms.law/2024/12/05/how-the-irs-taxes-foreign-owned-u-s-entities-selling-online/)
- Dependent-agent risk applies when a US agent can conclude contracts for the foreign principal. — [Klasing Associates](https://klasing-associates.com/question/international-tax-law-faq/business-income-earned-nonresidents-individual-corporation-taxed/)
- A weaker Q&A source (JustAnswer) says storage alone usually does not create a US trade or business. — [JustAnswer](https://www.justanswer.com/tax/qzj6u-gino-second-opinion-question.html)

### Inferences
- PrepPrime ships orders and handles returns, but does not conclude sales. Whether that amounts to an independent-agent arrangement or a fixed place of business, and how the US–Morocco tax treaty applies, are questions for a cross-border CPA.

### Gaps
- No IRS ruling specific to 3PLs was found.
- The US–Morocco treaty's permanent-establishment provisions were not reviewed.
