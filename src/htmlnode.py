class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # Initialize an HTML node with optional args
        self.tag = tag              # HTML Tag ('p', 'a', 'div', etc..)
        self.value = value          # The text content of a node
        self.children = children    # Child nodes (None for leaf nodes)
        self.props = props          # HTML attributes as key-value pairs

    def to_html(self): # Will be implemented for child classes
        raise NotImplementedError

    def props_to_html(self): # Updates props dict to HTML
        if not self.props:
            return ""
        html_props = ""
        for prop, value in self.props.items():
            html_props += f' {prop}="{value}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None): # Setting contructor for optional tags, props, and no children
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self): # Converting to HTML
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None): # Setting up contructor required tags/children, optional props, no value
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self): # Converts MD to HTML
        children_html = ""
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        elif self.children == None or len(self.children) == 0:
            raise ValueError("All parent nodes must have a child.")
        else: # recrusively iterates through children then returns them as HTML
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.children}, {self.tag}, {self.props})"
