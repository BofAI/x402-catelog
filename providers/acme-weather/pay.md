# Acme Weather API

## Service

- FQN: `acme-weather`
- Service URL: `https://gateway.bankofai.io/providers/acme-weather`
- Category: `data`
- Chains: `tron:mainnet`, `eip155:56`

## Endpoints

### GET /v1/current

Current weather for a city.

- URL: `https://gateway.bankofai.io/providers/acme-weather/v1/current`
- Price: `$0.002`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/acme-weather/v1/current?city=Shanghai'
```

## Notes

This file is public. Do not include upstream API keys, bearer tokens, provider.yml, `.env`, passwords, or private infrastructure URLs.
