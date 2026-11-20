import json
import os
import shutil
import subprocess as sp
from pathlib import Path

# check if pandoc is installed (required for .md support)
pandoc_installed = True
try:
    sp.run(['pandoc', '-h'], check=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
except:
    pandoc_installed = False
    print('Pandoc not found. Markdown will not be supported')

# check if tidy is installed (required for final HTML formatting)
tidy_installed = True
try:
    sp.run(['tidy', '-h'], check=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
except:
    tidy_installed = False
    print('Tidy not found. HTML formatting will not be supported')

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

    # check whether .md or .html
    p = Path(f"posts/{x["post"]}/index.html")
    q = Path(f"posts/{x["post"]}/index.md")

    # convert to HTML if MD, else skip
    if not p.exists() and q.exists() and pandoc_installed:
        sp.run(['pandoc', '-f', 'markdown', f'build/posts/{x["post"]}/index.md', '-o', f'build/posts/{x["post"]}/index.html'], check=False)
        os.remove(f'build/posts/{x["post"]}/index.md')
    elif not p.exists() and not q.exists():
        print(f'post "{x["post"]}" is malformed. skipping...')
        continue
    elif q.exists() and not pandoc_installed:
        print(f'post "{x["post"]}" is markdown but "pandoc" is not installed. skipping...')
        continue

    # writing into the template
    with open(f"build/posts/{x["post"]}/index.html") as fp:
        post = fp.read()
    with open(f"build/posts/{x["post"]}/index.html", "w") as fp:
        new_post = POST_TEMPLATE.format(x["title"], post)
        fp.write(new_post)

    # formatting
    if tidy_installed:
        sp.run(['tidy', '-i', '-q', '-m', f'build/posts/{x["post"]}/index.html'], check=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
