"""Generates phone/z-23w-ip-phone/index.html from z23w-page.template.html.

The repeated blocks (feature cards, highlight lists, carousel slides, and the
Country/State options copied from the live Gravity Form) are defined here so
copy edits happen in one place. Run: python3 tools/build_z23w_page.py
"""
import json, html
import os
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
t=open(os.path.join(HERE,'z23w-page.template.html')).read()
feats=[
("Remarkable HD Audio","feature-hd-audio",[640,1100],"Headset resting on a laptop keyboard",
 "You deserve a best-in-class experience. Your Z23W handsfree speakerphone comes with added hi-fidelity features including acoustic echo cancellation, crisp-clear wideband High Definition (HD) speaker, sensitive microphone, and handset components to modify each workstation. This lets you ensure conversations are always loud, clear, and delivered in a fashion that minimizes fatigue for even the heaviest phone users."),
("Wireless Headset Support (EHS)","feature-headset",[640,1100],"Team member wearing a wireless headset",
 "Users love the options and flexibility they gain with their Z 23W. You can combine your choice of compatible wireless headsets and the Zultys EHS adapter. Avoid limitations. Staff requiring mobility around the office, and the customers they support, will appreciate the convenience of the Electronic Hook Switch control. You also have the ability to use your Z 23W with a wide range of compatible Bluetooth headsets."),
("Color Display &amp; Ease of Use","feature-display",[600],"Close-up of the Z 23W color display showing line keys and soft keys",
 "The bright, easy-to-view 2.8″ 320 × 240-pixel Z 23W color display presents your team with the detailed call information your team needs to succeed along with dynamic icons to minimize training requirements and maximize usability. Eight LCD-labeled buttons support up to 21 user-programmable keys. Plus, four context-sensitive soft keys located just below the display make conferencing, transfer, and other operations a breeze."),
("Simplified Deployment","feature-deployment",[640,1100],"Ethernet cable next to a Gigabit network port",
 "Save time and money from setup through future upgrades. Dual auto-sensing switched Gigabit Ethernet ports simplify installation and eliminate added wiring. Integrated IEEE 802.3af Power over Ethernet and low power consumption support rapid, energy-efficient deployment. Industry-standard VLAN and QoS support prioritizes network voice traffic. MX Admin graphical interface centralized provisioning gives a single point of management within a complete UC solution."),
]
F=[]
for i,(title,img,ws,alt,copy) in enumerate(feats,1):
    srcset=", ".join(f"/assets/z23w/img/{img}-{w}.webp {w}w" for w in ws)
    F.append(f'''			<article class="z23w-feature-card" data-z23w-feature data-z23w-reveal style="--z23w-reveal-delay:{(i-1)%2*90}ms">
				<div class="z23w-feature-card__media">
					<picture>
						<source type="image/webp" srcset="{srcset}" sizes="(max-width: 767px) 100vw, 530px">
						<img src="/assets/z23w/img/{img}.jpg" width="1100" height="619" alt="{alt}" loading="lazy" decoding="async">
					</picture>
				</div>
				<div class="z23w-feature-card__body">
					<h3 class="z23w-type-card z23w-feature-card__title" id="z23w-feature-{i}-title">{title}</h3>
					<p class="z23w-feature-card__text" id="z23w-feature-{i}-text" data-z23w-feature-text>{copy}</p>
					<button class="z23w-more" type="button" aria-expanded="false" aria-controls="z23w-feature-{i}-text" aria-describedby="z23w-feature-{i}-title" data-z23w-feature-toggle hidden><span data-z23w-feature-label>Show More</span><svg viewBox="0 0 11.7271 6.70117" fill="currentColor" aria-hidden="true"><path d="M5.86353 6.70117 0 .837646V0h.837646L5.86353 5.02588 10.8894 0h.8377v.837646L5.86353 6.70117Z"/></svg></button>
				</div>
			</article>''')
icons={
"Interface &amp; Audio":'<rect x="5" y="3" width="14" height="18" rx="2.5"/><rect x="8" y="6" width="8" height="5" rx="1"/><path d="M8.5 14.5h.01M12 14.5h.01M15.5 14.5h.01M8.5 17.5h.01M12 17.5h.01M15.5 17.5h.01"/>',
"Call Management":'<path d="M6.6 3.5h2.6l1.4 3.6-1.9 1.3a11 11 0 0 0 5 5l1.3-1.9 3.6 1.4v2.6a2 2 0 0 1-2.2 2A16 16 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2Z"/><path d="M15 4h5v5M20 4l-5.5 5.5"/>',
"Collaboration &amp; Directories":'<circle cx="9" cy="8.5" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9.5" r="2.3"/><path d="M16.5 14.6a4.4 4.4 0 0 1 4.3 4.4"/>',
"Connectivity &amp; Deployment":'<path d="M4.5 10a11 11 0 0 1 15 0M7.5 13.2a6.6 6.6 0 0 1 9 0M10.3 16.3a2.6 2.6 0 0 1 3.4 0"/><path d="M12 19.5h.01"/>',
}
hl=[
("Interface &amp; Audio",["21 programmable LCD-labeled keys","4 context-sensitive soft keys","2.8″ 320 × 240 pixel color display","Handsfree speakerphone","Hearing Aid Compatible (HAC) handset","Display of caller and called line information"]),
("Call Management",["Call forward, call transfer, and call waiting","One-touch call transfer and conference","One-touch call record button with look-back capabilities","Call park and pickup","Call log and redial","Missed call notification"]),
("Collaboration &amp; Directories",["Full call control via ZAC","Local 6-way conference","Personal, MX system, and LDAP contact directories","Paging and intercom auto-answer capabilities","Log into Call Groups from the phone","Dedicated headset port with EHS support"]),
("Connectivity &amp; Deployment",["Built-in Bluetooth","Built-in Wi-Fi support (2.4G/5G Wi-Fi 6)","VLAN, DSCP, and QoS support","SIP open standard","802.3af Power over Ethernet","Wall mountable (optional bracket required)"]),
]
H=[]
for i,(title,items) in enumerate(hl):
    lis="\n".join(f"					<li>{x}</li>" for x in items)
    H.append(f'''			<div class="z23w-highlight" data-z23w-reveal style="--z23w-reveal-delay:{i*70}ms">
				<svg class="z23w-highlight__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icons[title]}</svg>
				<h3 class="z23w-type-feature">{title}</h3>
				<ul>
{lis}
				</ul>
			</div>''')
phones=[
("ZIP 49GA IP Phone","zip-49ga","https://www.zultys.com/phone/zip-49ga-ip-phone",1200,756,"Zultys ZIP 49GA IP phone with large touchscreen and camera"),
("ZIP 47GE IP Phone","zip-47ge","https://www.zultys.com/phone/zip-47ge-ip-phone",1200,735,"Zultys ZIP 47GE IP phone with wide color display"),
("ZIP 45W IP Phone","zip-45w","https://www.zultys.com/phone/zip-45w-ip-phone",1200,1251,"Zultys ZIP 45W IP phone with color display"),
("Z 22G IP Phone","z-22g","https://www.zultys.com/phone/z-22g-ip-phone",1200,1024,"Zultys Z 22G IP phone with color display"),
("Z 21i IP Phone","z-21i","https://www.zultys.com/phone/z-21i-ip-phone",1200,1024,"Zultys Z 21i IP phone with monochrome display"),
]
S=[]
for i,(name,img,url,w,h,alt) in enumerate(phones,1):
    S.append(f'''					<div class="z23w-slide{' is-active' if i==1 else ''}" role="group" aria-roledescription="slide" aria-label="{i} of {len(phones)}: {name}" data-z23w-slide data-name="{name}">
						<div class="z23w-slide__stage{' z23w-slide__stage--tall' if h/w>0.8 else ''}">
							<picture>
								<source type="image/webp" srcset="/assets/z23w/img/{img}-720.webp 720w, /assets/z23w/img/{img}-1200.webp 1200w" sizes="(max-width: 767px) 92vw, 660px">
								<img src="/assets/z23w/img/{img}.png" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async" draggable="false">
							</picture>
						</div>
						<h3 class="z23w-type-card z23w-slide__name">{name}</h3>
						<a class="z23w-btn z23w-btn--icon" href="{url}">View Phone<span class="z23w-visually-hidden">: {name}</span><span class="z23w-btn__icon z23w-btn__icon--arrow" aria-hidden="true"></span></a>
					</div>''')
o=json.load(open(os.path.join(HERE,'quote-form-options.json')))
C="\n".join(f'						<option value="{html.escape(v)}"{" selected" if s else ""}>{html.escape(l)}</option>' for v,s,l in o['input_6'])
St='						<option value="">Select a state</option>\n'+"\n".join(f'						<option value="{html.escape(v)}">{html.escape(l)}</option>' for v,s,l in o['input_7'])
for k,v in [('{{FEATURES}}',"\n".join(F)),('{{HIGHLIGHTS}}',"\n".join(H)),('{{SLIDES}}',"\n".join(S)),('{{COUNTRIES}}',C),('{{STATES}}',St)]:
    assert k in t; t=t.replace(k,v)
open(os.path.join(ROOT,'phone','z-23w-ip-phone','index.html'),'w').write(t)
print(len(t))
