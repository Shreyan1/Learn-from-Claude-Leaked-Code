import re
import sys

def main():
    filename = 'css/style.css'
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update :root
    root_replacements = """  /* Sidebar */
  --sidebar-bg:   #ffffff;
  --sidebar-border: rgba(0,0,0,0.08);
  --nav-hover-bg: rgba(0,0,0,0.04);
  --sidebar-w:    272px;"""
    content = re.sub(
        r'/\* Sidebar \*/.*?--sidebar-w:\s*272px;',
        root_replacements,
        content,
        flags=re.DOTALL
    )

    # Update dark theme
    dark_replacements = """[data-theme="dark"] {
  --bg:         #0f0f1a;
  --surface:    #1a1a2e;
  --border:     #2d2d45;
  --text:       #e2e8f0;
  --text-muted: #94a3b8;
  --sidebar-bg: #0f0f1a;
  --sidebar-border: rgba(255,255,255,0.08);
  --nav-hover-bg: rgba(255,255,255,0.04);
}"""
    content = re.sub(
        r'\[data-theme="dark"\] \{.*?\}',
        dark_replacements,
        content,
        flags=re.DOTALL
    )

    # site-header border
    content = content.replace('border-bottom: 1px solid rgba(255,255,255,0.08);', 'border-bottom: 1px solid var(--sidebar-border);')

    # site header logo text
    content = content.replace('.site-header .logo-text {\n  font-size: 0.9375rem;\n  font-weight: 600;\n  color: #fff;\n}', '.site-header .logo-text {\n  font-size: 0.9375rem;\n  font-weight: 600;\n  color: var(--text);\n}')

    # btn-icon
    content = content.replace('background: rgba(255,255,255,0.07);\n  border: 1px solid rgba(255,255,255,0.1);\n  border-radius: 8px;\n  color: #b0bac8;', 'background: var(--nav-hover-bg);\n  border: 1px solid var(--sidebar-border);\n  border-radius: 8px;\n  color: var(--text-muted);')
    content = content.replace('.btn-icon:hover { background: rgba(255,255,255,0.12); color: #fff; }', '.btn-icon:hover { background: var(--sidebar-border); color: var(--text); }')

    # sidebar border
    content = content.replace('border-right: 1px solid rgba(255,255,255,0.06);', 'border-right: 1px solid var(--sidebar-border);')

    # sidebar scrollbar
    content = content.replace('scrollbar-color: rgba(255,255,255,0.12) transparent;', 'scrollbar-color: var(--sidebar-border) transparent;')
    content = content.replace('.sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 4px; }', '.sidebar::-webkit-scrollbar-thumb { background: var(--sidebar-border); border-radius: 4px; }')

    # sidebar text colors
    content = content.replace('.sidebar-section-title {\n  font-size: 0.6875rem;\n  font-weight: 600;\n  letter-spacing: 0.08em;\n  text-transform: uppercase;\n  color: #4a5568;', '.sidebar-section-title {\n  font-size: 0.6875rem;\n  font-weight: 600;\n  letter-spacing: 0.08em;\n  text-transform: uppercase;\n  color: var(--text-muted);')

    # nav links
    content = content.replace('.sidebar-nav a {\n  display: flex;\n  align-items: center;\n  gap: 0.5rem;\n  padding: 0.425rem 1.25rem;\n  font-size: 0.875rem;\n  color: #8892a0;', '.sidebar-nav a {\n  display: flex;\n  align-items: center;\n  gap: 0.5rem;\n  padding: 0.425rem 1.25rem;\n  font-size: 0.875rem;\n  color: var(--text-muted);')

    content = content.replace('.sidebar-nav a:hover {\n  color: #d1d9e0;\n  background: rgba(255,255,255,0.04);\n}', '.sidebar-nav a:hover {\n  color: var(--text);\n  background: var(--nav-hover-bg);\n}')

    content = content.replace('.sidebar-nav a.active {\n  color: #fff;\n  background: rgba(217,119,87,0.12);\n}', '.sidebar-nav a.active {\n  color: var(--text);\n  background: rgba(217,119,87,0.12);\n}')

    # sidebar sub nav
    content = content.replace('color: #8892a0;\n  font-size: 0.8125rem;', 'color: var(--text-muted);\n  font-size: 0.8125rem;')
    content = content.replace('.sidebar-sub-nav a:hover {\n  color: #d1d9e0;\n}', '.sidebar-sub-nav a:hover {\n  color: var(--text);\n}')
    content = content.replace('.sidebar-sub-nav a.sub-active {\n  color: var(--coral);\n  font-weight: 500;\n}', '.sidebar-sub-nav a.sub-active {\n  color: var(--coral);\n  font-weight: 500;\n}')

    # Sidebar download border
    content = content.replace('.sidebar-download {\n  padding: 1rem 1.25rem 0;\n  margin-top: 0.5rem;\n  border-top: 1px solid rgba(255,255,255,0.07);\n}', '.sidebar-download {\n  padding: 1rem 1.25rem 0;\n  margin-top: 0.5rem;\n  border-top: 1px solid var(--sidebar-border);\n}')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
