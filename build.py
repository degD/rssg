
import json
import shutil

POST_ITEM_TEMPLATE = """
<div class="post-item">
    <a href="{}"><h2>({}) {}</h2></a>
</div>
"""

with open("posts/_metadata.json") as fp:
    metadata: list = json.load(fp)
    metadata.sort(key=lambda x: x["date"], reverse=True)

posts_list = ""
for x in metadata:
    post_item = POST_ITEM_TEMPLATE.format(f"posts/{x["post"]}/index.html", x["date"], x["title"])
    posts_list += post_item

with open("src/index.html") as fp:
    index_html = fp.read()
    new_index_html = index_html.replace("<!-- {{POSTS-LIST}} -->", posts_list)

with open("build/index.html", "w") as fp:
    fp.write(new_index_html)

shutil.copy("src/style.css", "build/style.css")
shutil.rmtree("build/posts", ignore_errors=True)
for x in metadata:
    shutil.copytree(f"posts/{x["post"]}", f"build/posts/{x["post"]}")
    with open(f"build/posts/{x["post"]}/index.html") as fp:
        post = fp.read()
    with open(f"build/posts/{x["post"]}/index.html", "w") as fp:
        post = f"<title>{x["title"]}</title>\n" + post
        fp.write(post)
