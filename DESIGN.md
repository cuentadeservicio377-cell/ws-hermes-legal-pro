---
version: alpha
name: Willow Legal Pro
description: Warm legal professionalism meets intuitive touch-first design. A legal dashboard that feels like a companion, not a spreadsheet.
colors:
  # Parchment & Ink — Base legal palette
  parchment: "#FAF9F4"
  ink: "#1A1A18"
  ink-soft: "#3D3D3A"
  ink-muted: "#6B6A63"
  stone: "#9C9B94"
  border-light: "#E8E6DC"
  border-mid: "#D4D2C8"
  
  # Legal Blue — Trust and authority
  legal-blue: "#1B365D"
  legal-blue-soft: "#2A4A7A"
  legal-blue-muted: "#4A6FA5"
  
  # Action Red — Urgency and importance (sparingly)
  action-red: "#8B0000"
  action-red-soft: "#B83232"
  
  # Success & Warning
  success: "#059669"
  warning: "#D97706"
  danger: "#DC2626"
  
  # Surfaces
  surface: "#FFFFFF"
  surface-elevated: "#FFFFFF"
  surface-hover: "#F5F4EF"
  
  # Text on colors
  on-legal-blue: "#FFFFFF"
  on-action-red: "#FFFFFF"
  on-success: "#FFFFFF"
  on-warning: "#FFFFFF"
  on-danger: "#FFFFFF"

typography:
  # Display — Warm authority
  display:
    fontFamily: "Source Serif 4, Newsreader, Charter, Georgia, serif"
    fontSize: 2.5rem
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  
  # Headings — Clean hierarchy
  h1:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1.75rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  h2:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.3
  h3:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1.125rem
    fontWeight: 500
    lineHeight: 1.4
  
  # Body — Readable, warm
  body-lg:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.5
  body-md:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  
  # Labels — All caps for UI chrome
  label:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 0.75rem
    fontWeight: 600
    letterSpacing: "0.08em"
    textTransform: "uppercase"
  
  # Numbers — Tabular for financials
  number:
    fontFamily: "Inter, -apple-system, sans-serif"
    fontSize: 1.5rem
    fontWeight: 600
    lineHeight: 1.2
    fontVariantNumeric: "tabular-nums"

rounded:
  sm: 6px
  md: 12px
  lg: 16px
  xl: 24px
  full: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px

shadows:
  sm: "0 1px 2px rgba(26, 26, 24, 0.05)"
  md: "0 4px 12px rgba(26, 26, 24, 0.08)"
  lg: "0 8px 24px rgba(26, 26, 24, 0.12)"
  xl: "0 16px 48px rgba(26, 26, 24, 0.16)"

components:
  # Buttons
  button-primary:
    backgroundColor: "{colors.legal-blue}"
    textColor: "{colors.on-legal-blue}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
  button-primary-hover:
    backgroundColor: "{colors.legal-blue-soft}"
  button-primary-active:
    backgroundColor: "{colors.legal-blue}"
  
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.legal-blue}"
    rounded: "{rounded.full}"
    padding: "14px 28px"
  button-secondary-hover:
    backgroundColor: "{colors.surface-hover}"
  
  button-fab:
    backgroundColor: "{colors.action-red}"
    textColor: "{colors.on-action-red}"
    rounded: "{rounded.full}"
    size: "56px"
  button-fab-hover:
    backgroundColor: "{colors.action-red-soft}"
  
  # Cards
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  card-hover:
    backgroundColor: "{colors.surface-hover}"
  card-urgent:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  
  # Inputs
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
    typography: "{typography.body-md}"
  input-focus:
    backgroundColor: "{colors.surface}"
  
  # Badges
  badge-success:
    backgroundColor: "rgba(5, 150, 105, 0.1)"
    textColor: "{colors.success}"
    rounded: "{rounded.full}"
    padding: "4px 12px"
    typography: "{typography.label}"
  badge-warning:
    backgroundColor: "rgba(217, 119, 6, 0.1)"
    textColor: "{colors.warning}"
    rounded: "{rounded.full}"
    padding: "4px 12px"
    typography: "{typography.label}"
  badge-danger:
    backgroundColor: "rgba(220, 38, 38, 0.1)"
    textColor: "{colors.danger}"
    rounded: "{rounded.full}"
    padding: "4px 12px"
    typography: "{typography.label}"
  
  # Navigation
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
    typography: "{typography.body-sm}"
  nav-item-active:
    backgroundColor: "{colors.legal-blue}"
    textColor: "{colors.on-legal-blue}"
  
  # Modal
  modal-overlay:
    backgroundColor: "rgba(26, 26, 24, 0.6)"
  modal:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl}"
  
  # Timeline
  timeline-dot:
    size: "12px"
    rounded: "{rounded.full}"
    backgroundColor: "{colors.legal-blue}"
  timeline-line:
    size: "2px"
    backgroundColor: "{colors.border-mid}"

---

## Overview

Willow Legal Pro is a legal practice management dashboard designed for lawyers
who value warmth over cold efficiency. The visual identity draws from
traditional legal materials — parchment, ink, leather-bound books — but
reinterprets them through a modern, touch-first lens.

The emotional goal: a lawyer opens the app and feels *accompanied*, not
*administered*. Every interaction should feel like turning a well-crafted page,
not filling a database form.

## Colors

- **Parchment (#FAF9F4):** The page background. Warm, inviting, never sterile
  white. Evokes legal pads and aged paper.
- **Ink (#1A1A18):** Primary text. Near-black with warmth, not harsh #000.
- **Legal Blue (#1B365D):** The firm's identity color. Deep, trustworthy,
  authoritative. Used for primary actions and active states.
- **Action Red (#8B0000):*" The only high-urgency accent. Used sparingly for
  the FAB (Floating Action Button) and critical alerts. Inherits from legal
  seals and wax stamps.
- **Stone (#9C9B94):** Muted text, borders, disabled states. Natural, not gray.

## Typography

Source Serif 4 for display headings — brings editorial gravitas and warmth.
Inter for everything else — clean, readable, excellent at small sizes on
mobile devices.

Display sizes use tight tracking for headlines. Body uses default tracking for
readability. Labels use all-caps with wide tracking for UI chrome.

Financial numbers use tabular figures to prevent jitter when values change.

## Layout

Mobile-first, touch-optimized. Minimum tap target: 44px (iOS) / 48px (Android).
Cards are the primary content container — no hard table borders.

Spacing follows a 4px baseline. Use md (16px) for internal card padding,
lg (24px) for card-to-card gaps, xl (32px) for section breaks.

The layout is a single-column stack on mobile, expanding to a 2-column grid
on tablet and 3-column on desktop. No sidebar navigation on mobile — bottom
nav or hamburger only.

## Elevation & Depth

Shadows are subtle and warm-tinted (using ink color, not black). Cards lift
on hover/touch with md shadow. Modals use xl shadow with backdrop blur.
No harsh borders — elevation creates separation.

## Shapes

Generous rounding: full (pill) for buttons and badges, lg (16px) for cards,
md (12px) for inputs. This creates a friendly, approachable feel that
contrasts with the traditional legal verticals.

## Components

- **button-primary:** Pill-shaped, legal-blue, with shadow. The main CTA on
  any screen. Only one per view.
- **button-fab:** Action-red, 56px circle, fixed bottom-right. For the
  single most important action ("+ Nueva Reunión").
- **card:** White surface, lg rounded, subtle border. Primary container for
  all content. Lifts on interaction.
- **input:** Generous padding (14px), md rounded, subtle border. Focus state
  uses ring shadow, not just border color change.
- **badge:** Pill-shaped, colored background at 10% opacity with matching
  text color. For status indicators.
- **timeline:** Vertical line with dots, for showing meeting history and
  upcoming events.

## Do's and Don'ts

- **Do** use parchment background for the app shell — never pure white.
- **Do** use action-red only for the FAB and critical alerts — it's a scarce
  resource.
- **Do** use card-hover state to indicate interactivity.
- **Do** use tabular numbers for all financial displays.
- **Don't** use tables for primary content display — always cards or lists.
- **Don't** use more than one button-primary per screen.
- **Don't** use sharp corners (0px radius) on any element.
- **Don't** use pure black (#000) — always ink (#1A1A18).
