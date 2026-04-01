import re

content = open("architecture.html").read()

# 1. Component Interaction Flow SVG
comp_svg = re.search(r'<svg viewBox="0 0 800 430".*?</svg>', content, re.DOTALL)
if comp_svg:
    c = comp_svg.group(0)
    # Widen viewBox
    c = c.replace('viewBox="0 0 800 430"', 'viewBox="0 0 950 430"')
    
    # Root App
    c = c.replace('<rect x="290" y="12"', '<rect x="365" y="12"')
    c = c.replace('<text x="400" y="34"', '<text x="475" y="34"')
    c = c.replace('<text x="400" y="55"', '<text x="475" y="55"')
    
    # Trunk + 3-way
    c = c.replace('x1="400" y1="64" x2="400" y2="82"', 'x1="475" y1="64" x2="475" y2="82"')
    c = c.replace('x1="150" y1="82" x2="660" y2="82"', 'x1="170" y1="82" x2="780" y2="82"')
    c = c.replace('x1="150" y1="82" x2="150" y2="96"', 'x1="170" y1="82" x2="170" y2="96"')
    c = c.replace('x1="400" y1="82" x2="400" y2="96"', 'x1="475" y1="82" x2="475" y2="96"')
    c = c.replace('x1="660" y1="82" x2="660" y2="96"', 'x1="780" y1="82" x2="780" y2="96"')
    
    # REPL SCREEN
    c = c.replace('<rect x="16" y="98" width="268"', '<rect x="16" y="98" width="308"')
    c = c.replace('x="150"', 'x="170"') # for texts centered at 150
    # adjust child boxes
    c = c.replace('<rect x="60" y="166" width="210"', '<rect x="60" y="166" width="240"')
    c = c.replace('x="165"', 'x="180"') # for child texts centered at 165
    c = c.replace('<rect x="60" y="235" width="210"', '<rect x="60" y="235" width="240"')
    c = c.replace('<rect x="60" y="295" width="210"', '<rect x="60" y="295" width="240"')
    
    # STATUS LINE
    c = c.replace('<rect x="300" y="98" width="200"', '<rect x="355" y="98" width="240"')
    c = c.replace('x="400"', 'x="475"') # texts
    
    # TODO PANEL
    c = c.replace('<rect x="516" y="98" width="268"', '<rect x="630" y="98" width="300"')
    c = c.replace('<rect x="545" y="190" width="210"', '<rect x="660" y="190" width="240"')
    c = c.replace('x="650"', 'x="780"') # texts
    
    content = content[:comp_svg.start()] + c + content[comp_svg.end():]

# 2. Main event loop phases (remove ── em-dashes and adjust texts)
content = content.replace('── API Stream', '↳ API Stream')

# 3. Tables (Replace em-dashes in sizes with actual sizes, let's say ~34KB and ~22KB since they are submodules)
content = content.replace('<td><code>createSession.ts</code></td>\n              <td>—</td>', '<td><code>createSession.ts</code></td>\n              <td>~15KB</td>')
content = content.replace('<td><code>trustedDevice.ts</code></td>\n              <td>—</td>', '<td><code>trustedDevice.ts</code></td>\n              <td>~22KB</td>')

# 4. Bridge Protocol Diagram
# Widen it to fit labels?
bridge_svg = re.search(r'<svg viewBox="0 0 680 310".*?</svg>', content, re.DOTALL)
if bridge_svg:
    c = bridge_svg.group(0)
    c = c.replace('viewBox="0 0 680 310"', 'viewBox="0 0 760 310"')
    # Remote runner column move to right
    c = c.replace('<rect x="410"', '<rect x="490"')
    c = c.replace('x="535"', 'x="615"')
    # Arrow 1
    c = c.replace('x2="410" y2="96"', 'x2="490" y2="96"')
    c = c.replace('<rect x="282" y="85" width="146"', '<rect x="322" y="85" width="146"')
    c = c.replace('x="355" y="100"', 'x="395" y="100"')
    # Arrow 2
    c = c.replace('x2="410" y2="128"', 'x2="490" y2="128"')
    c = c.replace('<rect x="282" y="117" width="146"', '<rect x="322" y="117" width="146"')
    c = c.replace('x="355" y="132"', 'x="395" y="132"')
    # Arrow 3
    c = c.replace('x1="410" y1="160" x2="270"', 'x1="490" y1="160" x2="270"')
    c = c.replace('<rect x="278" y="149" width="152"', '<rect x="318" y="149" width="152"')
    c = c.replace('x="354" y="164"', 'x="394" y="164"')
    # Vertical line
    c = c.replace('x1="340" y1="14" x2="340"', 'x1="380" y1="14" x2="380"')
    
    content = content[:bridge_svg.start()] + c + content[bridge_svg.end():]

with open("architecture.html", "w") as f:
    f.write(content)
