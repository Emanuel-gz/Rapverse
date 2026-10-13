'use strict';

(() => {
  function initializeGallery() {
    const gallery = document.querySelector('#galeria');
    if (!gallery) return;

    const photos = [...gallery.querySelectorAll('a.photo-link[href]')];
    const filters = [...gallery.querySelectorAll('.gallery-filter[data-gallery-filter]')];
    const count = gallery.querySelector('#gallery-count');
    const dialog = document.querySelector('#photo-dialog');
    const fullImage = document.querySelector('#photo-full');
    const title = document.querySelector('#photo-dialog-title');
    const position = document.querySelector('#photo-position');
    const closeButton = document.querySelector('#photo-close');
    const previousButton = document.querySelector('#photo-prev');
    const nextButton = document.querySelector('#photo-next');
    const supportedFilters = new Set(['all', 'carti', 'cochise']);
    const selectedFilter = filters.find((button) => button.getAttribute('aria-pressed') === 'true');
    let activeFilter = supportedFilters.has(selectedFilter?.dataset.galleryFilter)
      ? selectedFilter.dataset.galleryFilter
      : 'all';
    let currentPhoto = null;
    let originPhoto = null;
    let scrollState = null;

    function photoContainer(photo) {
      const container = photo.closest('.photo-card, figure');
      return container && gallery.contains(container) ? container : photo;
    }

    function visiblePhotos() {
      return photos.filter((photo) => !photo.hidden && !photoContainer(photo).hidden);
    }

    function focusElement(element) {
      if (element && typeof element.focus === 'function') element.focus({ preventScroll: true });
    }

    function updateNavigation(selection) {
      const index = selection.indexOf(currentPhoto);
      if (position) position.textContent = index < 0 ? '' : `${index + 1} / ${selection.length}`;
      if (previousButton) previousButton.disabled = selection.length < 2;
      if (nextButton) nextButton.disabled = selection.length < 2;
    }

    function showPhoto(photo) {
      if (!photo || !fullImage) return;
      const thumbnail = photo.querySelector('img');
      const caption = photo.dataset.caption?.trim() || '';
      const description = thumbnail?.getAttribute('alt')?.trim() || '';
      fullImage.src = photo.href;
      fullImage.alt = description || caption;
      if (title) title.textContent = caption || description || 'Fotografía de la galería';
      currentPhoto = photo;
      updateNavigation(visiblePhotos());
    }

    function lockScroll() {
      if (scrollState || !document.body) return;
      scrollState = {
        value: document.body.style.getPropertyValue('overflow'),
        priority: document.body.style.getPropertyPriority('overflow'),
      };
      document.body.style.setProperty('overflow', 'hidden');
    }

    function restoreScroll() {
      if (!scrollState || !document.body) return;
      if (scrollState.value) {
        document.body.style.setProperty('overflow', scrollState.value, scrollState.priority);
      } else {
        document.body.style.removeProperty('overflow');
      }
      scrollState = null;
    }

    function closePhoto() {
      if (dialog?.open && typeof dialog.close === 'function') dialog.close();
    }

    function applyFilter(filter) {
      if (!supportedFilters.has(filter)) return;
      activeFilter = filter;
      photos.forEach((photo) => {
        const hidden = filter !== 'all' && photo.dataset.artist !== filter;
        photo.hidden = hidden;
        photoContainer(photo).hidden = hidden;
      });
      filters.forEach((button) => {
        const selected = button.dataset.galleryFilter === filter;
        button.setAttribute('aria-pressed', String(selected));
        button.classList.toggle('selected', selected);
      });
      const selection = visiblePhotos();
      if (count) {
        count.textContent = `${selection.length} ${selection.length === 1 ? 'FOTOGRAFÍA' : 'FOTOGRAFÍAS'}`;
      }
      if (dialog?.open && !selection.includes(currentPhoto)) {
        if (selection.length) showPhoto(selection[0]);
        else closePhoto();
      } else {
        updateNavigation(selection);
      }
    }

    filters.forEach((button) => {
      button.addEventListener('click', () => applyFilter(button.dataset.galleryFilter));
    });
    applyFilter(activeFilter);

    // Unsupported browsers keep the original image links fully usable.
    if (!dialog || !fullImage || typeof dialog.showModal !== 'function'
      || typeof dialog.close !== 'function') return;

    photos.forEach((photo) => {
      photo.addEventListener('click', (event) => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey
          || event.ctrlKey || event.shiftKey || event.altKey || !visiblePhotos().includes(photo)) return;
        showPhoto(photo);
        if (!dialog.open) {
          try {
            dialog.showModal();
          } catch {
            return;
          }
        }
        event.preventDefault();
        originPhoto = photo;
        lockScroll();
        focusElement(closeButton || dialog);
      });
    });

    function navigatePhoto(direction) {
      if (!dialog.open) return;
      const selection = visiblePhotos();
      if (!selection.length) {
        closePhoto();
        return;
      }
      const currentIndex = selection.indexOf(currentPhoto);
      const nextIndex = currentIndex < 0
        ? 0
        : (currentIndex + direction + selection.length) % selection.length;
      showPhoto(selection[nextIndex]);
    }

    closeButton?.addEventListener('click', closePhoto);
    previousButton?.addEventListener('click', () => navigatePhoto(-1));
    nextButton?.addEventListener('click', () => navigatePhoto(1));

    dialog.addEventListener('keydown', (event) => {
      if (!dialog.open || (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight')) return;
      event.preventDefault();
      event.stopPropagation();
      navigatePhoto(event.key === 'ArrowRight' ? 1 : -1);
    });

    dialog.addEventListener('click', (event) => {
      if (!dialog.open || event.target !== dialog) return;
      const bounds = dialog.getBoundingClientRect();
      const outside = event.clientX < bounds.left || event.clientX > bounds.right
        || event.clientY < bounds.top || event.clientY > bounds.bottom;
      if (outside) closePhoto();
    });

    dialog.addEventListener('close', () => {
      restoreScroll();
      const sourceVisible = originPhoto?.isConnected && visiblePhotos().includes(originPhoto);
      const activeButton = filters.find((button) => button.dataset.galleryFilter === activeFilter);
      focusElement(sourceVisible ? originPhoto : activeButton || visiblePhotos()[0]);
      originPhoto = null;
      currentPhoto = null;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGallery, { once: true });
  } else {
    initializeGallery();
  }
})();
