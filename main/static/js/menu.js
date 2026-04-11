document.addEventListener('DOMContentLoaded', () => {
    const burger = document.getElementById('burger');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeBtn = document.getElementById('closeMenu');

    function openMenu() {
        mobileMenu.classList.add('active');
        burger.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileMenu.classList.remove('active');
        burger.classList.remove('active');
        document.body.style.overflow = '';
    }

    burger.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);

    document.querySelectorAll('.mobile-menu-links a').forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeMenu, 300);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            closeMenu();
        }
    });
});