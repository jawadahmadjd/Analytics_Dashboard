---
name: ui-ux-design-systems
description: Comprehensive design system standards, token architecture, 8px spatial grid, curated HSL color palettes, typography scales, and micro-interactions for modern web applications.
---

# UI/UX Design Systems Standards

This skill enforces enterprise-grade aesthetic quality, preventing AI from generating flat, uninspired, or generic interfaces.

## 1. The 8px Spatial Grid Scale
Every margin, padding, height, and gap must align to the 8px grid (with 4px half-step for micro-elements):
- `4px` (--space-1): Badge padding, icon gap.
- `8px` (--space-2): Compact padding, button horizontal gap.
- `12px` (--space-3): Standard card internal gap.
- `16px` (--space-4): Default container padding, standard gutter.
- `24px` (--space-6): Section separation, hero spacing.
- `32px` (--space-8): Large component separation.
- `48px` (--space-12): Header to main hero offset.
- `64px` (--space-16): Landing section spacing.

## 2. Curated Color Palettes (Never Use Pure Primitive Colors)
Avoid saturated primary colors (pure red #FF0000, pure blue #0000FF, pure green #00FF00).
Use curated, balanced semantic tokens:
- **Dark Luxury / Slate**:
  - Surface: `#0B192C` (Imperial Navy), `#0F172A` (Slate 900)
  - Card: `#1E293B` (Slate 800)
  - Border: `rgba(255, 255, 255, 0.08)`
  - Accent: `#C5A059` (Brushed Gold), `#38BDF8` (Cyan 400)
- **Minimalist White / Consumer SaaS (OpenAI / Vercel style)**:
  - Canvas: `#FFFFFF`
  - Sidebar / Secondary: `#F9F9F9`
  - Subtle Hover: `#ECECEC`
  - Border: `#E5E5E5` or `#E4E4E7`
  - Text Primary: `#0D0D0D`
  - Text Secondary: `#676767`
  - Text Muted: `#8E8E8E`
- **Semantic Status**:
  - Positive: `#10B981` (Emerald), background `#ECFDF5`, border `#A7F3D0`
  - Warning: `#F59E0B` (Amber), background `#FFFBEB`, border `#FDE68A`
  - Critical: `#EF4444` (Rose), background `#FEF2F2`, border `#FECACA`

## 3. Typographic Hierarchy
Always enforce clear scale and weights:
- **Display Hero**: `32px - 40px`, font-weight `600 - 700`, letter-spacing `-0.025em`.
- **Section Heading (H2)**: `20px - 24px`, font-weight `600`, line-height `1.3`.
- **Card Title / Subhead (H3)**: `15px - 17px`, font-weight `600`.
- **Body Text**: `14px - 15px`, line-height `1.5`, color `--text-primary`.
- **Secondary Caption**: `12px - 13px`, color `--text-secondary`.
- **Micro-Label / Metadata**: `10.5px - 11.5px`, font-weight `600`, letter-spacing `0.04em`, uppercase.
- **Metrics & Code**: JetBrains Mono or SF Mono, tabular figures (`font-variant-numeric: tabular-nums`).

## 4. Micro-Interactions & Elevation
- **Transitions**: Standardize on `150ms ease` or `200ms cubic-bezier(0.4, 0, 0.2, 1)`.
- **Hover Feedback**: Never leave interactive buttons without hover feedback (subtle background shift, border-color change, or 1px translateY).
- **Elevation Shadows**: Avoid harsh black drop shadows. Use layered ambient shadows:
  - Subtle: `0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02)`
  - Floating Card / Pill: `0 4px 16px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.03)`
  - Modal: `0 20px 40px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.06)`
