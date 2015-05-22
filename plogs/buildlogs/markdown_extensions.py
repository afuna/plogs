import markdown
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown import inlinepatterns
from markdown import util


class ImageFigureExtension(Extension):
    """ Extension class for markdown """
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["image_link"] = ImageFigurePattern(inlinepatterns.IMAGE_LINK_RE, md)


class ImageFigurePattern(inlinepatterns.LinkPattern):
    """
    Override the rendered HTML of images in markdown.
    Includes classes for bootstrap and a caption (instead of alt)
    """

    def handleMatch(self, m):
        """ Return an img element with caption from the given match. """
        figure = util.etree.Element("figure")
        inner = util.etree.SubElement(figure, "div")

        img = util.etree.SubElement(inner, "img")
        src_parts = m.group(9).split()
        if src_parts:
            src = src_parts[0]
            img.set('src', self.sanitize_url(self.unescape(src)))
        else:
            img.set('src', '')

        if len(src_parts) > 1:
            caption = util.etree.SubElement(inner, "figcaption")
            caption.text = util.AtomicString(inlinepatterns.dequote(
                self.unescape(" ".join(src_parts[1:]))
            ))

        alt = m.group(2)
        img.set('alt', self.unescape(alt))

        return figure

def makeExtension(*args, **kwargs):
    return ImageFigureExtension(*args, **kwargs)
