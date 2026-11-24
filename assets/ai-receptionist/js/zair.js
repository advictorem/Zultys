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
		if (!media || reduceMotion.matches) {
			document.documentElement.classList.remove('zair-hero-anim');
			return;
		}
		media.setAttribute('data-zair-hero', 'pending');
		function show() {
			requestAnimationFrame(function () {
				requestAnimationFrame(function () {
					media.setAttribute('data-zair-hero', 'in');
					document.documentElement.classList.remove('zair-hero-anim');
				});
			});
		}
		// Wait for the web font so the phone's text doesn't reflow mid-entrance.
		if (document.fonts && document.fonts.ready) {
			var done = false;
			document.fonts.ready.then(function () { if (!done) { done = true; show(); } });
			setTimeout(function () { if (!done) { done = true; show(); } }, 1200);
		} else show();

		// Parallax: the phone drifts up slightly as the page scrolls.
		var heroEl = $('.zair-hero');
		var ticking = false;
		function update() {
			ticking = false;
			var limit = heroEl.offsetTop + heroEl.offsetHeight + 200;
			var y = Math.min(Math.max(window.scrollY, 0), limit);
			var rate = window.innerWidth < 768 ? 0.05 : 0.09;
			media.style.setProperty('--zair-parallax', (-y * rate).toFixed(1) + 'px');
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

	/* Logo strip: pure CSS marquee; pauses on hover/focus, static for reduced motion. */

	/* ------------------------------------------------------------------
	 * Staging shell only: announcement dismiss + simple mobile menu.
	 * ------------------------------------------------------------------ */
	/* ------------------------------------------------------------------
	 * Voice demo players. Each card holds an <audio> element only once a
	 * recording URL is set (VOICE_DEMOS in the generator); without one the
	 * button and slider stay disabled and the card says "Recording coming
	 * soon". Starting one recording pauses the others.
	 * ------------------------------------------------------------------ */
	(function players() {
		var all = [];
		function fmt(t) {
			if (!isFinite(t) || t < 0) t = 0;
			var m = Math.floor(t / 60), s = Math.floor(t % 60);
			return m + ':' + (s < 10 ? '0' : '') + s;
		}
		$$('[data-zair-player]').forEach(function (el) {
			var audio = $('audio', el);
			if (!audio) return;
			var btn = $('.zair-player__btn', el);
			var seek = $('.zair-player__seek', el);
			var status = $('.zair-player__status', el);
			var cur = $('[data-zair-cur]', el);
			var dur = $('[data-zair-dur]', el);
			var label = btn.getAttribute('aria-label');
			all.push(audio);
			btn.disabled = false; seek.disabled = false;
			if (!el.classList.contains('is-playing')) status.textContent = 'Press play';

			function paint() {
				var d = audio.duration, pct = d ? (audio.currentTime / d) * 100 : 0;
				if (document.activeElement !== seek) seek.value = pct;
				seek.style.setProperty('--zair-seek', pct + '%');
				cur.textContent = fmt(audio.currentTime);
			}
			audio.addEventListener('loadedmetadata', function () { dur.textContent = fmt(audio.duration); });
			if (audio.readyState >= 1) dur.textContent = fmt(audio.duration);
			audio.addEventListener('timeupdate', paint);
			audio.addEventListener('play', function () {
				all.forEach(function (a) { if (a !== audio) a.pause(); });
				el.classList.add('is-playing');
				status.textContent = 'Playing';
				btn.setAttribute('aria-label', label.replace(/^Play/, 'Pause'));
			});
			audio.addEventListener('pause', function () {
				el.classList.remove('is-playing');
				status.textContent = audio.ended ? 'Press play to listen again' : 'Paused';
				btn.setAttribute('aria-label', label);
			});
			audio.addEventListener('ended', function () { audio.currentTime = 0; paint(); });
			audio.addEventListener('error', function () {
				status.textContent = 'This recording could not be loaded';
				btn.disabled = true; seek.disabled = true;
			});
			btn.addEventListener('click', function () {
				if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
				else audio.pause();
			});
			seek.addEventListener('input', function () {
				if (audio.duration) audio.currentTime = (seek.value / 100) * audio.duration;
				paint();
			});
		});
	})();

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
