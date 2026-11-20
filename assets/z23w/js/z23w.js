/*!
 * Zultys Z 23W product page interactions.
 * Dependency-free and scoped to the .z23w root, so it can be enqueued on the
 * WordPress page as-is. Each block is independent and exits quietly when its
 * markup is not present.
 */
(function () {
	'use strict';

	var root = document.querySelector('.z23w');
	if (!root) return;

	var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
	var $ = function (sel, ctx) { return (ctx || root).querySelector(sel); };
	var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || root).querySelectorAll(sel)); };

	/* ------------------------------------------------------------------
	 * Scroll reveal. Content is visible by default; only blocks that start
	 * below the fold are hidden, then revealed once as they scroll in.
	 * ------------------------------------------------------------------ */
	(function reveal() {
		var items = $$('[data-z23w-reveal]');
		if (!items.length || reduceMotion.matches || !('IntersectionObserver' in window)) return;

		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				entry.target.setAttribute('data-z23w-reveal', 'shown');
				io.unobserve(entry.target);
			});
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

		items.forEach(function (el) {
			if (el.getBoundingClientRect().top > window.innerHeight * 0.92) {
				el.setAttribute('data-z23w-reveal', 'pending');
				io.observe(el);
			}
		});

		// Keyboard users jumping into hidden content should never land on it invisible.
		root.addEventListener('focusin', function (e) {
			var hidden = e.target.closest('[data-z23w-reveal="pending"]');
			if (hidden) hidden.setAttribute('data-z23w-reveal', 'shown');
		});
	})();

	/* ------------------------------------------------------------------
	 * Module 4: Show More / Show Less. Three-line clamp at rest; each card
	 * expands on its own with an animated max-height.
	 * ------------------------------------------------------------------ */
	(function features() {
		var cards = $$('[data-z23w-feature]');
		if (!cards.length) return;

		function collapsedHeight(text) {
			return parseFloat(getComputedStyle(text).lineHeight) * 3;
		}

		cards.forEach(function (card) {
			var text = $('[data-z23w-feature-text]', card);
			var btn = $('[data-z23w-feature-toggle]', card);
			var label = $('[data-z23w-feature-label]', card);
			if (!text || !btn) return;

			text.setAttribute('data-clamped', '');

			function needsToggle() {
				if (btn.getAttribute('aria-expanded') === 'true') return true;
				return text.scrollHeight > collapsedHeight(text) + 2;
			}
			function sync() { btn.hidden = !needsToggle(); }

			function expand() {
				var from = text.offsetHeight;
				text.removeAttribute('data-clamped');
				text.style.maxHeight = from + 'px';
				// Force a frame so the transition starts from the clamped height.
				text.getBoundingClientRect();
				text.style.maxHeight = text.scrollHeight + 'px';
				btn.setAttribute('aria-expanded', 'true');
				label.textContent = 'Show Less';
			}
			function collapse() {
				text.style.maxHeight = text.scrollHeight + 'px';
				text.getBoundingClientRect();
				text.style.maxHeight = collapsedHeight(text) + 'px';
				btn.setAttribute('aria-expanded', 'false');
				label.textContent = 'Show More';
				if (reduceMotion.matches) finish();
			}
			function finish() {
				if (btn.getAttribute('aria-expanded') === 'true') {
					text.style.maxHeight = 'none'; // let it reflow freely on resize
				} else {
					text.style.maxHeight = '';
					text.setAttribute('data-clamped', '');
				}
			}

			text.addEventListener('transitionend', function (e) {
				if (e.propertyName === 'max-height') finish();
			});
			btn.addEventListener('click', function () {
				if (btn.getAttribute('aria-expanded') === 'true') collapse(); else expand();
				if (reduceMotion.matches) finish();
			});

			sync();
			window.addEventListener('resize', sync);
			if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
		});
	})();

	/* ------------------------------------------------------------------
	 * Module 6: phone suite carousel. Buttons, dots, arrow keys and swipe.
	 * Never advances on its own.
	 * ------------------------------------------------------------------ */
	(function carousel() {
		var el = $('[data-z23w-carousel]');
		if (!el) return;
		var viewport = $('[data-z23w-viewport]', el);
		var track = $('[data-z23w-track]', el);
		var slides = $$('[data-z23w-slide]', el);
		var dotsWrap = $('[data-z23w-dots]', el);
		var status = $('[data-z23w-status]', el);
		var count = slides.length;
		var index = 0;
		if (!track || count < 2) return;

		var dots = slides.map(function (slide, i) {
			var dot = document.createElement('button');
			dot.type = 'button';
			dot.className = 'z23w-carousel__dot';
			dot.setAttribute('aria-label', 'Show ' + slide.getAttribute('data-name'));
			dot.addEventListener('click', function () { go(i, true); });
			dotsWrap.appendChild(dot);
			return dot;
		});

		function render(announce) {
			track.style.transform = 'translateX(' + (-index * 100) + '%)';
			slides.forEach(function (slide, i) {
				var active = i === index;
				slide.classList.toggle('is-active', active);
				slide.inert = !active;
				slide.setAttribute('aria-hidden', active ? 'false' : 'true');
			});
			dots.forEach(function (dot, i) {
				if (i === index) dot.setAttribute('aria-current', 'true'); else dot.removeAttribute('aria-current');
			});
			if (announce && status) {
				status.textContent = slides[index].getAttribute('data-name') + ', ' + (index + 1) + ' of ' + count;
			}
		}
		function go(i, announce) {
			index = (i + count) % count;
			render(announce);
		}

		$('[data-z23w-prev]', el).addEventListener('click', function () { go(index - 1, true); });
		$('[data-z23w-next]', el).addEventListener('click', function () { go(index + 1, true); });

		el.addEventListener('keydown', function (e) {
			if (e.target.closest('input, select, textarea')) return;
			if (e.key === 'ArrowLeft') { e.preventDefault(); go(index - 1, true); }
			else if (e.key === 'ArrowRight') { e.preventDefault(); go(index + 1, true); }
			else if (e.key === 'Home') { e.preventDefault(); go(0, true); }
			else if (e.key === 'End') { e.preventDefault(); go(count - 1, true); }
		});

		// Swipe / drag. Vertical scrolling stays native (touch-action: pan-y).
		var startX = 0, startY = 0, dx = 0, dragging = false, moved = false, pointerId = null;
		viewport.addEventListener('pointerdown', function (e) {
			if (e.pointerType === 'mouse' && e.button !== 0) return;
			if (e.target.closest('a, button')) return;
			dragging = true; moved = false; dx = 0;
			startX = e.clientX; startY = e.clientY; pointerId = e.pointerId;
		});
		viewport.addEventListener('pointermove', function (e) {
			if (!dragging || e.pointerId !== pointerId) return;
			dx = e.clientX - startX;
			if (!moved) {
				if (Math.abs(dx) < 8) return;
				if (Math.abs(e.clientY - startY) > Math.abs(dx)) { dragging = false; return; }
				moved = true;
				viewport.classList.add('is-dragging');
				try { viewport.setPointerCapture(pointerId); } catch (err) { /* noop */ }
			}
			var pct = (dx / viewport.clientWidth) * 100;
			track.style.transform = 'translateX(' + (-index * 100 + pct) + '%)';
		});
		function endDrag() {
			if (!dragging) return;
			dragging = false;
			viewport.classList.remove('is-dragging');
			if (!moved) return;
			var threshold = Math.min(90, viewport.clientWidth * 0.18);
			if (dx <= -threshold) go(index + 1, true);
			else if (dx >= threshold) go(index - 1, true);
			else render(false);
		}
		viewport.addEventListener('pointerup', endDrag);
		viewport.addEventListener('pointercancel', endDrag);
		viewport.addEventListener('lostpointercapture', endDrag);
		// A drag must not trigger the slide's link.
		viewport.addEventListener('click', function (e) {
			if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
		}, true);

		render(false);
	})();

	/* ------------------------------------------------------------------
	 * Module 3: video dialog. Native <dialog> gives focus trapping, Esc and
	 * focus return. The MP4 is attached only when first opened.
	 * ------------------------------------------------------------------ */
	(function video() {
		var dialog = document.querySelector('[data-z23w-video-dialog]');
		var openers = $$('[data-z23w-video-open]');
		if (!dialog || !openers.length) return;
		var player = dialog.querySelector('[data-z23w-video]');
		var closeBtn = dialog.querySelector('[data-z23w-video-close]');

		function open() {
			if (!player.getAttribute('src')) player.setAttribute('src', player.getAttribute('data-src'));
			if (typeof dialog.showModal === 'function') dialog.showModal();
			else { window.open(player.getAttribute('data-src'), '_blank', 'noopener'); return; }
			var p = player.play();
			if (p && p.catch) p.catch(function () { /* autoplay blocked: controls remain */ });
		}
		openers.forEach(function (btn) { btn.addEventListener('click', open); });
		closeBtn.addEventListener('click', function () { dialog.close(); });
		dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
		dialog.addEventListener('close', function () { player.pause(); });
	})();

	/* ------------------------------------------------------------------
	 * Module 7: staging form. Validates like the live form but does not
	 * submit anywhere. WordPress replaces this markup with Gravity Forms,
	 * at which point this block simply finds nothing to bind to.
	 * ------------------------------------------------------------------ */
	(function quoteForm() {
		var form = $('[data-z23w-quote-form]');
		if (!form) return;
		var status = $('[data-z23w-form-status]', form);

		function message(field) {
			var label = form.querySelector('label[for="' + field.id + '"]');
			var name = label ? label.textContent.replace('*', '').trim() : 'This field';
			if (name.length > 24) name = 'This field';
			if (field.validity.valueMissing) return name + ' is required.';
			if (field.validity.typeMismatch && field.type === 'email') return 'Enter a valid email address, like name@company.com.';
			if (field.type === 'tel' && field.value.replace(/\D/g, '').length < 10) return 'Enter a phone number with at least 10 digits.';
			return '';
		}
		function check(field) {
			var msg = message(field);
			var err = document.getElementById(field.id + '-error');
			field.setAttribute('aria-invalid', msg ? 'true' : 'false');
			if (err) err.textContent = msg;
			return !msg;
		}
		var fields = $$('input, select, textarea', form);
		fields.forEach(function (field) {
			field.addEventListener('blur', function () { if (field.value || field.getAttribute('aria-invalid') === 'true') check(field); });
			field.addEventListener('input', function () { if (field.getAttribute('aria-invalid') === 'true') check(field); });
		});
		form.addEventListener('submit', function (e) {
			e.preventDefault();
			var firstBad = null;
			fields.forEach(function (field) { if (!check(field) && !firstBad) firstBad = field; });
			if (firstBad) {
				status.textContent = 'Please fix the highlighted fields.';
				firstBad.focus();
				return;
			}
			status.textContent = 'Looks good, but nothing was sent: this staging preview is not connected to the Zultys form system yet.';
		});
	})();

	/* ------------------------------------------------------------------
	 * Staging shell only: announcement dismiss + simple mobile menu.
	 * ------------------------------------------------------------------ */
	(function shell() {
		var dismiss = $('[data-z23w-dismiss]');
		if (dismiss) dismiss.addEventListener('click', function () { dismiss.closest('[data-z23w-announcement]').hidden = true; });
		var toggle = $('[data-z23w-menu-toggle]');
		var menu = document.getElementById('z23w-mobile-menu');
		if (!toggle || !menu) return;
		toggle.addEventListener('click', function () {
			var open = toggle.getAttribute('aria-expanded') === 'true';
			toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
			toggle.setAttribute('aria-label', open ? 'Open navigation menu' : 'Close navigation menu');
			menu.hidden = open;
		});
		menu.addEventListener('click', function (e) {
			if (e.target.closest('a[href^="#"]')) { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); }
		});
	})();
})();
