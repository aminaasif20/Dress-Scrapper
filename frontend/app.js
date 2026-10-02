const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const maxPriceInput = document.getElementById('maxPriceInput');
const brandSelect = document.getElementById('brandSelect');
const saleCheck = document.getElementById('saleCheck');
const sortSelect = document.getElementById('sortSelect');
const searchBtn = document.getElementById('searchBtn');
const productsGrid = document.getElementById('productsGrid');
const resultsCount = document.getElementById('resultsCount');
const loader = document.getElementById('loader');

// Mobile filter elements
const filterSidebar = document.getElementById('filterSidebar');
const mobileFilterBtn = document.getElementById('mobileFilterBtn');
const closeFilterBtn = document.getElementById('closeFilterBtn');

// Formatting utilities
const formatPKR = (amount) => {
    return 'Rs. ' + Number(amount).toLocaleString('en-PK', {
        maximumFractionDigits: 0
    });
};

// Fetch data from API
async function fetchProducts() {
    // Show loader
    loader.style.display = 'flex';
    productsGrid.innerHTML = '';
    resultsCount.textContent = 'Searching...';

    // Build Query Params
    const params = new URLSearchParams();
    
    if (searchInput.value.trim()) params.append('q', searchInput.value.trim());
    if (maxPriceInput.value) params.append('max_price', maxPriceInput.value);
    if (brandSelect.value) params.append('brand', brandSelect.value);
    if (saleCheck.checked) params.append('on_sale', 'true');
    params.append('sort', sortSelect.value);

    try {
        const response = await fetch(`${API_BASE_URL}/search?${params.toString()}`);
        if (!response.ok) throw new Error('API Request Failed');
        
        const data = await response.json();
        displayProducts(data);
    } catch (error) {
        console.error('Error fetching products:', error);
        resultsCount.textContent = 'Failed to load products. Make sure the API is running.';
        loader.style.display = 'none';
    }
}

// Display products in the grid
function displayProducts(data) {
    loader.style.display = 'none';
    
    if (data.total_results === 0) {
        resultsCount.textContent = 'No products found. Try adjusting your filters.';
        return;
    }

    resultsCount.textContent = `Found ${data.total_results} Products`;
    
    const productsHtml = data.results.map(product => {
        const hasDiscount = product.is_on_sale && product.original_price > product.price;
        const discountPercentage = hasDiscount 
            ? Math.round(((product.original_price - product.price) / product.original_price) * 100)
            : 0;

        return `
            <div class="product-card">
                <div class="product-image-container">
                    ${hasDiscount ? `<span class="sale-badge">-${discountPercentage}% OFF</span>` : ''}
                    <span class="brand-badge">${product.brand}</span>
                    <img src="${product.image_url || 'https://via.placeholder.com/400x533?text=No+Image'}" 
                         alt="${product.title}" 
                         class="product-image"
                         onerror="this.src='https://via.placeholder.com/400x533?text=Image+Not+Found'">
                </div>
                <div class="product-info">
                    <h3 class="product-title" title="${product.title}">${product.title}</h3>
                    <div class="product-price-wrapper">
                        <span class="price">${formatPKR(product.price)}</span>
                        ${hasDiscount ? `<span class="original-price">${formatPKR(product.original_price)}</span>` : ''}
                    </div>
                    <a href="${product.product_url}" target="_blank" rel="noopener noreferrer" class="view-btn">
                        View on Store
                    </a>
                </div>
            </div>
        `;
    }).join('');

    productsGrid.innerHTML = productsHtml;
}

// Event Listeners
searchBtn.addEventListener('click', () => {
    fetchProducts();
    // Close sidebar on mobile after applying filters
    filterSidebar.classList.remove('active');
});

// Mobile filter toggles
if (mobileFilterBtn && closeFilterBtn) {
    mobileFilterBtn.addEventListener('click', () => {
        filterSidebar.classList.add('active');
    });

    closeFilterBtn.addEventListener('click', () => {
        filterSidebar.classList.remove('active');
    });

    filterSidebar.addEventListener('click', (e) => {
        if (e.target === filterSidebar) {
            filterSidebar.classList.remove('active');
        }
    });
}

// Enable "Enter" key on inputs
[searchInput, maxPriceInput].forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') fetchProducts();
    });
});

// Auto-fetch when dropdowns or toggles change
[brandSelect, saleCheck, sortSelect].forEach(input => {
    input.addEventListener('change', fetchProducts);
});

// Initial load
window.addEventListener('DOMContentLoaded', fetchProducts);
