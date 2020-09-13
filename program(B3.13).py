class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            opening = "\n<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "\n<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "\n<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)
    def __iadd__(self, other):
        self.children.append(other)
        return self 

class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        if self.output is not None:
            opening = "<html>\n"
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "\n</html>"
            text_html = opening + internal + ending
            output_filename = self.output
            writer = open(output_filename, "w")
            writer.write(text_html)
            writer.close()
        else:
            print("<html>")
            for child in self.children:
                print(child)
            print("</html>")
    def __iadd__(self, other):
        self.children.append(other)
        return self

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.text = ""
        self.children = []
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __str__(self):
        if self.children:
            opening = "<%s>" % self.tag
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<%s/>" % self.tag
            else:
                return "<{tag}>{text}</{tag}>".format(tag=self.tag, text=self.text)
    def __iadd__(self, other):
        self.children.append(other)
        return self

#=================================================================

if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img
                body += div
            doc += body
