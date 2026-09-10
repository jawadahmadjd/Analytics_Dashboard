---
name: pixel-perfect-ui
description: Industry-grade workflow for cloning and engineering modern user interfaces with 1-to-1 visual fidelity, geometry deconstruction, font ligature protection, two-state conversational layouts, and automated browser screenshot verification.
---

# Pixel-Perfect UI Engineering Skill

This skill guides the agent to replicate and engineer user interfaces with exact visual parity to design targets (screenshots, mockups, Figma references).

## 1. Visual Geometry Deconstruction (Before Writing Any Code)
When given a target screenshot or mockup, divide the layout into standard architectural zones:
1. **Global Header / Top Bar**: Model selectors, brand badges, profile triggers, breadcrumbs.
2. **Left Navigation Sidebar**: Brand emblem, action triggers (+ New Chat, Search), categorized list (Chats), pinned bottom utilities (Settings, Help).
3. **Main Viewport Canvas**: Responsive max-width constraints (e.g. 760px for conversational threads, 1440px for analytical cockpits).
4. **Hero State vs Active State**:
   - **Empty / Initial State**: Vertically centered headline, centered input pill, suggestion chips, and bottom-anchored disclaimer.
   - **Active State**: Top-down message stream, user bubble right-aligned or subtle background, assistant content with rich markdown, sticky bottom input bar.

## 2. Font & Icon Ligature Protection (Strict Zero-Glitch Rule)
Never apply indiscriminate universal font overrides like `* { font-family: ... !important; }` or `span { font-family: ... !important; }`.
- Universal font rules break icon ligatures used by Google Material Symbols, FontAwesome, Lucide, and Feather icons, causing raw text strings to leak onto the screen (e.g., `keyboard_double_arrow_left`, `_arr_div_Settings`).
- Standard Rule:
```css
/* Apply font family to text elements while explicitly exempting icons */
body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, input, textarea {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif !important;
}

/* Explicitly preserve icon fonts */
.material-symbols-rounded,
.material-symbols-outlined,
[class*="material-symbols"],
[data-testid*="Icon"],
span[data-testid*="Icon"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    direction: ltr !important;
}
```

## 3. Two-State Conversational Architecture (ChatGPT Standard)
When building AI chat interfaces:
1. **Empty State (messages == 0)**:
   - Headline: Large, clean, medium-weight centered prompt (e.g., "Where should we begin?").
   - Input: Centered pill with `border-radius: 28px`, subtle shadow `0 4px 16px rgba(0,0,0,0.06)`, and an integrated circular send button.
   - Suggestion Chips: Pill-shaped quick-prompts placed cleanly below the input pill (`border-radius: 9999px; border: 1px solid #E5E5E5;`).
   - Disclaimer: Pinned to the very bottom of the viewport.
2. **Active State (messages > 0)**:
   - The centered hero and suggestion chips smoothly disappear.
   - The message thread starts from the top with clear distinction between user and assistant.
   - The input pill anchors firmly to the bottom with a subtle fade gradient background.

## 4. Framework Chrome Elimination
Always cleanly suppress framework-specific chrome that interferes with consumer UI aesthetics:
- In Streamlit: Hide `[data-testid="stDeployButton"]`, `div[data-testid="stToolbarActions"]`, `div[data-testid="stStatusWidget"]`, `#MainMenu`, and `footer`.
- In Gradio: Hide `.footer`, `.share-button`.
- In Next.js/React: Remove default dev badges in production preview.

## 5. Automated Visual Feedback Loop
Never assume CSS looks correct without visual confirmation:
1. After rendering a UI, run an automated browser check (`browser_subagent` or Playwright) to capture a full-viewport screenshot.
2. Inspect the screenshot for:
   - Icon ligature leakage or broken text.
   - Form buttons rendering outside input pills.
   - Misaligned margins, overlapping layers, or container scrollbars.
3. Fix any defects before reporting completion to the user.
