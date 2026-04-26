Here's your complete prompt to hand off to an AI coding assistant (like Cursor, Claude, ChatGPT with file access, etc.) that will read your existing `index.html` and build the products page:

---

# PROMPT: Build Products Catalog Page for Existing Deli Packaging Website

## Context & Prerequisites

Read the existing `index.html` file in this project folder **first** before writing any code. Extract the following from it:

- The exact color palette (CSS variables or hex values used)
- The font families loaded (Google Fonts links)
- The navbar/header HTML structure (replicate it exactly)
- The footer HTML structure (replicate it exactly)
- The CSS class naming conventions used
- The animation patterns used (scroll fade-ins, etc.)
- The contact form's `id` or `anchor` attribute (you will link product CTAs to it)
- Also read `style.css` and `script.js` for variables, breakpoints, and JS patterns

Also read the **price list file** (PDF, image, or spreadsheet) in this project folder and extract:

- Product SKU / item code (e.g., `S-8`)
- Full product title (e.g., `8oz Microwavable Rectangular Container`)
- Case quantity (e.g., `240/case`)
- Any category groupings visible in the price list (e.g., Containers, Trays, Bags, Wraps, etc.)
- Product photographs if embedded in the price list
- Do **NOT** use any prices from the price list — pricing will display as `Price on Request` with a link to the contact form

---

## Task

Create a **new file** called `products.html` in the project root that:

1. Is a **standalone HTML page** (not a modal or iframe)
2. Shares the **exact same header/navbar and footer** as `index.html`
3. Has an **e-commerce style product catalog layout**
4. Links back to `index.html#contact` for all pricing/quote CTAs
5. Uses the **same `style.css`** — add any new styles needed into a **new linked file** called `products.css`
6. Uses the **same `script.js`** — add any new JS needed into a **new linked file** called `products.js`

---

## Products Page Structure

### Page Header / Banner

```
- Page title: "Our Products"
- Subtitle: "Food-Safe Packaging Solutions for Every Need — Serving the Greater Toronto Area"
- Same hero-style banner treatment as index.html hero but shorter (not full viewport height)
- Use the same background color/gradient from the flyer branding
```

### Filter / Category Bar

```
- A horizontal sticky filter bar below the page header
- "All Products" default selected tab/button
- One button per category extracted from the price list (e.g., Containers, Lids, Trays, Bags, Wraps, Custom, Eco-Friendly)
- Clicking a category filters visible products (vanilla JS, no page reload)
- Active filter button highlighted with accent color
- On mobile: horizontally scrollable filter bar
```

### Product Grid

```
Layout:
- Desktop: 4 columns
- Tablet: 2 columns  
- Mobile: 1 column (or 2 if cards are compact)
- CSS Grid layout
- Cards have subtle hover effect (lift + shadow)

Each Product Card contains:
┌─────────────────────────────┐
│  [Product Image or          │
│   Placeholder with icon]    │
│                             │
│  CATEGORY TAG (pill badge)  │
│                             │
│  S-8 | 8oz Microwavable     │
│  Rectangular Container      │
│  240/case                   │
│                             │
│  ✅ In stock, ready to ship │
│  🚚 Delivery Available      │
│  ⏱ Usually ready in 24hrs  │
│                             │
│  Price: [Price on Request]  │
│  (linked to #contact form)  │
│                             │
│  [Request a Quote] button   │
└─────────────────────────────┘
```

### Product Card Specifications

Each card must have:

```html
- data-category="containers" (or whatever category, for JS filtering)
- Product image: use actual photo from price list if available, otherwise a styled placeholder div with the product name and a package SVG icon
- SKU badge: small pill showing the item code (e.g., "S-8") in accent color
- Category badge: another pill (e.g., "Containers") 
- Title: Full descriptive product name — bold, 2 lines max
- Case info: "240/case" — muted text below title
- Stock status row:
    ✅ In stock, ready to ship
- Delivery row:
    🚚 Delivery Available  
- Lead time row:
    ⏱ Usually ready in 24 hours
- Price line:
    "Price: " + hyperlink styled as price text → links to index.html#contact
    Link text: "On Request"
- CTA Button: "Request a Quote" → links to index.html#contact
    Full width, primary button style matching index.html buttons
```

### "Can't Find What You're Looking For?" Section

```
Below the product grid, a full-width CTA banner:
- Heading: "Need a Custom Order or Don't See Your Product?"
- Subtext: "We supply a wide range of deli packaging products. Contact us and we'll source exactly what you need."
- Button: "Contact Us Today" → links to index.html#contact
- Use accent/secondary color background from the brand palette
```

---

## Wire Up `products.html` into `index.html`

Make the following changes to `index.html`:

### 1. Navigation Link

Add a `Products` nav link to the existing navbar in `index.html`:

```
- Insert "Products" nav item in the navbar (between appropriate existing items)
- href="products.html"
- Same styling as other nav items
- Also add it to the mobile hamburger menu
```

### 2. Products Section Teaser (on homepage)

In the existing Products/What We Offer section of `index.html`:

```
- Keep the existing product category cards as-is
- Add a button below the grid: "View Full Product Catalog →"
- href="products.html"  
- Style: outlined/secondary button style
- Center-aligned below the grid
```

### 3. Update Footer

In the footer of `index.html`, add a "Products" link in the quick nav links column:

```
- Add: <a href="products.html">Product Catalog</a>
- Same style as existing footer links
```

---

## SEO & Meta for `products.html`

```html
<title>Product Catalog | [Business Name from index.html] — GTA Deli Packaging</title>
<meta name="description" content="Browse our full catalog of food-safe deli packaging products including containers, lids, trays, bags, and custom printed options. Serving the Greater Toronto Area. Request a quote today.">
<meta name="keywords" content="deli packaging products GTA, food containers Toronto, deli containers wholesale, sandwich bags Mississauga, food trays Brampton, packaging supplier Toronto">

<!-- Open Graph -->
<meta property="og:title" content="Product Catalog | [Business Name] — GTA Deli Packaging">
<meta property="og:description" content="Browse food-safe deli packaging products for restaurants, delis, and caterers across the GTA.">
<meta property="og:type" content="website">
<meta property="og:url" content="[same domain as index.html og:url]">

<!-- Canonical -->
<link rel="canonical" href="[domain]/products.html">

<!-- Same favicon as index.html -->
<!-- Same Google Fonts link as index.html -->
<!-- Link to style.css AND products.css -->
```

---

## Animations & Interactions for `products.html`

Use the same scroll animation patterns from `script.js`:

```javascript
// In products.js:

// 1. Category filter functionality
// - On filter button click: hide all cards not matching category, show matching ones
// - Animate cards out (opacity 0, scale down) and in (opacity 1, scale up)
// - Update active button state
// - "All" shows everything

// 2. Scroll animations
// - Same IntersectionObserver pattern as script.js
// - Cards fade in + slide up as they enter viewport
// - Stagger delay based on card index within visible grid

// 3. Search bar (optional enhancement)
// - If price list has many products (20+), add a text search input above the filter bar
// - Real-time filtering as user types (searches title + SKU)
// - Debounce input at 300ms

// 4. "Back to Top" button
// - Same style as any existing back-to-top in index.html
// - If none exists, add a floating button that appears after 300px scroll
```

---

## Product Data Structure

Build products as a **JavaScript array** in `products.js` so it's easy to update:

```javascript
const products = [
  {
    sku: "S-8",
    title: "8oz Microwavable Rectangular Container",
    caseQty: "240/case",
    category: "containers",
    categoryLabel: "Containers",
    image: null, // set to image path if extracted from price list, e.g. "images/products/s-8.jpg"
    inStock: true,
    deliveryAvailable: true,
    leadTime: "Usually ready in 24 hours",
    // ADD ALL OTHER PRODUCTS FROM PRICE LIST HERE
  },
  // ... more products
];
```

Then **dynamically render** all product cards from this array into the grid using JS — do not hardcode individual cards in HTML. This makes the catalog easy to maintain.

---

## File Output Required

Produce the following files (complete, production-ready code):

```
/project-root
├── index.html          ← MODIFIED (nav link added, teaser button added, footer updated)
├── style.css           ← UNMODIFIED (read-only reference)
├── script.js           ← UNMODIFIED (read-only reference)
├── products.html       ← NEW FILE (complete page)
├── products.css        ← NEW FILE (catalog-specific styles only)
├── products.js         ← NEW FILE (filter logic + dynamic card rendering + animations)
└── /images
    └── /products       ← NEW SUBFOLDER (place any extracted product photos here)
        └── placeholder-product.svg  ← NEW (a clean SVG placeholder for products without photos)
```

---

## Quality Checklist (verify before outputting)

- [ ] `products.html` navbar is pixel-identical to `index.html` navbar
- [ ] `products.html` footer is pixel-identical to `index.html` footer
- [ ] All brand colors match `index.html` exactly (no new colors introduced)
- [ ] All fonts match `index.html` exactly
- [ ] No prices from the price list appear anywhere on the page
- [ ] Every "On Request" text and "Request a Quote" button links to `index.html#contact`
- [ ] Filter bar works correctly on mobile (horizontal scroll, no wrapping)
- [ ] Cards display correctly at all 3 breakpoints
- [ ] JS product array contains ALL products extracted from the price list
- [ ] `index.html` changes are minimal and non-breaking (only 3 additions listed above)
- [ ] Page loads fast — no external dependencies beyond what `index.html` already uses
- [ ] SEO meta tags complete on `products.html`

---

**Begin by reading `index.html`, `style.css`, `script.js` and the `Price List.docx` file. Then output all files in full.**