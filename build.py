
import json
import shutil
from pathlib import Path

# recreate build directory
BUILD = Path("build")
shutil.rmtree(BUILD, ignore_errors=True)
BUILD.mkdir()

# load predefined templates
POST_TEMPLATE = ""
POST_ITEM_TEMPLATE = ""
with open("src/template/post.html") as fp:
    POST_TEMPLATE = fp.read()
with open("src/template/post-item.html") as fp:
    POST_ITEM_TEMPLATE = fp.read()

# load posts' metadata
with open("posts/_metadata.json") as fp:
    metadata: list = json.load(fp)
    metadata.sort(key=lambda x: x["date"], reverse=True)

# create post items' list using metadata info
posts_list = ""
for x in metadata:
    post_item = POST_ITEM_TEMPLATE.format(f"posts/{x["post"]}/index.html", x["date"], x["title"])
    posts_list += post_item

# write post items' list on index.html
with open("src/index.html") as fp:
    index_html = fp.read()
    new_index_html = index_html.format(posts_list)
with open("build/index.html", "w") as fp:
    fp.write(new_index_html)

# copy accompanying files from src to build
shutil.copy("src/style.css", "build/style.css")

# format post bodies into HTML files and write them into build
shutil.rmtree("build/posts", ignore_errors=True)
for x in metadata:
    shutil.copytree(f"posts/{x["post"]}", f"build/posts/{x["post"]}")
    with open(f"build/posts/{x["post"]}/index.html") as fp:
        post = fp.read()
    with open(f"build/posts/{x["post"]}/index.html", "w") as fp:
        new_post = POST_TEMPLATE.format(x["title"], post)
        fp.write(new_post)
