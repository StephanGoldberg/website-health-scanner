# website-health-scanner
🔬 Website Health Scanner for Founders
A free, open-source CLI tool that runs a full website audit across four pillars: Security, SEO, Performance, and Compliance — in one command.
Built for founders who want to know exactly what's wrong with their site before they launch, pitch investors, or spend money on ads.

Why Four Pillars?
Most free tools check one thing. Google PageSpeed checks performance. Lighthouse checks SEO. SSL checkers check... SSL. You end up using five different tools and stitching the results together yourself.
This scanner runs all four audits in a single command and gives you a unified score per category — so you can see at a glance where your site is strong and where it's leaking.

For the full detailed report — with fix instructions, priority ordering, compliance checklist, and PDF export — use FounderScan.dev.


What It Checks
🔒 Security (8 checks)
CheckWhy It MattersHTTPS/SSLBaseline requirement — browsers warn users on HTTP sitesHSTS headerPrevents protocol downgrade attacksContent Security PolicyBlocks XSS and injection attacksX-Frame-OptionsPrevents clickjackingX-Content-Type-OptionsStops MIME-type sniffing attacksReferrer-PolicyControls what data leaks to third partiesPermissions-PolicyRestricts browser feature accessNo mixed contentHTTP assets on HTTPS pages break security
🔍 SEO (8 checks)
CheckWhy It MattersTitle tag (30–60 chars)Primary ranking signal and click-through driverMeta description (70–160 chars)Your pitch in search resultsH1 tag (exactly one)Signals page topic to search enginesCanonical tagPrevents duplicate content penaltiesSchema markup (JSON-LD)Enables rich results and AI search citationsOpen Graph tagsControls link previews on social and messagingrobots.txtCrawl control for search enginessitemap.xmlEnsures all pages get discovered and indexed
⚡ Performance (5 checks)
CheckWhy It MattersLoad time <2sEvery second of delay reduces conversions ~7%Load time <3sGoogle's threshold for mobile ranking penaltyMobile viewportRequired for Google's mobile-first indexingImage alt textAccessibility + ranking signal for image searchHTML not bloatedExcessive whitespace/markup slows parse time
📋 Compliance (4 checks)
CheckWhy It MattersPrivacy policyRequired by GDPR, CCPA, and most ad networksCookie noticeLegal requirement in EU and increasingly globallyTerms of serviceProtects you legally and required by app storesContact informationRequired by GDPR; builds trust with visitors

Installation
No pip install. Python 3.7+ only.
bashgit clone https://github.com/yourusername/website-health-scanner.git
cd website-health-scanner
python website_scanner.py <domain>

Usage
bashpython website_scanner.py mystartup.com
Example output:
==============================================================
  🔬 FounderScan — Website Health Report
  Site: mystartup.com   |   Load time: 0.94s
==============================================================

  OVERALL SCORE: 62/100  —  🟡 Good — a few things to fix

  ──────────────────────────────────────────────────────
  🔒 SECURITY         [███████░░░] 70%
  🔍 SEO              [██████░░░░] 63%
  ⚡ PERFORMANCE      [████████░░] 80%
  📋 COMPLIANCE       [████░░░░░░] 40%

--------------------------------------------------------------
  ISSUES FOUND (9)  —  ordered by impact
--------------------------------------------------------------

  🔒 SECURITY
    🔴 Content Security Policy
    🟠 HSTS header
    🟡 Referrer-Policy

  🔍 SEO
    🔴 Schema markup
    🟠 Canonical tag
    🟡 Open Graph tags

  📋 COMPLIANCE
    🟠 Privacy policy
    🟡 Cookie notice
    🟡 Terms of service

--------------------------------------------------------------
  PASSING (15/24)
--------------------------------------------------------------
  🔒 SECURITY: HTTPS/SSL, X-Frame-Options, X-Content-Type-Options
  🔍 SEO: Title tag, Meta description, H1 tag, robots.txt, sitemap.xml
  ⚡ PERFORMANCE: Load time (<2s), Load time (<3s), Mobile viewport, ...
  📋 COMPLIANCE: Contact info

==============================================================
  📊 Get the full FounderScan report:
  Detailed fixes, priority order, compliance checklist,
  performance recommendations & PDF export:
  👉  https://founderscan.dev
==============================================================

Score Interpretation
ScoreMeaning85–100🟢 Excellent — well-built, investor-ready site65–84🟡 Good — fix the flagged issues before major launches45–64🟠 Needs work — multiple issues affecting trust and rankings0–44🔴 Critical — security or compliance risks need immediate attention

When to Run This
Before launching a new site or landing page — catch issues before real users see them.
Before running paid ads — ad networks (Google, Meta) can suspend accounts for privacy policy violations. Missing compliance checks cost real money.
Before a fundraise or acquisition — investors and acquirers do technical due diligence. A clean scan report signals a professional operation.
After major updates — new CMS plugins, theme changes, or deployments can accidentally remove security headers or break canonical tags.
On competitor sites — understanding where competitors have gaps informs your own content and SEO strategy.

The Full FounderScan Platform
This CLI covers the quick-check layer. FounderScan.dev goes significantly deeper:

Detailed fix instructions — not just "missing CSP" but the exact header value to add for your stack
Priority ordering — fixes ranked by impact so you know what to tackle first
Compliance checklist — GDPR, CCPA, and cookie law requirements by region
PDF report — shareable audit you can hand to a developer or show to investors
Historical tracking — monitor your site health over time, catch regressions
Performance deep-dive — Core Web Vitals, render-blocking resources, image optimization

→ Run a full scan at FounderScan.dev

Common Issues and Quick Fixes
Missing Content Security Policy? Add to your server or <meta>:
html<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
Or in Nginx:
nginxadd_header Content-Security-Policy "default-src 'self'";
Missing Privacy Policy? You need one if you collect any data (including analytics). Generator: Termly.io or PrivacyPolicies.com
Missing Schema markup? Start with WebPage or Organization:
html<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Page Title",
  "description": "Page description",
  "url": "https://yourdomain.com/page"
}
</script>
Missing canonical?
html<link rel="canonical" href="https://yourdomain.com/this-page/" />

Roadmap

 --json flag for CI/CD integration
 --compare domain1.com domain2.com competitor mode
 DNS and email security checks (SPF, DKIM, DMARC)
 Lighthouse integration via PageSpeed API
 Broken links checker
 Third-party script audit (tracking bloat)

PRs welcome.

Contributing
Each check is a simple function returning {"pass": bool, "impact": str, "category": str}. Add your check to the appropriate check_* function and submit a PR explaining what it catches and why it matters for founders.

License
MIT — free to use and modify.

Related

FounderScan.dev — Full website audit platform with detailed reports
Website security checklist for startups — Complete security guide
GDPR compliance checklist for SaaS — What you legally need
Technical SEO audit guide — Fix rankings fast
Performance optimization for founders — Speed up your site


Because "it looks fine" isn't a technical audit.
