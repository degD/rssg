
# Redged's Static Site Generator (RSSG)

Deliberately minimal static site generator. Just a single Python script that transforms 
HTML under `posts` into a static site in `build`. No dependencies needed.

## How to Use?

Clone the source, put your posts under `posts` directory. Put your source and template files
under `src` and `src/templates`. Update `posts/_metadata.json` accordingly. Run `python3 build.py`.
To configure the build process, simply modify to code inside `build.py`. Modify templates and 
sources as it fits.

A post is an `index.html` file inside a directory under `posts`. It contains body in plain HTML.
Each post needs a corresponding entry in `posts/_metadata.json` in the following format:

```json
{
  "title": "My First Post",
  "date": "2026-05-13",
  "post": "mypost"
}
```

- `title`: The post title.
- `date`: The date in `YYYY-MM-DD` format. Posts are sorted by it, newest first.
- `post`: The name of the post's directory under `posts`. For example, `posts/mypost`.

## How to Deploy?

It depends on the provider. For Codeberg, create an empty `pages` branch and run 
`bash deploy.sh`. It copies the build output onto the `pages` branch of the 
Codeberg repository and pushes it. Codeberg serves that branch as the live site.

## License

MIT
