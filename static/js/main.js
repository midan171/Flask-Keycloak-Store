document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for navigation
    document.getElementById('loginBtn').addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Login clicked');
    });

    document.getElementById('registerBtn').addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Register clicked');
    });

    document.getElementById('storesBtn').addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Stores clicked');
    });

    document.getElementById('itemsBtn').addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Items clicked');
    });
}); 