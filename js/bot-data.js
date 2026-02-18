/**
 * RC Investment Properties - Marketing Bot Data
 * All seed data converted from Python/JSON seeds into JS objects.
 */

const BOT_DATA = {

  // ── Firm Facts (42 items across 5 categories) ──────────────────────────────
  firmFacts: {
    track_record: [
      { key: "meta_street_value_increase", value: "43.4%", label: "Meta Street Value Increase" },
      { key: "meta_street_hold_period", value: "18 months", label: "Meta Street Hold Period" },
      { key: "meta_street_acquisition", value: "$1.325M", label: "Meta Street Acquisition Price" },
      { key: "meta_street_sale", value: "$1.9M", label: "Meta Street Sale Price" },
      { key: "avondale_annualized_return", value: "19.7%", label: "Avondale Annualized Return" },
      { key: "marshall_target_irr", value: "~40%", label: "Marshall Target IRR" },
      { key: "moritz_year1_return", value: "9.3%", label: "Moritz Year 1 Return" }
    ],
    portfolio: [
      { key: "total_units", value: "143", label: "Total Units" },
      { key: "total_properties", value: "5", label: "Total Properties" },
      { key: "houston_units", value: "128+", label: "Houston Units" },
      { key: "houston_properties", value: "4", label: "Houston Properties" },
      { key: "phoenix_units", value: "15", label: "Phoenix Units" },
      { key: "phoenix_properties", value: "1", label: "Phoenix Properties" },
      { key: "total_transaction_volume", value: "$20M+", label: "Total Transaction Volume" },
      { key: "property_1", value: "101 Avondale St, Houston TX", label: "Property 1" },
      { key: "property_2", value: "414 Marshall St, Houston TX", label: "Property 2" },
      { key: "property_3", value: "1218 Jackson Blvd, Houston TX", label: "Property 3" },
      { key: "property_4", value: "1541 Moritz Dr, Houston TX (Oaks of Moritz)", label: "Property 4" },
      { key: "property_5", value: "3406 N 38th St, Phoenix AZ (Arcadia Lite)", label: "Property 5" }
    ],
    thesis: [
      { key: "target_irr", value: "18-25%", label: "Target IRR" },
      { key: "target_equity_multiple", value: "2.0x+", label: "Target Equity Multiple" },
      { key: "annual_cash_return", value: "7-9%", label: "Annual Cash Return" },
      { key: "hold_period", value: "5-7 years", label: "Hold Period" },
      { key: "deal_size_range", value: "$5-20M", label: "Deal Size Range" },
      { key: "rental_range", value: "$1,100-$1,450/month", label: "Rental Range" },
      { key: "focus", value: "Workforce housing in Sunbelt markets", label: "Investment Focus" },
      { key: "strategy", value: "Acquire, reposition, and manage multifamily properties", label: "Strategy" },
      { key: "leverage_approach", value: "Conservative, low leverage, fixed-rate debt", label: "Leverage Approach" }
    ],
    advantage: [
      { key: "co_investment", value: "5-10% personal capital at risk alongside investors", label: "Co-Investment" },
      { key: "deal_sourcing", value: "Proprietary broker relationships, off-market deals", label: "Deal Sourcing" },
      { key: "market_knowledge", value: "Deep Houston/Phoenix submarket expertise", label: "Market Knowledge" },
      { key: "operational_excellence", value: "Proven playbook for workforce housing repositioning", label: "Operational Excellence" },
      { key: "conservative_approach", value: "Low leverage, stress-tested assumptions", label: "Conservative Approach" },
      { key: "boutique_execution", value: "Rapid decision-making, hands-on management", label: "Boutique Execution" }
    ],
    terms: [
      { key: "minimum_investment", value: "$100,000", label: "Minimum Investment" },
      { key: "target_equity_raise", value: "$1.5M-$2.5M per deal", label: "Target Equity Raise" },
      { key: "acquisition_fee", value: "2.0% of purchase price", label: "Acquisition Fee" },
      { key: "asset_management_fee", value: "2.0% of EGI annually", label: "Asset Management Fee" },
      { key: "promote", value: "15-20% (deal dependent)", label: "Promote" },
      { key: "disposition_fee", value: "1.0% of sale price", label: "Disposition Fee" },
      { key: "refinance_fee", value: "0.5% of loan amount", label: "Refinance Fee" },
      { key: "distributions", value: "Quarterly", label: "Distributions" }
    ]
  },

  // ── Market Data (14 data points) ───────────────────────────────────────────
  marketData: {
    houston: {
      "Q4 2025": [
        { metric: "Occupancy", value: "90.4%", source: "CoStar" },
        { metric: "Annual Absorption", value: "26,510 units", source: "CoStar" },
        { metric: "Supply Pipeline", value: "9,087 units under construction", source: "CoStar" },
        { metric: "Rent Growth (Projected)", value: "2.1% annualized", source: "CoStar" },
        { metric: "Avg Effective Rent", value: "$1,277/month", source: "CoStar" }
      ],
      "2024": [
        { metric: "Population Growth", value: "~200,000 residents added", source: "U.S. Census Bureau" },
        { metric: "Net Migration Share", value: "75% of growth from migration", source: "U.S. Census Bureau" },
        { metric: "Net Migration Rank", value: "#1 net migration among U.S. metros", source: "U.S. Census Bureau" },
        { metric: "Jobs Added", value: "57,800 new jobs", source: "BLS" },
        { metric: "Avg Effective Rent", value: "$1,277/month", source: "CoStar" },
        { metric: "Metro Occupancy", value: "89.0%", source: "CoStar" },
        { metric: "Occupancy Rank", value: "#1 among Texas markets", source: "CoStar" }
      ]
    },
    phoenix: {
      "2025": [
        { metric: "Portfolio Units", value: "15 units", source: "Internal" },
        { metric: "Property", value: "Arcadia Lite - 3406 N 38th St", source: "Internal" }
      ]
    }
  },

  // ── Data Sources (6 items) ─────────────────────────────────────────────────
  dataSources: [
    { name: "BLS Employment Release", url: "https://www.bls.gov/news.release/empsit.nr0.htm", frequency: "Monthly", notes: "National and metro-level employment data" },
    { name: "CoStar Houston Multifamily Report", url: null, frequency: "Quarterly", notes: "Subscription-based. Key metrics: occupancy, absorption, rent growth, supply pipeline" },
    { name: "U.S. Census Bureau Population Estimates", url: "https://www.census.gov/programs-surveys/popest.html", frequency: "Annual", notes: "Metro-level population and migration estimates" },
    { name: "Texas Workforce Commission", url: "https://www.twc.texas.gov", frequency: "Monthly", notes: "Texas-specific employment and labor market data" },
    { name: "Greater Houston Partnership", url: "https://www.houston.org", frequency: "Monthly", notes: "Houston economic development updates and reports" },
    { name: "Federal Reserve Interest Rate Decisions", url: "https://www.federalreserve.gov", frequency: "8x per year", notes: "FOMC meetings and rate decisions impacting cap rates and financing" }
  ],

  // ── Brand Rules (25 items across 4 types) ──────────────────────────────────
  brandRules: {
    terminology: [
      { rule: "Use 'workforce housing' instead of 'affordable housing'", example: "Houston's workforce housing segment continues to show resilience" },
      { rule: "Use 'value creation' instead of 'flipping' or 'fixing up'", example: "Our value creation strategy focuses on operational improvements" },
      { rule: "Use 'Sunbelt thesis' when discussing geographic strategy", example: "Our Sunbelt thesis targets markets with favorable population and employment trends" },
      { rule: "Use 'sub-institutional advantage' for market positioning", example: "The sub-institutional advantage allows us to source deals institutions overlook" },
      { rule: "Use 'durable cash flow' for income reliability", example: "Durable cash flow from workforce housing reduces exit reliance" },
      { rule: "Use 'repositioning' for property improvement strategy", example: "Our repositioning playbook targets interior upgrades and operational improvements" },
      { rule: "Use 'basis' when discussing acquisition price relative to replacement cost", example: "Our low basis position provides meaningful downside protection" }
    ],
    tone: [
      { rule: "Professional, analytical, and data-driven", example: "Houston occupancy reached 90.4% in Q4 2025, supported by 26,510 units of absorption" },
      { rule: "Confident but never aggressive or boastful", example: "The fundamentals support our thesis \u2014 not 'We're the best in the business'" },
      { rule: "Educational rather than promotional", example: "Share market insights, not sales pitches" },
      { rule: "Focus on downside protection and discipline", example: "Our conservative leverage approach limits downside exposure" }
    ],
    compliance: [
      { rule: "Never guarantee returns or imply guaranteed outcomes", example: "Target IRR of 18-25% (not 'guaranteed 18-25% returns')" },
      { rule: "Include past performance disclaimer when referencing track record", example: "Past performance is not indicative of future results." },
      { rule: "Market analysis should note 'For informational purposes only'", example: "For informational purposes only. This does not constitute investment advice." },
      { rule: "No specific investment solicitation in public social media content", example: "" },
      { rule: "No discussion of specific fund terms or current offerings on social media", example: "" },
      { rule: "Do not disclose investor names or specific LP information", example: "" }
    ],
    avoid: [
      { rule: "Do not use 'affordable housing'" },
      { rule: "Do not use 'flipping' or 'flip'" },
      { rule: "Do not use 'guaranteed' or 'guaranteed returns'" },
      { rule: "Do not use 'risk-free' or 'risk free'" },
      { rule: "Do not use 'get rich'" },
      { rule: "Do not use 'wealth building'" },
      { rule: "Do not use 'passive income' (use 'cash flow' or 'distributions')" },
      { rule: "Do not use 'deal of a lifetime' or hyperbolic language" }
    ]
  },

  // ── Forbidden terms for compliance checker ─────────────────────────────────
  forbiddenTerms: [
    "affordable housing", "flipping", "flip", "guaranteed", "guaranteed returns",
    "risk-free", "risk free", "get rich", "wealth building", "passive income",
    "deal of a lifetime"
  ],

  // ── Calendar Entries (12 items) ────────────────────────────────────────────
  seedCalendar: [
    { id: "cal-1", date: "2026-01-15", type: "blog_post", topic: "Houston Q4 2025 Market Update", principal: "Michael Rosen", notes: "Use latest Colliers/CoStar Q4 data. Highlight occupancy recovery and supply pipeline contraction.", status: "published" },
    { id: "cal-2", date: "2026-01-22", type: "linkedin_post", topic: "Workforce Housing Demand Drivers", principal: "Michael Rosen", notes: "Short-form post on why workforce housing outperforms luxury in occupancy.", status: "published" },
    { id: "cal-3", date: "2026-02-01", type: "blog_post", topic: "RC Portfolio Performance: 2025 in Review", principal: "Bradley Couch", notes: "Summarize portfolio-level metrics, highlight Moritz acquisition and Avondale performance.", status: "published" },
    { id: "cal-4", date: "2026-02-10", type: "linkedin_post", topic: "Sub-Institutional Advantage Explained", principal: "Michael Rosen", notes: "Define the sub-institutional space and why it creates opportunity.", status: "published" },
    { id: "cal-5", date: "2026-02-17", type: "linkedin_post", topic: "Houston Population & Migration Trends", principal: "Michael Rosen", notes: "Census data: Houston #1 in net migration. Tie to rental demand.", status: "approved" },
    { id: "cal-6", date: "2026-02-24", type: "blog_post", topic: "Conservative Leverage in a Rising Rate Environment", principal: "Bradley Couch", notes: "Discuss our approach to debt: fixed-rate preference, low LTV, stress-testing.", status: "queued" },
    { id: "cal-7", date: "2026-03-03", type: "linkedin_post", topic: "Off-Market Deal Sourcing Strategy", principal: "Michael Rosen", notes: "How proprietary broker relationships surface deals before broad marketing.", status: "queued" },
    { id: "cal-8", date: "2026-03-10", type: "blog_post", topic: "Phoenix Multifamily: Arcadia Lite Submarket Deep Dive", principal: "Michael Rosen", notes: "Highlight Phoenix entry via 1031, Arcadia Lite fundamentals, expansion plans.", status: "draft" },
    { id: "cal-9", date: "2026-03-17", type: "linkedin_post", topic: "Co-Investment: Aligned Interests", principal: "Bradley Couch", notes: "GP co-invest of 5-10%. Why alignment matters for LP returns.", status: "draft" },
    { id: "cal-10", date: "2026-03-24", type: "blog_post", topic: "Houston Submarket Analysis: Inner Loop vs. Suburbs", principal: "Michael Rosen", notes: "Compare workforce housing dynamics across Houston submarkets.", status: "draft" },
    { id: "cal-11", date: "2026-04-01", type: "market_report", topic: "Q1 2026 Houston Multifamily Market Report", principal: "Michael Rosen", notes: "Quarterly deep-dive using fresh CoStar data for Q1 2026.", status: "draft" },
    { id: "cal-12", date: "2026-04-14", type: "linkedin_post", topic: "Why Cash Flow Beats Speculation", principal: "Bradley Couch", notes: "Durable cash flow vs. cap rate compression plays. Educational tone.", status: "draft" }
  ],

  // ── Content Items (11 items with real body text) ───────────────────────────
  seedContent: [
    {
      id: "content-1",
      title: "Houston Q4 2025: Strong Absorption and Slowing Supply Signal Market Inflection",
      type: "blog_post",
      platform: "website",
      status: "published",
      principal: "Michael Rosen",
      created: "2026-01-12",
      published: "2026-01-15",
      body: "Houston's multifamily market closed 2025 on solid footing, with Q4 data confirming what we've observed on the ground: demand is absorbing supply, occupancy is recovering, and the construction pipeline is finally contracting.\n\nAccording to Colliers' Q4 2025 Houston Multifamily Report, the market absorbed 26,510 units during 2025, representing a 32.3% increase over 2024 and the highest annual total since 2021. This demand surge, combined with a meaningful pullback in new construction, is creating a more favorable supply-demand balance.\n\nKey metrics:\n- Overall occupancy: 90.4% (up 200 bps YoY)\n- Under construction: 9,087 units (down 34% YoY)\n- Average effective rent: $1,258/month\n- Class B/C occupancy: 92%+ (outperforming Class A by 600+ bps)\n\nFor workforce housing investors, the data reinforces our thesis: demand is durable, supply is contracting, and existing assets in established submarkets are well-positioned for rent growth over the next 24-36 months.\n\nPast performance is not indicative of future results. For informational purposes only.",
      metrics: { views: 1240, shares: 45, engagement: "3.6%" }
    },
    {
      id: "content-2",
      title: "Workforce Housing Demand Drivers: Why Class B/C Outperforms",
      type: "linkedin_post",
      platform: "linkedin",
      status: "published",
      principal: "Michael Rosen",
      created: "2026-01-20",
      published: "2026-01-22",
      body: "Houston's workforce housing fundamentals continue to outperform the broader market.\n\nQ4 2025 data shows Class B and C properties maintaining 92%+ occupancy \u2014 600+ basis points above Class A. Why?\n\n1. Essential workers need housing near employment centers\n2. New construction targets luxury renters, not workforce\n3. Building costs make new workforce supply economically infeasible\n4. Domestic migration adds 200,000+ residents annually to Houston\n\nThe structural supply-demand imbalance in workforce housing isn't a cycle \u2014 it's a durable trend.\n\n#MultifamilyInvesting #WorkforceHousing #HoustonRealEstate\n\nFor informational purposes only. Past performance is not indicative of future results.",
      metrics: { views: 3200, shares: 67, engagement: "4.2%" }
    },
    {
      id: "content-3",
      title: "RC Portfolio Performance: 2025 in Review",
      type: "blog_post",
      platform: "website",
      status: "published",
      principal: "Bradley Couch",
      created: "2026-01-28",
      published: "2026-02-01",
      body: "2025 was a transformative year for RC Investment Properties. We expanded our portfolio to 143 units across 5 properties in Houston and Phoenix while maintaining our commitment to conservative underwriting and durable cash flow.\n\nPortfolio Highlights:\n- Avondale (19 units): 19.7% annualized return, strong occupancy throughout 2025\n- Marshall (27 units): Off-market acquisition with 50% seller financing, targeting ~40% IRR\n- Jackson (26 units): Loan distress acquisition, Year 1 cash-on-cash trending 7%+\n- Moritz (56 units): December 2025 acquisition, 9.3% Year 1 return projection\n- Arcadia Lite (15 units): Capital preservation in premium Phoenix submarket\n\nTotal transaction volume exceeded $20M, and every deal was sourced through proprietary relationships. Our principals co-invested 5-10% alongside LPs in each transaction.\n\nLooking ahead to 2026, we see continued opportunity in Houston's workforce housing segment as supply contracts and occupancy recovers.\n\nPast performance is not indicative of future results.",
      metrics: { views: 890, shares: 32, engagement: "3.1%" }
    },
    {
      id: "content-4",
      title: "The Sub-Institutional Advantage: Why $5-20M Deals Offer Superior Returns",
      type: "linkedin_post",
      platform: "linkedin",
      status: "published",
      principal: "Michael Rosen",
      created: "2026-02-07",
      published: "2026-02-10",
      body: "There's a sweet spot in multifamily investing that most investors overlook.\n\nDeals between $5M-$20M are:\n- Too small for institutional buyers (they can't deploy enough capital)\n- Too large for individual investors (requires operational capability)\n- Perfectly sized for boutique operators with proprietary sourcing\n\nThis is the sub-institutional advantage.\n\nAt RC Investment Properties, we've built our entire thesis around this gap. Less competition means better pricing. Better pricing means stronger basis protection. Stronger basis means lower risk and higher returns.\n\nOur portfolio: 143 units, $20M+ in transactions, all sourced through direct relationships.\n\n#RealEstateInvesting #MultifamilyHousing #SubInstitutional\n\nFor informational purposes only.",
      metrics: { views: 4100, shares: 89, engagement: "5.1%" }
    },
    {
      id: "content-5",
      title: "Houston Multifamily: Why Workforce Housing Remains Resilient in 2025",
      type: "blog_post",
      platform: "website",
      status: "published",
      principal: "Michael Rosen",
      created: "2025-01-10",
      published: "2025-01-15",
      body: "Despite broader economic uncertainty, Houston's workforce housing segment continues to demonstrate strong fundamentals driven by sustained population growth, economic diversification, and structural supply constraints.\n\nHouston's appeal rests on durable structural factors: economic diversification across healthcare, aerospace, technology, and manufacturing; population growth of 100,000+ residents per year; and a business-friendly Texas environment.\n\nWorkforce housing occupies a favorable position serving households at 60-120% of area median income. New construction targets luxury renters, leaving the workforce segment underserved. Demand from essential workers is inherently sticky.\n\nFor patient investors focused on risk-adjusted returns, Houston's workforce housing offers durability, cash flow, and long-term appreciation potential.\n\nFor informational purposes only. Past performance is not indicative of future results.",
      metrics: { views: 2100, shares: 56, engagement: "3.8%" }
    },
    {
      id: "content-6",
      title: "Houston #1 in Net Migration: What It Means for Rental Demand",
      type: "linkedin_post",
      platform: "linkedin",
      status: "published",
      principal: "Michael Rosen",
      created: "2026-02-14",
      published: "2026-02-15",
      body: "The latest Census data confirms Houston as #1 in net migration among U.S. metros.\n\n200,000+ new residents in 2024, with 75% driven by domestic and international migration. These aren't just numbers \u2014 they're households that need housing.\n\nFor workforce housing investors, sustained in-migration means:\n- Growing demand for rental units at $1,100-$1,450/month\n- Reduced vacancy risk in established submarkets\n- Support for moderate rent growth (2-3% annually)\n\nPopulation fundamentals don't lie. Houston's growth trajectory reinforces our Sunbelt thesis.\n\n#HoustonGrowth #MultifamilyInvesting #PopulationTrends\n\nFor informational purposes only.",
      metrics: { views: 2800, shares: 71, engagement: "4.5%" }
    },
    {
      id: "content-7",
      title: "Houston Population & Migration Trends",
      type: "linkedin_post",
      platform: "linkedin",
      status: "approved",
      principal: "Michael Rosen",
      created: "2026-02-15",
      published: null,
      body: "Houston's population story keeps getting stronger.\n\nNew Census estimates show the metro added ~200,000 residents in 2024, ranking #1 nationally for net migration. 75% of that growth came from people moving in, not natural increase.\n\nWhat's driving it?\n- No state income tax\n- Job growth across energy, healthcare, tech, and logistics\n- Cost of living well below coastal metros\n- Quality of life improvements across the metro\n\nFor multifamily investors, this translates directly to rental demand. More households = more renters = stronger occupancy and rent growth potential.\n\nOur Sunbelt thesis is built on these structural tailwinds.\n\n#Houston #Migration #MultifamilyInvesting\n\nFor informational purposes only.",
      metrics: null
    },
    {
      id: "content-8",
      title: "Conservative Leverage in a Rising Rate Environment",
      type: "blog_post",
      platform: "website",
      status: "queued",
      principal: "Bradley Couch",
      created: "2026-02-20",
      published: null,
      body: "In today's interest rate environment, leverage discipline isn't just prudent \u2014 it's essential.\n\nAt RC Investment Properties, our approach to debt has always been conservative:\n\n1. Fixed-rate preference: We seek fixed-rate financing to eliminate interest rate risk during our hold period\n2. Low LTV targets: Our acquisitions typically target 65-70% LTV, well below market norms\n3. Stress-tested assumptions: Every deal is underwritten to withstand 200+ bps of rate increases\n4. Cash flow coverage: We require minimum 1.25x debt service coverage at acquisition\n\nWhy does this matter?\n\nMany operators who leveraged aggressively at low rates in 2021-2022 are now facing refinancing challenges. Properties with 80%+ LTV and floating-rate debt are particularly vulnerable.\n\nOur conservative approach means:\n- No forced sales due to loan maturities\n- Ability to hold through market cycles\n- Capacity to acquire distressed assets from overleveraged sellers\n\nDiscipline in leverage creates optionality. Optionality creates returns.\n\nFor informational purposes only. Past performance is not indicative of future results.",
      metrics: null
    },
    {
      id: "content-9",
      title: "Off-Market Deal Sourcing: Our Competitive Edge",
      type: "linkedin_post",
      platform: "linkedin",
      status: "queued",
      principal: "Michael Rosen",
      created: "2026-02-22",
      published: null,
      body: "Every property in our portfolio was sourced through proprietary relationships. Zero came from marketed deal processes.\n\nHow we find deals:\n- Direct broker relationships cultivated over years\n- Property manager network referrals\n- Direct-to-seller outreach in target submarkets\n- Loan distress monitoring and lender relationships\n\nWhy off-market matters:\n- Less competition = better pricing\n- More diligence time = better decisions\n- Relationship-based = repeat opportunities\n\n5 properties. 143 units. $20M+ in transactions. All sourced directly.\n\n#DealSourcing #MultifamilyInvesting #OffMarket\n\nFor informational purposes only.",
      metrics: null
    },
    {
      id: "content-10",
      title: "Phoenix Multifamily: Arcadia Lite Submarket Deep Dive",
      type: "blog_post",
      platform: "website",
      status: "draft",
      principal: "Michael Rosen",
      created: "2026-02-25",
      published: null,
      body: "Phoenix represents our second Sunbelt market, entered via 1031 exchange from our Meta Street exit in Houston.\n\nArcadia Lite is one of Phoenix's most desirable submarkets, characterized by:\n- Proximity to Scottsdale and Biltmore corridor\n- Strong renter demographics (young professionals, healthcare workers)\n- Limited new supply in the immediate area\n- Premium positioning with 15 units at 3406 N 38th St\n\nOur Phoenix strategy focuses on capital preservation in a high-quality submarket while we evaluate expansion opportunities across the metro.\n\nDraft - needs additional market data and competitive analysis before publication.",
      metrics: null
    },
    {
      id: "content-11",
      title: "Co-Investment: Why We Put Our Own Capital at Risk",
      type: "linkedin_post",
      platform: "linkedin",
      status: "draft",
      principal: "Bradley Couch",
      created: "2026-02-26",
      published: null,
      body: "At RC Investment Properties, our principals invest 5-10% of total equity in every deal. Here's why:\n\nAlignment isn't a talking point \u2014 it's a check we write.\n\nWhen GPs have meaningful capital at risk:\n- Underwriting is more conservative\n- Asset management is more hands-on\n- Exit timing prioritizes returns over fees\n\nOur investors know we succeed only when they succeed. That's the way it should be.\n\nDraft - review tone and add specific examples.",
      metrics: null
    }
  ],

  // ── Generate Template Library ──────────────────────────────────────────────
  templates: {
    blog_post: {
      openings: [
        "Houston's multifamily market continues to demonstrate {trend} as we analyze the latest data from {source}.",
        "The latest market data paints a compelling picture for workforce housing investors in {market}.",
        "As {market}'s multifamily fundamentals strengthen, disciplined investors are finding opportunity in {segment}.",
        "New data from {source} confirms what we've observed on the ground: {market}'s workforce housing segment is {trend}."
      ],
      bodies: [
        "\n\nKey Market Metrics:\n- Occupancy: {occupancy}\n- Annual Absorption: {absorption}\n- Supply Pipeline: {supply}\n- Average Effective Rent: {rent}\n\nThese numbers tell a story of {narrative}. For investors focused on workforce housing, the implications are clear: {implication}.\n\n",
        "\n\nOur portfolio of {units} units across {properties} properties continues to perform well, with {highlight_property} delivering {highlight_metric} returns.\n\nThe thesis remains straightforward: acquire well-located workforce housing at a meaningful discount to replacement cost, implement our operational playbook, and generate durable cash flow for our investors.\n\n",
        "\n\nThe sub-institutional advantage continues to create opportunity. Deals between $5-20M face limited institutional competition, allowing operators like us to source proprietary opportunities with favorable pricing.\n\nOur approach:\n1. Conservative leverage with fixed-rate debt preference\n2. GP co-investment of 5-10% alongside LPs\n3. Hands-on asset management and repositioning\n4. Focus on durable cash flow over speculative appreciation\n\n"
      ],
      closings: [
        "\nFor disciplined investors focused on risk-adjusted returns, {market}'s workforce housing segment offers a compelling combination of durability, cash flow, and long-term appreciation potential.\n\nFor informational purposes only. Past performance is not indicative of future results.",
        "\nThe fundamentals support continued conviction in our Sunbelt thesis. We remain actively acquiring in {market} and look forward to sharing more insights as the data evolves.\n\nPast performance is not indicative of future results.",
        "\nAs always, our focus remains on downside protection, durable cash flow, and disciplined execution. The data confirms we're in the right markets with the right strategy.\n\nFor informational purposes only. This does not constitute investment advice."
      ]
    },
    linkedin_post: {
      openings: [
        "Houston just posted another strong quarter for multifamily fundamentals.",
        "The latest {source} data is in, and the numbers reinforce our workforce housing thesis.",
        "Here's what's happening in {market}'s multifamily market right now:",
        "Workforce housing demand remains resilient. Here's why:"
      ],
      bodies: [
        "\n\nThe numbers:\n- {occupancy} occupancy ({occupancy_trend})\n- {absorption} units absorbed\n- {supply} units under construction ({supply_trend})\n- {rent} average effective rent\n\n",
        "\n\nAt RC Investment Properties:\n- {units} units across {properties} properties\n- {volume} in transaction volume\n- GP co-invest of 5-10% in every deal\n- 100% proprietary sourcing\n\n",
        "\n\nWhy we're bullish on workforce housing:\n1. Class B/C occupancy above 92%\n2. New supply declining 34% YoY\n3. Migration-driven demand adding 200K+ residents annually\n4. Acquisition basis well below replacement cost\n\n"
      ],
      closings: [
        "\n#MultifamilyInvesting #WorkforceHousing #HoustonRealEstate\n\nFor informational purposes only.",
        "\nThe structural tailwinds remain intact.\n\n#RealEstateInvesting #SunbeltMarkets #MultifamilyHousing\n\nFor informational purposes only. Past performance is not indicative of future results.",
        "\n#Houston #MultifamilyInvesting #WorkforceHousing\n\nFor informational purposes only."
      ]
    },
    market_report: {
      openings: [
        "This quarterly report examines {market}'s multifamily market performance using the latest available data from {source}.",
        "{market} Multifamily Market Report: {period}\n\nExecutive Summary: {market}'s multifamily fundamentals showed {trend} during {period}."
      ],
      bodies: [
        "\n\nMarket Overview:\n\nOccupancy: {occupancy}\nThe market {occupancy_narrative}.\n\nAbsorption: {absorption}\n{absorption_narrative}.\n\nSupply: {supply}\nThe construction pipeline {supply_narrative}.\n\nRent Trends: {rent}\n{rent_narrative}.\n\nInvestment Activity:\nTransaction volume {volume_trend}. Average price per unit reached {price_per_unit}. Cap rates averaged {cap_rate}.\n\n",
        "\n\nSubmarket Performance:\n\nHouston's workforce housing submarkets showed varied performance:\n- Class B: 92.1% occupancy, $1,249/month average rent\n- Class C: 92.5% occupancy, $982/month average rent\n\nBoth segments outperformed Class A (86.1% occupancy) by more than 600 basis points, reinforcing the structural demand advantage in workforce housing.\n\n"
      ],
      closings: [
        "\n\nOutlook:\nWe expect {market}'s multifamily fundamentals to continue strengthening as the market absorbs remaining lease-up inventory and the construction pipeline contracts further.\n\nFor informational purposes only. This report does not constitute investment advice. Past performance is not indicative of future results.",
        "\n\nConclusion:\nThe data supports a constructive outlook for workforce housing in {market}. Disciplined investors with operational capability are well-positioned to capitalize on improving fundamentals.\n\nFor informational purposes only."
      ]
    }
  },

  // ── Template data values for interpolation ─────────────────────────────────
  templateValues: {
    market: ["Houston", "Houston, TX"],
    source: ["CoStar", "Colliers", "U.S. Census Bureau", "BLS"],
    segment: ["workforce housing", "Class B/C multifamily", "sub-institutional multifamily"],
    trend: ["strengthening fundamentals", "improving occupancy", "supply-demand rebalancing", "continued resilience"],
    occupancy: ["90.4%", "92.1% (Class B)", "92.5% (Class C)"],
    occupancy_trend: ["up 200 bps YoY", "highest since 2021", "above long-term average"],
    absorption: ["26,510", "record annual absorption"],
    supply: ["9,087", "declining construction pipeline"],
    supply_trend: ["down 34% YoY", "lowest since 2020"],
    rent: ["$1,277/month", "$1,258/month", "$1,249/month (Class B)"],
    units: ["143"],
    properties: ["5"],
    volume: ["$20M+"],
    narrative: ["market recovery and supply discipline", "strengthening demand against contracting supply"],
    implication: ["existing assets in established submarkets are well-positioned for rent growth", "the supply-demand imbalance favors workforce housing owners"],
    highlight_property: ["Avondale", "Marshall", "Moritz"],
    highlight_metric: ["19.7% annualized", "~40% target IRR", "9.3% Year 1"],
    period: ["Q4 2025", "Q1 2026"],
    occupancy_narrative: ["recovered 200 basis points year-over-year to 90.4%"],
    absorption_narrative: ["Annual absorption of 26,510 units represented a 32.3% increase over 2024"],
    supply_narrative: ["contracted 34% year-over-year to 9,087 units"],
    rent_narrative: ["Average effective rents held steady around $1,258-$1,277/month"],
    volume_trend: ["showed continued recovery"],
    price_per_unit: ["$173,079 (all-time high)"],
    cap_rate: ["5.9%"]
  }
};
