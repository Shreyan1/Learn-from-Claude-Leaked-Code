import os
import re

faqs = {
    "index.html": [
        ("How do I install this leaked version of Claude Code?", "You don't — this guide is strictly educational. It exists to study the codebase architecture, not to run it."),
        ("What are the key takeaways from the Claude Code source?", "It reveals incredible patterns for an agentic loop, robust tool dispatching, compact context management, and graceful rendering of terminal UI using React."),
        ("Is it legal to study leaked code?", "This repository serves as educational material on state-of-the-art AI agent design. Use it to learn design and architectural patterns, not to reproduce proprietary systems."),
        ("What language is Claude Code built in?", "It is built heavily in TypeScript, utilizing Node.js with Bun for bundling and React Ink for terminal rendering."),
        ("Where should I start if I want to learn the system?", "Start with the Architecture page to understand the core loop, then read about the Query Engine and Tool Dispatching.")
    ],
    "architecture.html": [
        ("Does Claude Code use Redux for state?", "No. Claude Code uses a custom, lightweight, Zustand-inspired store pattern rather than Redux. This keeps state immutable and predictably threaded through the Ink component tree without the heavy boilerplate of Redux."),
        ("What is BRIDGE_MODE used for?", "<code>BRIDGE_MODE</code> is a compile-time feature flag that powers Claude Code's remote execution architecture. In typical local builds, it is eliminated via dead-code elimination (DCE). In remote environments, it proxies the REPL across WebSockets."),
        ("Can I customize the \"thinking\" verb animations?", "Yes! Claude Code includes over 190 built-in spinner verbs (like \"Flibbertigibbeting...\"). You can override or append to this list via your <code>~/.claude/settings.json</code> file using the <code>spinnerVerbs</code> configuration hook."),
        ("Does Claude Code use a standard frontend framework?", "It uses React alongside Ink to render a reactive component tree directly into the terminal, rather than a browser."),
        ("How is the codebase structured?", "It is surprisingly flat. The most critical files like query.ts, main.tsx, and QueryEngine.ts live in the root directory rather than deep nested folders."),
        ("Can the SDK mode be used in other applications?", "Yes, because of the two-path architecture, QueryEngine.ts acts as an async generator that can be headless and integrated into any environment programmatically.")
    ],
    "query-engine.html": [
        ("How does Claude Code compress context?", "It uses aggressive compaction techniques, prioritizing errors and recent interactions to keep the context window under the token limit without losing critical working history."),
        ("Does it use the standard Anthropic API?", "Yes, it interacts primarily via Anthropic's streaming SSE endpoints, allowing tool usages and incremental outputs to stream natively into the terminal."),
        ("What happens if the context limit is reached?", "The query engine will trigger a context collapse, stripping out older tool logs and retaining only the summaries of past actions to preserve the flow."),
        ("Can I customize the system prompt?", "The core system prompt is deeply synthesized from configuration, current environment context, and the tool schemas available at runtime, rather than being a static string."),
        ("How is token usage measured efficiently?", "Token lengths are rigorously tracked with a dedicated cost-tracker to measure limits and compute estimated dollar costs during interactions.")
    ],
    "tools.html": [
        ("How do I add my own tool?", "You can build a class implementing the abstract Tool interface, define a zod schema for arguments, and register it in the central tool registry."),
        ("Are bash commands executed natively or safely?", "BashTool executes commands natively, which is why the permission system acts as a crucial checkpoint before potentially dangerous executions."),
        ("How does the WebFetchTool work?", "It scrapes specific URLs, extracts the core content usually converting to markdown, and allows Claude to natively read and interpret remote documentation."),
        ("Why are there so many tools built-in?", "Having over 40 specialised tools like FileEdit, Bash, WebFetch, and MCP prevents the model from relying on slow, error-prone generic bash scripts to perform complex multi-step actions."),
        ("Can tools yield partial results?", "Yes, tools can yield ProgressMessages which render real-time UI feedback to the terminal before the tool action fully resolves.")
    ],
    "security.html": [
        ("Is it safe to give Claude bash access?", "Claude Code provides a granular permission system (ask, allow, deny) to prevent unattended destruction. You are always prompted before dangerous actions unless you explicitly whitelist them."),
        ("Does the tool system circumvent permissions?", "No. Every execution goes through the <code>canUseTool()</code> function which securely evaluates the current PermissionMode constraint before continuing."),
        ("What is the isolated execution mode?", "For advanced use cases, there are mechanisms designed to sandbox executions, ensuring that rogue commands do not compromise your entire file system."),
        ("Can I auto-approve specific folders?", "Yes, you can specify trusted directories where certain non-destructive commands are auto-approved to significantly speed up your development workflows."),
        ("How does OAuth token management work?", "The session utilizes secure JWT-based device trust persistently stored in your local keychain to maintain authentication with the Anthropic cloud infrastructure.")
    ],
    "best-practices.html": [
        ("What is the recommended way to edit files?", "It is highly recommended to use the targeted <code>FileEditTool</code> rather than relying on standard sed commands or asking the agent to rewrite entire files. This prevents context exhaustion and mistakes."),
        ("How should I write a CLAUDE.md file?", "Provide brief, high-signal project overview, conventions, and constraints. Do not put overly generic coding advice inside it; treat it as the DNA of your repository."),
        ("Should I keep the agent task running indefinitely?", "No, use `/compact` or start fresh sessions regularly to reset context overhead, keep inference fast, and dramatically reduce API block costs."),
        ("How can I debug agent loops?", "Pay attention to the tool executions and use the verbose mode if available to see exactly what prompts are being serialized to the runtime API."),
        ("What is the best way to utilize skills?", "Encode heavily repeated multi-step tasks into explicit skills rather than typing out the same verbose manual instructions every single session.")
    ],
    "mcp-skills.html": [
        ("What is MCP (Model Context Protocol)?", "MCP allows seamless connection to external data sources and custom local toolchains without hardcoding them into the main binary application."),
        ("How do skills differ from tools?", "Skills are typically declarative markdown or instruction sets that map to a sequence of actions, whereas tools are hardcoded, native TypeScript functionality."),
        ("Can I build my own MCP server?", "Yes! You can serve endpoints that the agent connects to natively for extending its capabilities and bridging it to internal tools or databases."),
        ("How are skills parsed?", "They are loaded from the file structure and interpreted as dynamic tool expansions, allowing Claude to read and execute the unique workflows described within."),
        ("Are skills shared globally?", "You can have workspace-specific skill directories and global tools, making it easy to specialize the agent for a specific project without muddying your global CLI setup.")
    ],
    "interpret.html": [
        ("What is the quickest way to traverse the codebase?", "Start at <code>main.tsx</code> for the entry sequence, and then jump to <code>query.ts</code> to see the core agentic loop execution."),
        ("How do I track down a specific CLI command?", "All commands are registered into the CLI parsing utility inside <code>main.tsx</code> and cleanly map to specific execution modules in the <code>commands/</code> directory."),
        ("Where is the UI defined?", "The terminal interface is fully defined using standard React components found within the <code>ink/</code> and <code>components/</code> directory abstractions."),
        ("How do I test the internal code?", "Without the full build environment or Anthropic backend, it is difficult to compile, but you can read through the pure TypeScript logic functionally without issue."),
        ("Is the repository documentation up to date?", "This leaked code documentation acts as a snapshot analysis of the architecture and might not perfectly align with future official Claude Code iterations.")
    ]
}

def build_faq_html(items):
    html = '      <section class="faq-section" id="faq">\n'
    html += '        <h2>Frequently Asked Questions</h2>\n'
    for q, a in items:
        html += '        <details class="faq-item">\n'
        html += f'          <summary>{q}</summary>\n'
        html += f'          <div class="faq-content">{a}</div>\n'
        html += '        </details>\n'
    html += '      </section>\n'
    return html

for filename, items in faqs.items():
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    faq_html = build_faq_html(items)
    
    # If the faq-section already exists, replace it
    if '<section class="faq-section" id="faq">' in content:
        content = re.sub(r'<section class="faq-section" id="faq">.*?</section>', faq_html.strip(), content, flags=re.DOTALL)
    else:
        # Inject right before </main>
        content = content.replace('    </main>', faq_html + '\n    </main>')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

