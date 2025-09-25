document.addEventListener('DOMContentLoaded', () => {
    const stickyNav = document.getElementById('stickyNav');
    const hamburgerMenu = document.getElementById('hamburgerMenu');
    const menuItems = document.getElementById('menuItems');
    
    // Show/hide sticky navigation based on scroll position
    window.addEventListener('scroll', () => {
        const headerHeight = document.querySelector('.main-header').offsetHeight;
        
        if (window.scrollY > headerHeight) {
            stickyNav.classList.add('visible');
        } else {
            stickyNav.classList.remove('visible');
        }
    });
    
    // Toggle mobile menu
    hamburgerMenu.addEventListener('click', () => {
        menuItems.classList.toggle('active');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (event) => {
        if (!hamburgerMenu.contains(event.target) && !menuItems.contains(event.target)) {
            menuItems.classList.remove('active');
        }
    });
});