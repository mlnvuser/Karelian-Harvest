document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeBtn = document.getElementById('closeMenu');

    function openMenu() {
        mobileMenu.style.display = 'flex';
        document.body.classList.add('menu-open');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileMenu.style.display = 'none';
        document.body.classList.remove('menu-open');
        document.body.style.overflow = '';
    }

    menuBtn.addEventListener('click', (e) => {
        e.preventDefault();           // предотвращаем переход по ссылке #
        openMenu();
    });

    closeBtn.addEventListener('click', closeMenu);

    // Закрытие по клику на ссылки в меню
    document.querySelectorAll('.mobile-menu-links a').forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeMenu, 300);
        });
    });

    // Закрытие по клавише Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenu.style.display === 'flex') {
            closeMenu();
        }
    });
});