# Shreevari Civil & Interiors — Website Architecture & Layout Specification

> **Document Version**: 1.0.0  
> **Primary File**: [`shreevari.html`](file:///c:/Users/Admin/OneDrive/Desktop/agentic_universe/shreevari.html)  
> **Brand**: Shreevari Civil & Interiors (Tumakuru & Bengaluru Atelier)  
> **Classification**: Editorial Architectural Portfolio & Commercial Atelier Landing Page

---

## 1. Architectural & Design Philosophy

The website is engineered with a **Deccan Brutalist / Minimalist Atelier** visual aesthetic, paying homage to Bengaluru and Karnataka's architectural heritage—raw Sadarahalli granite, teak louvers, passive cooling impluviums, and monolithic geometry.

### Core Visual Principles
- **Tectonic Honesty**: Sharp 1px hairlines (`#DDD7CB`) create an architectural drafting-grid structure separating content blocks without heavy drop shadows.
- **Warm Earthy Palette**: Soft travertine and lime plaster (`#F7F4EE`, `#FDF9F3`) contrasted against basalt charcoal (`#1B1A17`) and Deccan olive-sand (`#55573A`, `#7C8458`).
- **Editorial Dual-Type Hierarchy**: Classical serif headline typography paired with structured, uppercase monospaced technical labels.
- **Microclimate & Geotechnical Motifs**: Integrated SVG topographic contour watermarks, CAD drafting grids, and real geographic coordinates.

---

## 2. Technology Stack & Dependencies

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Markup** | HTML5 (Semantic) | Accessible, structured DOM with section anchors |
| **CSS Framework** | Tailwind CSS CDN (v3.x) | Utility-first styling configured with custom design tokens |
| **Typography** | Google Fonts (`Newsreader` & `Inter`) | Display serifs and technical body/label typography |
| **Iconography** | Google Material Symbols Outlined | UI control symbols (arrows, phone, location, mail, menu) |
| **Scripting** | Vanilla JavaScript (ES6+) | Modal dossier store, services carousel, form validation, drawer |
| **Media Assets** | Local PNG & WebP / Google CDN | Transparent brand marks, favicons, editorial photography |

---

## 3. Design System & Token Architecture

### 3.1 Color Palette
The site extends Tailwind's color scheme with architectural stone and soil values:

```javascript
colors: {
  "background": "#FDF9F3",          // Warm ivory canvas
  "surface": "#FDF9F3",             // Primary surface plane
  "surface-container": "#F2EDE8",   // Soft limestone container
  "surface-container-high": "#ECE8E0", // Chiseled granite plinth
  "primary": "#3E4025",             // Dark Deccan forest
  "primary-container": "#55573A",   // Deccan olive primary button & accent
  "on-primary": "#FFFFFF",          // High-contrast white text on primary
  "on-surface": "#1D1B18",          // Deep basalt charcoal text
  "on-surface-variant": "#5E5951",  // Muted editorial prose text
  "outline": "#DDD7CB",             // 1px architectural hairline wireframe
  "secondary": "#7C8458",           // Warm sage / moss secondary badge
  "secondary-container": "#DCE4B1"  // Highlight selection container
}
```

### 3.2 Typography System

| Role | Font Family | Weight / Style | Sample Usage |
| :--- | :--- | :--- | :--- |
| **Display** | `Newsreader` | `300 / 700 Italic` | Hero Headline (`Designing Spaces, Designing Stories`) |
| **Headline Large** | `Newsreader` | `300 / 400 Regular` | Studio Statement, Contact Intro (`48px / 56px`) |
| **Headline Medium** | `Newsreader` | `400 Regular` | Section Headings (`32px / 40px`) |
| **Headline Small** | `Newsreader` | `400 Regular` | Card Titles, Modal Headings (`24px / 32px`) |
| **Stat Number** | `Newsreader` | `300 Light` | Numerical Counter Metrics (`56px / 60px`) |
| **Body Large / Md** | `Inter` | `400 Regular` | Editorial body copy, descriptions (`15px / 24px`) |
| **Technical Label** | `Inter` | `600 Bold Uppercase`| Category pills, metadata, coordinates (`11px`, `tracking-[0.2em]`) |

---

## 4. Page Layout & Component Breakdown

```
+--------------------------------------------------------------------------+
|  [FLOATING CAPSULE NAVBAR] (Fixed Top, Glassmorphism, Logo + Nav Links)  |
+--------------------------------------------------------------------------+
|  1. HERO SECTION (Split: Monolith Image [58%] | Editorial Mission [42%])  |
+--------------------------------------------------------------------------+
|  2. HIGHLIGHTED PROJECTS (3-Column Interactive Dossier Cards)            |
+--------------------------------------------------------------------------+
|  3. OUR STUDIO / ATELIER (Atelier Interior Image | Blueprint Schematic)   |
+--------------------------------------------------------------------------+
|  4. STATS BAND (4 Metrics with Continuous Centered Wireframe Hairline)   |
+--------------------------------------------------------------------------+
|  5. WHY SHREEVARI (6-Cell Monolithic Architectural Methodology Grid)     |
+--------------------------------------------------------------------------+
|  6. SERVICES CAROUSEL (7 Disciplines, Autoplay, Play/Pause Controls)     |
+--------------------------------------------------------------------------+
|  7. CONTACT DESK & MAP (3 Columns: Invitation | Form | Stone Details)    |
|     + Desaturated Monochrome Atelier Location Map Strip                  |
+--------------------------------------------------------------------------+
|  [FOOTER] (51px Minimal Strip, Copyright, Monochrome Inverted Brand)     |
+--------------------------------------------------------------------------+
|  [MODAL OVERLAY] (Full-Screen Project Specification Dossier Viewer)      |
+--------------------------------------------------------------------------+
```

---

### Component Details

### A. Floating Header / Navbar
- **Placement**: `fixed top-4 sm:top-6 left-1/2 -translate-x-1/2 z-50`
- **Dimensions**: `w-[calc(100%-2rem)] sm:w-[calc(100%-3rem)] max-w-7xl h-[72px] sm:h-[78px]`
- **Styling**: `bg-[#F7F4EE]/92 backdrop-blur-md border border-[#DDD7CB] shadow-[0_8px_30px_rgba(27,26,23,0.07)]`
- **Left**: Transparent brand mark ([`logo-trimmed.png`](file:///c:/Users/Admin/OneDrive/Desktop/agentic_universe/logo-trimmed.png)) + vertical hairline border + `SHREEVARI / CIVIL & INTERIORS` typography.
- **Center / Right (Desktop)**: Direct section navigation (`PROJECTS`, `STUDIO`, `WHY US`, `SERVICES`, `CONTACT`) with active underline indicator.
- **Mobile Drawer**: Responsive hamburger toggle revealing a synchronized floating navigation drawer.

### B. Section 1: Hero (`min-h-[720px]`)
- **Background Watermark**: Topographical contour curve SVG (`stroke-[#55573A]/25`) anchored to the bottom-right.
- **Left Column (~58%)**: Editorial architectural photography with linear gradient alpha mask and discrete technical badge (`LAT 12.9716° N / LON 77.5946° E`).
- **Right Column (~42%)**: 
  - Eyebrow: Hairline tick + uppercase letter-spaced label.
  - Headline: 3-line serif with italicized gold emphasis (`"Designing Spaces / Designing Stories"`).
  - Mission Copy & Primary CTA (`EXPLORE OUR WORK ——→`).

### C. Section 2: Highlighted Projects (`#projects`)
- **Grid Layout**: 3 equal cards separated by `gap-[30px]`.
- **Card Elements**:
  1. Aspect ratio `3:2` image with zoom on hover (`scale-105 duration-500`).
  2. Category tag badge (`RESIDENTIAL`, `HOSPITALITY & RETREAT`, `COMMERCIAL & STUDIO`).
  3. Project Title, Completion Year, Location, and Square Footage.
  4. Interactive trigger: `onclick="openProjectModal('project-id')"` with sliding directional arrow.

### D. Section 3: Our Studio (`#studio`)
- **Left Column (40%)**: Atmospheric atelier study (solid teak drafting plinth, plaster massing models).
- **Right Column (60%)**: 
  - Subtle background architectural CAD drafting schematic SVG (`GRID 04-A // SOUTH COLONNADE`, `VENTILATION SHIFT +2400`).
  - Studio philosophy on passive cooling, Karnataka stone carvers, and unhurried craftsmanship.
  - Secondary CTA (`TALK TO US ——→`).
  - Principal founder credit: **Sheetal Umesh**, Principal Architect & Founder.

### E. Section 4: Technical Stats Band
- **Structure**: 4-column metrics grid on chiseled granite background (`#ECE8E0`).
- **Detailing**: A continuous 1px centerline hairline (`#DDD7CB`) running horizontally behind the stat blocks.
- **Data Points**:
  - `150+` Projects Completed
  - `15` Years of Experience
  - `120+` Satisfied Clients
  - `2M+` Sq. Ft. Designed & Built

### F. Section 5: Why Shreevari Grid (`#why-us`)
- **Layout**: 3-column × 2-row monolithic grid bordered by 1px hairlines.
- **Modules**:
  - `01`: Design-Led Approach
  - `02`: One Team, Start to Finish
  - `03`: Clear Timelines & Costs
  - `04`: Local Bengaluru Expertise
  - `05`: Quality Materials & Workmanship
  - `06`: Open Communication

### G. Section 6: Comprehensive Services Carousel (`#services`)
- **Tracks**: 7 spatial discipline cards:
  1. Interior Works & Fit-Outs
  2. Turnkey Construction
  3. Renovation & Restoration
  4. Civil & Architectural Plans
  5. 3D Exterior Elevation & Walkthrough
  6. Acoustic Engineering
  7. Real Estate & Site Feasibility
- **Interactivity**:
  - Autoplay timer (every 4.2 seconds).
  - Play / Pause toggle with dynamic icon swap (`play_arrow` / `pause`).
  - Next (`→`) and Previous (`←`) navigation.
  - Viewport-aware slide offset calculation (4 visible on desktop, 2 on tablet, 1 on mobile).
  - Window `resize` listener preventing offset boundary overflow.
  - Card CTA (`ENQUIRE ——→`) scrolls directly to `#contact` and pre-selects the dropdown option.

### H. Section 7: Contact Desk & Geospatial Map (`#contact`)
- **3-Column Architecture**:
  1. **Column 1 (Editorial Invitation)**: Client engagement readiness notice (`2026/2027 Commissions`).
  2. **Column 2 (Inquiry Form)**:
     - Minimal underline input fields (`border-0 border-b border-[#DDD7CB] focus:border-[#55573A]`).
     - Anti-spam hidden honeypot input (`b_company_field`).
     - Real-time client feedback state machine (`TRANSMITTING BRIEF...` → `INQUIRY LOGGED ——✓`).
  3. **Column 3 (Stone Details Panel)**:
     - Official Shreevari logo brand mark.
     - Studio Location: *Shri Lakshmi Venkateshwara Road, Jayanagar, Tumakuru - 572 102*.
     - Email Desk: `shreevaribuildcon@yahoo.com`.
     - Direct Phone Desk: `+91 91489 36149` with click-to-call and WhatsApp deep-links.
- **Full-Width Map Strip**: Desaturated high-contrast architectural map background with floating atelier location plinth.

### I. Full-Screen Interactive Project Dossier Modal
- **Trigger**: Click any project card in Section 2.
- **State Management**: JavaScript-driven client store `projectsData`.
- **Features**:
  - Full-screen modal overlay with background lock (`overflow: hidden`).
  - Dynamic content population: Title, photo, category, brief, location, built area, year, scope, and principal architect.
  - Controls: Next/Prev arrows, Escape key listener, Arrow key navigation, and Close button (`✕`).

### J. Footer (51px)
- Deccan olive background (`#55573A`).
- Monochrome inverted Shreevari icon mark.
- Copyright attribution and uppercase Privacy/Terms links.

---

## 5. Local File & Asset Manifest

```
agentic_universe/
├── shreevari.html             # Master production HTML file
├── WEBSITE_ARCHITECTURE.md    # This architecture specification document
├── logo.png                   # Original uploaded high-resolution logo (500x500 PNG)
├── logo-trimmed.png           # Trimmed transparent logo mark for header & footer
├── favicon.ico                # Standard multi-format browser tab icon
├── favicon.png                # High-DPI 64x64 PNG favicon
├── favicon-32x32.png          # Standard 32x32 PNG favicon
└── apple-touch-icon.png       # 180x180 iOS home screen touch icon
```

---

## 6. JavaScript Architecture & Key Functions

| Function | Purpose |
| :--- | :--- |
| `openProjectModal(id)` | Finds project record in `projectsData`, executes `renderModalContent()`, displays overlay |
| `renderModalContent()` | Injects project title, imagery, location, specifications, and architect credit into modal DOM |
| `closeProjectModal()` | Dismisses modal overlay, restores body scroll |
| `nextProject()` / `prevProject()` | Cycles through project index ring with modulo arithmetic |
| `scrollCarousel(direction)` | Shifts carousel track by slide width; loops seamlessly at boundaries |
| `startAutoplay()` / `toggleCarouselAutoplay()` | Controls automated continuous slide progression |
| `selectServiceOption(name)` | Pre-populates the `#projectTypeSelect` dropdown when an inquiry link is clicked |
| `handleFormSubmit(e)` | Validates inputs, verifies honeypot spam filter, triggers simulated transmission state |
| `toggleMobileMenu()` / `closeMobileMenu()` | Toggles the responsive floating mobile navigation drawer |

---

## 7. Responsiveness & Breakpoint Matrix

| Viewport | Breakpoint | Layout Adaptations |
| :--- | :--- | :--- |
| **Mobile** | `< 640px` | 1-column layouts, hamburger menu drawer, single-slide carousel, stacked hero |
| **Tablet** | `640px - 1023px` | 2-column project/why grids, 2-slide carousel view, compact stats |
| **Desktop** | `1024px +` | Full floating capsule header, 3-column project cards, 4-slide carousel view, split-screen hero |
