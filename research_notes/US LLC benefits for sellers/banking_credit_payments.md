# Banking, Fintech, Payments and Business Credit for a Non-Resident-Owned US LLC (Moroccan founder, EIN, no SSN, Mercury + Stripe + PayPal)

Method note: WebFetch and direct page fetches were blocked in this environment (DNS/egress proxy denied mercury.com, stripe.com, support.mercury.com and others). All findings below come from web-search result summaries of the cited pages, not full-page reads. Treat exact numbers as "reported by the cited page". Many sources are vendor or affiliate blogs, flagged where relevant. No Reddit threads came up in any search, so the "Reddit tips" section uses consultant blogs, Shopify Community threads and TechCrunch instead.

## 1. Mercury: perks, IO credit card, Treasury/yield, non-resident eligibility

### Takeaway
Mercury officially accepts US-formed companies whose founders are not US residents, with some countries excluded. It rejects registered-agent, PO box and UPS Store addresses as the principal place of business. The IO card pays 1.5% cashback with no annual fee, is underwritten on account balance rather than SSN or credit score, and gets 30-day terms at about $15k or more on deposit. The perks catalog lists about 272 deals (AWS credits, Gusto and others). Treasury yield figures conflict.

### Cited Findings
- Eligibility: the business must be formed and registered in the US or a US territory. Founders don't need to be US citizens or residents. Mercury "cannot currently support accounts for businesses with founders living in certain countries and regions" (this search did not confirm whether Morocco is on that list). — [Mercury Support: Eligibility](https://support.mercury.com/hc/en-us/articles/28770467511060-Eligibility)
- Address: a US or international principal-place-of-business address is required. Residential addresses are OK. Registered agent addresses, PO boxes and UPS Store addresses are NOT accepted. — [Mercury Support: Company address requirements](https://support.mercury.com/hc/en-us/articles/28769699533588-Company-address-requirements)
- One third-party guide calls a registered-agent or mailbox address the most common reason for decline or later closure. In one consultant anecdote, a Mercury account was closed after the founder used the registered-agent address as the principal place of business. — [ExpatMemo: Mercury outside US 2026](https://expatmemo.com/mercury-account-outside-us/); [James Baker CPA](https://jamesbakercpa.com/blog/stripe-account-frozen-what-to-do/)
- Required documents: formation documents, the IRS EIN document, and a government ID (passport) for each founder or majority owner. — [WooCommerce Mercury listing (reproduces Mercury help text)](https://woocommerce.com/products/mercury/)
- KYC for a non-US founder reportedly takes 2–3 weeks, and OFAC screening excludes UBOs resident in Russia with Russia-linked business (secondary wiki). — [wiki.private.law: Mercury](https://wiki.private.law/en/mercury)
- History: in July 2024 Mercury gave some founders 30 days' notice of account closure based on where they lived (e.g. Ukraine, Nigeria), even though their startups were domiciled in the US. Mercury said "Passports were not considered in these offboarding decisions." — [TechCrunch, Jul 2024](https://techcrunch.com/2024/07/23/mercury-bank-fintech-sanctions-ukraine-nigeria)
- IO card: unlimited 1.5% cashback on all spend, deposited once the balance is paid, no annual fee. — [Mercury: IO credit](https://mercury.com/credit); [Merchant Maverick review](https://www.merchantmaverick.com/reviews/mercury-business-credit-card-review/)
- IO is issued by Patriot Bank, Member FDIC. "Most US-based businesses" qualify on day one. There is no set minimum balance for basic eligibility. $15,000+ across Mercury accounts unlocks 30-day repayment terms; below that it autopays daily. — [WooCommerce/Mercury text](https://woocommerce.com/products/mercury/); [Rho blog: Mercury card reviews (competitor)](https://www.rho.co/blog/mercury-business-credit-card-reviews)
- Third-party guides say IO underwriting is balance-based, not SSN or personal credit based, making it one of the few real US credit cards reachable without an SSN. No official Mercury page confirmed card-specific rules for international founders. — [crossborderplus](https://crossborderplus.com/fintech/how-to-open-mercury-account-abroad/); [GlobalSolo: Mercury IO vs Ramp vs Brex vs Rho for non-resident LLCs 2026](https://www.globalsolo.global/blog/mercury-card-vs-ramp-vs-brex-vs-rho-corporate-cards-2026)
- Treasury yield: Mercury's credit page says "up to 4.00%". A 2026 review (possibly stale) says "up to 2.6%". Rho (a competitor) says Mercury Treasury needs a $250,000 minimum and charges 0.15%–0.60% a month based on balance. These conflict. — [Mercury: credit](https://mercury.com/credit); [StartupSavant review](https://startupsavant.com/service-reviews/mercury-io-mastercard); [Rho vs Mercury](https://www.rho.co/versus/mercury)
- Perks marketplace: one aggregator counted 272 Mercury perks as of 2 Oct 2026, including AWS ($5k credits) and Gusto (3 months free, a new-customer promo offered by Gusto). Mercury also lists perks like Decile Partners (20% off). — [startupperks.co: Mercury perks](https://startupperks.co/partner-perks/mercury); [Mercury Perks](https://mercury.com/perks); [Mercury perk: Decile Partners](https://mercury.com/perks/decile-partners)
- A secondary source claims the "Mercury Raise + Perks" bundle is worth $200,000+ in partner credits (includes an unverified Google Cloud figure). — [guptadeepak.com](https://guptadeepak.com/startup-offers/programs/mercury-raise)
- Referral promo: $250 credit for depositing $10k within the first 90 days (aggregator, Aug 2026). For a new account only; this LLC already has Mercury. — [JoinSecret: Mercury](https://www.joinsecret.com/mercury)

### Inferences
- With an existing account and a real (non-registered-agent) address on file, the main untapped value is likely: (a) applying for IO in-app (balance-based, no SSN), keeping $15k+ for 30-day float; (b) browsing mercury.com/perks inside the dashboard for SaaS credits; (c) Treasury only if the balance approaches the reported $250k threshold.
- If the address on file is a registered agent address, fixing it is a priority, because sources link this to closures.

### Gaps
- Whether Morocco is on Mercury's restricted-country list. The support page could not be fetched; the founder should check it directly. Morocco is not a sanctioned jurisdiction, but this is not confirmed against Mercury's list.
- The current official Treasury yield and minimums, and the exact current perks list, could not be confirmed because fetches were blocked.
- Mercury Vault / sweep FDIC coverage amounts were not verified in this session.

## 2. Alternative/complementary accounts for non-resident owners (Relay, Wise, Payoneer, Airwallex, Revolut, Brex, Ramp, Novo, Found, Slash, Meow, Rho, Lili)

### Takeaway
The most consistently reported non-resident-friendly options in 2026 are Wise Business, Relay, Airwallex, Lili and Mercury, with Ramp as the most accessible card. Novo and Found effectively require an SSN. Brex and Rho reportedly want a real US address, US funding or a US-SSN owner. Every source says policies are tightening and vary by country.

### Cited Findings
- Relay (official): accepts US-registered businesses owned by non-US citizens or residents, but the business "must have an operating presence in the U.S." Non-US citizens must provide a passport (national ID cards not accepted). An EIN is required. — [Relay Support: Required documents](https://support.relayfi.com/hc/en-us/articles/38049251551636-Required-Documents-and-Organization-Details-to-Open-a-Relay-Account-by-Entity-Type)
- Relay restricted countries: one 2026 guide says owners with citizenship or residency in 31 listed countries can't open accounts (case-by-case exceptions). This is not Relay's official list. — [payglobalhub](https://payglobalhub.com/relay-financial-non-us-resident-account/); [wyomingllc.co](https://wyomingllc.co/relay-bank-wyoming-llc/)
- Relay banks through Thread Bank (Member FDIC), with up to $3M FDIC coverage through an IntraFi sweep as of early 2026 (secondary). — [LLC University guide](https://www.llcuniversity.com/foreigners/open-us-bank-account-llc-non-resident)
- Wise Business: described as the easiest approval for non-residents (24–48h reported). It accepts a registered agent address, has a $0 monthly fee and requires an EIN. It is an EMI/MSB, not a bank, and is not FDIC insured (funds safeguarded). Best for receiving USD (and multi-currency, e.g. EUR/GBP details) rather than holding large balances. — [LLC University](https://www.llcuniversity.com/foreigners/open-us-bank-account-llc-non-resident/comment-page-1/); [usllc.io 2026](https://www.usllc.io/blog/us-bank-account-for-non-residents); [truescho 2026](https://truescho.com/en/blog/best-us-business-bank-account-non-residents-2026)
- Airwallex: a payments platform, not a chartered bank. A $0 monthly fee and a registered agent address reportedly accepted (blog). — [hynogo 2026](https://hynogo.com/blog/best-us-bank-accounts-non-residents-2026); [internationcorpus 2026](https://www.internationcorpus.com/post/best-business-bank-accounts-for-non-us-residents-after-forming-a-usa-llc-in-2026)
- Revolut Business: sources conflict. One guide says it accepts non-resident US LLC owners, is not FDIC insured, and has a free plan with paid tiers from about $25/month. Revolut's UK/EEA eligibility depends on EEA/UK residence, which may not apply to US entities. — [llcstarters](https://llcstarters.com/non-residents/bank-account/); [Wise UK blog](https://wise.com/gb/blog/best-business-account-non-residents); [OffshoreCorpTalk thread](https://www.offshorecorptalk.com/threads/revolut-and-wise-business-accounts-for-llcs-as-non-residents.47117/)
- Payoneer: suits "marketplace revenue first" use cases (e.g. Amazon/Etsy payouts). No fee details were found. — [internationcorpus](https://www.internationcorpus.com/post/best-business-bank-accounts-for-non-us-residents-after-forming-a-usa-llc-in-2026)
- Lili: reportedly lets eligible non-US residents apply remotely with a foreign passport and EIN, supporting 24+ countries. Its footnote says non-US residents may apply with a passport number. — [activategloballimited: Mercury vs Relay vs Lili 2026](https://activategloballimited.com/mercury-vs-relay-vs-lili/); [startfleet](https://startfleet.io/guide/us-business-bank-account-for-non-us-resident-guide)
- Novo and Found: listed as US residents/persons only, requiring an SSN, so not viable without one. — [llcstarters](https://llcstarters.com/non-residents/bank-account/); [GlobalSolo Banking Access Index 2026](https://www.globalsolo.global/data/banking-access-index)
- Brex: sources disagree. Some say it needs $50K cash or VC backing; others say non-residents can apply with a real US business address and evidence of US operations. — [GlobalSolo cards comparison](https://www.globalsolo.global/blog/mercury-card-vs-ramp-vs-brex-vs-rho-corporate-cards-2026); [ein.so](https://www.ein.so/ein-for-bank-account/)
- Rho: needs a US business address or a beneficial owner with a US SSN (blog). — [GlobalSolo banks comparison](https://www.globalsolo.global/blog/mercury-vs-wise-vs-relay-best-bank-2026)
- Ramp: several sources call it the most accessible card for non-residents. One says it accepts a foreign passport plus EIN with no US address requirement (unverified against Ramp's own terms). — [GlobalSolo](https://www.globalsolo.global/blog/mercury-card-vs-ramp-vs-brex-vs-rho-corporate-cards-2026)
- One 2026 guide says US fintechs have tightened requirements for non-resident LLC accounts. — [truescho 2026](https://truescho.com/en/blog/best-us-business-bank-account-non-residents-2026)
- Traditional banks (Chase, BofA etc.) mostly refuse remote foreign owners. Specialty fintechs fill the gap. — [LLC University](https://www.llcuniversity.com/foreigners/open-us-bank-account-llc-non-resident)

### Inferences
- A practical redundant stack: Mercury (primary) + Relay or Lili (second US bank, as a backup against a sudden closure) + Wise Business (multi-currency receiving, EUR/GBP payouts to Morocco at low FX) + Payoneer (only if selling on marketplaces that favor it).
- Slash and Meow: no sources returned in these searches (see Gaps).

### Gaps
- Slash, Meow, Rho and Airwallex official non-resident policies were not found or confirmed.
- No official Payoneer fees for 2026 were found.
- Whether Morocco is on Relay's or Lili's restricted lists was not confirmed.

## 3. Business credit cards without an SSN, and the ITIN route

### Takeaway
Without an SSN or ITIN, realistic cards are balance- or cash-flow-underwritten corporate cards (Mercury IO, Ramp, possibly Brex, Aspire-type secured models). Traditional bank business cards (Amex Business, Chase Ink, Capital on Tap) need a personal guarantee, which in practice means an SSN or ITIN plus US credit history. An ITIN makes Amex and others possible but does not guarantee approval.

### Cited Findings
- EIN-only cards are almost always corporate cards (Ramp, Brex, Aspire) underwritten on cash balance, revenue or processing history, not FICO. Many require about $25,000+ in the bank or a cash deposit. Aspire uses a secured collateral model. — [Aspire blog 2026 (vendor)](https://aspireapp.com/us/blog/business-credit-cards-with-ein-only); [GlobalBanks](https://globalbanks.com/business-credit-cards-with-ein-only/)
- Issuers can't deny you solely for lacking an SSN, but can deny for no credit history. — [NerdWallet: foreign national business card](https://www.nerdwallet.com/article/credit-cards/business-credit-card-foreign-national); [Chase: business card with no SSN](https://www.chase.com/personal/credit-cards/education/basics/business-card-with-no-ssn)
- Classic bank business cards like Amex Business or Chase Ink require a personal guarantee, and so an SSN or ITIN. — [globalizationguide](https://globalizationguide.com/credit-cards/us-credit-cards-non-resident/)
- "Seven of the ten largest US card issuers accept an ITIN" (Capital One, BofA, Citi, Chase, US Bank, Amex, Synchrony), but "ITIN accepted does not mean ITIN approved." — [founderscredit.llc (vendor)](https://founderscredit.llc/blog/us-amex-for-non-residents)
- Amex says some applicants without an SSN may use an ITIN or other government ID. There is no automatic approval route for non-residents, and extra identity, address or ownership documents may be required. — [Financely](https://www.financely.io/how-to-get-an-amex-business-card-without-u-s-residency)
- Amex Global Transfer: if you hold an Amex in your home country, it can be used to get a first US Amex. — [GlobalBanks: Amex for non-residents](https://globalbanks.com/american-express-for-non-us-residents/)
- Without history, a new ITIN holder is "credit invisible" at first. A secured card is often suggested to build history. — [NerdWallet: business card without SSN](https://www.nerdwallet.com/business/credit-cards/learn/business-credit-card-without-ssn); [Nav](https://www.nav.com/business-credit-card/get-card-without-ein/)
- An ITIN also unlocks Shopify Balance (it requires an SSN or ITIN; see section 5) and makes PayPal Working Capital possible (the owner SSN field). — [Shopify Help: Balance eligibility](https://help.shopify.com/en/manual/finance/shopify-balance/eligibility); [PayPal Working Capital](https://www.paypal.com/us/webapps/mpp/paypal-working-capital)

### Inferences
- Order of operations: Mercury IO now → Ramp (if balance qualifies) → get an ITIN → secured or ITIN-friendly personal card to build a US file → Amex Business / Chase Ink after 6–12 months of history.
- Amex Global Transfer works only if the founder holds an Amex issued in their home country. Whether Amex operates there was not confirmed for Morocco.

### Gaps
- No Reddit first-hand ITIN–Amex approval reports surfaced. Searches returned only blogs; r/churning and r/tax are suggested for manual review.
- Capital on Tap US and Divvy (now BILL Spend & Expense) non-resident policies were not found in these searches.
- ITIN mechanics were not researched in detail. W-7 generally must be filed with a federal tax return or under an exception, via a Certifying Acceptance Agent. IRS pages were blocked (irs.gov egress denied), so this is unverified here.

## 4. Building business credit (D-U-N-S, Nav, Experian, net-30 vendors) as a foreign-owned LLC

### Takeaway
A foreign-owned LLC can start a business credit file with just the EIN: get a free D-U-N-S number, then open net-30 accounts that report to the bureaus (Uline, Quill, Grainger, Crown Office Supplies). Expect some vendors to ask for a personal guarantee or extra documents. No source confirmed vendor-specific non-resident acceptance.

### Cited Findings
- D-U-N-S is a free nine-digit identifier. D&B says there is no cost to request one. Paid expedite and "Credit Builder" upsells are unnecessary. Standard processing is about 30 days. — [United Capital Source 2026](https://www.unitedcapitalsource.com/blog/dnb-duns-number/); [Nav: got a D-U-N-S, now what](https://www.nav.com/blog/help-ive-got-a-d-u-n-s-number-now-what-32476/)
- Net-30 vendors that report to commercial bureaus include Uline, Quill, Grainger and Crown Office Supplies. Pay early to raise PAYDEX faster. — [Ramp: build business credit](https://ramp.com/blog/how-to-establish-build-business-credit); [Wayflyer 2026](https://wayflyer.com/blog/build-business-credit-low-personal-score)
- A foreign-owned LLC can build US business credit without an SSN, but some vendors may request more documentation or a personal guarantee, especially for new businesses. — [foundeck 2026](https://foundeck.com/blog/can-a-foreign-owned-llc-build-business-credit/); [foreignfounder](https://foreignfounder.com/articles/how-to-build-us-business-credit-non-resident); [allstatetaxresolution](https://www.allstatetaxresolution.com/post/us-business-credit-foreign-llc-owners)
- Suggested sequence (from a credit-builder firm, so partly a sales pitch): business credit via EIN + D-U-N-S → personal credit via ITIN → premium cards. — [James Baker CPA: credit building](https://jamesbakercpa.com/services/credit-building/)

### Inferences
- The LLC is about 1.5 years old with a US bank and Stripe history, which helps. Using a consistent legal name, address and phone number across D&B, Experian Business, Equifax Business, vendors and the bank matters, as does a non-registered-agent address.
- Free monitoring via Nav, and D&B's free basic profile view, are commonly used. Specific tiers were not verified here.

### Gaps
- No source confirmed that Uline, Quill, Grainger or Crown approve non-resident-owned LLCs specifically.
- Experian Business and Equifax Business self-registration processes for foreign owners were not found.

## 5. Payment processors: Stripe, PayPal, Shopify, Square (benefits, financing, requirements)

### Takeaway
Stripe Capital officially requires a US-located or incorporated business and a US home address for representatives, which may block a foreign owner (third-party sources disagree). PayPal Working Capital asks for owner SSNs. Shopify Balance officially requires an SSN or ITIN. Stripe Tax (0.5% per transaction on Basic) is usable without these restrictions.

### Cited Findings
- Stripe Capital: supports businesses located or incorporated in the US. Business representatives must provide a physical US home address. Requires 3+ months of processing on Stripe and at least $5,000 USD a year in volume. Third-party guides claim a foreign residential address is acceptable and that no SSN is required; this conflicts with the docs. — [Stripe Docs: Capital eligibility](https://docs.stripe.com/capital/eligibility); [businessanywhere](https://businessanywhere.io/stripe-paypal-non-resident-us-llcs-what-to-know/); [terms.law](https://terms.law/Invest-USA/bank-compliance/stripe-for-foreign-llc.html)
- Stripe sometimes asks for an SSN or ITIN, and an ITIN works as a workaround. — [LLC Starters](https://llcstarters.com/non-residents/bank-account/); [zenind](https://www.zenind.com/help/post/how-to-open-a-stripe-account-for-a-us-llc-as-a-non-resident-founder)
- Stripe Tax pricing (third-party, 2026):
  - Basic no-code: 0.5% of volume in jurisdictions where you're registered.
  - API: $0.50 per transaction call and $0.05 per calculation call.
  - Tax Complete: from $90/month (Tier 1) and $430/month (Tier 2).
  - One source says the rate drops to 0.4% above $100k a month (unverified).
  - Sources: [dodopayments](https://dodopayments.com/blogs/stripe-tax-explained); [frontdeskreview](https://frontdeskreview.com/software/sales-tax-automation/stripe-tax/); [feetrace](https://feetrace.com/blog/stripe-tax-fees-for-saas-in-2026-complete-guide)
- PayPal Working Capital: needs a Business or Premier account for at least 90 days, $15,000+ in PayPal sales over 12 months ($20,000 for Premier), and no outstanding loan. PayPal asks for "Social Security numbers of your primary business owners", which won't be used for a credit check. No official ITIN or foreign-ID alternative is stated. — [PayPal Working Capital](https://www.paypal.com/us/webapps/mpp/paypal-working-capital); [Wise: PayPal SSN](https://wise.com/us/blog/paypal-ssn)
- Shopify Balance (official): a valid US SSN or ITIN is required, used for identity only (no credit impact). It also needs Shopify Payments active. — [Shopify Help: Balance eligibility](https://help.shopify.com/en/manual/finance/shopify-balance/eligibility)
- Shopify Payments US: account representatives must provide an SSN or ITIN (official requirements page). A CPA blog claims a passport exception for non-US representatives with a foreign residential address (unverified). Shopify Community staff have said SSN/ITIN is mandatory (older threads). A 2026 guide says registered agent, virtual mailbox or CMRA addresses don't satisfy "operational presence". — [Shopify Help: US requirements](https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries/united-states/requirements); [James Baker CPA](https://jamesbakercpa.com/blog/shopify-sales-tax-nonresident-llc/); [Shopify Community thread](https://community.shopify.com/t/shopify-payments-for-foreign-owned-us-llc/306063/7); [Shopify Community: Balance without SSN/ITIN](https://community.shopify.com/c/payments-shipping-and/eligibility-for-shopify-balance-without-ssn-or-itin/m-p/2667507); [nvinc 2026](https://nvinc.com/shopify-payments-u-s-for-non-resident-sellers-a-step-by-step-guide/)

### Inferences
- An ITIN is the single biggest unlock across processors: Shopify Payments/Balance, PayPal Working Capital, smoother Stripe verification and bank cards.
- Stripe Capital offers appear in the dashboard by invitation. If none appear, the US home address requirement is a likely reason.

### Gaps
- Stripe Atlas perks list, Stripe Issuing for non-resident accounts, Stripe Climate, and negotiated Stripe fee discounts were not covered in the search results.
- Square's non-resident policy was not searched (budget). Square generally requires an SSN/ITIN for US sellers (from background knowledge, not verified here).
- Venmo Business and PayPal Business Loan (LoanBuilder) owner-ID requirements were not verified.

## 6. Financing (Shopify Capital, Stripe Capital, Amazon Lending, Etsy, Clearco, Wayflyer, Payability)

### Takeaway
Most e-commerce financiers key eligibility to the business being US-incorporated with a US bank account, which this LLC meets. None of the sources address owner residency, so it must be confirmed with each provider. Shopify Capital and Amazon Lending are invitation-only.

### Cited Findings
- Shopify Capital is invite-only. Capital Flex needs a US principal place of business and US bank account; one source says $50K+ trailing-12-month GMV. — [ask-luca: Shopify Capital 2026](https://ask-luca.com/blogs/shopify-capital); [credilinq: Shopify Capital alternatives](https://credilinq.ai/blogs/shopify-capital-alternatives-2026)
- Amazon Lending: pre-selected sellers only. Partners include SellersFi, Parafin, Lendistry and Marcus. Typically 12+ months of history. — [credilinq: Amazon lending](https://credilinq.ai/blogs/amazon-small-business-lending-loans)
- Wayflyer: about $10,000 average monthly revenue minimum if incorporated in the US (or CA, UK, AU, IE, BE); 11 eligible countries in total. — [ask-luca: Wayflyer](https://ask-luca.com/blogs/wayflyer-reviews-pricing); [onrampfunds](https://www.onrampfunds.com/resources/revenue-based-financing-providers-ecommerce)
- Clearco: US incorporation plus a US checking account. Revenue minimums conflict: $10k a month vs 12+ months above $100k a month. — [weareuncapped](https://www.weareuncapped.com/blog/clearco-alternatives); [ask-luca](https://ask-luca.com/blogs/best-alternative-lenders-for-ecommerce)
- Payability: US-focused, depends on the funding package, with no published sales minimum. — [credilinq: alternative lenders](https://credilinq.ai/blogs/alternative-lenders)
- Stripe Capital: see section 5 (US home address requirement in the docs). — [Stripe Docs](https://docs.stripe.com/capital/eligibility)

### Inferences
- Revenue-based financiers (Wayflyer, Clearco) underwrite the business and its bank/ads/store data, so they may be more workable for a foreign owner than PayPal or Shopify products tied to SSN/ITIN. This needs confirmation.

### Gaps
- Etsy financing and owner-residency rules for every lender were not found.

## 7. Reddit-style "secrets": avoiding freezes and closures

### Takeaway
Freezes and closures for foreign-owned LLCs most often come from mismatched details or using a registered agent or virtual address as the operating address. Defenses are consistency, real policies on the website, having a backup bank and processor, and exporting data promptly if closed.

### Cited Findings
- Top trigger: mismatches across the legal name, EIN, business address, website and bank. Inconsistency is called "the single most common reason foreign accounts stall." — [James Baker CPA: Stripe frozen 2026](https://jamesbakercpa.com/blog/stripe-account-frozen-what-to-do/)
- Stripe pays out cleanly when a US business bank account in the LLC's exact name is linked. A mismatched bank link is a frequent flag. Open the bank first, then Stripe. — [prodezk](https://www.prodezk.com/post/stripe-account-us-llc-abroad); [usllcglobal: Why Stripe rejects non-US LLCs](https://usllcglobal.com/guides/stripe-rejection-non-resident-llc)
- Publish ToS, Privacy and Refund policies. Use a domain 30+ days old. Keep a backup processor. — [usllcglobal](https://usllcglobal.com/guides/stripe-rejection-non-resident-llc)
- One vendor claims founders from certain countries (Pakistan, Bangladesh, Nigeria, Iran, Russia, Vietnam, Indonesia, Philippines) get extra scrutiny (single unverified source). Morocco was not listed. — [usllcglobal](https://usllcglobal.com/guides/stripe-rejection-non-resident-llc)
- After a Stripe closure, export transaction, dispute, payout and customer data immediately. Dashboard access reportedly lasts 60–90 days, but exports are restricted quickly. Notify your bank. — [Epitychia Consulting: 90-day recovery playbook](https://www.epitychiaconsulting.com/insights/stripe-account-closure-foreign-owned-llc-recovery/)
- Mercury has offboarded founders based on where they live (2024). — [TechCrunch](https://techcrunch.com/2024/07/23/mercury-bank-fintech-sanctions-ukraine-nigeria)

### Inferences
- A second US bank (Relay or Lili) plus Wise is cheap insurance against a single-provider closure.
- Keep personal transfers to Morocco clearly labeled as owner draws/distributions.

### Gaps
- No actual Reddit threads were retrieved (search returned none; direct fetch blocked). The report writer should present these as consultant/blog tips, not Reddit consensus.
