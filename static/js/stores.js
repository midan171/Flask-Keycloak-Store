async function loadStores() {
    try {
        const response = await fetch('/api/users');
        const data = await response.json();
        const container = document.getElementById('stores-container');
        container.innerHTML = ''; // Clear existing content
        
        if (!data.users || data.users.length === 0) {
            container.innerHTML = '<p>No stores found. Please initialize the database first.</p>';
            return;
        }

        data.users.forEach(store => {
            const storeCard = document.createElement('div');
            storeCard.className = 'card';
            storeCard.innerHTML = `
                <h3>${store.name}</h3>
                <div class="card-content">
                    <p><strong>Store ID:</strong> ${store.id}</p>
                    <p><strong>Number of Items:</strong> ${store.rewards ? store.rewards.length : 0}</p>
                </div>
            `;
            container.appendChild(storeCard);
        });
    } catch (error) {
        console.error('Error:', error);
        const container = document.getElementById('stores-container');
        container.innerHTML = '<p>Error loading stores. Please try again later.</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadStores); 