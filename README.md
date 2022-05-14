# Blog banner generator

I was tired of making banners for my blog posts, so I created a script that does it for me.

![Example](.github/assets/example.png)


## Installation

```bash
git clone https://github.com/Dhravya/blog-banner-generator.git
cd blog-banner-generator
pip install -r requirements.txt
```

## Config

The default config works well, but if you want your banner to be a different colour, or change the positioning of elements, feel free to edit the [config file](src/config.py)

Here are the config options (note that this may break the script, because I haven't tested it out much)

`BG_COLOR` : `rgb(r, g, b)`

`ART_POSITION` : `Coordinates(x, y, size=(430, 430))`

`TITLE_POSITION` : `Coordinates(x, y)`

`IMG_POSITION` : `Coordinates(x, y)`

`FOOTER_POSITION` : `Coordinates(x, y)`

`FOOTER` : `"<your small footer>"`

## Running the script
You can run the script by using the `generate()` method of the `ImageFactory` class

```python
if __name__ == "__main__":
    generator = ImageFactory()
    generator.generate(
        ... # Options here
    )
```

Generate options:

`title`, `description`: Required, self explanatory

`art_img_path`: Optional, path to the image to be used as the "banner art" (image on the top left)

This can also be a URL, if it's a URL, the image will automatically be downloaded and used
To set a default value, you need to change [art.png](templates/art.png) in the `templates` folder.

`img_path`: Optional, path to the image to be used as the "banner image" (the main display image)

This can also be a URL, if it's a URL, the image will automatically be downloaded and used
By default, it uses the [default.png](templates/default.png) in the `templates` folder. so you can change that if you want to change the default image

`save_path` : Optional, path to save the image to. If not specified, it will save to `output.png`

`tags`: (List) Optional, list of tags to be used in the footer. Basically pastes the images as tags in the footer.

All the tags are sourced from the [icons](icons/) folder, add more tags in there with the appropriate name, and it will be used.

`resize_width`: Resize the output image to this width. If not specified, it will not resize.


## support
[Follow me on Github](https://github.com/dhravya)

[Follow me on twitter](https://twitter.com/dhravyashah)