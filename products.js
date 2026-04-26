// products.js — Product data and catalog logic for H2 Consultants

const products = [
    { sku: "S-8", title: "Low Density 8oz Microwavable Deli (240/case) with lids", caseQty: "240/case", category: "containers", categoryLabel: "Containers", image: "images/products/S-8.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "S-12", title: "Low Density 12oz Microwavable Deli (240/case) with lids", caseQty: "240/case", category: "containers", categoryLabel: "Containers", image: "images/products/S-12.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "S-16", title: "Low Density 16oz Microwavable Deli (240/case) with lids", caseQty: "240/case", category: "containers", categoryLabel: "Containers", image: "images/products/S-16.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "S-24", title: "Low Density 24oz Microwavable Deli (240/case) with lids", caseQty: "240/case", category: "containers", categoryLabel: "Containers", image: "images/products/S-24.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "S-32", title: "Low Density 32oz Microwavable Deli (240/case) with lids", caseQty: "240/case", category: "containers", categoryLabel: "Containers", image: "images/products/S-32.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2808", title: "Heavy Duty 8oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2808.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2812", title: "Heavy Duty 12oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2812.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2816", title: "Heavy Duty 16oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2816.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2820", title: "Heavy Duty 20oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2820.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2824", title: "Heavy Duty 24oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2824.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H2832", title: "Heavy Duty 32oz Microwavable Deli (500/case) without lids", caseQty: "500/case", category: "containers", categoryLabel: "Containers", image: "images/products/H2832.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "H8", title: "4.5’’ Deli container lid (500/case)", caseQty: "500/case", category: "lids", categoryLabel: "Lids", image: "images/products/H8.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "T-28", title: "28oz Microwavable Rectangle (150/case) with lids", caseQty: "150/case", category: "trays", categoryLabel: "Trays", image: "images/products/T-28.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "T-38", title: "38oz Microwavable Rectangle (150/case) with lids", caseQty: "150/case", category: "trays", categoryLabel: "Trays", image: "images/products/T-38.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "PP-008", title: "6x6x3’’ Microwavable (250/case)", caseQty: "250/case", category: "containers", categoryLabel: "Containers", image: "images/products/PP-008.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "PP-018", title: "9x6x3’’ Microwavable (250/case)", caseQty: "250/case", category: "containers", categoryLabel: "Containers", image: "images/products/PP-018.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" },
    { sku: "PP-071", title: "7x7x3’’ Microwavable (250/case)", caseQty: "250/case", category: "containers", categoryLabel: "Containers", image: "images/products/PP-071.jpg", inStock: true, deliveryAvailable: true, leadTime: "Usually ready in 24 hours" }
];

const categories = [
    { key: "all", label: "All Products" },
    { key: "containers", label: "Containers" },
    { key: "lids", label: "Lids" },
    { key: "trays", label: "Trays" },
    { key: "bags", label: "Bags" },
    // { key: "wraps", label: "Wraps" },
    // { key: "custom", label: "Custom" },
    // { key: "eco", label: "Eco-Friendly" }
];

// --- All logic runs after DOM is ready ---
document.addEventListener('DOMContentLoaded', () => {

    // ✅ DOM references are now safe — elements exist
    const grid = document.getElementById('productGrid');
    const filterBar = document.getElementById('filterBar');

    // --- Modal elements ---
    const modal = document.getElementById('imageZoomModal');
    const zoomedImg = document.getElementById('zoomedProductImg');
    const closeBtn = document.getElementById('imageZoomClose');
    const backdrop = document.getElementById('imageZoomBackdrop');

    // --- Image Zoom Modal Logic ---
    function showImageZoomModal(imgSrc, altText) {
        zoomedImg.src = imgSrc;
        zoomedImg.alt = altText || 'Zoomed product image';
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        zoomedImg.focus();
    }

    function closeImageZoomModal() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        zoomedImg.src = '';
    }

    // ✅ Close button - X click
    closeBtn.addEventListener('click', closeImageZoomModal);

    // ✅ Close button - keyboard
    closeBtn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            closeImageZoomModal();
        }
    });

    // ✅ Backdrop click closes modal
    backdrop.addEventListener('click', closeImageZoomModal);

    // ✅ Escape key closes modal
    document.addEventListener('keydown', function (e) {
        if (
            (modal.style.display === 'flex') &&
            (e.key === 'Escape' || e.key === 'Esc')
        ) {
            closeImageZoomModal();
        }
    });

    // --- Set Category for Filter Bar ---
    function setCategory(categoryKey) {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.category === categoryKey) {
                btn.classList.add('active');
            }
        });
        renderProducts(categoryKey);
    }

    // --- Render filter bar ---
    function renderFilterBar() {
        filterBar.innerHTML = '';
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.textContent = cat.label;
            btn.dataset.category = cat.key;
            if (cat.key === 'all') btn.classList.add('active');
            btn.onclick = () => setCategory(cat.key);
            filterBar.appendChild(btn);
        });
    }

    // --- Render product cards ---
    function renderProducts(category = 'all') {
        grid.innerHTML = '';
        let filtered = category === 'all'
            ? products
            : products.filter(p => p.category === category);

        filtered.forEach((p) => {
            const card = document.createElement('div');
            card.className = 'product-card fade-in-up';
            card.setAttribute('data-category', p.category);

            let imgHtml;
            if (p.image) {
                imgHtml = `<img src="${p.image}" alt="${p.title}" class="product-img zoomable" data-img="${p.image}">`;
            } else {
                imgHtml = `<div class="product-img-placeholder"><img src="images/products/placeholder-product.svg" alt="Product placeholder"></div>`;
            }

            card.innerHTML = `
                ${imgHtml}
                <div class="product-badges">
                    <span class="badge badge-sku">${p.sku}</span>
                    <span class="badge badge-cat">${p.categoryLabel}</span>
                </div>
                <div class="product-title">${p.title}</div>
                <div class="product-case">${p.caseQty}</div>
                <div class="product-status">
                    <span>✅ In stock, ready to ship</span><br>
                    <span>🚚 Delivery Available</span><br>
                    <span>⏱ ${p.leadTime}</span>
                </div>
                <div class="product-price">
                    Price: <a href="index.html#contact" class="price-link">On Request</a>
                </div>
                <a href="index.html#contact" class="btn btn-primary product-cta">Request a Quote</a>
            `;
            grid.appendChild(card);
        });

        // ✅ Add zoom listeners after cards are rendered
        document.querySelectorAll('.zoomable').forEach(img => {
            img.style.cursor = 'zoom-in';
            img.setAttribute('tabindex', '0');
            img.setAttribute('role', 'button');
            img.setAttribute('aria-label', 'Zoom product image');

            img.addEventListener('click', function () {
                showImageZoomModal(this.dataset.img, this.alt);
            });

            img.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    showImageZoomModal(this.dataset.img, this.alt);
                }
            });
        });

        animateCards();
    }

    // --- Init ---
    renderFilterBar();
    renderProducts();
});