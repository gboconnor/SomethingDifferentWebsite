#!/usr/bin/env python3
"""Generates the standalone SEM/SEO landing pages.
Run: python3 build_pages.py
"""

GTAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-72K4162M29"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-72K4162M29');
</script>'''

HEAD = '''<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
__GTAG__
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__CANON__">
<meta name="theme-color" content="#004240">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Something Different">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__CANON__">
<meta property="og:image" content="https://somethingdifferent.co.nz/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="__OGTITLE__">
<meta name="twitter:description" content="__DESC__">
<meta name="twitter:image" content="https://somethingdifferent.co.nz/assets/og-image.png">
__JSONLD__
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="nav">
  <div class="container">
    <a class="brand" href="index.html"><img src="assets/logo.png" alt="Something Different"></a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">&#9776;</button>
    <nav class="nav-links" id="nav">
      <a href="index.html#outcomes">Outcomes</a>
      <a href="index.html#method">The Method</a>
      <a href="index.html#proof">Proof</a>
      <a href="index.html#about">About</a>
      <a href="index.html#services">Ways in</a>
      <a href="musings.html">Musings</a>
      <a class="btn btn-primary" href="contact.html">Book a conversation</a>
    </nav>
  </div>
</header>
'''

FOOTER = '''<footer class="footer">
  <div class="container footer-grid">
    <div>
      <a class="brand" href="index.html"><img src="assets/logo.png" alt="Something Different"></a>
      <p style="margin-top:10px;max-width:32ch;">Brand &amp; growth strategy consultancy. Helping leadership teams get to the root and grow.</p>
    </div>
    <div class="footer-services">
      <span class="h">Services</span>
      <a href="strategy-consultant">Strategy consulting</a>
      <a href="brand-strategy">Brand strategy</a>
      <a href="marketing-strategy">Marketing strategy</a>
      <a href="strategy-workshops">Strategy workshops</a>
    </div>
    <div>
      <p><strong style="color:var(--ink)">Gareth O'Connor</strong><br>Founder &amp; Strategist</p>
      <p><a href="mailto:gareth@somethingdifferent.co.nz">gareth@somethingdifferent.co.nz</a><br><a href="tel:+6421674364">+64 21 674 364</a></p>
    </div>
  </div>
</footer>
</body>
</html>'''

def jsonld(name, stype, desc):
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"Service",'
            '"serviceType":"' + stype + '","name":"' + name + '","description":"' + desc + '",'
            '"provider":{"@type":"Organization","name":"Something Different","url":"https://somethingdifferent.co.nz/"},'
            '"areaServed":"New Zealand","url":"__CANON__"}\n</script>')

PAGES = {}

# ---------------------------------------------------------------- 1. STRATEGY CONSULTANT
PAGES["strategy-consultant"] = dict(
    title="Strategy Consultant NZ | Something Different",
    ogtitle="Strategy Consultant NZ | Something Different",
    desc="Independent strategy consulting for leadership teams facing complex business problems. Create clarity, make better choices and turn strategy into action.",
    canon="https://somethingdifferent.co.nz/strategy-consultant",
    jsonld=jsonld("Strategy consulting", "Strategy consulting",
                  "Independent strategy consulting to make complex business problems understandable and actionable."),
    body='''
<section class="hero">
  <div class="container">
    <p class="eyebrow">Strategy Consultant</p>
    <h1>Complex problem. Unclear answer?</h1>
    <p class="lp-lead">Independent strategy consulting to make complex business problems understandable and actionable.</p>
    <p style="max-width:58ch;margin-top:1.2rem;">Sometimes the problem isn't a lack of ideas. It's knowing which problem actually needs solving. Something Different works with leadership teams facing complex business, brand, customer and marketing challenges to create clarity, make better choices and turn strategy into action.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="contact.html">Start a conversation</a></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">Start with the problem</p>
    <h2>The harder questions</h2>
    <p class="lead">Organisations rarely suffer from a shortage of activity. The harder questions are usually:</p>
    <ul class="qlist">
      <li>What are we actually trying to achieve?</li>
      <li>What's getting in the way?</li>
      <li>Where should we focus?</li>
      <li>What should we stop doing?</li>
      <li>And what needs to happen next?</li>
    </ul>
    <p style="margin-top:1.5rem;">That's where I can help.</p>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">How I work</p>
    <h2>From complexity to clear, practical direction</h2>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h3>Get to the Root</h3><p>Understand what's really happening across the Customer, Category, Culture and Company.</p></div>
      <div class="step"><div class="step-num">2</div><h3>Define the Focus</h3><p>Turn complexity into a clear problem, direction and set of strategic choices.</p></div>
      <div class="step"><div class="step-num">3</div><h3>Build the Plan</h3><p>Translate the strategy into priorities, actions and decisions people can actually use.</p></div>
      <div class="step"><div class="step-num">4</div><h3>Steward the Direction</h3><p>Help maintain alignment as the organisation moves from thinking to doing.</p></div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container narrow">
    <p class="eyebrow">The Better Business Operating Model</p>
    <h2>Performance is built across the organisation, not department by department</h2>
    <p>Better businesses aren't built department by department. They're built by an operating system that works across the organisation. The Better Business Operating Model provides a practical way to diagnose where performance is being created, where it is being constrained and where leaders should focus next.</p>
    <p style="margin-top:1.6rem;"><a class="btn btn-outline" href="musings/the-better-business-operating-model.html">Explore the Better Business Operating Model</a></p>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">When I can help</p>
    <h2>You might need Something Different when</h2>
    <ul class="qlist">
      <li>The business has become complicated, and the direction isn't clear.</li>
      <li>Growth has slowed, and you're not sure why.</li>
      <li>Leadership needs alignment around what happens next.</li>
      <li>Strategy exists, but isn't changing decisions.</li>
      <li>Marketing, customer, brand and business priorities aren't connecting.</li>
      <li>You need experienced independent thinking without hiring a large consultancy.</li>
    </ul>
  </div>
</section>

<section class="section-alt">
  <div class="container narrow">
    <p class="eyebrow">Something different?</p>
    <h2>Experienced, independent thinking</h2>
    <p>I'm Gareth O'Connor, an independent strategist with more than 20 years' experience working across business, brand, marketing and customer strategy. I work directly with leadership teams, agencies and organisations to get to the root of complex problems and turn them into practical strategic direction.</p>
    <p>No predetermined methodology. No army of junior consultants. Just experienced, independent thinking focused on the problem that actually needs solving.</p>
  </div>
</section>

<section class="cta-band">
  <div class="container narrow">
    <h2>Have a problem worth solving?</h2>
    <p class="lead">Let's have a conversation.</p>
    <a class="btn btn-primary" href="contact.html" style="margin-top:10px;">Start a conversation</a>
  </div>
</section>
''')

# ---------------------------------------------------------------- 2. BRAND STRATEGY
PAGES["brand-strategy"] = dict(
    title="Brand Strategy Consultant NZ | Something Different",
    ogtitle="Brand Strategy Consultant NZ | Something Different",
    desc="Independent brand strategy to clarify what your organisation should mean, why people should choose it and how the brand should help the business grow.",
    canon="https://somethingdifferent.co.nz/brand-strategy",
    jsonld=jsonld("Brand Strategy", "Brand strategy consulting",
                  "Brand strategy that clarifies what your organisation should mean, do and become."),
    body='''
<section class="hero">
  <div class="container">
    <p class="eyebrow">Brand Strategy</p>
    <h1>A clearer brand starts with a clearer business problem.</h1>
    <p class="lp-lead">Brand strategy that clarifies what your organisation should mean, do and become.</p>
    <p style="max-width:60ch;margin-top:1.2rem;">A brand refresh isn't always the answer. Neither is a new campaign, logo or proposition. Sometimes the real challenge sits deeper: the organisation isn't clear about who it needs to matter to, what it should stand for, why people should choose it or how the brand should help the business grow. That's where brand strategy starts.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="contact.html">Talk about your brand</a></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">Before design comes direction</p>
    <h2>The questions that should come before creative execution</h2>
    <ul class="qlist">
      <li>Who are we trying to matter to?</li>
      <li>What do they actually value?</li>
      <li>What's happening in our category?</li>
      <li>What can we credibly own?</li>
      <li>Why should someone choose us?</li>
      <li>What should remain consistent as the organisation evolves?</li>
      <li>And what role does the brand need to play in the future of the business?</li>
    </ul>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">Four lenses</p>
    <h2>Finding the territory a brand can credibly occupy</h2>
    <div class="steps">
      <div class="step"><h3>Customer</h3><p>What do people need, value, believe and do?</p></div>
      <div class="step"><h3>Category</h3><p>How does the market work, and where are the conventions and opportunities?</p></div>
      <div class="step"><h3>Culture</h3><p>What wider forces are changing expectations and behaviour?</p></div>
      <div class="step"><h3>Company</h3><p>What is genuinely true, distinctive and valuable about the organisation?</p></div>
    </div>
    <p style="margin-top:1.6rem;max-width:60ch;">Together, they help identify the strategic territory a brand can credibly occupy.</p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">What that can lead to</p>
    <h2>Clarity that helps people make better decisions</h2>
    <p class="lead">Depending on the problem, the work might include:</p>
    <ul class="pill-list">
      <li>Brand diagnosis</li><li>Audience strategy</li><li>Positioning</li><li>Brand proposition</li><li>Brand platform</li><li>Brand story</li><li>Brand architecture</li><li>Communications strategy</li><li>Go-to-market strategy</li><li>Creative and design briefing</li><li>Leadership workshops</li>
    </ul>
    <p style="margin-top:1.6rem;max-width:60ch;">The output isn't simply a brand document. It's clarity that helps people make better decisions.</p>
  </div>
</section>

<section>
  <div class="container narrow">
    <p class="eyebrow">Brand strategy before brand design</p>
    <h2>Good design can't compensate for an unclear idea underneath it</h2>
    <p>Good design can make a brand distinctive. But it can't compensate for an unclear idea underneath it. The strongest brand identities express a clear strategic direction: what the organisation wants to mean, why that matters, and how it should show up consistently. That's why I like to get the strategy right first.</p>
  </div>
</section>

<section class="cta-band">
  <div class="container narrow">
    <h2>Thinking about where your brand goes next?</h2>
    <p class="lead">Let's talk about the problem before deciding on the answer.</p>
    <a class="btn btn-primary" href="contact.html" style="margin-top:10px;">Talk about your brand</a>
  </div>
</section>
''')

# ---------------------------------------------------------------- 3. MARKETING STRATEGY
PAGES["marketing-strategy"] = dict(
    title="Marketing Strategy Consultant NZ | Something Different",
    ogtitle="Marketing Strategy Consultant NZ | Something Different",
    desc="Independent marketing strategy for clearer priorities, better decisions and more effective investment across brand, customer, communications and marketing.",
    canon="https://somethingdifferent.co.nz/marketing-strategy",
    jsonld=jsonld("Marketing Strategy", "Marketing strategy consulting",
                  "Independent marketing strategy to create clearer priorities, better decisions and more effective investment."),
    body='''
<section class="hero">
  <div class="container">
    <p class="eyebrow">Marketing Strategy</p>
    <h1>More marketing activity isn't always the answer.</h1>
    <p class="lp-lead">An independent marketing strategy to create clearer priorities, better decisions and more effective investment.</p>
    <p style="max-width:60ch;margin-top:1.2rem;">Most organisations aren't short of marketing activity. Campaigns are running. Content is being produced. Channels are being managed. Leads are being generated. Reports are being written. The harder question is whether all that activity is actually contributing to meaningful progress.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="contact.html">Talk about your marketing challenge</a></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">Activity isn't strategy</p>
    <h2>The questions underneath the tactics</h2>
    <p class="lead">Something Different helps organisations step back from the tactics and answer the questions underneath them.</p>
    <ul class="qlist">
      <li>What are we trying to change?</li>
      <li>Which customers matter most?</li>
      <li>What behaviour needs to move?</li>
      <li>What role should brand play?</li>
      <li>What role should activation play?</li>
      <li>Where should we invest?</li>
      <li>What should each channel actually do?</li>
      <li>And how will we know whether it's working?</li>
    </ul>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">Evidence before fashion</p>
    <h2>Better decisions using the best available evidence</h2>
    <p class="lead">My approach draws on established thinking in marketing effectiveness, behavioural science, brand growth and customer behaviour. That means balancing things too often treated as opposites:</p>
    <ul class="pill-list">
      <li>Brand and activation</li><li>Long and short term</li><li>Mental and physical availability</li><li>Emotion and information</li><li>Customer value and commercial value</li><li>Creativity and effectiveness</li>
    </ul>
    <p style="margin-top:1.6rem;max-width:60ch;">The aim isn't to follow a formula. It's to make better decisions using the best available evidence.</p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">Where I can help</p>
    <h2>Depending on the challenge</h2>
    <ul class="pill-list">
      <li>Marketing strategy</li><li>Communications strategy</li><li>Brand and activation planning</li><li>Customer and audience strategy</li><li>Channel roles and planning</li><li>Marketing effectiveness</li><li>Go-to-market strategy</li><li>Measurement frameworks</li><li>Agency briefing</li><li>Leadership alignment</li><li>Marketing workshops</li>
    </ul>
  </div>
</section>

<section>
  <div class="container narrow">
    <p class="eyebrow">From activity to progress</p>
    <h2>The objective isn't more marketing. It's better outcomes.</h2>
    <p>Good marketing strategy should make choices clearer. What matters. What doesn't. Where to invest. What to stop. What needs to remain consistent. And how marketing contributes to the organisation's wider performance. Because the objective isn't more marketing. It's better outcomes.</p>
  </div>
</section>

<section class="cta-band">
  <div class="container narrow">
    <h2>Need a clearer marketing direction?</h2>
    <p class="lead">Let's get to the root of the problem first.</p>
    <a class="btn btn-primary" href="contact.html" style="margin-top:10px;">Talk about your marketing challenge</a>
  </div>
</section>
''')

# ---------------------------------------------------------------- 4. STRATEGY WORKSHOPS
PAGES["strategy-workshops"] = dict(
    title="Strategy Workshop Facilitator NZ | Something Different",
    ogtitle="Strategy Workshop Facilitator NZ | Something Different",
    desc="Strategy workshops for leadership teams tackling complex business, brand, customer and marketing problems. Create clarity, alignment and action.",
    canon="https://somethingdifferent.co.nz/strategy-workshops",
    jsonld=jsonld("Strategy Workshops", "Strategy workshop facilitation",
                  "Strategy workshops for leadership teams tackling complex business, brand, customer and marketing problems."),
    body='''
<section class="hero">
  <div class="container">
    <p class="eyebrow">Strategy Workshops</p>
    <h1>Sometimes you just need to get the right people in a room and sort the bloody thing out.</h1>
    <p style="max-width:62ch;margin-top:1.4rem;">Not every problem needs a six-month strategy project. Sometimes you know something needs to change, but the problem isn't quite clear. Competing views are around the table. Too many priorities. Decisions keep getting deferred. Or plenty is happening without enough agreement on where it's all heading.</p>
    <p style="max-width:62ch;">A well-designed workshop can change that. Something Different works with leadership teams to get to the root of complex business, brand, customer and marketing problems, create clarity around what matters, and make the decisions needed to move forward. Not workshops for the sake of workshops. Workshops designed to change what happens next.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="contact.html">Talk about a workshop</a></div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">Start with the problem, not the workshop</p>
    <h2>We start with what you're trying to solve</h2>
    <p class="lead">There isn't a standard Something Different workshop that gets rolled out regardless of the brief. We start with what you're trying to solve. That might be:</p>
    <div class="steps">
      <div class="step"><h3>Business direction</h3><p>Where are we going, what's getting in the way, and where should we focus?</p></div>
      <div class="step"><h3>Growth</h3><p>What's really constraining performance and what needs to change?</p></div>
      <div class="step"><h3>Brand</h3><p>What should we stand for, who should we matter to and why should people choose us?</p></div>
      <div class="step"><h3>Customer</h3><p>Where are we creating value, friction or disappointing experiences?</p></div>
      <div class="step"><h3>Marketing</h3><p>What are we actually trying to change and where should we invest?</p></div>
      <div class="step"><h3>Alignment</h3><p>How do we get different teams making decisions around the same direction?</p></div>
    </div>
    <p style="margin-top:1.6rem;max-width:60ch;">Once the problem is clearer, I'll design the workshop around it.</p>
  </div>
</section>

<section>
  <div class="container narrow">
    <p class="eyebrow">A practical toolkit for better conversations</p>
    <h2>The framework serves the problem, not the other way around</h2>
    <p>Behind the workshops sits the Something Different Manual: a growing collection of models, principles, diagnostic questions and practical tools developed through more than 20 years of working across strategy, brand, marketing and customer problems.</p>
    <p>Depending on what we're trying to solve, we might use the Better Business Operating Model to diagnose where performance is being constrained. We might explore Customer, Category, Culture and Company to understand a brand or market problem. Or we might go deeper into Purpose, Value, Memory, Preference, Access, Experience and Consistency to understand where the organisation needs to become stronger.</p>
    <p>And I'm not a neutral facilitator. I'll make sure the right conversations happen, but I'll also bring an independent perspective, challenge assumptions, introduce useful evidence and ask the difficult questions when they need asking.</p>
    <p>There will probably be Post-it Notes. But Post-it Notes aren't the output.</p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <p class="eyebrow">How it works</p>
    <h2>From complexity towards clarity and choices</h2>
    <ol class="steps-mini">
      <li><strong>Get to the Root.</strong> Before anyone walks into the room, we clarify the problem we're trying to solve: conversations with key people, reviewing existing research and strategy, looking at customer or performance information, or some initial diagnostic work.</li>
      <li><strong>Design the Session.</strong> The workshop is built around the questions that need answering and the decisions that need making, drawing on the most useful tools and frameworks for the problem.</li>
      <li><strong>Work Through It Together.</strong> Get the right people in the room, introduce outside perspective, challenge assumptions and work systematically from complexity towards clarity and choices.</li>
      <li><strong>Turn Discussion Into Decisions.</strong> The important thinking is captured and synthesised into something useful: clear choices, agreed priorities, actions and, where appropriate, a framework or plan for what happens next.</li>
    </ol>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">What you leave with matters</p>
    <h2>You should leave with greater clarity than you arrived with</h2>
    <p class="lead">A good workshop shouldn't end with photographs of walls covered in Post-it Notes. Depending on the problem, that could mean:</p>
    <ul class="pill-list">
      <li>A clearer diagnosis</li><li>A shared direction</li><li>Strategic choices</li><li>Agreed priorities</li><li>A practical action plan</li><li>A framework for future decisions</li>
    </ul>
    <p style="margin-top:1.6rem;max-width:62ch;">And sometimes the workshop reveals that more work is required. That's useful too. Because knowing what problem you actually need to solve is considerably better than spending six months solving the wrong one.</p>
  </div>
</section>

<section class="cta-band">
  <div class="container narrow">
    <h2>Have something you need to sort out?</h2>
    <p class="lead">You don't need a perfectly formed brief. Figuring out what the brief should be is often part of the job. Tell me what's going on, where you're getting stuck and what you're trying to achieve.</p>
    <a class="btn btn-primary" href="contact.html" style="margin-top:10px;">Talk to Gareth about a workshop</a>
  </div>
</section>
''')

for slug, p in PAGES.items():
    head = (HEAD.replace("__GTAG__", GTAG)
                .replace("__TITLE__", p["title"])
                .replace("__OGTITLE__", p["ogtitle"])
                .replace("__DESC__", p["desc"])
                .replace("__CANON__", p["canon"])
                .replace("__JSONLD__", p["jsonld"].replace("__CANON__", p["canon"])))
    html = head + p["body"] + FOOTER
    open(f"{slug}.html", "w", encoding="utf-8").write(html)
    print("wrote", slug + ".html", len(html), "bytes")
