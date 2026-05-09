"""
Management command: render_design_system

Renders the DCR design system reference to a self-contained HTML file.
Intended for use as part of the documentation build pipeline.

Usage:
    python manage.py render_design_system
    python manage.py render_design_system --output path/to/output.html

Makefile usage (from repo root):
    python example_project/manage.py render_design_system --output docs/design-system.html
"""

import os

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

STATIC_ROOT = os.path.join(
    REPO_ROOT, "dj_control_room_base", "static", "dj_control_room_base"
)

DEFAULT_OUTPUT = os.path.join(REPO_ROOT, "docs", "design-system.html")

TABS = [
    ("application", "Application"),
    ("tokens", "Tokens"),
    ("buttons", "Buttons &amp; Badges"),
    ("forms", "Forms"),
    ("data", "Data Tables"),
    ("cards", "Cards &amp; Feeds"),
    ("nav", "Navigation"),
]


def _read_static(*parts):
    with open(os.path.join(STATIC_ROOT, *parts), encoding="utf-8") as f:
        return f.read()


class Command(BaseCommand):
    help = "Render the DCR design system to a self-contained HTML file for the docs site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=DEFAULT_OUTPUT,
            help="Path to write the generated HTML file (default: docs/design-system.html).",
        )

    def handle(self, *args, **options):
        output_path = options["output"]

        self.stdout.write("Rendering design system partials...")
        rendered = {
            tab_id: render_to_string(
                f"admin/dj_control_room_base/sg_partials/{tab_id}.html", {}
            )
            for tab_id, _ in TABS
        }

        self.stdout.write("Assembling page...")
        html = self._build_page(rendered)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.stdout.write(
            self.style.SUCCESS(
                f"Written {len(html):,} bytes to {output_path}"
            )
        )

    def _build_page(self, rendered_partials):
        design_system_css = _read_static("css", "design-system.css")
        styles_css = _read_static("css", "styles.css")
        highlight_css = _read_static("vendor", "highlight-github-dark.min.css")
        highlight_js = _read_static("vendor", "highlight.min.js")
        highlight_python_js = _read_static("vendor", "highlight-python.min.js")

        tabs_html = "\n    ".join(
            f'<a href="#{tab_id}" class="dcr-tabs__tab" data-sg-tab="{tab_id}">{label}</a>'
            for tab_id, label in TABS
        )

        panes_html = "\n".join(
            '<div id="sg-pane-{tab_id}" class="dcr-sg-tab-pane"{hidden}>\n{content}\n</div>'.format(
                tab_id=tab_id,
                hidden="" if i == 0 else " hidden",
                content=rendered_partials[tab_id],
            )
            for i, (tab_id, _) in enumerate(TABS)
        )

        tab_ids_js = str([t for t, _ in TABS])

        inline_js = f"""
document.addEventListener('DOMContentLoaded', function () {{
  document.querySelectorAll('.dcr-sg-code code, .dcr-code-viewer__body code').forEach(function (el) {{
    hljs.highlightElement(el);
  }});

  var TABS = {tab_ids_js};
  var DEFAULT_TAB = 'application';

  function showTab(id) {{
    if (TABS.indexOf(id) === -1) id = DEFAULT_TAB;
    TABS.forEach(function (t) {{
      var pane = document.getElementById('sg-pane-' + t);
      var tab  = document.querySelector('[data-sg-tab="' + t + '"]');
      if (pane) pane.hidden = (t !== id);
      if (tab) {{
        tab.classList.toggle('active', t === id);
        tab.setAttribute('aria-current', t === id ? 'page' : 'false');
      }}
    }});
    history.replaceState(null, '', '#' + id);
  }}

  document.querySelectorAll('[data-sg-tab]').forEach(function (tab) {{
    tab.addEventListener('click', function (e) {{
      e.preventDefault();
      showTab(tab.dataset.sgTab);
    }});
  }});

  var initial = (location.hash || '').replace('#', '') || DEFAULT_TAB;
  showTab(initial);

  document.addEventListener('click', function (e) {{
    if (!e.target.closest('.dcr-dropdown')) {{
      document.querySelectorAll('.dcr-dropdown.is-open').forEach(function (d) {{
        d.classList.remove('is-open');
        var trigger = d.querySelector('[aria-expanded]');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      }});
    }}
  }});

  document.addEventListener('keydown', function (e) {{
    if (e.key === 'Escape') {{
      document.querySelectorAll('.dcr-dropdown.is-open').forEach(function (d) {{
        d.classList.remove('is-open');
        var trigger = d.querySelector('[aria-expanded]');
        if (trigger) {{ trigger.setAttribute('aria-expanded', 'false'); trigger.focus(); }}
      }});
    }}
  }});
}});
"""

        # --dcr-font-sans is used in design-system.css but defined by Django admin's
        # base.css at runtime. Define it here so the standalone page matches the live panel.
        standalone_style = """
:root {
  --dcr-font-sans:
    -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, Roboto,
    "Helvetica Neue", Arial, sans-serif,
    "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
body {
  font-family: var(--dcr-font-sans);
  font-size: 14px;
  margin: 0;
  padding: 0;
  background: var(--dcr-color-bg);
}
.dcr-docs-topbar {
  display: flex;
  align-items: center;
  gap: var(--dcr-space-md);
  padding: var(--dcr-space-sm) var(--dcr-space-lg);
  background: var(--dcr-color-bg);
  border-bottom: 1px solid var(--dcr-color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.dcr-docs-topbar__back {
  color: var(--dcr-color-accent);
  text-decoration: none;
  font-size: var(--dcr-font-size-sm);
  font-weight: 500;
}
.dcr-docs-topbar__back:hover { text-decoration: underline; }
.dcr-docs-topbar__title {
  color: var(--dcr-color-text-muted);
  font-size: var(--dcr-font-size-sm);
}
.dcr-content {
  padding-top: var(--dcr-space-lg);
}
"""

        return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DCR Design System - dj-control-room-base</title>
  <style>{design_system_css}</style>
  <style>{styles_css}</style>
  <style>{highlight_css}</style>
  <style>{standalone_style}</style>
</head>
<body>

<div class="dcr-docs-topbar">
  <a href="index.html" class="dcr-docs-topbar__back">&#8592; Back to docs</a>
  <span class="dcr-docs-topbar__title">dj-control-room-base / Design System</span>
</div>

<div class="dcr-content dcr-content--lg">

  <div class="dcr-page-header">
    <div class="dcr-page-header__main">
      <div class="dcr-page-header__icon" style="background:var(--dcr-color-accent)">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
          <path d="M2 12h20"/>
        </svg>
      </div>
      <div class="dcr-page-header__body">
        <div class="dcr-page-header__title-row">
          <h1 class="dcr-page-header__title">DCR Design System</h1>
          <span class="dcr-pill dcr-pill--success">
            <span class="dcr-pill__dot"></span>STYLES
          </span>
        </div>
        <p class="dcr-page-header__subtitle">
          Components and tokens for building Django Control Room panels.
          Extend <code class="dcr-code">panel_base.html</code> to inherit this design system in any panel.
        </p>
      </div>
    </div>
  </div>

  <nav class="dcr-tabs dcr-sg-topnav" aria-label="Design system sections">
    {tabs_html}
  </nav>

  {panes_html}

</div>

<script>{highlight_js}</script>
<script>{highlight_python_js}</script>
<script>{inline_js}</script>

</body>
</html>"""
