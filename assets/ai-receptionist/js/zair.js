/*!
 * Zultys AI Receptionist page interactions.
 * Dependency-free and scoped to the .zair root. Same behaviours as the
 * Z 23W page: scroll reveal, hero entrance + parallax, background wave.
 */
(function () {
	'use strict';

	var root = document.querySelector('.zair');
	if (!root) return;

	var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
	var $ = function (sel, ctx) { return (ctx || root).querySelector(sel); };
	var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || root).querySelectorAll(sel)); };

	/* ------------------------------------------------------------------
	 * Hero: the caller photo fades and rises in once it has loaded, the
	 * conversation bubbles follow in sequence (CSS delays), and the photo
	 * drifts gently inside its frame as the page scrolls.
	 * ------------------------------------------------------------------ */
	(function hero() {
		var media = $('.zair-hero__media');
		var img = media && media.querySelector('.zair-hero__photo img');
		if (!media || !img || reduceMotion.matches) {
			document.documentElement.classList.remove('zair-hero-anim');
			return;
		}
		media.setAttribute('data-zair-hero', 'pending');
		var shown = false;
		function show() {
			if (shown) return;
			shown = true;
			requestAnimationFrame(function () {
				requestAnimationFrame(function () {
					media.setAttribute('data-zair-hero', 'in');
					document.documentElement.classList.remove('zair-hero-anim');
				});
			});
		}
		if (img.complete && img.naturalWidth) show();
		else {
			img.addEventListener('load', show, { once: true });
			img.addEventListener('error', show, { once: true });
			setTimeout(show, 2500);
		}

		var heroEl = $('.zair-hero');
		var ticking = false;
		function update() {
			ticking = false;
			var limit = heroEl.offsetTop + heroEl.offsetHeight + 200;
			var y = Math.min(Math.max(window.scrollY, 0), limit);
			var rate = window.innerWidth < 768 ? 0.04 : 0.07;
			media.style.setProperty('--zair-parallax', (y * rate).toFixed(1) + 'px');
		}
		window.addEventListener('scroll', function () {
			if (!ticking) { ticking = true; requestAnimationFrame(update); }
		}, { passive: true });
		update();
	})();

	/* ------------------------------------------------------------------
	 * Scroll reveal: only blocks that start below the fold are hidden.
	 * ------------------------------------------------------------------ */
	(function reveal() {
		var items = $$('[data-zair-reveal]');
		if (!items.length || reduceMotion.matches || !('IntersectionObserver' in window)) return;
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				entry.target.setAttribute('data-zair-reveal', 'shown');
				io.unobserve(entry.target);
			});
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
		items.forEach(function (el) {
			if (el.getBoundingClientRect().top > window.innerHeight * 0.92) {
				el.setAttribute('data-zair-reveal', 'pending');
				io.observe(el);
			}
		});
		root.addEventListener('focusin', function (e) {
			var hidden = e.target.closest('[data-zair-reveal="pending"]');
			if (hidden) hidden.setAttribute('data-zair-reveal', 'shown');
		});
	})();

	/* ------------------------------------------------------------------
	 * Results background: the site's dotted traveling wave
	 * (window.z26CreateSpotlightWave from vendor/zultys-wave.js). Runs only
	 * while on screen, with a pause control; phones, reduced-motion and
	 * data-saver visitors get a still frame.
	 * ------------------------------------------------------------------ */
	(function wave() {
		var host = $('[data-zair-wave]');
		var button = $('[data-zair-wave-toggle]');
		if (!host || typeof window.z26CreateSpotlightWave !== 'function') return;
		var controller;
		try { controller = window.z26CreateSpotlightWave(host); } catch (err) { controller = null; }
		if (!controller) return;
		var phone = window.matchMedia('(max-width: 767px)');
		var connection = navigator.connection;
		var inView = false, userPaused = false;
		function canAnimate() { return !reduceMotion.matches && !phone.matches && !(connection && connection.saveData); }
		function sync() {
			var animate = canAnimate();
			controller.setEnabled(true);
			controller.setRunning(animate && inView && !userPaused && !document.hidden);
			if (button) {
				button.hidden = !animate;
				button.setAttribute('aria-label', (userPaused ? 'Play' : 'Pause') + ' background animation');
			}
		}
		if (button) button.addEventListener('click', function () { userPaused = !userPaused; sync(); });
		if ('IntersectionObserver' in window) {
			new IntersectionObserver(function (entries) { inView = entries[0].isIntersecting; sync(); }).observe(host);
		} else { inView = true; }
		document.addEventListener('visibilitychange', sync);
		[reduceMotion, phone].forEach(function (mq) {
			if (mq.addEventListener) mq.addEventListener('change', sync); else if (mq.addListener) mq.addListener(sync);
		});
		sync();
	})();

	/* ------------------------------------------------------------------
	 * Logo strip: CSS marquee that pauses on hover/focus; the button
	 * gives a persistent pause (WCAG 2.2.2). Reduced motion: no animation.
	 * ------------------------------------------------------------------ */
	(function marquee() {
		var strip = $('[data-zair-marquee]');
		var button = $('[data-zair-marquee-toggle]');
		if (!strip || !button) return;
		if (reduceMotion.matches) { button.hidden = true; return; }
		button.addEventListener('click', function () {
			var paused = strip.classList.toggle('is-paused');
			button.setAttribute('aria-label', (paused ? 'Play' : 'Pause') + ' logo animation');
		});
	})();

	/* ------------------------------------------------------------------
	 * Staging shell only: announcement dismiss + simple mobile menu.
	 * ------------------------------------------------------------------ */
	(function shell() {
		var dismiss = $('[data-zair-dismiss]');
		if (dismiss) dismiss.addEventListener('click', function () { dismiss.closest('[data-zair-announcement]').hidden = true; });
		var toggle = $('[data-zair-menu-toggle]');
		var menu = document.getElementById('zair-mobile-menu');
		if (!toggle || !menu) return;
		toggle.addEventListener('click', function () {
			var open = toggle.getAttribute('aria-expanded') === 'true';
			toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
			toggle.setAttribute('aria-label', open ? 'Open navigation menu' : 'Close navigation menu');
			menu.hidden = open;
		});
	})();
})();
