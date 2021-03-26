# Hg Brasil Finance Custom Component

Custom component provides information about currencies, stocks, and taxes for Home Assistant

![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

# Installation

## HACS

- Have [HACS](https://hacs.xyz/) installed, this will allow you to easily update.

- Add https://github.com/hudsonbrendon/Home-Assistant-Hg-Brasil-Finance as a custom repository with Type: Integration
- Click Install under "HG Brasil Finance" integration.
- Restart Home-Assistant.

## Manual

- Copy directory custom_components/hg_brasil_finance to your <config dir>/custom_components directory.
- Configure.
- Restart Home-Assistant.

# Configuration

```yaml
- platform: hg_brasil_finance
  key: your-key
```

# Debugging

```yaml
logger:
  default: info
  logs:
    custom_components.hg_brasil_finance: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
