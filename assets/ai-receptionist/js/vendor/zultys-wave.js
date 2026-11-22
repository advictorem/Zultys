/* Native, responsive wave surfaces for approved Homepage decorations. */
(function (window, document) {
	'use strict';

	if (!window || !document || window.z26CreateSpotlightWave) return;

	var TAU = Math.PI * 2;
	var MAX_POINTS = 2500;
	var ROWS = 20;
	var LINE_CURVES = 30;
	var LINE_SEGMENTS = 72;
	var MAX_DPR = 1.5;
	var FRAME_INTERVAL = 1000 / 30;
	var PERIOD_MS = 9000;
	var SECONDARY_PERIOD_MS = 10500;
	var DOT_COLORS = [
		'rgba(153, 199, 235, .15)',
		'rgba(153, 199, 235, .18)',
		'rgba(153, 199, 235, .21)',
		'rgba(153, 199, 235, .24)',
		'rgba(153, 199, 235, .27)',
		'rgba(153, 199, 235, .30)',
		'rgba(153, 199, 235, .33)',
		'rgba(153, 199, 235, .36)',
		'rgba(153, 199, 235, .39)',
		'rgba(153, 199, 235, .42)',
		'rgba(153, 199, 235, .46)',
		'rgba(153, 199, 235, .50)'
	];

	function clamp(value, minimum, maximum) {
		return Math.max(minimum, Math.min(maximum, value));
	}

	function smoothstep(start, end, value) {
		var progress = clamp((value - start) / (end - start), 0, 1);
		return progress * progress * (3 - 2 * progress);
	}

	function clockNow() {
		if (window.performance && typeof window.performance.now === 'function') {
			return window.performance.now();
		}
		return Date.now();
	}

	/*
	 * Public contract: return a small controller for the existing decoration host.
	 * Geometry samples a traveling 3D-like surface; elapsed time is held while paused.
	 */
	window.z26CreateSpotlightWave = function (host, options) {
		options = options || {};
		var lineMode = options.mode === 'lines';
		var readyClassTarget = options.readyClassTarget && options.readyClassTarget.classList ? options.readyClassTarget : null;
		var readyClass = typeof options.readyClass === 'string' && options.readyClass ? options.readyClass : '';
		if (
			!host ||
			!host.classList ||
			typeof host.appendChild !== 'function' ||
			typeof host.getBoundingClientRect !== 'function' ||
			typeof window.requestAnimationFrame !== 'function' ||
			typeof window.cancelAnimationFrame !== 'function' ||
			typeof document.createElement !== 'function'
		) return null;

		var canvas;
		var context;
		try {
			canvas = document.createElement('canvas');
			context = canvas.getContext && canvas.getContext('2d');
			if (!context) return null;
			if (lineMode && (typeof context.moveTo !== 'function' || typeof context.lineTo !== 'function' || typeof context.stroke !== 'function')) return null;
			if (!lineMode && (typeof context.arc !== 'function' || typeof context.fill !== 'function')) return null;

			canvas.className = 'z26-live-wave';
			canvas.setAttribute('aria-hidden', 'true');
			canvas.setAttribute('focusable', 'false');
			canvas.style.position = 'absolute';
			canvas.style.inset = '0';
			canvas.style.display = 'block';
			canvas.style.width = '100%';
			canvas.style.height = '100%';
			canvas.style.pointerEvents = 'none';
			canvas.style.visibility = 'hidden';

			host.appendChild(canvas);
		} catch (error) {
			return null;
		}

		var enabled = false;
		var running = false;
		var frameId = 0;
		var lastClock = null;
		var elapsed = 0;
		var lastFrame = -Infinity;
		var width = 0;
		var height = 0;
		var dpr = 1;
		var columns = 0;
		var observer = null;
		var destroyed = false;

		function stopFrame() {
			if (frameId) {
				window.cancelAnimationFrame(frameId);
				frameId = 0;
			}
		}

		function readSize() {
			var bounds = host.getBoundingClientRect();
			var nextWidth = Math.max(0, bounds.width || host.clientWidth || 0);
			var nextHeight = Math.max(0, bounds.height || host.clientHeight || 0);
			if (!nextWidth || !nextHeight) return false;

			var nextDpr = clamp(Number(window.devicePixelRatio) || 1, 1, MAX_DPR);
			var backingWidth = Math.max(1, Math.round(nextWidth * nextDpr));
			var backingHeight = Math.max(1, Math.round(nextHeight * nextDpr));
			var changed = width !== nextWidth || height !== nextHeight || dpr !== nextDpr;

			width = nextWidth;
			height = nextHeight;
			dpr = nextDpr;
			columns = lineMode ? LINE_SEGMENTS : Math.max(12, Math.min(Math.floor(MAX_POINTS / ROWS), Math.ceil(width / 12)));

			if (canvas.width !== backingWidth) canvas.width = backingWidth;
			if (canvas.height !== backingHeight) canvas.height = backingHeight;
			if (changed) context.setTransform(dpr, 0, 0, dpr, 0, 0);
			return changed;
		}

		function setReady(isReady) {
			if (isReady) host.classList.add('z26-live-wave-ready');
			else host.classList.remove('z26-live-wave-ready');
			if (readyClassTarget && readyClass) readyClassTarget.classList[isReady ? 'add' : 'remove'](readyClass);
		}

		function sampleSurface(u, depth, width, height, wavePhase, secondaryPhase) {
			var phase = TAU * (u * 1.25 + depth * 0.28) - wavePhase;
			var phase2 = TAU * (u * 1.35 - depth * 0.36 + 0.13) - secondaryPhase;
			var wave = Math.sin(phase);
			var secondary = Math.sin(phase2);
			var envelope = smoothstep(lineMode ? 0.12 : 0.24, 0.98, u);
			var top = lineMode
				? height * (0.12 - envelope * 0.05)
				: height * (0.72 - envelope * 0.12);
			var verticalSpread = lineMode ? height * 0.54 : height * 0.22;
			var yOffset = depth * verticalSpread;
			var waveAmplitude = height * (lineMode ? 0.075 + depth * 0.03 : 0.12 + depth * 0.03);
			var secondaryAmplitude = height * (lineMode ? 0.018 + depth * 0.012 : 0.025 + depth * 0.01);
			var y = top + yOffset + wave * waveAmplitude + secondary * secondaryAmplitude;
			var x = u * width + Math.cos(phase + depth * 0.3) * (2 + depth * 12);
			var surfaceSlope = Math.atan2(
				waveAmplitude * Math.cos(phase) + secondaryAmplitude * Math.cos(phase2),
				width / Math.max(1, columns - 1)
			);
			var crestLight = 0.5 + 0.5 * Math.sin(phase + surfaceSlope);
			return { x: x, y: y, phase: phase, phase2: phase2, waveAmplitude: waveAmplitude, secondaryAmplitude: secondaryAmplitude, crestLight: crestLight };
		}

		function lineColor(alpha) {
			return 'rgba(153, 199, 235, ' + clamp(alpha, 0.01, 0.58).toFixed(3) + ')';
		}

		function drawLines(width, height, wavePhase, secondaryPhase) {
			var gradient = null;
			if (typeof context.createLinearGradient === 'function') {
				gradient = context.createLinearGradient(0, 0, width, 0);
				gradient.addColorStop(0, 'rgba(153, 199, 235, .16)');
				gradient.addColorStop(0.16, 'rgba(153, 199, 235, .42)');
				gradient.addColorStop(0.38, 'rgba(153, 199, 235, .58)');
				gradient.addColorStop(0.52, 'rgba(153, 199, 235, .44)');
				gradient.addColorStop(0.7, 'rgba(153, 199, 235, .18)');
				gradient.addColorStop(1, 'rgba(153, 199, 235, .025)');
			}

			for (var curve = 0; curve < LINE_CURVES; curve += 1) {
				var depth = curve / (LINE_CURVES - 1);
				var depthAlpha = 0.86 - depth * 0.42;
				context.globalAlpha = depthAlpha;
				context.strokeStyle = gradient || lineColor(0.34 * depthAlpha);
				context.lineWidth = 1 + depth * 0.75;
				context.lineCap = 'round';
				context.lineJoin = 'round';
				context.beginPath();
				for (var segment = 0; segment < LINE_SEGMENTS; segment += 1) {
					var u = segment / (LINE_SEGMENTS - 1);
					var point = sampleSurface(u, depth, width, height, wavePhase, secondaryPhase);
					if (segment === 0) context.moveTo(point.x, point.y);
					else context.lineTo(point.x, point.y);
				}
				context.stroke();
			}
			context.globalAlpha = 1;
		}

		function drawFrame() {
			if (!width || !height) readSize();
			if (!width || !height || !columns) return false;

			try {
				context.clearRect(0, 0, width, height);
				/* Testimonial lines travel four times more slowly than the Spotlight dots. */
				var seconds = elapsed / 1000 * (lineMode ? 0.25 : 1);
				var wavePhase = TAU * seconds / (PERIOD_MS / 1000);
				var secondaryPhase = TAU * seconds / (SECONDARY_PERIOD_MS / 1000);

				if (lineMode) {
					/* Keep the same traveling geometry, composed as a fine line mesh for the quote panel. */
					drawLines(width, height, wavePhase, secondaryPhase);
				} else {
					/* Project the shared traveling surface into staggered light-blue dots. */
					var rows = ROWS;
					for (var row = 0; row < rows; row += 1) {
						var depth = row / (rows - 1);
						for (var column = 0; column < columns; column += 1) {
							var u = column / (columns - 1);
							var point = sampleSurface(u, depth, width, height, wavePhase, secondaryPhase);
							var x = point.x;
							var y = point.y;
							if (y < 0 || y > height || x < 0 || x > width) continue;

							var leftFade = 0.18 + 0.82 * smoothstep(width * 0.02, width * 0.44, x);
							var topFade = smoothstep(height * 0.38, height * 0.76, y);
							var bottomFade = 1 - smoothstep(height * 0.9, height, y);
							var copyAreaFade = 1 - 0.62 * smoothstep(width * 0.54, width * 0.83, x) *
								(1 - smoothstep(height * 0.55, height * 0.86, y));
							var alpha = (0.15 + depth * 0.15 + point.crestLight * 0.2) * leftFade * topFade * bottomFade * copyAreaFade;
							if (alpha < 0.025) continue;

							var colorIndex = clamp(
								Math.round((alpha - 0.15) * (DOT_COLORS.length - 1) / 0.35),
								0,
								DOT_COLORS.length - 1
							);
							var radius = 1 + depth * 0.9 + point.crestLight * 0.4;
							context.fillStyle = DOT_COLORS[colorIndex];
							context.beginPath();
							context.arc(x, y, radius, 0, TAU);
							context.fill();
						}
					}
				}

				if (enabled) {
					canvas.style.visibility = 'visible';
					setReady(true);
				}
				lastFrame = clockNow();
				return true;
			} catch (error) {
				return false;
			}
		}

		function fail() {
			stopFrame();
			running = false;
			enabled = false;
			canvas.style.visibility = 'hidden';
			setReady(false);
		}

		function schedule() {
			if (!destroyed && enabled && running && !document.hidden && !frameId && width && height) {
				frameId = window.requestAnimationFrame(onFrame);
			}
		}

		function onFrame() {
			frameId = 0;
			if (destroyed || !enabled || !running || document.hidden) return;

			var current = clockNow();
			if (lastClock !== null) elapsed += Math.max(0, current - lastClock);
			lastClock = current;
			if (current - lastFrame >= FRAME_INTERVAL - 1) {
				if (!drawFrame()) {
					fail();
					return;
				}
			}
			schedule();
		}

		function resize() {
			var changed = readSize();
			if (changed && enabled && !drawFrame()) {
				fail();
				return;
			}
			if (enabled && running) schedule();
		}

		function setEnabled(nextEnabled) {
			if (destroyed) return;
			enabled = !!nextEnabled;
			if (!enabled) {
				if (running && lastClock !== null) elapsed += Math.max(0, clockNow() - lastClock);
				stopFrame();
				running = false;
				lastClock = null;
				canvas.style.visibility = 'hidden';
				setReady(false);
				if (width && height) context.clearRect(0, 0, width, height);
				return;
			}

			canvas.style.visibility = 'visible';
			if (!drawFrame()) {
				canvas.style.visibility = 'hidden';
				setReady(false);
			}
		}

		function setRunning(nextRunning) {
			if (destroyed) return;
			nextRunning = !!nextRunning;
			if (!nextRunning) {
				if (running && lastClock !== null) elapsed += Math.max(0, clockNow() - lastClock);
				running = false;
				lastClock = null;
				stopFrame();
				if (enabled && !drawFrame()) fail();
				return;
			}

			running = true;
			if (enabled && !document.hidden) {
				if (lastClock === null) lastClock = clockNow();
				if (!drawFrame()) {
					fail();
					return;
				}
				schedule();
			}
		}

		function destroy() {
			if (destroyed) return;
			destroyed = true;
			stopFrame();
			if (observer) observer.disconnect();
			else if (typeof window.removeEventListener === 'function') window.removeEventListener('resize', resize);
			canvas.remove();
			setReady(false);
		}

		try {
			if (typeof window.ResizeObserver === 'function') {
				observer = new window.ResizeObserver(resize);
				observer.observe(host);
			} else if (typeof window.addEventListener === 'function') {
				window.addEventListener('resize', resize, { passive: true });
			}
			resize();
		} catch (error) {
			destroy();
			return null;
		}

		return {
			setEnabled: setEnabled,
			setRunning: setRunning,
			destroy: destroy
		};
	};
})(window, document);
