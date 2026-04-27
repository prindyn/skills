# Financial Foundation & Position Building

Use this file before the user views a property or lists a home. The numbers established here become the reference point for every later decision — the opening offer, the concession roadmap, when to walk away, whether to accept a repair credit, whether a deal is worth fighting for.

If the user is already mid-negotiation and has skipped this phase, back them up to it gently. A negotiator without a walk-away number is negotiating against themselves.

## Core outputs by situation

| Situation | The number you must produce |
|---|---|
| Buying a primary residence | **Hard Stop price** — max purchase price that keeps monthly all-in cost at or below the user's comfort threshold after accounting for known repairs |
| Selling | **Minimum acceptable sale price** — the price that yields the net proceeds target after commission, closing costs, likely repair credits, and payoff |
| Investing (rental) | **Maximum offer price** for target cash-on-cash return |
| Investing (flip) | **Maximum allowable offer** using 70% Rule = (0.70 × ARV) − repair costs |
| Deciding when to act | **Cost of waiting** — the monthly dollar cost of delaying 3/6/12 months |

## 1. Hard Stop calculation (buyer)

Work backward from comfortable monthly payment. The inputs you need:

- Comfortable total monthly housing cost (PITI + HOA, not just P&I)
- Current 30-year fixed rate for their credit profile
- Property taxes (local rate × purchase price, usually)
- Homeowners insurance estimate
- HOA dues if applicable
- Down payment available
- **Known repair/improvement list** with contractor estimates (this is the most commonly omitted input)
- Other monthly debt obligations (for DTI check)

Calculation steps:

1. Subtract estimated taxes, insurance, and HOA from the comfortable monthly total → that leaves the P&I budget.
2. Use a standard amortization formula to back out the maximum loan amount from the P&I budget at the current rate.
3. Add the down payment → that's the comfortable purchase price *before* repairs.
4. Convert the known repair list into monthly terms: amortize the repair cost over the loan term (or over the user's planned hold period if shorter) and subtract from the P&I budget. Recompute the max purchase price. That's the **Hard Stop**.
5. Show consequences of exceeding it by $5k, $10k, $15k — in monthly dollars and in total interest over the loan term. Concrete numbers keep the user disciplined when emotions spike.

### Why repairs belong in the Hard Stop

Many buyers treat inspection-phase repair estimates as separate from purchase price. They aren't. A $12,000 roof replacement is $12,000 of capital that has to come from somewhere, and if it's financed, it's ~$70–$100 of monthly payment for 30 years. Fold it in up front so the user isn't blindsided later.

## 2. Seller's net proceeds

Inputs:

- Outstanding mortgage balance (payoff quote if available — balance + per-diem interest)
- Expected agent commission (typically 5–6% total, often split)
- Closing costs (title, transfer tax, prorated taxes, attorney, recording — 1–3% is typical)
- Likely buyer-requested repair credits (estimate from property condition)
- Target net proceeds for next move (down payment on next home, investment, retirement)

Produce:

1. **Net at asking price** — asking − commission − closing costs − expected credits − payoff.
2. **Minimum acceptable sale price** — work backward from net proceeds target.
3. **Negotiation bandwidth** — the dollar range between asking and minimum acceptable. This is the room the seller actually has to move.
4. **Sensitivity table** — net impact of each $5,000 reduction. Useful during counteroffer phase to make concessions feel concrete.

## 3. Investment ROI — rental

Quick filters before deep analysis:

- **1% Rule**: monthly rent ≥ 1% of purchase price. Passing means the property is worth underwriting in detail; failing doesn't automatically kill it (especially in high-appreciation markets) but raises the bar.
- **Cap rate** = annual net operating income ÷ purchase price. Compare to local cap rate norms and to the user's required return given financing.
- **Cash-on-cash return** = annual pre-tax cash flow ÷ total cash invested. This is the metric most retail investors actually care about.

Produce a price-sensitivity table: show cash-on-cash at asking, −$10k, −$20k, −$30k. The price at which the user's target return is met is the **Maximum Offer Price**.

Annual expenses the user is likely under-estimating: vacancy (5–8%), maintenance (5–10% of rent or 1% of property value annually), capex reserves, property management (8–10% if used), insurance uplift for rentals, and higher mortgage rate for non-owner-occupied.

## 4. Investment ROI — flip (70% Rule)

**Maximum Allowable Offer = (0.70 × ARV) − repair costs**

- **ARV** (after-repair value) should come from truly comparable sales — same size, same layout, same post-renovation condition, same neighborhood, last 90 days. Be skeptical of the user's ARV; it's the most commonly inflated input.
- Repairs should be estimated with a 20% buffer; run a sensitivity case at +20% repairs to see if the deal survives.
- The 30% spread (100% − 70%) covers: holding costs (taxes, insurance, utilities, loan interest for 3–9 months), selling costs (agent + closing), and the flipper's profit margin. If the market is softer or hold time will be longer, use 65% or 60%.

Show the user: max offer, expected profit, break-even purchase price, and margin under the +20% repairs scenario.

## 5. Cost of waiting

Quantify the dollar cost of delay to force an explicit decision rather than letting inertia decide.

Inputs:

- Current monthly housing cost (rent, or existing mortgage + maintenance if selling)
- Expected monthly payment after transaction
- Expected monthly appreciation in the target market (annual / 12)
- Expected return on proceeds if invested elsewhere (for sellers)
- Months of delay being considered

Outputs:

- **Direct cost**: rent paid minus equity built elsewhere (buyer), or investment returns forgone (seller)
- **Opportunity cost**: missed property appreciation
- **Indifference point**: the monthly appreciation rate or rent differential at which waiting vs. acting breaks even
- **Recommendation**: act now / wait N months / wait indefinitely

## 6. DTI optimization

The user's negotiating power starts with loan approval. If DTI is marginal, small debt paydowns in the 90 days before application can unlock significantly more house or a lower rate.

Inputs:

- Annual gross income
- Each monthly debt obligation (car, student loan, credit cards with balances, etc.)
- Credit score
- Months until offer

Back-of-envelope lending thresholds (confirm with lender — these shift):

- Front-end DTI (housing only / gross income) — ideally ≤28%
- Back-end DTI (all debt / gross income) — ideally ≤36%, FHA often allows ≤43%, some programs to 50%

Produce a prioritized paydown plan: which debts, in which order, yield the largest DTI improvement per dollar paid. A $400/month car loan with 8 payments left is a far better paydown target than a $400/month mortgage; it disappears from DTI entirely once closed.

Translate improvements into purchasing power: each $100/month of DTI freed up, at the user's rate, buys roughly $15,000–$20,000 more house.

## Producing the Hard Stop as a decision memo

The final output for a buyer should be short and concrete:

```
Comfortable monthly all-in: $X
Implied max loan at Y% rate: $L
Plus down payment: $D
Subtotal: $L + $D
Minus known repairs (financed): −$R
HARD STOP: $H

At Hard Stop + $5k: monthly increases by $z/mo, total interest by $Z
At Hard Stop + $10k: ...
At Hard Stop + $15k: ...
```

Post this where the user will see it during viewings and negotiations. The number is useless if it isn't in front of them when the listing agent says "there are two other offers."
