import os
import re
import glob

def main():
    # Find all html files
    html_files = glob.glob('*.html')
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Regex to find SVG tags with mindmap-svg class and a viewBox
        # <svg viewBox="0 0 800 400" ... class="mindmap-svg" ...>
        
        def svg_replacer(match):
            svg_tag = match.group(0)
            
            # If it already has max-width style, skip
            if 'style="max-width:' in svg_tag:
                return svg_tag
                
            # Extract width from viewBox
            vb_match = re.search(r'viewBox="0\s+0\s+(\d+)\s+\d+"', svg_tag)
            if not vb_match:
                return svg_tag
                
            width = vb_match.group(1)
            
            # Insert style="max-width: {width}px;" after the <svg part
            new_svg_tag = svg_tag.replace('<svg ', f'<svg style="max-width: {width}px;" ')
            return new_svg_tag

        # We match from <svg... up to class="mindmap-svg"...> or vice versa
        # Actually, simpler regex: find the full <svg ...> tag
        new_content = re.sub(r'<svg [^>]*class="[^"]*mindmap-svg[^"]*"[^>]*>', svg_replacer, content)
        # Also handle if class comes first
        new_content = re.sub(r'<svg [^>]*mindmap-svg[^>]*>', svg_replacer, new_content)
        
        if new_content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")

if __name__ == '__main__':
    main()
