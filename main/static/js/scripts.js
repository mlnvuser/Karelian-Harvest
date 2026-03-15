(function () {
  // Самовызывающаяся функция для изоляции переменных

  const wrapper = document.querySelector('.slider-wrapper');
  // Находим обёртку слайдов

  const slides = document.querySelectorAll('.slide');
  // Получаем все слайды (включая клоны)

  const dots = document.querySelectorAll('.dot');
  // Получаем все точки-индикаторы

  const arrowLeft = document.querySelector('.arrow-left');
  // Левая стрелка

  const arrowRight = document.querySelector('.arrow-right');
  // Правая стрелка

  const totalOriginal = slides.length - 2;
  // Количество оригинальных слайдов: 5 - 2 клона = 3

  let currentIndex = 1;
  // Текущий индекс (1 = первый оригинальный слайд)

  let isTransitioning = false;
  // Флаг защиты от двойного клика

  let autoPlayInterval = null;
  // ID интервала автопрокрутки

  let userInteracted = false;
  // Флаг: пользователь уже взаимодействовал

  let transitionTimer = null;
  // Страховочный таймер на случай если transitionend не сработает

  function getSlideStep() {
    // Вычисляет ширину одного шага прокрутки

    const slideEl = slides[1];
    // Берём первый оригинальный слайд как эталон

    const style = getComputedStyle(slideEl);
    // Получаем вычисленные стили

    const slideWidth = slideEl.offsetWidth;
    // Ширина слайда в пикселях

    const marginLeft = parseFloat(style.marginLeft);
    // Левый отступ

    const marginRight = parseFloat(style.marginRight);
    // Правый отступ

    return slideWidth + marginLeft + marginRight;
    // Полная ширина шага
  }

  function getOffset(index) {
    // Вычисляет смещение для центрирования слайда

    const containerWidth = document.querySelector('.slider-container').offsetWidth;
    // Ширина контейнера

    const step = getSlideStep();
    // Ширина одного шага

    const slideWidth = slides[index].offsetWidth;
    // Ширина целевого слайда

    const offset = index * step - (containerWidth - slideWidth) / 2;
    // Смещение для центрирования

    return offset;
    // Возвращаем смещение
  }

  function updateClasses(index) {
    // Обновляет визуальные классы (активный слайд и точки)

    slides.forEach((s, i) => s.classList.toggle('active-slide', i === index));
    // Класс active-slide только у текущего слайда

    const originalIndex = ((index - 1) % totalOriginal + totalOriginal) % totalOriginal;
    // Вычисляем индекс для точек (0, 1, 2)

    dots.forEach((d, i) => d.classList.toggle('active', i === originalIndex));
    // Обновляем точки
  }

  function jumpTo(index) {
    // Мгновенный перескок БЕЗ каких-либо анимаций

    wrapper.classList.add('no-transition');
    // Отключаем все transition через CSS-класс

    wrapper.style.transition = 'none';
    // Дополнительно отключаем inline transition обёртки

    const offset = getOffset(index);
    // Вычисляем новое смещение

    wrapper.style.transform = `translateX(-${offset}px)`;
    // Мгновенно сдвигаем

    updateClasses(index);
    // Мгновенно обновляем классы

    wrapper.offsetHeight;
    // Принудительный reflow

    wrapper.classList.remove('no-transition');
    // Возвращаем возможность анимаций
  }

  function onTransitionDone() {
    // Общая логика, выполняемая после завершения анимации перехода

    clearTimeout(transitionTimer);
    // Очищаем страховочный таймер, если он был запущен

    transitionTimer = null;
    // Сбрасываем ссылку на таймер

    isTransitioning = false;
    // Анимация завершена, можно кликать снова

    if (currentIndex >= totalOriginal + 1) {
      // Доехали до клона первого слайда

      currentIndex = 1;
      // Перескакиваем на настоящий первый

      jumpTo(currentIndex);
      // Мгновенный перескок
    }

    if (currentIndex <= 0) {
      // Доехали до клона последнего слайда

      currentIndex = totalOriginal;
      // Перескакиваем на настоящий последний

      jumpTo(currentIndex);
      // Мгновенный перескок
    }
  }

  function goTo(index) {
    // Переход к слайду с анимацией

    if (isTransitioning) return;
    // Если анимация уже идёт — выходим

    isTransitioning = true;
    // Ставим флаг анимации

    currentIndex = index;
    // Обновляем индекс

    wrapper.classList.remove('no-transition');
    // Убираем класс блокировки анимаций

    wrapper.style.transition = 'transform 0.5s ease-in-out';
    // Включаем плавный переход

    const offset = getOffset(currentIndex);
    // Вычисляем смещение

    wrapper.style.transform = `translateX(-${offset}px)`;
    // Применяем сдвиг с анимацией

    updateClasses(currentIndex);
    // Обновляем визуальные классы

    clearTimeout(transitionTimer);
    // Очищаем предыдущий страховочный таймер если был

    transitionTimer = setTimeout(() => {
      // Запускаем страховочный таймер на 600мс
      // (чуть больше длительности анимации 500мс)
      // Если transitionend не сработает по какой-то причине,
      // этот таймер разблокирует слайдер

      onTransitionDone();
      // Выполняем ту же логику что и при transitionend
    }, 600);
    // 600мс — гарантированно больше чем 500мс анимации
  }

  wrapper.addEventListener('transitionend', (e) => {
    // Событие окончания CSS-анимации

    if (e.target !== wrapper) return;
    // Реагируем только на анимацию самой обёртки

    onTransitionDone();
    // Выполняем логику завершения перехода
  });

  arrowRight.addEventListener('click', () => {
    // Клик по правой стрелке

    stopAutoPlay();
    // Останавливаем автопрокрутку

    goTo(currentIndex + 1);
    // Следующий слайд
  });

  arrowLeft.addEventListener('click', () => {
    // Клик по левой стрелке

    stopAutoPlay();
    // Останавливаем автопрокрутку

    goTo(currentIndex - 1);
    // Предыдущий слайд
  });

  dots.forEach((dot) => {
    // Перебираем точки

    dot.addEventListener('click', () => {
      // Клик по точке

      stopAutoPlay();
      // Останавливаем автопрокрутку

      const target = parseInt(dot.dataset.index) + 1;
      // Целевой индекс (+1 из-за клона в начале)

      goTo(target);
      // Переходим
    });
  });

  // ===== Свайпы =====

  let touchStartX = 0;
  // Начальная позиция касания

  let touchEndX = 0;
  // Конечная позиция касания

  wrapper.addEventListener('touchstart', (e) => {
    // Начало касания

    touchStartX = e.changedTouches[0].screenX;
    // Запоминаем X
  }, { passive: true });

  wrapper.addEventListener('touchend', (e) => {
    // Конец касания

    touchEndX = e.changedTouches[0].screenX;
    // Запоминаем X

    const diff = touchStartX - touchEndX;
    // Дистанция свайпа

    if (Math.abs(diff) > 50) {
      // Свайп достаточно длинный

      stopAutoPlay();
      // Останавливаем автопрокрутку

      if (diff > 0) {
        // Свайп влево

        goTo(currentIndex + 1);
        // Следующий
      } else {
        // Свайп вправо

        goTo(currentIndex - 1);
        // Предыдущий
      }
    }
  }, { passive: true });

  // ===== Автопрокрутка =====

  function startAutoPlay() {
    // Запуск автосмены слайдов

    autoPlayInterval = setInterval(() => {
      // Каждые 5 секунд

      goTo(currentIndex + 1);
      // Следующий слайд
    }, 5000);
  }

  function stopAutoPlay() {
    // Остановка автопрокрутки навсегда

    if (!userInteracted) {
      // Только при первом взаимодействии

      userInteracted = true;
      // Ставим флаг

      clearInterval(autoPlayInterval);
      // Очищаем интервал
    }
  }

  // ===== Ресайз =====

  window.addEventListener('resize', () => {
    // Изменение размера окна

    jumpTo(currentIndex);
    // Мгновенно пересчитываем позицию без анимации
  });

  // ===== Инициализация =====

  jumpTo(currentIndex);
  // Начальная позиция без анимации

  startAutoPlay();
  // Запуск автопрокрутки

})();
