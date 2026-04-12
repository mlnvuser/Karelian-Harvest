(function () {
  const wrapper = document.querySelector('.slider-wrapper');
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  const arrowLeft = document.querySelector('.arrow-left');
  const arrowRight = document.querySelector('.arrow-right');
  const sliderContainer = document.querySelector('#news-slider');

  // Определяем количество оригинальных слайдов (без клонов)
  const originalSlides = [...slides].filter(s => !s.classList.contains('clone'));
  const totalOriginal = originalSlides.length;

  // Если новостей нет или всего одна — просто скрываем интерфейс
  if (totalOriginal === 0 || totalOriginal === 1) {
    // Прячем стрелки и точки если нужна 1 новость
    if (arrowLeft && arrowRight) {
      arrowLeft.style.display = 'none';
      arrowRight.style.display = 'none';
    }
    if (dots.length > 0) {
      dots.forEach(dot => dot.style.display = 'none');
    }
    // Запускаем автопрокрутку для одиночной новости (опционально)
    return;
  }

  let currentIndex = 1;
  let isTransitioning = false;
  let autoPlayInterval = null;
  let userInteracted = false;
  let transitionTimer = null;

  function getSlideStep() {
    const slideEl = slides[1];
    const style = getComputedStyle(slideEl);
    const slideWidth = slideEl.offsetWidth;
    const marginLeft = parseFloat(style.marginLeft);
    const marginRight = parseFloat(style.marginRight);
    return slideWidth + marginLeft + marginRight;
  }

  function getOffset(index) {
    const containerWidth = document.querySelector('.slider-container').offsetWidth;
    const step = getSlideStep();
    const slideWidth = slides[index].offsetWidth;
    const offset = index * step - (containerWidth - slideWidth) / 2;
    return offset;
  }

  function updateClasses(index) {
    slides.forEach((s, i) => s.classList.toggle('active-slide', i === index));

    // Безопасная формула для индексов точек
    const originalIndex = ((index - 1 + totalOriginal) % totalOriginal);

    dots.forEach((d, i) => d.classList.toggle('active', i === originalIndex));
  }

  function jumpTo(index) {
    wrapper.classList.add('no-transition');
    wrapper.style.transition = 'none';
    const offset = getOffset(index);
    wrapper.style.transform = `translateX(-${offset}px)`;
    updateClasses(index);
    wrapper.offsetHeight;
    wrapper.classList.remove('no-transition');
  }

  function onTransitionDone() {
    clearTimeout(transitionTimer);
    transitionTimer = null;
    isTransitioning = false;

    if (currentIndex >= totalOriginal + 1) {
      currentIndex = 1;
      jumpTo(currentIndex);
    }

    if (currentIndex <= 0) {
      currentIndex = totalOriginal;
      jumpTo(currentIndex);
    }
  }

  function goTo(index) {
    if (isTransitioning) return;
    isTransitioning = true;
    currentIndex = index;

    wrapper.classList.remove('no-transition');
    wrapper.style.transition = 'transform 0.5s ease-in-out';

    const offset = getOffset(currentIndex);
    wrapper.style.transform = `translateX(-${offset}px)`;
    updateClasses(currentIndex);

    clearTimeout(transitionTimer);
    transitionTimer = setTimeout(() => {
      onTransitionDone();
    }, 600);
  }

  wrapper.addEventListener('transitionend', (e) => {
    if (e.target !== wrapper) return;
    onTransitionDone();
  });

  arrowRight.addEventListener('click', () => {
    stopAutoPlay();
    goTo(currentIndex + 1);
  });

  arrowLeft.addEventListener('click', () => {
    stopAutoPlay();
    goTo(currentIndex - 1);
  });

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      stopAutoPlay();
      const target = parseInt(dot.dataset.index) + 1;
      goTo(target);
    });
  });

  // ===== СВАЙПЫ =====
  let touchStartX = 0;
  let touchEndX = 0;

  wrapper.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  wrapper.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > 50) {
      stopAutoPlay();
      if (diff > 0) {
        goTo(currentIndex + 1);
      } else {
        goTo(currentIndex - 1);
      }
    }
  }, { passive: true });

  // ===== АВТОПРОКРУТКА =====
  function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
      goTo(currentIndex + 1);
    }, 5000);
  }

  function stopAutoPlay() {
    if (!userInteracted) {
      userInteracted = true;
      clearInterval(autoPlayInterval);
    }
  }

  // ===== РЕЗИЗ =====
  window.addEventListener('resize', () => {
    jumpTo(currentIndex);
  });

  // ===== ИНИЦИАЛИЗАЦИЯ =====
  if (wrapper) {
    jumpTo(currentIndex);
    startAutoPlay();
  }

})();