# UI Refresh Quickstart Guide

## Overview
This guide helps developers get started with the refreshed UI for the Todo app featuring neon purple theme and glassmorphism design.

## Setup

### Prerequisites
- Node.js 18+
- npm, yarn, or bun package manager

### Installation
1. Install dependencies:
```bash
npm install
# or
yarn install
# or
bun install
```

2. Verify Tailwind CSS configuration:
- Configuration file: `tailwind.config.js`
- PostCSS configuration: `postcss.config.js`
- Global styles: `app/globals.css`

3. Start the development server:
```bash
npm run dev
# or
yarn dev
# or
bun dev
```

## Theme System

### CSS Variables
The theme uses CSS variables defined in `:root` in `app/globals.css`:

- **Dark theme base**: `--background-dark`, `--background-card`, `--text-primary`, `--text-secondary`
- **Neon purple accents**: `--neon-purple-500`, `--neon-purple-600`, gradient variables
- **Cyan accents**: `--neon-cyan-400`, `--neon-cyan-500`
- **Glassmorphism effects**: `--glass-bg`, `--glass-border`, `--glass-backdrop`

### Reusable Classes
Custom CSS classes for consistent styling:

- `.glass-card`: Glassmorphism container with backdrop blur
- `.neon-button`: Animated button with neon shine effect
- `.neon-focus`: Focus state with neon outline
- `.neon-shadow`: Neon glow shadow effect
- `.neon-shadow-hover`: Hover with enhanced neon glow

### Tailwind Extensions
Extended Tailwind theme in `tailwind.config.js`:

- **Colors**: `neon-purple` and `neon-cyan` color scales
- **Backdrops**: `backdropBlur.xs` for fine-tuned blur effects
- **Shadows**: `shadow.neon`, `shadow.neon-lg`, `shadow.cyan`, `shadow.cyan-lg`

## Component Patterns

### Glass Card
```jsx
<div className="glass-card bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
  {/* Card content */}
</div>
```

### Primary Gradient Button
```jsx
<button className="px-6 py-3 bg-gradient-to-r from-neon-purple-500 to-pink-500 text-white rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/30">
  Button Text
</button>
```

### Input Field
```jsx
<input
  className="w-full px-4 py-3 bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all duration-300"
  placeholder="Input placeholder"
/>
```

## Page Structure

### Landing Page
- Located at: `app/page.tsx`
- Features neon-themed dashboard with glassmorphism task cards
- Includes statistics cards, search functionality, and task management

### Auth Pages
- Login: `app/login/page.tsx`
- Signup: `app/signup/page.tsx`
- Both use centered glassmorphism cards with gradient accents

## Development Tips

1. **Testing Glassmorphism**: Test on various devices as backdrop-filter can impact performance on lower-end hardware
2. **Color Contrast**: Ensure accessibility standards are maintained with neon colors
3. **Responsive Design**: Verify glassmorphism effects work well across all screen sizes
4. **Performance**: Monitor render performance when adding complex neon effects

## Troubleshooting

### Glassmorphism not appearing
- Check browser support for `backdrop-filter`
- Ensure `app/globals.css` is properly imported in `app/layout.tsx`

### Tailwind classes not working
- Verify `tailwind.config.js` content paths include all component directories
- Restart development server after configuration changes