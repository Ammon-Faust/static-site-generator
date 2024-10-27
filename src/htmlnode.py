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
            
