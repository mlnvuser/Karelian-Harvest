document.addEventListener('DOMContentLoaded', () => {
    const mobileMenu = document.getElementById('mobileMenu');
    const closeBtn = document.getElementById('closeMenu');
    let startX = 0;
    let currentX = 0;
    let isSwiping = false;

    // Открытие меню свайпом
    function openMenu() {
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Свайп обработчики
    document.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isSwiping = true;
    });

    document.addEventListener('touchmove', (e) => {
        if (!isSwiping) return;
        currentX = e.touches[0].clientX;
    });

    document.addEventListener('touchend', () => {
        if (!isSwiping) return;

        const diff = startX - currentX;

        // Если свайп был справа налево и достаточно длинный
        if (diff > 80 && startX > window.innerWidth * 0.7) {
            openMenu();
        }

        isSwiping = false;
    });

    // Закрытие по крестику
    closeBtn.addEventListener('click', closeMenu);

    // Закрытие по клику на ссылки
    document.querySelectorAll('.mobile-menu-links a').forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeMenu, 250);
        });
    });
});