# Meterial Symbols

A [Material Symbols](https://github.com/google/material-design-icons) compatible font for all your meter/progress needs!

Have you ever wished your icons could be more granular?
Sure, you have battery icons for 0%, 10%, 20%, etc., but there are 100 possible values, creating 100 different icons is just cumbersome.

Meterial solves this by using variable fonts!
A single icon can support potentially infinite progress values seamlessly.

## Usage

Simply include the font in your project as you would any other font.
TrueType and WOFF2 files are provided.

Code-points for different icons can be found in [the symbols file](symbols.json).
Alternatively, you can use equivalent Material Symbols code-points from [Google Fonts](https://fonts.google.com/icons).
For example: the `battery` icon can use `U+F0000`, or the code-points for `battery_full`, `battery_0_bar`, `battery_1_bar`, etc., from Material symbols.

### Web example

#### Material Symbols

Here's how you would show a battery value in an icon using Material Symbols, you need to define all usable icons and a function to choose the correct one based on the battery value.

```html
<span class="battery">
    <!-- Defined in script -->
</span>

<script>
    const BATTERY_ICONS = [
        "battery_0_bar",
        "battery_1_bar",
        "battery_2_bar",
        "battery_3_bar",
        "battery_4_bar",
        "battery_5_bar",
        "battery_6_bar",
        "battery_full",
    ];

    const iconRange = (icons, value, min = 0, max = 100) => {
        value = (value - min) / (max - min) * (icons.length - 1);
        value = Math.min(Math.max(Math.floor(value), 0), icons.length - 1)
        return icons[value];
    };

    const battery = document.querySelect(".battery");
    battery.textContent = iconRange(BATTERY_ICONS, batteryValue);
</script>

<style>
    .battery {
        font-family: 'Material Symbols';
    }
</style>
```

#### Meterial Symbols

Using Meterial is much simpler, you just need to change the `PGRS` axis on the font! Everything else is taken care of for you.

```html
<span class="battery">&#xF0000;</span>

<script>
    const battery = document.querySelect(".battery");
    battery.style.setProperty("--battery", batteryValue);
</script>

<style>
    .battery {
        font-family: 'Meterial Symbols';
        font-variation-settings: 'PGRS' var(--battery);
    }
</style>
```

## Development

Meterial uses Python and [fonttools](https://github.com/fonttools/fonttools) to generate the font.
Use `pip` or your favorite package manager to install these dependencies, then move on to the next chapters!

### Building

To generate the fonts, just run the [`__main__.py`](__main__.py) file:

```shell
python3 __main__.py
```

This will create a `dist` folder with a `.ttf` and a `.woff2` file.

### Verification

This repository uses ruff and pyright to check the code.
You should run these tools before pushing your code, to keep the coding style consistent.

You can run these tools directly, through your favorite editor, or using tox:

```shell
python3 -m tox -e lint # or format or typecheck
```

### Adding new symbols

To add new symbols just add a new entry to the `SYMBOLS` list in the [`symbols.json`](symbols.json) file, and a new directory with the appropriate name in [`symbols`](symbols).

The parameters are explained in [`__main__.py`](__main__.py), but the gist of it is:

- the `name` parameter can be anything you want, but should be somewhat descriptive;
- the `codepoints` parameter defines the code-points that should represent this icon, in hex format;
- the `ligatures` parameter defines the ligatures that should represent this icon;
- the `_.svg` file has the SVG path definition for the default version of the icon (i.e. when `PGRS` is 0). It should fit in a 960x960 square;
- the remaining `<float>.svg` files define the different versions of the icon for different values of `PGRS`. They should all be compatible with the default icon, by having the same number of contours and points in the same order;

## Planned features

- Website for previewing the font.
- Ligature support: blocked by `fonttools` not supporting `GSUB` tables.
- Support for all of Material Symbols' axes; currently all symbols have the default values (i.e. weight = 400, optical size = 24, etc.).
- Support for all of Material Symbols' styles; currently only *Outlined* is supported.
- Improve `battery_charging`, maybe using `COLR` tables.
