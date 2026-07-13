# Slug Generator — Usage Examples

## 1. Generate a basic slug

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "Hello, World! 2024"
```

```
hello-world-2024
```

## 2. Custom separator

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "My Blog Post Title" --separator "_"
```

```
my_blog_post_title
```

## 3. With max length

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "This is a very long blog post title that should be truncated" --max-length 40
```

```
this-is-a-very-long-blog-post-title
```

## 4. Transliteration

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "Café & Résumé"
```

```
cafe-resume
```

## 5. Batch from file

```bash
python skills/slug-generator/scripts/slug_gen.py batch --file titles.txt
```

```
hello-world  <-  Hello World
my-post  <-  My Post!
```

## 6. JSON output

```bash
python skills/slug-generator/scripts/slug_gen.py generate --text "Hello World" --json
```

```json
{
  "input": "Hello World",
  "slug": "hello-world"
}
```
