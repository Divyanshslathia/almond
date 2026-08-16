# Browser Scrolling Feature

## Overview

Added vertical scrolling support to the browser to handle long web pages.

## Implementation

### Components Added

1. **Scrollbar Widget**
   - Visual scrollbar on the right side of viewport
   - Updates position based on content height
   - Supports click-and-drag scrolling

2. **Mouse Wheel Support**
   - Scroll up/down with mouse wheel
   - 30-pixel increment per wheel tick

3. **Scroll State Tracking**
   - `scroll_offset`: Current vertical scroll position
   - `content_height`: Total height of rendered content
   - Automatic recalculation on page load

### Files Modified

- `src/browser/gui.py`:
  - Added scroll state variables
  - Added `_create_viewport()` with scrollbar
  - Added `_calculate_content_height()` method
  - Added `_update_scrollbar()` method
  - Added `_on_scroll()` for scrollbar events
  - Added `_on_mousewheel()` for mouse wheel events
  - Modified `_display_page()` to reset scroll on navigation

- `src/browser/gui_render.py`:
  - Updated `_render_layout()` to use `offset_y` parameter
  - All rendering coordinates adjusted by scroll offset

## Usage

When viewing long pages:
- Use mouse wheel to scroll up/down
- Click and drag scrollbar
- Scrollbar automatically appears when content exceeds viewport height

## Testing

Test with `test_pages/long_page.html` which contains multiple sections designed to require scrolling.
