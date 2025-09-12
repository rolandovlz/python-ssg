class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        s = ''
        for k, v in self.props.items():
            s += f' {k}="{v}"'
        return s
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{f'{self.props_to_html()}' if self.props else ''}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("All ParentNodes must have children")
        children_to_html = ""
        for child in self.children:
            children_to_html += child.to_html()
        return f"<{self.tag}{f'{self.props_to_html()}' if self.props else ''}>{children_to_html}</{self.tag}>"