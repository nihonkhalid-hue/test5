# Amazon US and Walmart Marketplace for a Moroccan-owned US single-member LLC (EIN, Mercury, StartFleet) using the PrepPrime 3PL, as of October 2026

> **Method note for the report writer:** In this session, direct page fetching was blocked. WebFetch returned DNS errors and the egress proxy rejected curl, including for prepprime.com, marketplacelearn.walmart.com and viral-launch.com. All findings below therefore come from search-result snippets and summaries of the cited pages. I could not read the pages in full. Official Amazon help pages that sit behind a Seller Central login, such as "Countries accepted for seller registration" and the tax interview help, were not retrievable. Treat specific numbers and lists as needing a final check against the live official pages. Vendor and formation-company blogs are marked **[vendor/biased]**.

## Q1: What is PrepPrime? (location, services, FBA prep, WFS, FBM and returns)

### Takeaway
PrepPrime (prepprime.com) is a small 3PL and prep center in the Houston area (Stafford, TX). It advertises Amazon FBA prep, FBM order fulfillment, returns handling and Walmart support, with simple per-unit pricing and no onboarding fee. Its company details are inconsistent across sources, and I found no published pricing specific to Walmart WFS.

### Cited Findings
- PrepPrime's own site footer gives the address "806 Summer Park Dr Suite 250, Stafford, TX 77477" (Copyright 2023). — [Prep Prime homepage](https://prepprime.com/)
- Directory profiles give a different address, 2121 Brittmoore Rd (Ste 3100), Houston, TX. They list roughly 1–10 employees and a founding date of about 2020. — [RocketReach](https://rocketreach.co/prepprime-profile_b7f136ecc25df4c7); [ZoomInfo](https://www.zoominfo.com/c/prepprime/561680858)
- The homepage gives two different warehouse sizes, "22,000 square feet" and "31,000 sq ft", both in the Houston area. — [Prep Prime homepage](https://prepprime.com/)
- Listed services: inbound logistics, storage, and outbound for Amazon FBA, FBM and Walmart Fulfillment Services. Also cross-docking, prep, bundling and kitting. — [Prep Prime homepage](https://prepprime.com/)
- A prep-center directory lists Prep Prime (Stafford, TX) as serving Amazon FBA, Amazon FBM/SFP and Walmart Marketplace, with 24–48 hour turnaround. It also lists locations in Texas, Ohio and Hamburg, Germany. The directory does **not** flag Prep Prime as WFS-capable, although it does flag other centers that way. — [EcomCircles prep center directory](https://ecomcircles.com/prep-centers/)
- Published pricing: FBM at $2 per order plus shipping. Prep or bundling at $0.60 each, FNSKU labeling not included. Returns management at $1 per return for boxes under 2 cu ft, and $2 per cu ft for oversized. No onboarding fee. — [Prep Prime pricing](https://prepprime.com/pricing/)
- A competitor comparison page exists that lists Prep Prime alternatives **[vendor/biased]**. — [Speed Commerce vs Prep Prime](https://www.speedcommerce.com/vs/prepprime/)
- WFS has its own prep chargebacks if units arrive without proper labels or bags (for example, label about $0.65 and poly bag about $0.80, per a calculator site). This makes a 3PL's WFS-compliant prep worth having. — [EcomCircles WFS calculator](https://ecomcircles.com/software/wfs-calculator/)

### Inferences
- PrepPrime looks able to cover all three flows the user needs: FBA inbound prep, FBM/Walmart seller-fulfilled pick-pack-ship, and returns. It is very small, so service-level, insurance and integration questions should be confirmed in writing. Key ones: whether it integrates with Seller Central, Walmart Seller Center or ShipStation, whether it supports Walmart's 2-day/OTD tags, and its WFS prep and labeling standards.
- Texas has no state income tax, but holding inventory in a Texas warehouse creates sales-tax physical nexus in Texas. Marketplace-facilitator laws mean Amazon and Walmart collect and remit sales tax on their own sales, but any off-marketplace sales (Shopify) would need Texas registration. This is an inference; confirm with a tax professional.
- PrepPrime's address can serve as the Walmart **returns address**, since Walmart requires a physical US return address and does not accept PO boxes. It should **not** be presented as the LLC's "operating office" unless that is true and agreed with PrepPrime.

### Gaps
- I could not open prepprime.com directly, so I could not confirm current services (WFS prep, TikTok Shop, Shopify integration), current 2026 pricing, storage fees, minimums, or which of the two addresses is current.
- I found no independent reviews of PrepPrime on Reddit, Trustpilot or Google, and nothing on its experience with non-US clients.

## Q2: Is Morocco a supported country for Amazon seller registration? Should you register as the LLC or as an individual?

### Takeaway
Third-party lists consistently include Morocco among the roughly 188 countries Amazon accepts for seller registration on Amazon.com. I could not read Amazon's official list page directly. Because the user has a US LLC, the cleaner path is to register as a **business** (the LLC, with its EIN), with the Moroccan owner as the verified primary contact and beneficial owner.

### Cited Findings
- Amazon accepts registrations from roughly 188 countries but operates only about 21 marketplaces. Eligibility to register and where you can sell are separate questions. — [Feedvisor (2026)](https://feedvisor.com/university/countries-approved-by-amazon/)
- Morocco and Kenya appear on third-party copies of the "Countries accepted for US seller registration" list. — [EcomCrew (2026 updated)](https://www.ecomcrew.com/what-countries-are-allowed-to-sell-on-amazon-usa/); [amazondatalab list (older)](https://amazondatalab.wordpress.com/countries-accepted-for-us-seller-registration/); [WorldFirst Morocco guide](https://www.worldfirst.com/af/blog/online-sellers/selling-on-amazon-ecommerce-sellers-morocco/) **[payment-provider, biased]**
- Marketplace Pulse reported Amazon expanding accepted seller countries to nearly all countries. That article is older, so check it against the current list. — [Marketplace Pulse](https://marketplacepulse.com/articles/amazon-opens-doors-to-sellers-from-nearly-100-more-countries)
- An Amazon moderator noted that a country can be accepted for **registration** but not for **disbursement**. Sellers in that position need a bank account in a supported disbursement country or a third-party payment provider. — [Seller Forums (EU)](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b1bc521a40065caa79b3a931e38e238a)
- A Moroccan citizen who set up a UK LTD (with no UK residence) reported repeated verification rejections with no stated reason. A reply said the business needs proof of establishment in the eligible country, a local phone number and more. — [Seller Forums (EU) thread](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b1bc521a40065caa79b3a931e38e238a)
- Amazon does not strictly require a US entity. Non-US individuals can register directly. — [Globalfy](https://globalfy.com/blog/amazon-us-seller/) **[vendor/biased]**; [Wise](https://wise.com/us/blog/ein-requirements-for-non-us-amazon-sellers) **[payment-provider]**

### Inferences
- The user's Mercury US account is in the LLC's name, so it removes the disbursement problem: payouts go to a US account. The registration country choice (US entity versus Morocco residence) still has to be consistent with the documents.
- A weaker approach is to register as an individual Moroccan resident and deposit to Mercury, because the bank-account holder (the LLC) would not match the seller (the individual). That mismatch is a known verification trigger, so registering as the LLC keeps names consistent across the EIN letter, articles, bank and seller account.

### Gaps
- I could not open Amazon's live "Countries accepted for seller registration" help page (it requires a Seller Central login and fetching was blocked), so Morocco's October 2026 status relies on third-party copies.

## Q3: Amazon registration documents, video verification, business address, credit card and deposit method

### Takeaway
Expect to need the following:
- Passport (the owner's government ID)
- A recent bank or credit card statement in the owner's name, which doubles as proof of address
- A phone number for OTP or calls
- An internationally chargeable credit card (not prepaid)
- A deposit bank account
- The EIN letter (CP575 or 147C) plus the LLC formation documents

Amazon then usually requires a live **video call** with an Amazon associate, in which you show the original ID and documents. For the address, use real, documentable addresses only. Virtual or mail-forwarding addresses tend to fail automated verification.

### Cited Findings
- Core registration items: a government ID (passport or driver's license, with clear color photos), a bank account and routing number for payouts, an internationally chargeable credit card (prepaid generally not accepted), tax information (EIN for a business), a phone number for verification, and possibly proof of address (a recent bank or credit card statement) and a business license or registration. — [sell.amazon.de registration guide](https://sell.amazon.de/en/online-verkaufen/registrierungsleitfaden); [sell.amazon.es registration guide](https://sell.amazon.es/en/vender-online/guia-de-registro); [hustlegotreal guide](https://hustlegotreal.com/blog/create-amazon-seller-account/)
- Documents commonly requested from a non-resident LLC: the LLC name exactly as filed, the EIN, a US business address, a US business bank account in the LLC's name, a passport copy, and proof of the owner's personal address. — [NVINC 2026 non-resident guide](https://nvinc.com/non-resident-amazon-sellers-guide/) **[vendor/biased]**
- The sources conflict on the business address. One consultancy says Amazon wants proof of real operating presence, not a registered-agent address. Other vendors say the registered-agent address is acceptable as the LLC's address. — [NVINC](https://nvinc.com/non-resident-amazon-sellers-guide/) **[vendor]**; [Globalfy](https://globalfy.com/blog/amazon-us-seller/) **[vendor]**
- INFORM Consumers Act or business-address verification: a seller reported the system saying it "cannot verify P.O. Box or virtual addresses." If database matching fails, Amazon may mail a postcard with a verification code. — [Seller Forums: INFORM address verification](https://sellercentral.amazon.com/seller-forums/discussions/t/29f2f849-a1d0-4e3f-8cc0-e39fbfc5726a); [Emplicit INFORM guide](https://emplicit.co/amazon-inform-act-seller-compliance-guide/)
- PO boxes and mail-forwarding addresses are reported as rejected. — [Laramie Ledger](https://laramieledger.com/blog/amazon-inform-consumers-act-address-verification-sublease/) **[sells office subleases, biased]**
- Common rejection causes in forum threads:
  - One digit mismatched between the typed ID number and the ID image
  - Statements Amazon judged "forged or manipulated"
  - "Multiple selling accounts" flags
  - Only a utility bill being accepted for address proof

  — [Seller Forums: verification rejected](https://sellercentral.amazon.com/seller-forums/discussions/t/f17a373b-d09c-4283-bb9a-fa25277acae3); [Seller Forums: identity verification keeps failing](https://sellercentral.amazon.com/seller-forums/discussions/t/67e002ee-766d-4c1b-a85a-3f1ac5f0dd75); [Seller Forums: verification rejection](https://sellercentral.amazon.com/seller-forums/discussions/t/4d629f17-9879-49b3-8bc6-fae8e99fdedc)
- Video verification: an Amazon staffer in a forum thread asked for a case ID and screenshots after a failed video ID call. I found no official guide specific to non-US sellers. — [Seller Forums: video identification verification call](https://sellercentral.amazon.com/seller-forums/discussions/t/beacdb50-9541-45fb-ba86-0b2f28fbf081)

### Inferences
Practical, non-deceptive setup, inferred from the sources above:
- **Legal business name and registered address:** the LLC exactly as on the articles and EIN letter, at the address on the IRS records (often the StartFleet or registered-agent address).
- **Primary contact / beneficial owner:** the Moroccan owner, with their **real Moroccan residential address**, supported by a Moroccan bank statement or utility bill in their name.
- **Do not** present a 3PL or virtual address as a residence or office.
- **Credit card:** a Mercury debit or IO card in the LLC's name is commonly used. A Moroccan international Visa or Mastercard in the owner's name also works conceptually, but its statement address must match what was entered. Not verified from an official source.
- **Deposit method:** Mercury (US routing and account number in the LLC's name) matches the seller name, which is ideal.
- **Video call:** do it from the same device and connection used for registration, with the original passport and the same documents uploaded.

### Gaps
- I found no official Amazon page specifying what a foreign-owned US LLC should enter as "business address" versus "primary contact address", or whether a registered-agent address passes INFORM verification in 2026.
- I found no 2026 Amazon statement confirming Mercury debit or IO cards are accepted. Anecdotally they are, but I have no source.

## Q4: Amazon tax interview: W-8BEN vs W-9 for a foreign-owned disregarded LLC

### Takeaway
A single-member LLC owned by a non-US individual is a disregarded entity, so the IRS "beneficial owner" is the Moroccan individual, who is not a US person. The usual answer is therefore a **W-8 series form** (typically W-8BEN in the owner's name), not a W-9. Some sellers report being forced to choose "Individual". Professional review is advised because sources conflict, and Form 5472 plus a pro-forma Form 1120 are separate annual filings.

### Cited Findings
- Forum posts say a foreign-owned single-member LLC owner should select "Individual" in the tax interview because the LLC is disregarded. One user reported being forced to pick "Individual" rather than "Business". — [Seller Forums: Single-member LLC – foreign owner](https://sellercentral.amazon.com/seller-forums/discussions/t/e410adbd-1b33-42fc-893a-f5292a27953a); [Seller Forums: tax interview guidance](https://sellercentral.amazon.com/seller-forums/discussions/t/5a9b07c3-84e6-4d10-9def-677ce5d11e00)
- A foreign individual owner commonly provides W-8BEN, using the owner's legal name, citizenship, permanent foreign address, foreign TIN where required, and date of birth. — [GenZone W-8 vs W-9 guide (2026)](https://www.genzone.com/guides-w8-w9-forms-us-llc-foreign-owners/) **[vendor/biased]**; [O&G Tax and Accounting](https://oandgaccounting.com/u-s-tax-guide-for-foreign-owned-wyoming-llcs-selling-on-amazon-fba/)
- One source suggests a W-9 route in the LLC's name, but says this implies the LLC files Form 1120 and pays US tax. It flags this as needing professional review. — [JustAnswer](https://www.justanswer.com/tax/quty3-i-m-non-us-resident-formed-single-member-llc.html)
- Common tax-interview mistakes for non-residents with LLCs **[vendor/biased]**. — [NVINC](https://nvinc.com/understanding-amazons-tax-interview-non-residents-us-llc/); [Riverbend Consulting](https://riverbendconsulting.com/blog/amazon-tax-interview/)
- Since the 2017 Treasury regulations, foreign-owned disregarded entities must file Form 5472, with a $25,000 penalty for non-filing. — [Wikipedia: disregarded entity](https://en.wikipedia.org/wiki/Disregarded_entity); [NVINC](https://nvinc.com/non-resident-amazon-sellers-guide/) **[vendor]**

### Inferences
- Signing a W-9 certifies US-person status. A non-resident individual owner of a disregarded LLC is not a US person, so doing so could be a false certification. The defensible default is W-8BEN (or W-8ECI if the owner treats the income as effectively connected with a US trade or business). The choice affects US tax exposure and depends on whether there is a US trade or business; for example, whether inventory in a US warehouse with a dependent agent creates one is a fact-specific question. The owner should confirm this with a cross-border CPA.

### Gaps
- I could not retrieve Amazon's official tax interview help page for this scenario.
- I found no authoritative ruling on whether FBA or 3PL inventory creates ECI for a Moroccan owner. The US–Morocco tax treaty exists (signed 1977), but I did not research its permanent-establishment article in this session.

## Q5: Logging in from Morocco, VPNs, related accounts and device consistency (Amazon and Walmart)

### Takeaway
Logging in from Morocco is consistent with the truthful profile: a Moroccan owner of a US LLC. Amazon registers sellers from Morocco, and residence is declared during KYC. The bigger risk is switching between locations or using VPN IPs, which forum sellers associate with hijack-detection suspensions. Shared devices or IPs with other seller accounts can also link accounts. The usual advice is one dedicated device and stable home or office internet, with no VPN.

### Cited Findings
- A seller who switched to a US VPN was suspended within hours. Replies attributed it to Amazon treating sudden IP or country changes as possible account takeover. — [Seller Forums: VPN for traveling](https://sellercentral.amazon.com/seller-forums/discussions/t/03eb8fff0f910a899b43d68edc51a9f3)
- Related accounts: forum replies say Amazon never discloses how links are made. Logging in to another account even once from the same device could link them, even with a VPN. Another seller said two accounts on one IP are fine unless one violates policy. These views are unresolved. — [Seller Forums: same IP address](https://sellercentral.amazon.com/seller-forums/discussions/t/6fa39f71-fee2-4b6b-af1f-d4301497c943)
- Proxy and IP vendors claim Amazon tracks IPs, addresses, bank accounts, cards, phones, emails and tax IDs, and suspends all linked accounts together. — [IPBurger](https://www.ipburger.com/blog/why-your-amazon-seller-account-needs-a-dedicated-ip-amazon-seller-account/) **[sells proxies, biased]**; [GoLogin](https://gologin.com/blog/why-is-my-amazon-account-suspended/) **[sells anti-detect browsers, biased]**
- A related-accounts appeal specialist describes linked-account bans **[vendor/biased]**. — [Mr Jeff AMZ](https://mrjeffamz.com/bans/related-accounts)
- A "suspended: unable to verify information" thread illustrates verification-driven suspensions. — [Seller Forums](https://sellercentral.amazon.com/seller-forums/discussions/t/f4415ad88581f534b6e7943975476afd)

### Inferences
- Using a VPN or US residential proxy to *appear* US-based while declaring Moroccan residence creates an inconsistency, which is a fraud signal. Doing so while *claiming* to be US-based would misrepresent residence in KYC. The latter likely breaches marketplace terms (accurate information) and could fall under US bank KYC (Mercury) misrepresentation. Recommendation: be transparent about Moroccan residence, log in from Morocco on a consistent device and ISP, and avoid VPNs and anti-detect browsers.
- Before registering, the owner should never log in to anyone else's seller account (a friend's, a former VA's) from the same device. Any VA or agency should be added as a user through Amazon's User Permissions, not given shared credentials.
- Moroccan mobile IPs are often carrier-grade NAT. Stable fixed-line home or office internet is preferable. This is an inference with no source.

### Gaps
- I found no official Amazon or Walmart policy text explicitly addressing VPN use. All IP and VPN evidence is anecdotal or from vendors.
- I found no Walmart-specific reports about logins from foreign IPs.

## Q6: Amazon Handmade, FBA vs FBM with a 3PL, Global Selling and common suspension reasons

### Takeaway
Amazon Handmade suits genuine Moroccan crafts, but makers must apply, and products must be made entirely by hand, hand-altered or hand-assembled by the applicant or a small team or cooperative. I found no source confirming Morocco-specific Handmade eligibility. FBA with PrepPrime handling prep is the lower-ops option. FBM through PrepPrime ($2 per order) keeps control but needs strict ship-time and valid-tracking performance.

### Cited Findings
- Handmade eligibility: items made by hand, hand-altered or hand-assembled. Mass-produced, resold and dropshipped goods are excluded. Applicants can be individual artisans, small teams (fewer than 20 people), or cooperatives, non-profits and social enterprises. — [Threecolts](https://www.threecolts.com/blog/amazon-handmade-artisan-beginners/); [SellerSessions 2026](https://sellersessions.com/amazon-handmade-sellers-guide/)
- Handmade requires a Professional account, and the $39.99 monthly fee is waived after approval. Sources disagree on timing: after the first month, or from the second month. The application asks for descriptions of the production process and product photos. Approval reportedly takes up to about 2 weeks. — [TheCraftMap 2026](https://www.thecraftmap.com/blog/amazon-handmade-application); [Linkmybooks fees guide](https://linkmybooks.com/blog/amazon-handmade-fees-guide)
- Prep centers receive inventory, prep it to Amazon standards and ship it to FCs. Bad prep causes delays, fees or rejections. — [BQool](https://blog.bqool.com/what-is-a-prep-center/); [Hopstack](https://www.hopstack.io/blog/11-things-to-consider-while-choosing-the-right-fba-prep-center) **[vendor]**
- Amazon Global Selling has country landing pages. The China page illustrates the structure; no Morocco-specific page was found. — [sell.amazon.com Global Selling (China)](https://sell.amazon.com/global-selling/china)

### Inferences
- For Moroccan handicrafts (rugs, leather, ceramics, argan cosmetics), Handmade gives a 15% referral fee and no monthly fee once approved (per common descriptions; confirm). The maker must be the applicant or a disclosed cooperative partner. Reselling other artisans' goods as one's own "handmade" would be a misrepresentation.
- Importing from Morocco into the US: ship B2B to PrepPrime (with a customs broker and possibly a CBP bond). FBA labels can be applied in Morocco or at PrepPrime. Cosmetics such as argan oil fall under FDA MoCRA facility and product listing rules (not researched here).
- Common suspension reasons for foreign sellers, synthesized from the forums: document mismatches, unverifiable addresses, related-account links, sudden IP or device changes, and inauthenticity or IP complaints.

### Gaps
- I found no source confirming whether Moroccan-resident artisans are accepted into Handmade, or any Handmade-specific verification steps.
- I found no current (2026) Amazon fee schedule in this session.

## Q7: Walmart Marketplace eligibility in 2026 for a US LLC with a foreign owner (US address, W-9/W-8, EIN, phone, history, GTINs, returns)

### Takeaway
Walmart decides eligibility by **country of incorporation** and tax classification, not by the owner's nationality. A US-incorporated LLC with an EIN falls into the W-9 path in Walmart's onboarding guide. This creates the core problem for a single-member LLC owned by a non-resident individual: it is disregarded, and the owner is not a US person.

Morocco is **not** on Walmart's list of non-US incorporation countries, which means the US-LLC route is the only available route. Walmart also wants a US physical return address (no PO boxes), an EIN letter (CP575 or 147C), GS1 GTINs (or an exemption), and often evidence of ecommerce history.

### Cited Findings
- Walmart's official tax guide: a seller with an EIN and US country of incorporation uses W-9. Walmart may request IRS CP575, 147C or CP148B. Non-US incorporation with an EIN maps to W-8ECI. — [Walmart Marketplace Learn: Tax classifications](https://marketplacelearn.walmart.com/guides/Getting%20started/Onboarding/Tax-classifications-and-documentation)
- The non-US incorporation countries supported for the W-8BEN-E path are China, Hong Kong, UK, Japan, Canada, Mexico, India, Singapore, South Korea, Taiwan, Germany, Vietnam, Thailand, Chile and Turkey. **Morocco is not listed.** W-8BEN is supported only for sole proprietors from Mexico or India. — [Walmart Marketplace Learn: Tax classifications](https://marketplacelearn.walmart.com/guides/Getting%20started/Onboarding/Tax-classifications-and-documentation); [Ecomclips 2026](https://ecomclips.com/blog/walmart-marketplace-requirements-in-2026-what-you-really-need-to-know-before-apply/) **[agency]**
- Payment holds: up to 14 days for new US sellers and up to 21 days for non-US sellers. A physical US return address is required and PO boxes are not accepted. — [Walmart Marketplace Learn (via search summary)](https://marketplacelearn.walmart.com/guides/Getting%20started/Onboarding/Tax-classifications-and-documentation); [GeekSeller 2026](https://www.geekseller.com/walmart-marketplace-for-international-sellers/) **[vendor]**
- A formation firm warns that the most common mistake is a non-resident filing a W-9 for a single-member disregarded LLC, which amounts to a false certification. It recommends the LLC elect C-corp tax status (Form 8832), so the LLC itself becomes a US taxpayer able to sign the W-9. It says Walmart gives little flexibility to avoid US taxpayer status. — [NVINC: Walmart W-9 mistakes](https://nvinc.com/walmart-w-9-mistakes/); [NVINC: Entity for Walmart](https://nvinc.com/which-entity-is-best-to-sell-on-walmart/) **[vendor/biased; verify with CPA]**
- A 2026 guide says Walmart still requires a US-registered entity, EIN and US return address, and that "pure international applications without US presence" are declined. Older articles (2021–2023) said listed-country sellers did not need a US company. Those are likely outdated. — [GeekSeller 2026](https://www.geekseller.com/walmart-marketplace-for-international-sellers/); [EcomCrew (older)](https://www.ecomcrew.com/walmart-non-us-vendors/); [Helium10 (older)](https://www.helium10.com/blog/walmart-international-sellers/)
- Third-party summaries of application requirements:
  - US-registered business with an EIN (SSN not accepted)
  - Business address and US bank account
  - Phone number
  - W-9 or W-8 plus the EIN verification letter, with name and address matching IRS records
  - GS1 GTINs (exemptions possible for private-label or handmade goods)
  - Often, links to existing marketplace stores (Amazon, eBay, Shopify) as proof of experience

  Approval takes about 2–4 weeks, and you can reapply after fixing the rejection reason. — [GoAura 2026](https://goaura.com/blog/walmart-seller-application) **[vendor]**; [RepricerExpress](https://www.repricerexpress.com/how-to-get-approved-on-walmart-marketplace/) **[vendor]**; [Accrue Agency](https://theaccrueagency.com/blog/walmart-seller-requirements-2025-how-to-get-approved-and-tips-to-succeed/) **[agency]**; [BellaVix](https://www.bellavix.com/tips-tricks-to-get-approved-faster-on-walmart-marketplace/) **[agency]**
- Marketplace Pulse reported that foreign (mostly Chinese) sellers outnumber US sellers on Walmart. — [Marketplace Pulse](https://www.marketplacepulse.com/articles/foreign-sellers-outnumber-the-us-on-walmart)
- Non-resident owners of single-member LLCs report the same W-9-only problem on other platforms: an Etsy W-9 loop, and Apple offering only a W-9. This illustrates the systemic issue. — [Etsy community](https://community.etsy.com/t5/Technical-Issues/Stuck-in-a-Tax-Verification-Loop-Non-US-LLC/td-p/149009213); [Apple developer forums](https://developer.apple.com/forums/thread/669240)

### Inferences
- To give an honest W-9 on Walmart, the LLC probably needs to be a US taxpayer in its own right, for example by electing C-corp treatment (Form 8832). That brings 21% federal corporate tax on profit, Form 1120 and different 5472 handling. The alternative is to accept that a disregarded single-member LLC owned by a Moroccan resident may not fit Walmart's onboarding cleanly. This is a significant decision for a CPA, and it should not be papered over by signing a W-9 as if the owner were a US person.
- Rejection reasons, synthesized from vendor sources:
  - Mismatched names or addresses against IRS records
  - No marketplace history
  - Restricted categories
  - Missing GTINs
  - Unverifiable US presence
  - Missed document requests (the Scribd appeal example)

  Tips: apply with an established Amazon account history, a real website, GS1 barcodes, and a clear list of products and categories.
- The PrepPrime address is a legitimate **return address** and ship-from address for seller-fulfilled orders, with PrepPrime processing returns at $1 per return.

### Gaps
- I could not read the live Walmart Marketplace Learn page in full, so I could not confirm whether Walmart 2026 explicitly addresses foreign-owned US disregarded LLCs, or whether a US phone number or US-resident primary contact is mandatory.
- I found no Reddit (r/WalmartSellers) or forum reports from Moroccan, or more broadly African, owners of US LLCs. Searches targeting Reddit returned no relevant threads.
- I found no information on how Walmart's identity verification handles a Moroccan passport or a Moroccan IP.

## Q8: WFS eligibility and Walmart cross-border programs for non-US sellers

### Takeaway
WFS is open to approved Marketplace sellers. A US LLC that passes onboarding can use WFS, inbounding through PrepPrime, provided PrepPrime's prep meets WFS standards. Walmart's cross-border programs do not cover Morocco:
- **Walmart Imports:** ships from China, Vietnam or India to WFS.
- **Walmart Exports:** launched early 2026; ships US WFS inventory to Canada and Mexico.

### Cited Findings
- Walmart Exports (early 2026) lets eligible WFS items ship from the US to shoppers in Canada and Mexico, with WFS sellers reportedly opted in by default. Comprehensive documentation (duties, returns, category eligibility) was not yet published. — [Supply Chain Dive](https://www.supplychaindive.com/news/walmart-exports-program-wfs-sellers/810858/); [GeekSeller](https://www.geekseller.com/blog/walmart-wfs-sellers-now-have-access-to-canada-and-mexico-via-walmart-exports/); [Winning With Walmart](https://winningwithwalmart.com/walmart-exports-a-new-cross-border-expansion-path-for-u-s-marketplace-sellers/)
- Walmart Cross Border Imports requires US orders to be fulfilled through WFS, an account in good standing, and a validated tax profile. Third-party sources say goods must come from China, Vietnam or India via select ports. — [Walmart Marketplace Learn: Cross Border Imports](https://marketplacelearn.walmart.com/guides/Walmart%20Fulfillment%20Services%20(WFS)/WFS%20programs%20&%20services/walmart-cross-border-imports-overview); [china-fulfillment.com](https://www.china-fulfillment.com/walmart-wfs-fulfillment-from-china-2026.html) **[vendor]**
- Walmart's guide states that a foreign entity without US presence importing under a CAIN should use "care of WFS" as consignee. — [Walmart Marketplace Learn: involved parties](https://marketplacelearn.walmart.com/guides/walmart-cross-border-imports-involved-parties-and-signatory-parties)
- Walmart has a "WFS international sellers" guide. — [Walmart Marketplace Learn: WFS international sellers](https://marketplacelearn.walmart.com/guides/Walmart%20Fulfillment%20Services%20(WFS)/Getting%20started%20with%20WFS/WFS-international-sellers)
- In August 2025, Walmart recruited UK sellers for the US marketplace and for its Canada, Mexico and Chile marketplaces. — [Walmart corporate news](https://corporate.walmart.com/news/2025/08/29/walmart-recruits-uk-sellers-to-its-online-marketplace-at-uk-seller-summit)
- WFS returns: the seller pays return processing for returns that are not Walmart's fault. Sellable returns go back into inventory with no restocking fee. — [Walmart Marketplace Learn: WFS returns](https://marketplacelearn.walmart.com/guides/Walmart%20Fulfillment%20Services%20(WFS)/WFS%20basics/wfs-returns-overview)

### Inferences
- The Moroccan owner should import into the US (to PrepPrime) as the US LLC, and then send inventory to WFS and FBA from there. No Walmart program supports Morocco as an origin country.

### Gaps
- I could not read the content of the "WFS international sellers" guide.
- The current eligible-country list for Walmart Exports and Imports in October 2026 is unconfirmed.

## Q9: Honest guidance on presenting as US-based, and what experienced sellers recommend

### Takeaway
Do not use a VPN, US proxies, or claim a US operating address or residence that is not real. The owner is a Moroccan resident and the business is a US LLC, so declare exactly that. Keep every document, name and address identical across the IRS (EIN letter), StartFleet formation documents, Mercury, Amazon, Walmart and PrepPrime. Use one dedicated device and network, and add helpers as sub-users.

### Cited Findings
- Consistency of business name, address and personal details (including middle initials) across all documents is the most repeated verification advice. — [Laramie Ledger](https://laramieledger.com/blog/amazon-inform-consumers-act-address-verification-sublease/) **[vendor]**; [Ecomclips](https://ecomclips.com/blog/walmart-marketplace-requirements-in-2026-what-you-really-need-to-know-before-apply/) **[agency]**
- Walmart requires application details to match IRS records. — [GoAura](https://goaura.com/blog/walmart-seller-application) **[vendor]**
- VPN-triggered suspensions and related-account linking appear in the Amazon forum anecdotes. — [Seller Forums: VPN](https://sellercentral.amazon.com/seller-forums/discussions/t/03eb8fff0f910a899b43d68edc51a9f3); [Seller Forums: same IP](https://sellercentral.amazon.com/seller-forums/discussions/t/6fa39f71-fee2-4b6b-af1f-d4301497c943)
- StartFleet is a formation vendor targeting non-residents (LLC, EIN, banking and processor help, tax filings), with uniformly positive self-selected Trustpilot reviews. — [GlobeNewswire 2022 press release](https://www.globenewswire.com/fr/news-release/2022/04/05/2416758/0/en/StartFleet-Launch-LLC-US-Company-Formation-and-Tax-Advice-Guide-for-International-Online-Entrepreneurs.html) **[self-promotional]**; [Trustpilot](https://fr-be.trustpilot.com/review/startfleet.io)

### Inferences
- Claiming a US residence or operating office that does not exist, to Amazon, Walmart or Mercury, is a KYC misrepresentation. It risks permanent suspension with funds held, and bank account closure. The legitimate approach is a real Moroccan residence plus a real US legal and registered address and a real US 3PL warehouse address (for inventory and returns), each labeled for what it is.
- Practical checklist (inferred):
  - EIN letter name matches the articles exactly.
  - Mercury statements are in the LLC's name.
  - The passport name matches the owner's name everywhere.
  - Proof of the Moroccan address is a recent (within 180 days) utility or bank statement in the owner's name, with a translation where needed.
  - A phone number reachable for OTP: a Moroccan mobile is acceptable for Amazon. A US VoIP number is often rejected for OTP (anecdotal, unsourced).

### Gaps
- I found no Reddit threads from r/AmazonSeller, r/FulfillmentByAmazon or r/WalmartSellers in this session's search results specific to Moroccan or foreign-owned US single-member LLCs. Forum evidence comes from Amazon Seller Forums only.
- I found no official statement from Amazon or Walmart on whether a non-US primary contact for a US LLC is acceptable (Amazon appears to accept it in practice; Walmart is unclear).
