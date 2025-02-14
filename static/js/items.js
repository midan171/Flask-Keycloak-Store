async function loadItems() {
    try {
        const response = await fetch('/api/rewards');
        const data = await response.json();
        const container = document.getElementById('items-container');
        container.innerHTML = ''; // Clear existing content
        
        if (!data.rewards || data.rewards.length === 0) {
            container.innerHTML = '<p>No items found. Please initialize the database first.</p>';
            return;
        }

        data.rewards.forEach(item => {
            const itemCard = document.createElement('div');
            itemCard.className = 'card';
            itemCard.innerHTML = `
                <h3>${item.reward_name}</h3>
                <div class="card-content">
                    <p><strong>Item ID:</strong> ${item.id}</p>
                    <p><strong>Store ID:</strong> ${item.marsh_id || 'N/A'}</p>
                </div>
            `;
            container.appendChild(itemCard);
        });
    } catch (error) {
        console.error('Error:', error);
        const container = document.getElementById('items-container');
        container.innerHTML = '<p>Error loading items. Please try again later.</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadItems); 