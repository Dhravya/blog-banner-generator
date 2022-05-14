import os
import textwrap

from rich import print
from rich.traceback import install
from PIL import Image, ImageDraw, ImageFont

install()

from helpers import check_path, do_download, cleanup
from _types import Coordinates, rgb
from config import (
    BG_COLOR,
    ART_POSITION,
    TITLE_POSITION,
    IMG_POSITION,
    FOOTER_POSITION,
    FOOTER,
)


class ImageFactory:
    def __init__(self):
        self.img = None

    def _round_corners(self, img: Image, rad: int) -> Image:
        """Adds rounded corners to any image

        Args:
            img (Image): The image to be treated
            rad (int): The radius of corners

        Returns:
            Image: Image with rounded corners
        """
        circle = Image.new("L", (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)

        alpha = Image.new("L", img.size, 255)
        w, h = img.size

        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

        img.putalpha(alpha)

        return img

    def _create_template_img(self, art_path: os.PathLike) -> Image:
        check_path(art_path)
        art_img = Image.open(art_path)

        # Create img with 2240, 1260
        img = Image.new("RGB", (2240, 1260), BG_COLOR)
        art_img = art_img.resize(
            (
                ART_POSITION.size[0],
                int(ART_POSITION.size[0] * art_img.size[1] / art_img.size[0]),
            ),
        )
        try:
            img.paste(art_img, (ART_POSITION.x, ART_POSITION.y), art_img)
        except ValueError:
            img.paste(art_img, (ART_POSITION.x, ART_POSITION.y))

        self.img = img

    def _add_title(self, title: str) -> Image:
        if self.img is None:
            raise Exception("No image to add title to")

        wrapped = textwrap.wrap(title, width=35 if len(title) > 35 else 30)
        title_font = ImageFont.truetype(
            r"templates\ceribri.ttf", size=100 if len(wrapped) > 1 else 120
        )
        title_height = title_font.getsize(title)[1]
        overhead = 100 / len(wrapped)

        margin = TITLE_POSITION.x
        offset = TITLE_POSITION.y + overhead
        draw = ImageDraw.Draw(self.img)

        def draw_title(coords: Coordinates, text: str):
            draw.text(
                (coords.x, coords.y), text, font=title_font, fill=rgb(231, 237, 235)
            )

        for line in wrapped:
            draw_title(Coordinates(x=margin, y=offset), line)
            offset += title_height + 5

        return self.img

    def _add_image(self, img_path: os.PathLike = "templates/default.png") -> Image:
        if self.img is None:
            raise Exception(
                "No image. Generate one by calling the create_template_img method"
            )

        check_path(img_path)
        img = Image.open(img_path)

        img = img.resize((1280, int(1280 * img.size[1] / img.size[0])))

        if img.size[1] > 720:
            img = img.crop((0, 0, img.size[0], img.size[0] / 1.777))

        img = self._round_corners(img, 40)
        try:
            self.img.paste(img, (IMG_POSITION.x, IMG_POSITION.y), img)
        except ValueError:
            self.img.paste(img, (IMG_POSITION.x, IMG_POSITION.y))
        self.img.save("output.png")
        return self.img

    def _add_description(self, description: str) -> Image:
        if self.img is None:
            raise Exception(
                "There is no image to add description to. Generate one by using the create_template_img method"
            )
        text_width = 25
        text_size = 50
        if len(description) > 200:
            text_width = 35
            text_size = 35
        wrapped = textwrap.wrap(description, width=text_width)
        description_font = ImageFont.truetype(
            "templates/jetbrains_mono.ttf", size=text_size
        )
        description_height = description_font.getsize(description)[1]

        DESCRIPTION_POSITION = Coordinates(
            x=IMG_POSITION.x + 1280 + 30, y=IMG_POSITION.y
        )

        margin = DESCRIPTION_POSITION.x
        offset = DESCRIPTION_POSITION.y + description_height + 5

        draw = ImageDraw.Draw(self.img)

        def draw_description(coords: Coordinates, text: str):
            draw.text(
                (coords.x, coords.y),
                text,
                font=description_font,
                fill=rgb(255, 255, 255),
            )

        for line in wrapped:
            draw_description(Coordinates(x=margin, y=offset), line)
            offset += description_height + 5

        self.img.save("output.png")
        return self.img

    def _add_footer(self, tags:list = None) -> Image:
        if self.img is None:
            raise Exception(
                "There is no image to add footer to. Generate one by using the create_template_img method"
            )
        footer_font = ImageFont.truetype(r"templates\jetbrains_mono.ttf", size=40)

        # Paste footer text
        draw = ImageDraw.Draw(self.img)
        draw.text(
            (FOOTER_POSITION.x, FOOTER_POSITION.y),
            FOOTER,
            font=footer_font,
            fill=rgb(200, 200, 255),
        )

        tag_x = self.img.size[0] - 130
        tag_y = IMG_POSITION.y + 600

        # Adding footers
        if tags:
            for tag in tags:
                if os.path.exists(f"./icons/{tag}.png"):
                    img = Image.open(f"./icons/{tag}.png")
                    img = img.resize((100, 100))
                    self.img.paste(img, (tag_x, tag_y), img)
                    tag_x -= 120


        return self.img

    def resize(self, width) -> Image:
        if self.img is None:
            raise Exception("No image to resize")

        self.img = self.img.resize((width, 630))

        return self.img

    def generate(
        self,
        /,
        title: str,
        description: str,
        art_img_path: os.PathLike = "templates/art.png",
        img_path: os.PathLike = "templates/default.png",
        save_path: os.PathLike = "output.png",
        tags: list = None,
        resize_width: int = None,
    ) -> Image:

        if str(art_img_path).startswith("https://"):
            art_img_path = do_download(art_img_path, "art.temp.png")

        if str(img_path).startswith("https://"):
            img_path = do_download(img_path, "img.temp.png")

        self._create_template_img(art_img_path)
        self._add_title(title)
        self._add_description(description)
        self._add_image(img_path)
        self._add_footer(tags=tags)

        if resize_width:
            self.resize(resize_width)

        self.img.save(save_path)
        cleanup()

        return self.img

