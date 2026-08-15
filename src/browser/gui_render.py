    def _render_layout(self, layout_box, offset_y=0):
        """
        Render a layout box tree onto the canvas.

        Args:
            layout_box: LayoutBox to render
            offset_y: Y offset for scrolling
        """
        for box in layout_box.children:
            node = box.node

            if isinstance(node, DOMText):
                # Render text
                self.viewport.create_text(
                    box.x + 10,
                    box.y - offset_y + 5,
                    anchor=tk.NW,
                    text=node.text,
                    font=("Arial", 12),
                    fill="black",
                    width=box.width - 20
                )

            elif isinstance(node, DOMElement):
                # Render element based on tag
                if node.tag_name in ('h1', 'h2', 'h3'):
                    # Heading
                    size = {'h1': 24, 'h2': 18, 'h3': 14}[node.tag_name]
                    text = self._get_element_text(node)
                    self.viewport.create_text(
                        box.x + 10,
                        box.y - offset_y + 5,
                        anchor=tk.NW,
                        text=text,
                        font=("Arial", size, "bold"),
                        fill="black"
                    )

                elif node.tag_name == 'a':
                    # Link - render as blue underlined
                    text = self._get_element_text(node)
                    href = node.get_attribute('href', '')

                    text_id = self.viewport.create_text(
                        box.x + 10,
                        box.y - offset_y + 5,
                        anchor=tk.NW,
                        text=text,
                        font=("Arial", 12, "underline"),
                        fill="blue"
                    )

                    # Store clickable area
                    bbox = self.viewport.bbox(text_id)
                    if bbox:
                        self.clickable_areas.append({
                            'bbox': bbox,
                            'url': href
                        })

                # Render children
                self._render_layout(box, offset_y)

    def _get_element_text(self, element):
        """Get all text content from an element."""
        text_parts = []
        for child in element.children:
            if isinstance(child, DOMText):
                text_parts.append(child.text)
            elif isinstance(child, DOMElement):
                text_parts.append(self._get_element_text(child))
        return " ".join(text_parts)

    def _on_canvas_click(self, event):
        """Handle clicks on the canvas."""
        x, y = event.x, event.y

        # Check if click is on a link
        for area in self.clickable_areas:
            bbox = area['bbox']
            if (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]):
                url = area['url']

                # Handle relative URLs
                if url and not url.startswith(('http://', 'https://')):
                    if self.current_url:
                        from browser.url import parse_url
                        current = parse_url(self.current_url)
                        # Simple relative URL handling
                        if url.startswith('/'):
                            url = f"{current.scheme}://{current.host}{url}"
                        else:
                            url = f"{current.scheme}://{current.host}/{url}"

                if url:
                    self.navigate(url)
                break
