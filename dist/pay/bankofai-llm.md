# BANK OF AI LLM API

## Service

- FQN: `bankofai-llm`
- Service URL: `https://gateway.bankofai.io/providers/bankofai-llm`
- Category: `ai_ml`
- Chains: `eip155:97`

## Endpoints

### GET /v1/models

List available BANK OF AI LLM models.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/models`
- Price: `$0.001`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/models'
```

### POST /v1/chat/completions

Create a chat completion.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/chat/completions`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/chat/completions' \
  --method POST \
  --json '{"model":"MODEL_ID","messages":[{"role":"user","content":"hello"}]}'
```

### POST /v1/messages

Create a Claude-compatible message.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/messages`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/messages' \
  --method POST \
  --json '{"model":"claude-sonnet-4-6","max_tokens":1024,"messages":[{"role":"user","content":"hello"}]}'
```

## Notes

Gateway runtime must configure `BANKOFAI_API_KEY`; this file is public and must not include API keys, bearer tokens, provider.yml, `.env`, passwords, private keys, or private infrastructure URLs. BANK OF AI upstream charges by Credits; current x402 gateway pricing is fixed per request until usage-based settlement is enabled.
