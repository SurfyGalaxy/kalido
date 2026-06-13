# Kalido

A python-based colouriser inspired by `lolcat` and `kekcat`, capable of handling both escape sequences and streamed input

## Installation

Kalido is easily downloaded, simply run:
```bash
pip install kalido
```

## Arguments

```bash
--stops <list> # Default = "random"
--count <int> # Default = 5
--size <int> # Default = 1
```
<br><hr><br>

### --stops

Define a list of hex codes which the gradient will go between, or alternatively use a premade template

#### Examples:
  `--stops "#000000" "#FFFFFF"` 
  Creates a gradient between black and white

  `--stops "#FFD800" "#790293" "#FFD800"`
  Creates a gradient between yellow and purple, before returning to yellow

  `--stops aroace`
  Uses the premade gradient of the aroace flag

#### Presets:
- Rainbow
- Lesbian
- Gay (MLM)
- Bisexual
- Transgender
- Queer
- Intersex
- Aroace
- All (Combines every flag end-to-end)
- Random (Will pick any preset)

<hr>

### --count

Define how many additional colours the gradient will have between your stops

Use `0` if you want there to be no additional colours added

<hr>

### --size

Define how many characters each colour will cover.

<br><hr><br>

## Known bugs

- Interactive programs sometimes will leak escape sequences

## AI Disclaimer

No AI was used to generate code nor this README