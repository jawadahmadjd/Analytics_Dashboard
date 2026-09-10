# Global Frontend & UI Design Standards

These rules apply across all projects whenever generating, editing, or refactoring user interfaces:

1. **Pixel Parity with Design References**:
   - When provided with a screenshot or design reference, match its geometry, typography, colors, and layout structure with 1-to-1 fidelity before adding unrequested extra widgets.
2. **Font Ligature Protection**:
   - Never apply blanket `span { font-family: ... !important; }`. Always explicitly preserve icon fonts (`.material-symbols`, FontAwesome, SVG icons) to avoid broken text like `keyboard_double_` or `_arr_div_`.
3. **Clean Conversational Layout Architecture**:
   - In consumer conversational apps, provide a clean two-state transition: centered input for empty chats, bottom sticky bar for active chats, and a clean sidebar maintaining full conversation history.
4. **Visual Inspection**:
   - Always run a visual verification check (e.g. browser screenshot) before presenting completed UI work to ensure no alignment collisions, overlapping text, or framework chrome leaks.
