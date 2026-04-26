# CRM Setup Guide & Activity Goals
## Call Tracking, Pipeline Management & Daily Targets

---

## PIPELINE STATUS DEFINITIONS

Use these exact labels in the "Pipeline Status" column of your CRM spreadsheet:

| Status | Definition | Next Action |
|--------|-----------|-------------|
| **Cold** | Lead added, not yet called | Schedule first call |
| **Contacted** | Spoke on phone or voicemail left | Follow up within 3 days |
| **Nurturing** | Multiple touchpoints, not ready yet | Monthly check-in |
| **Interested** | Expressed interest, wants info/quote | Send email within 2 hours, follow up within 2 days |
| **Meeting Booked** | In-person or phone meeting scheduled | Confirm 24 hrs prior, prep materials |
| **Quoted** | Formal quote/pricing sent | Follow up within 3 business days |
| **Negotiating** | Discussing terms/pricing | Respond within same day |
| **Closed - Won** | Order placed, became a customer | Onboard, check in at 2 weeks |
| **Closed - Lost** | Will not purchase at this time | Re-engage in 90 days |
| **Do Not Call** | Requested no further contact | Remove from active list |

---

## GOOGLE SHEETS SETUP INSTRUCTIONS

### Step 1 — Import the CSV
1. Open Google Sheets (sheets.google.com)
2. File → Import → Upload → Select `Call_Tracking_Template.csv`
3. Select "Replace spreadsheet" and "Detect automatically" for separator
4. Click Import

### Step 2 — Format the Sheet
**Freeze top row:** View → Freeze → 1 row

**Color-code Pipeline Status column using Conditional Formatting:**

| Status | Background Color | Text Color |
|--------|-----------------|------------|
| Cold | Light grey (#E8EAED) | Dark grey |
| Contacted | Light blue (#C9DAF8) | Dark blue |
| Nurturing | Light yellow (#FFF2CC) | Dark yellow |
| Interested | Light green (#D9EAD3) | Dark green |
| Meeting Booked | Orange (#FCE5CD) | Dark orange |
| Quoted | Purple (#EAD1DC) | Dark purple |
| Negotiating | Gold (#FFE599) | Dark brown |
| Closed - Won | Green (#B6D7A8) | Dark green |
| Closed - Lost | Red (#EA9999) | Dark red |
| Do Not Call | Dark grey (#666666) | White |

### Step 3 — Add Drop-down Validation for Key Columns
For "Business Type" column:
- Right-click column → Data validation → List of items
- Paste: `Deli,Restaurant,Caterer,Grocery Store,Butcher Shop,Bakery,Food Truck,Meal Prep,Sandwich Shop,Ghost Kitchen,Hotel/Banquet,Other`

For "Pipeline Status" column:
- Same method → Paste: `Cold,Contacted,Nurturing,Interested,Meeting Booked,Quoted,Negotiating,Closed - Won,Closed - Lost,Do Not Call`

For "Call Outcome" columns:
- Paste: `No Answer,Voicemail Left,Spoke - Not Interested,Spoke - Interested,Email Requested,Meeting Booked,Callback Scheduled,Wrong Number`

### Step 4 — Create a Dashboard Tab
Add a second sheet tab called "Dashboard" with these summary cells:

```
=COUNTIF('Sheet1'!Pipeline_Status,"Cold")         → Cold Leads
=COUNTIF('Sheet1'!Pipeline_Status,"Contacted")    → Contacted
=COUNTIF('Sheet1'!Pipeline_Status,"Interested")   → Hot Leads
=COUNTIF('Sheet1'!Pipeline_Status,"Meeting Booked") → Meetings
=COUNTIF('Sheet1'!Pipeline_Status,"Quoted")       → Quotes Out
=COUNTIF('Sheet1'!Pipeline_Status,"Closed - Won") → Closed Won
=SUM('Sheet1'!Quote_Value where Closed - Won)     → Revenue
```

---

## DAILY ACTIVITY GOALS

### Minimum Daily Targets (Established Rep)

| Activity | Daily Target | Weekly Target |
|----------|-------------|---------------|
| Dials made (total calls attempted) | 50 | 250 |
| Live contacts reached | 15 | 75 |
| Emails sent | 10 | 50 |
| New leads added to CRM | 20 | 100 |
| Follow-ups completed | 15 | 75 |
| Meetings booked | 1–2 | 5–10 |
| Quotes sent | 1–2 | 5–10 |

### Ramp-Up Targets (First 30 Days)

| Week | Dials/Day | Live Contacts/Day | Meetings/Week |
|------|-----------|-------------------|---------------|
| Week 1 | 20 | 6 | 1–2 |
| Week 2 | 30 | 9 | 2–3 |
| Week 3 | 40 | 12 | 3–5 |
| Week 4 | 50 | 15 | 5+ |

---

## WEEKLY CONVERSION BENCHMARKS

These are industry-standard benchmarks for B2B cold calling in food packaging/supply:

| Metric | Benchmark | Your Target |
|--------|-----------|-------------|
| Contact rate (live answers / dials) | 20–30% | 25%+ |
| Interest rate (interested / contacts) | 15–25% | 20%+ |
| Meeting rate (meetings / interests) | 30–50% | 40%+ |
| Quote rate (quotes sent / meetings) | 60–80% | 70%+ |
| Close rate (closed / quotes) | 20–40% | 30%+ |
| Overall conversion (closed / dials) | 1–3% | 2%+ |

**Example math for a good week:**
- 250 dials → 62 contacts → 12 interested → 5 meetings → 4 quotes → 1–2 closed

---

## MONTHLY REVENUE TARGETS

| Month | New Accounts Target | Revenue Target |
|-------|--------------------|--------------------|
| Month 1 | 3–5 new accounts | $2,000–$5,000 |
| Month 2 | 5–8 new accounts | $4,000–$10,000 |
| Month 3 | 8–12 new accounts | $7,000–$15,000 |
| Month 6 | 15–20 active accounts | $15,000–$30,000/mo |

---

## WEEKLY REVIEW CHECKLIST

Run this review every Friday afternoon:

**1. Update CRM**
- [ ] All calls logged
- [ ] All statuses current
- [ ] Follow-up dates set for every open lead

**2. Review Numbers**
- [ ] Dials made vs. target
- [ ] Contacts reached vs. target
- [ ] Meetings booked this week
- [ ] Quotes out

**3. Pipeline Check**
- [ ] How many leads in "Interested" — need follow-up?
- [ ] How many quotes open — need to follow up?
- [ ] Any "Meeting Booked" leads coming up next week?

**4. Plan Next Week**
- [ ] Top 10 priority callbacks identified
- [ ] New leads added to call list
- [ ] Any accounts to re-engage (30+ days no contact)?

---

## CALL LOG SHORTCODES (for fast data entry)

Use these in the Notes column for quick entry during calls:

| Code | Meaning |
|------|---------|
| `NA` | No Answer |
| `VM` | Voicemail left |
| `CB [date]` | Callback requested on [date] |
| `NI` | Not Interested |
| `INT` | Interested |
| `ES [date]` | Email sent on [date] |
| `MB [date]` | Meeting booked for [date] |
| `QS [amount]` | Quote sent for $[amount] |
| `CW` | Closed Won |
| `CL` | Closed Lost |
| `DNC` | Do Not Call |

---

*Log every single call — even no-answers. Your data is your most valuable asset.*
