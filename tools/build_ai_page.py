"""Generates zultys-ai-receptionist/index.html.

All copy is taken verbatim from the current zultys.com AI Receptionist page
(headings converted from all caps to title case). Icons are drawn here as
inline SVG in the redesign's line style: royal blue line work with green
accents, 2px strokes at any size.

Run: python3 tools/build_ai_page.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A = "/assets/ai-receptionist"

DEMO = "https://www.zultys.com/AI-Receptionist-demo-request/"
FLYER = "https://www.zultys.com/wp-content/uploads/2026/08/Zultys-AI-Receptionist-Product-Flyer-Overview_vJuly2026.pdf"
REQUEST_DEMO = "https://www.zultys.com/request-demo/"
REQUEST_QUOTE = "https://www.zultys.com/get-a-quote/"

# 24px grid. Blue line work uses currentColor; elements with class "a" are the green accent.
ICONS = {
    "always": '<circle cx="12" cy="8.6" r="4.1"/><path class="a" d="M10.2 8.7l1.3 1.3 2.5-2.6"/><path class="a" d="M5.3 6.2a7.2 7.2 0 0 1 13.4 0" stroke-dasharray="0 2.6"/><path d="M2.5 15.2h2.7v6H2.5z"/><path d="M5.2 16.3l2.9-1.4h4.4a1.5 1.5 0 0 1 0 3H9.3"/><path d="M5.2 20.2h7.7l6.6-3.9a1.4 1.4 0 0 0-1.5-2.4l-4.2 2.4"/>',
    "intelligence": '<rect x="6" y="6" width="12" height="12" rx="2.2"/><path d="M9.5 3v3M14.5 3v3M9.5 18v3M14.5 18v3M3 9.5h3M3 14.5h3M18 9.5h3M18 14.5h3"/><path class="a" d="M12 8.4c.3 2 1.3 3 3.3 3.3-2 .3-3 1.3-3.3 3.3-.3-2-1.3-3-3.3-3.3 2-.3 3-1.3 3.3-3.3z"/>',
    "scale": '<circle cx="12" cy="13.6" r="7.4"/><path d="M9.8 3h4.4M12 3v3.2M18.2 6.6l1.6-1.6"/><path class="a" d="M12 13.6l3.2-3.2"/><path class="a" d="M12 8.2v1M17.4 13.6h-1M12 19v-1M6.6 13.6h1"/>',
    "sources": '<ellipse cx="11" cy="5.6" rx="7" ry="2.6"/><path d="M4 5.6v11.8c0 1.4 3.1 2.6 7 2.6.4 0 .8 0 1.2-.1M18 5.6v5.6"/><path d="M4 11.5c0 1.4 3.1 2.6 7 2.6 1 0 2-.1 2.8-.2"/><circle class="a" cx="17.6" cy="17.4" r="4.4"/><path class="a" d="M15.8 17.5l1.3 1.3 2.4-2.6"/>',
    "transfer": '<path d="M21.5 16.4v2.9a1.9 1.9 0 0 1-2.1 1.9 18.9 18.9 0 0 1-8.2-2.9 18.6 18.6 0 0 1-5.7-5.7 18.9 18.9 0 0 1-2.9-8.3A1.9 1.9 0 0 1 4.5 2.2h2.9a1.9 1.9 0 0 1 1.9 1.6c.1.9.4 1.8.7 2.7a1.9 1.9 0 0 1-.4 2L8.3 9.7a15.2 15.2 0 0 0 5.7 5.7l1.2-1.2a1.9 1.9 0 0 1 2-.4c.9.3 1.8.6 2.7.7a1.9 1.9 0 0 1 1.6 1.9z"/><path class="a" d="M17.5 2.2l3.6 3.6-3.6 3.6M13.6 5.8h7.5"/>',
    "access": '<circle cx="9" cy="7.6" r="3.6"/><path d="M2.8 20.2c0-3.4 2.8-6.2 6.2-6.2 1.6 0 3 .6 4.1 1.5"/><path class="a" d="M17.6 11.6l3.6 1.4v2.9c0 2.4-1.5 4.4-3.6 5-2.1-.6-3.6-2.6-3.6-5v-2.9z"/><path class="a" d="M16.3 16.3l1 1 1.7-1.8"/>',
    "shield": '<path d="M12 2.6l7.4 2.9v5.9c0 4.8-3.1 8.7-7.4 10-4.3-1.3-7.4-5.2-7.4-10V5.5z"/><path class="a" d="M8.6 12l2.3 2.3 4.5-4.6"/>',
    "sentiment": '<path d="M2.8 10.5v3M6.2 7.5v9M9.6 4.5v15M13 8.5v7"/><circle class="a" cx="18" cy="16.6" r="4.2"/><path class="a" d="M16.4 17.5c.9.9 2.3.9 3.2 0M16.6 15.3h.01M19.4 15.3h.01"/>',
    "nomiss": '<path d="M21.5 16.4v2.9a1.9 1.9 0 0 1-2.1 1.9 18.9 18.9 0 0 1-8.2-2.9 18.6 18.6 0 0 1-5.7-5.7 18.9 18.9 0 0 1-2.9-8.3A1.9 1.9 0 0 1 4.5 2.2h2.9a1.9 1.9 0 0 1 1.9 1.6c.1.9.4 1.8.7 2.7a1.9 1.9 0 0 1-.4 2L8.3 9.7a15.2 15.2 0 0 0 5.7 5.7l1.2-1.2a1.9 1.9 0 0 1 2-.4c.9.3 1.8.6 2.7.7a1.9 1.9 0 0 1 1.6 1.9z"/><path class="a" d="M14.6 6.2l1.9 1.9 3.9-4"/>',
    "frontdesk": '<path d="M4.8 17.6a7.2 7.2 0 0 1 14.4 0M12 10.4V8.6M10.2 8.6h3.6"/><path d="M3 17.6h18"/><path class="a" d="M5 20.6h14"/><path class="a" d="M18.6 3.2v2.4M17.4 4.4h2.4"/>',
    "overhead": '<path d="M3 3v18h18"/><path class="a" d="M7 7.5l4.2 4.2 3-3 5.3 5.3"/><path class="a" d="M19.5 9.8v4.2h-4.2"/>',
    "dtmf": '<rect x="4.6" y="2.6" width="5.2" height="9.6" rx="2.6"/><path d="M2.6 10a4.6 4.6 0 0 0 9.2 0M7.2 14.6v3.4M5 18h4.4"/><g class="a" fill="currentColor" stroke="none"><circle cx="15" cy="5" r="1.05"/><circle cx="18" cy="5" r="1.05"/><circle cx="21" cy="5" r="1.05"/><circle cx="15" cy="8.6" r="1.05"/><circle cx="18" cy="8.6" r="1.05"/><circle cx="21" cy="8.6" r="1.05"/><circle cx="15" cy="12.2" r="1.05"/><circle cx="18" cy="12.2" r="1.05"/><circle cx="21" cy="12.2" r="1.05"/><circle cx="18" cy="15.8" r="1.05"/></g>',
}


def icon(name, cls=""):
    return (f'<svg class="zair-icon {cls}".strip() viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>').replace('".strip()', '"').replace('zair-icon "', 'zair-icon"')


def pic(name, widths, sizes, w, h, alt, cls="", lazy=True, extra=""):
    srcset = ", ".join(f"{A}/img/{name}-{x}.webp {x}w" for x in widths)
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture>\n\t\t\t\t\t<source type="image/webp" srcset="{srcset}" sizes="{sizes}">\n'
            f'\t\t\t\t\t<img{c} src="{A}/img/{name}.jpg" width="{w}" height="{h}" alt="{alt}" {load}{extra}>\n\t\t\t\t</picture>')


COVERAGE = [
    ("always", "Always Available", "Answers every call instantly with natural, conversational interactions — no hold music, no rigid menus."),
    ("intelligence", "Context Intelligence", "Identifies caller intent, filters spam, and transfers with context so customers never repeat themselves."),
    ("scale", "Consistent Performance at Scale", "Handles unlimited concurrent calls and captures after-hours leads — turning your phone system into a revenue engine."),
]
ORGS = [
    "Receive predictable, repetitive inbound calls (e.g., hours, directions, FAQs)",
    "Operate outside standard 9–5 business hours or need after-hours coverage",
    "Manage multiple locations and want a unified receptionist experience that scales",
    "Are leaner, cost-conscious operations and want to free up staff to focus on higher-value work",
    "Require different levels of users managing the system",
]
CALLS = [
    ("phone-approved-sources", "sources", "AI Receptionist answers questions based on only approved information sources.",
     "Phone showing a call to Superior Care Automotive. Caller asks when the service department opens; AI Receptionist replies they are open 7 days a week from 9 AM to 6 PM."),
    ("phone-transfer", "transfer", "When AI Receptionist doesn’t have the information to answer the question, it will transfer the call to a department that can assist them.",
     "Phone showing a call to Superior Care Automotive. Caller asks about the cost of rebuilding an engine; AI Receptionist offers to connect them with the service department."),
]
RISK = [
    ("access", "Configure Data Sources and Role-Based Access",
     "Administrators define what information the AI can access, which roles can use it, and how it responds, allowing organizations to enforce security policies and compliance requirements while maintaining operational flexibility."),
    ("shield", "No Hallucinations!",
     "AI Receptionist pulls only from explicitly approved data sources and can be configured to route callers to an expert who can help, rather than generating inaccurate responses when the information is unavailable."),
]
RESULTS = [
    ("sentiment", "Call recordings and sentiment analysis indicators for continuous service improvement"),
    ("nomiss", "No missed calls or slow responses, reducing the number of lost leads and frustrated customers"),
    ("frontdesk", "A consistent, professional “front desk” experience that’s always available"),
    ("overhead", "Lower overhead to handle complex or customer-critical needs"),
    ("dtmf", "Flexibility enables callers to use voice or DTMF digit entry — improving the customer experience"),
]


def build():
    header = open(os.path.join(HERE, "ai-shell-header.html")).read()
    footer = open(os.path.join(HERE, "ai-shell-footer.html")).read()

    coverage = "\n".join(
        f'''			<article class="zair-card" data-zair-reveal style="--zair-reveal-delay:{i * 90}ms">
				{icon(ic)}
				<h3 class="zair-type-feature">{t}</h3>
				<p>{d}</p>
			</article>''' for i, (ic, t, d) in enumerate(COVERAGE))
    orgs = "\n".join(f"\t\t\t\t\t<li>{x}</li>" for x in ORGS)
    calls = "\n".join(
        f'''			<figure class="zair-call" data-zair-reveal style="--zair-reveal-delay:{i * 90}ms">
				<div class="zair-call__img">
				{pic(n, [640, 1000], "(max-width: 767px) 100vw, 520px", 1000, 895, alt)}
				</div>
				<figcaption>{icon(ic)}<span>{cap}</span></figcaption>
			</figure>''' for i, (n, ic, cap, alt) in enumerate(CALLS))
    risk = "\n".join(
        f'''					<div class="zair-point">
						{icon(ic)}
						<div>
							<h3 class="zair-type-feature">{t}</h3>
							<p>{d}</p>
						</div>
					</div>''' for ic, t, d in RISK)
    results = "\n".join(
        f'''			<div class="zair-result" data-zair-reveal style="--zair-reveal-delay:{(i % 3) * 80}ms">
				{icon(ic)}
				<p>{t}</p>
			</div>''' for i, (ic, t) in enumerate(RESULTS))

    sparkle = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10 3c.6 4 2.6 6 6.6 6.6-4 .6-6 2.6-6.6 6.6-.6-4-2.6-6-6.6-6.6C7.4 9 9.4 7 10 3z"/><path d="M18 13.5c.3 1.9 1.2 2.8 3.1 3.1-1.9.3-2.8 1.2-3.1 3.1-.3-1.9-1.2-2.8-3.1-3.1 1.9-.3 2.8-1.2 3.1-3.1z"/></svg>'
    phone = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.5 16.4v2.9a1.9 1.9 0 0 1-2.1 1.9 18.9 18.9 0 0 1-8.2-2.9 18.6 18.6 0 0 1-5.7-5.7 18.9 18.9 0 0 1-2.9-8.3A1.9 1.9 0 0 1 4.5 2.2h2.9a1.9 1.9 0 0 1 1.9 1.6c.1.9.4 1.8.7 2.7a1.9 1.9 0 0 1-.4 2L8.3 9.7a15.2 15.2 0 0 0 5.7 5.7l1.2-1.2a1.9 1.9 0 0 1 2-.4c.9.3 1.8.6 2.7.7a1.9 1.9 0 0 1 1.6 1.9z"/></svg>'
    mic = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/></svg>'
    keypad = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="6" cy="5" r="1.7"/><circle cx="12" cy="5" r="1.7"/><circle cx="18" cy="5" r="1.7"/><circle cx="6" cy="11" r="1.7"/><circle cx="12" cy="11" r="1.7"/><circle cx="18" cy="11" r="1.7"/><circle cx="6" cy="17" r="1.7"/><circle cx="12" cy="17" r="1.7"/><circle cx="18" cy="17" r="1.7"/><circle cx="12" cy="22" r="1.5"/></svg>'
    speaker = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4.5 4.5 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/></svg>'
    endcall = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 9c-3.4 0-6.6.9-8.9 2.6-.8.6-1 1.7-.5 2.5l1 1.6c.5.8 1.5 1.1 2.4.8l2.4-1c.7-.3 1.1-1 1.1-1.8v-1.4c1.6-.5 3.4-.5 5 0v1.4c0 .8.4 1.5 1.1 1.8l2.4 1c.9.3 1.9 0 2.4-.8l1-1.6c.5-.8.3-1.9-.5-2.5C18.6 9.9 15.4 9 12 9z"/></svg>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zultys AI Receptionist | Zultys</title>
<meta name="description" content="Zultys AI Receptionist: an enterprise-safe, 24/7 conversational front line that answers questions from approved sources and routes callers to the right person.">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="{A}/icons/favicon.svg" type="image/svg+xml">
<!-- Hero entrance: hide the photo before first paint only when the script will reveal it. -->
<script>(function(d){{if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;d.classList.add('zair-hero-anim');setTimeout(function(){{d.classList.remove('zair-hero-anim')}},4000)}})(document.documentElement)</script>
<link rel="preconnect" href="https://use.typekit.net" crossorigin>
<link rel="preload" as="image" href="{A}/img/hero-caller-900.webp" imagesrcset="{A}/img/hero-caller-600.webp 600w, {A}/img/hero-caller-900.webp 900w, {A}/img/hero-caller-1400.webp 1400w" imagesizes="(max-width: 767px) 92vw, 560px" fetchpriority="high">
<!-- Proxima Nova: the same Adobe Fonts kit the Zultys site loads -->
<link rel="stylesheet" href="https://use.typekit.net/gid7nhu.css">
<link rel="stylesheet" href="{A}/css/zair.css">
<!-- Staging only: stand-in header/footer. Not needed in WordPress. -->
<link rel="stylesheet" href="{A}/css/staging-shell.css">
</head>
<body>
<div class="zair" id="zair-page">
<a class="zair-skip-link" href="#zair-content">Skip to main content</a>

<!-- =====================================================================
     1: HERO (the header inside is a staging stand-in for the global nav)
     ===================================================================== -->
<div class="zair-hero zair-on-dark">

{header}

	<div class="zair-container zair-hero__inner">
		<div class="zair-hero__copy">
			<h1 class="zair-type-hero">Zultys AI Receptionist</h1>
			<p class="zair-type-card zair-hero__subtitle">Your Enterprise-Safe AI for Answering Questions and Routing Calls</p>
			<p class="zair-hero__body">Delivers a 24/7 conversational front line that answers questions, guides callers, and routes them to the right person when needed. Powered by natural language and configured to your business, it uses only approved sources—like your website, FAQs, and documents—to ensure accurate, consistent responses.</p>
			<div class="zair-hero__actions">
				<a class="zair-btn zair-btn--gradient" href="{DEMO}">Get a Demo</a>
				<a class="zair-btn zair-btn--outline-dark zair-btn--icon" href="{FLYER}" target="_blank" rel="noopener">Product Flyer<span class="zair-visually-hidden"> (PDF, opens in a new tab)</span><span class="zair-btn__icon zair-btn__icon--pdf" aria-hidden="true"></span></a>
			</div>
		</div>
		<div class="zair-hero__media">
			<div class="zair-hero__photo">
				{pic("hero-caller", [600, 900, 1400], "(max-width: 767px) 92vw, 560px", 900, 857, "Smiling professional on a call with a business", lazy=False)}
			</div>
			<!-- Phone mockup: the example conversation from the current page's hero graphic,
			     redrawn in the redesign's chat style (Mobile ZAC). Decorative. -->
			<div class="zair-phone" aria-hidden="true">
				<div class="zair-phone__screen">
					<div class="zair-phone__status"><span>10:20</span><span class="zair-phone__island"></span><span class="zair-phone__sys"><i></i><i></i><i></i></span></div>
					<div class="zair-phone__head">
						<span class="zair-phone__avatar">{sparkle}</span>
						<span class="zair-phone__who"><strong>Northbridge Outfitters</strong><span><b class="zair-live"></b>AI Receptionist · 0:42</span></span>
					</div>
					<div class="zair-phone__thread">
						<p class="zair-msg zair-msg--ai">Hello, what can I help you with today?</p>
						<p class="zair-msg zair-msg--caller">What’s your return policy?</p>
						<p class="zair-msg zair-msg--ai zair-msg--typing"><i></i><i></i><i></i></p>
					</div>
					<div class="zair-phone__controls">
						<span class="zair-phone__ctl">{mic}</span>
						<span class="zair-phone__ctl">{keypad}</span>
						<span class="zair-phone__ctl">{speaker}</span>
						<span class="zair-phone__ctl zair-phone__ctl--end">{endcall}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<main id="zair-content" tabindex="-1">

<!-- =====================================================================
     2: 24/7/365 RECEPTIONIST COVERAGE
     ===================================================================== -->
<section class="zair-coverage" aria-labelledby="zair-coverage-title">
	<div class="zair-container zair-container--wide">
		<div class="zair-section-head" data-zair-reveal>
			<h2 class="zair-type-section" id="zair-coverage-title">24/7/365 Receptionist Coverage</h2>
			<p class="zair-type-lead zair-text-blue">No Turnover, No Sick Days, No Ongoing Training</p>
		</div>
		<div class="zair-coverage__grid">
{coverage}
		</div>
	</div>
</section>

<!-- =====================================================================
     3: ESPECIALLY IMPACTFUL FOR ORGANIZATIONS THAT...
     ===================================================================== -->
<section class="zair-orgs" aria-labelledby="zair-orgs-title">
	<div class="zair-container zair-orgs__inner">
		<figure class="zair-orgs__photo" data-zair-reveal>
			{pic("business-owner", [800, 1400], "(max-width: 900px) 100vw, 520px", 800, 650, "Small business owner taking a customer call at her laptop")}
		</figure>
		<div data-zair-reveal style="--zair-reveal-delay:90ms">
			<h2 class="zair-type-section" id="zair-orgs-title">Zultys AI Receptionist Is Especially Impactful for Organizations That:</h2>
			<ul class="zair-checklist">
{orgs}
			</ul>
			<a class="zair-btn zair-btn--gradient" href="{DEMO}">Get a Demo</a>
		</div>
	</div>
</section>

<!-- =====================================================================
     4: CALL EXAMPLES (product images from the current page)
     ===================================================================== -->
<section class="zair-calls" aria-label="AI Receptionist call examples">
	<div class="zair-container zair-container--wide">
		<div class="zair-calls__panel">
{calls}
		</div>
	</div>
</section>

<!-- =====================================================================
     5: MINIMIZE RISK WHILE MAINTAINING ACCURACY
     ===================================================================== -->
<section class="zair-risk" aria-labelledby="zair-risk-title">
	<div class="zair-container zair-risk__inner">
		<div data-zair-reveal>
			<h2 class="zair-type-section" id="zair-risk-title">Minimize Risk While Maintaining Accuracy</h2>
			<p class="zair-risk__intro">Zultys AI Receptionist is practical, purpose-built AI designed to reduce risk — not create it — enabling AI adoption without customer anxiety about compliance or incorrect information.</p>
			<div class="zair-risk__points">
{risk}
			</div>
		</div>
		<figure class="zair-risk__photo" data-zair-reveal style="--zair-reveal-delay:90ms">
			{pic("front-desk", [800, 1400], "(max-width: 900px) 100vw, 540px", 800, 534, "Patient checking in with a receptionist at a dental clinic front desk")}
			<span class="zair-shield" aria-hidden="true">{icon("shield")}</span>
		</figure>
	</div>
</section>

<!-- =====================================================================
     6: RESULTS
     ===================================================================== -->
<section class="zair-results" aria-labelledby="zair-results-title">
	<!-- Animated dotted wave: same canvas routine as the Mobile ZAC section (vendor/zultys-wave.js) -->
	<div class="zair-results__wave" data-zair-wave aria-hidden="true"></div>
	<button class="zair-wave-toggle" type="button" data-zair-wave-toggle aria-label="Pause background animation" hidden></button>
	<div class="zair-container zair-container--wide">
		<div class="zair-section-head" data-zair-reveal>
			<h2 class="zair-type-section" id="zair-results-title">Results That Improve Both Service and Efficiency</h2>
		</div>
		<div class="zair-results__grid">
{results}
		</div>
	</div>
</section>

<!-- =====================================================================
     7: CLOSING CALL TO ACTION
     ===================================================================== -->
<section class="zair-cta" aria-labelledby="zair-cta-title">
	<div class="zair-container zair-container--wide">
		<div class="zair-cta__card zair-on-dark" data-zair-reveal>
			<h2 class="zair-type-section" id="zair-cta-title">Get started with smarter communications today.</h2>
			<div class="zair-cta__actions">
				<a class="zair-btn zair-btn--gradient" href="{REQUEST_DEMO}">Request Demo</a>
				<a class="zair-btn zair-btn--outline-dark" href="{REQUEST_QUOTE}">Request Quote</a>
			</div>
		</div>
	</div>
</section>

</main>

{footer}
</div>

<!-- Same file the site enqueues as assets/redesign/homepage-wave.js; skip this tag in WordPress if it is already loaded. -->
<script src="{A}/js/vendor/zultys-wave.js" defer></script>
<script src="{A}/js/zair.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, "zultys-ai-receptionist", "index.html")
    open(out, "w").write(html)
    print(out, len(html))


if __name__ == "__main__":
    build()
