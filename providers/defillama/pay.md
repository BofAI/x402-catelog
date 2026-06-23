# DefiLlama DeFi Data API (TRON/BSC x402, Minimum Price)

Minimum-price x402 passthrough for DefiLlama protocol TVL, fees/revenue, token prices and pool yields. Key-free DeFi decision data layer for agents. Data by DefiLlama.

## Service

- FQN: `defillama-tvl-tron`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-tron`
- Category: `finance`
- Chain: `tron:mainnet` (TRON)
- Scheme: `exact_gasfree`
- Tags: defillama, defi, tvl, fees, stablecoins, minimum-price
- Listed price: minimum price (`0.000001 USD` min and max price)

## When To Use

Use to read protocol TVL, fees/revenue and stablecoin metrics for DeFi research, allocation or risk screening.

## Endpoint Summary

### GET /protocols

All protocols with current TVL, category and chain breakdown
### GET /protocol/{slug}

Single protocol: historical TVL, fees, tokens, metadata
### GET /tvl/{protocol}

Current total TVL of a protocol (lightweight)

## Request Examples

- `GET /providers/defillama-tvl-tron/protocols`
- `GET /providers/defillama-tvl-tron/protocol/sunswap-v3`
- `GET /providers/defillama-tvl-tron/tvl/sunswap-v3`

## Response Shape

- Returns DefiLlama JSON: protocol list with tvl/chainTvls/category, or a single protocol's historical TVL, fees and metadata.

## Code Usage

Pay the catalog route with the x402 CLI. Example:

```bash
x402-cli pay 'https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols' \
  --method GET \
  --network tron:mainnet \
  --token USDT \
  --scheme exact_gasfree \
  --max-amount 0.001
```

Equivalent route form after payment:

```text
GET https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols
```

## Spend-Aware Usage

- Prefer per-protocol endpoints (/protocol/{slug}, /tvl/{protocol}) over the full /protocols dump to keep payloads small.
- Cache TVL/fees results; these update on the order of minutes, not seconds.

## When Not To Use

- Do not use for real-time token spot prices (DefiLlama price is on a separate host: coins.llama.fi).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
