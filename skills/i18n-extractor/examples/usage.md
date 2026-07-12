# Usage

Given `src/app.ts`:

```ts
const title = t('Welcome back');
const save = i18n.t("Save changes");
const duplicate = t('Welcome back');
const dynamic = t(`Hello ${name}`);
```

Run:

```bash
python scripts/extract.py src
```

Output:

```json
{
  "save_changes": "Save changes",
  "welcome_back": "Welcome back"
}
```

Pass either a supported source file or a directory. Directories are searched recursively for `.js`, `.jsx`, `.ts`, and `.tsx` files. An invalid path exits with code `2` and writes an error to standard error.
