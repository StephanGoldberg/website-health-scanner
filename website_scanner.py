#!/usr/bin/env python3
"""
Website Health Scanner for Founders
Quick security, SEO, performance, and compliance check
for any website — from your terminal.

For a full detailed report with actionable fixes:
→ https://founderscan.dev
"""

import urllib.request
import urllib.error
import ssl
import sys
import re
import socket
from datetime import datetime


def fetch_url(url: str, timeout: int = 12):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "FounderScan/1.0 (https://founderscan.dev)"}
    )
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, context=ctx, timeout=timeout)


def check_security(url: str, html: str, headers: dict) -> dict:
    results = {}

    # Security headers
    security_headers = {
        "strict-transport-security": ("HSTS", "high"),
        "x-content-type-options": ("X-Content-Type-Options", "medium"),
        "x-frame-options": ("X-Frame-Options", "medium"),
        "content-security-policy": ("CSP", "high"),
        "referrer-policy": ("Referrer-Policy", "low"),
        "permissions-policy": ("Permissions-Policy", "low"),
    }
    for header, (label, impact) in security_headers.items():
        results[label] = {
            "pass": header in headers,
            "impact": impact,
            "category": "security",
        }

    # HTTPS
    results["HTTPS/SSL"] = {
        "pass": url.startswith("https://"),
        "impact": "critical",
        "category": "security",
    }

    # Mixed content
    results["No mixed content"] = {
        "pass": "http://" not in re.sub(r'<script[^>]*src=["\']http://', '', html),
        "impact": "high",
        "category": "security",
    }

    return results


def check_seo(html: str, url: str) -> dict:
    results = {}

    # Title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else None
    if not title:
        results["Title tag"] = {"pass": False, "impact": "critical", "category": "seo", "detail": "Missing"}
    elif len(title) < 30 or len(title) > 60:
        results["Title tag"] = {"pass": False, "impact": "high", "category": "seo", "detail": f"{len(title)} chars (target: 30-60)"}
    else:
        results["Title tag"] = {"pass": True, "impact": "critical", "category": "seo", "detail": title[:50]}

    # Meta description
    desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    desc = desc_match.group(1) if desc_match else None
    if not desc:
        results["Meta description"] = {"pass": False, "impact": "high", "category": "seo", "detail": "Missing"}
    elif len(desc) < 70 or len(desc) > 160:
        results["Meta description"] = {"pass": False, "impact": "medium", "category": "seo", "detail": f"{len(desc)} chars (target: 70-160)"}
    else:
        results["Meta description"] = {"pass": True, "impact": "high", "category": "seo", "detail": f"{len(desc)} chars ✓"}

    # H1
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s]
    if not h1s:
        results["H1 tag"] = {"pass": False, "impact": "critical", "category": "seo", "detail": "Missing"}
    elif len(h1s) > 1:
        results["H1 tag"] = {"pass": False, "impact": "high", "category": "seo", "detail": f"{len(h1s)} H1s found (should be 1)"}
    else:
        results["H1 tag"] = {"pass": True, "impact": "critical", "category": "seo", "detail": h1s[0][:50]}

    # Canonical
    has_canonical = bool(re.search(r'rel=["\']canonical["\']', html, re.IGNORECASE))
    results["Canonical tag"] = {"pass": has_canonical, "impact": "high", "category": "seo", "detail": None}

    # Schema
    has_schema = 'application/ld+json' in html
    results["Schema markup"] = {"pass": has_schema, "impact": "high", "category": "seo", "detail": None}

    # OG tags
    has_og = 'property="og:title"' in html.lower() or "property='og:title'" in html.lower()
    results["Open Graph tags"] = {"pass": has_og, "impact": "medium", "category": "seo", "detail": None}

    return results


def check_performance(load_time: float, html: str) -> dict:
    results = {}

    results["Load time (<2s)"] = {
        "pass": load_time < 2.0,
        "impact": "high",
        "category": "performance",
        "detail": f"{load_time}s",
    }

    results["Load time (<3s)"] = {
        "pass": load_time < 3.0,
        "impact": "critical",
        "category": "performance",
        "detail": f"{load_time}s",
    }

    # Viewport
    has_viewport = 'name="viewport"' in html.lower() or "name='viewport'" in html.lower()
    results["Mobile viewport"] = {"pass": has_viewport, "impact": "high", "category": "performance", "detail": None}

    # Image alt text
    imgs = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
    missing_alt = sum(1 for img in imgs if not re.search(r'alt=["\'][^"\']+["\']', img, re.IGNORECASE))
    if imgs:
        results["Image alt text"] = {
            "pass": missing_alt == 0,
            "impact": "medium",
            "category": "performance",
            "detail": f"{missing_alt}/{len(imgs)} missing alt" if missing_alt else f"All {len(imgs)} have alt text",
        }

    # Minification hint (rough check)
    long_whitespace = len(re.findall(r'\n\s{10,}', html))
    results["HTML not bloated"] = {
        "pass": long_whitespace < 50,
        "impact": "low",
        "category": "performance",
        "detail": None,
    }

    return results


def check_compliance(html: str, url: str) -> dict:
    results = {}
    html_lower = html.lower()

    # Privacy policy
    has_privacy = any(x in html_lower for x in ['privacy policy', 'privacy-policy', '/privacy', 'gdpr', 'data protection'])
    results["Privacy policy"] = {"pass": has_privacy, "impact": "high", "category": "compliance", "detail": None}

    # Cookie notice
    has_cookie = any(x in html_lower for x in ['cookie', 'consent', 'gdpr', 'we use cookies'])
    results["Cookie notice"] = {"pass": has_cookie, "impact": "medium", "category": "compliance", "detail": None}

    # Terms of service
    has_terms = any(x in html_lower for x in ['terms of service', 'terms and conditions', '/terms', 'terms of use'])
    results["Terms of service"] = {"pass": has_terms, "impact": "medium", "category": "compliance", "detail": None}

    # Contact info
    has_contact = any(x in html_lower for x in ['contact', 'email', '@', 'mailto:'])
    results["Contact info"] = {"pass": has_contact, "impact": "low", "category": "compliance", "detail": None}

    return results


def check_infra(domain: str, base_url: str) -> dict:
    results = {}

    for path, label, impact in [
        ("/robots.txt", "robots.txt", "medium"),
        ("/sitemap.xml", "sitemap.xml", "high"),
    ]:
        try:
            with fetch_url(base_url + path, timeout=8) as r:
                results[label] = {"pass": r.status == 200, "impact": impact, "category": "seo", "detail": None}
        except Exception:
            results[label] = {"pass": False, "impact": impact, "category": "seo", "detail": None}

    return results


IMPACT_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
IMPACT_ICONS = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

CATEGORY_LABELS = {
    "security": "🔒 SECURITY",
    "seo": "🔍 SEO",
    "performance": "⚡ PERFORMANCE",
    "compliance": "📋 COMPLIANCE",
}


def print_report(domain: str, all_checks: dict, load_time: float):
    passed = {k: v for k, v in all_checks.items() if v["pass"]}
    failed = {k: v for k, v in all_checks.items() if not v["pass"]}

    total = len(all_checks)
    score = int((len(passed) / total) * 100)

    # Category scores
    categories = ["security", "seo", "performance", "compliance"]
    cat_scores = {}
    for cat in categories:
        cat_checks = {k: v for k, v in all_checks.items() if v["category"] == cat}
        if cat_checks:
            cat_pass = sum(1 for v in cat_checks.values() if v["pass"])
            cat_scores[cat] = int((cat_pass / len(cat_checks)) * 100)

    if score >= 85:
        verdict = "🟢 Excellent — well-built site"
    elif score >= 65:
        verdict = "🟡 Good — a few things to fix"
    elif score >= 45:
        verdict = "🟠 Needs work — multiple issues detected"
    else:
        verdict = "🔴 Critical — significant problems found"

    print(f"\n{'='*62}")
    print(f"  🔬 FounderScan — Website Health Report")
    print(f"  Site: {domain}   |   Load time: {load_time}s")
    print(f"{'='*62}")

    print(f"\n  OVERALL SCORE: {score}/100  —  {verdict}")
    print(f"\n  {'─'*55}")
    for cat in categories:
        if cat in cat_scores:
            bar_filled = int(cat_scores[cat] / 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            print(f"  {CATEGORY_LABELS[cat]:<22} [{bar}] {cat_scores[cat]}%")

    # Failed checks by category
    if failed:
        print(f"\n{'─'*62}")
        print(f"  ISSUES FOUND ({len(failed)})  —  ordered by impact")
        print(f"{'─'*62}")

        for cat in categories:
            cat_failed = {k: v for k, v in failed.items() if v["category"] == cat}
            if not cat_failed:
                continue
            print(f"\n  {CATEGORY_LABELS[cat]}")
            for name, check in sorted(cat_failed.items(), key=lambda x: IMPACT_ORDER.get(x[1]["impact"], 3)):
                icon = IMPACT_ICONS.get(check["impact"], "⚪")
                detail = f"  ({check['detail']})" if check.get("detail") else ""
                print(f"    {icon} {name}{detail}")

    # Passed checks
    print(f"\n{'─'*62}")
    print(f"  PASSING ({len(passed)}/{total})")
    print(f"{'─'*62}")
    for cat in categories:
        cat_passed = [k for k, v in passed.items() if v["category"] == cat]
        if cat_passed:
            print(f"  {CATEGORY_LABELS[cat]}: {', '.join(cat_passed)}")

    print(f"\n{'='*62}")
    print(f"  📊 Get the full FounderScan report:")
    print(f"  Detailed fixes, priority order, compliance checklist,")
    print(f"  performance recommendations & PDF export:")
    print(f"  👉  https://founderscan.dev")
    print(f"{'='*62}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python website_scanner.py <domain>")
        print("Example: python website_scanner.py mystartup.com")
        sys.exit(1)

    domain = sys.argv[1].replace("https://", "").replace("http://", "").strip("/")
    base_url = f"https://{domain}"

    print(f"\n⏳ Scanning {domain}...")
    print("   Checking security, SEO, performance, and compliance...\n")

    try:
        start = datetime.now()
        with fetch_url(base_url) as r:
            load_time = round((datetime.now() - start).total_seconds(), 2)
            html = r.read().decode("utf-8", errors="ignore")
            resp_headers = {k.lower(): v for k, v in r.headers.items()}
    except Exception as e:
        print(f"  ❌ Could not reach {base_url}: {e}")
        sys.exit(1)

    all_checks = {}
    all_checks.update(check_security(base_url, html, resp_headers))
    all_checks.update(check_seo(html, base_url))
    all_checks.update(check_performance(load_time, html))
    all_checks.update(check_compliance(html, base_url))
    all_checks.update(check_infra(domain, base_url))

    print_report(domain, all_checks, load_time)


if __name__ == "__main__":
    main()
