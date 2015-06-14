from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
import re

IMAGE_REGEX = re.compile("\[\[image (.*?)\]\]")
IMAGE_TEMPLATE = """
    <p class="Post-image"><img src="/static/images/{filename}"></p>
"""

VIDEO_REGEX = re.compile("\[\[video (.*?)\]\]")
VIDEO_TEMPLATE = """
    <p class="Post-video"><video src="/static/images/{filename}" autoplay controls loop>
    Sorry, your browser doesn't support embedded videos, 
    but don't worry, you can <a href="/static/images/{filename}">download it</a>
    and watch it with your favorite video player!
    </video></p>
"""


class MarkdownImagePostprocessor(Postprocessor):
    def run(self, text):
        def _handle_match(match):
            return IMAGE_TEMPLATE.format(filename=match.group(1))
        return IMAGE_REGEX.sub(_handle_match, text)

class MarkdownVideoPostprocessor(Postprocessor):
    def run(self, text):
        def _handle_match(match):
            return VIDEO_TEMPLATE.format(filename=match.group(1))
        return VIDEO_REGEX.sub(_handle_match, text)

class MarkdownEmbedMedia(Extension):
    def extendMarkdown(self, md, md_globals):
        # Insert instance of 'mypattern' before 'references' pattern
        md.postprocessors.add('image', MarkdownImagePostprocessor(md), '>amp_substitute')
        md.postprocessors.add('video', MarkdownVideoPostprocessor(md), '>amp_substitute')

def makeExtension(**kwargs):
    return MarkdownImage(**kwargs)
