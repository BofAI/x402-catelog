# x402 Catalog API 文档

本文档给前端开发使用。Catalog API 一期是静态 JSON 服务，不需要登录，不保存数据库，不返回任何上游 API key、钱包私钥、`provider.yml` 或 `.env`。

## 1. Base URL

本地开发：

```text
http://127.0.0.1:8088/api
```

测试或生产环境按部署域名替换：

```text
https://catalog.bankofai.io/api
```

前端建议使用环境变量：

```bash
VITE_X402_CATALOG_API=http://127.0.0.1:8088/api
NEXT_PUBLIC_X402_CATALOG_API=http://127.0.0.1:8088/api
```

## 2. 接口总览

```text
GET /api/status.json
GET /api/catalog.json
GET /api/providers/<fqn>.json
GET /api/pay/<fqn>.json
GET /api/pay/<fqn>.md
GET /api/categories.json
GET /api/search-index.json
```

一期接口路径都带 `.json` 或 `.md` 后缀，因为 Catalog Server 当前按静态文件发布。前端请直接使用带后缀路径，不要调用 `/api/catalog` 这种无后缀地址。

`<fqn>` 是 provider 的唯一标识，例如：

```text
open-meteo-weather
```

## 3. 健康状态

```http
GET /api/status.json
```

用途：

```text
前端启动检查
调试环境检查
监控健康检查
```

响应示例：

```json
{
  "version": 1,
  "generated_at": "2026-06-08T03:02:44Z",
  "provider_count": 2,
  "status": "ok"
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version` | number | Catalog API 版本 |
| `generated_at` | string | 当前静态快照生成时间，UTC ISO 8601 |
| `provider_count` | number | 当前 provider 数量 |
| `status` | string | `ok` 表示服务正常 |

## 4. Provider 列表

```http
GET /api/catalog.json
```

用途：

```text
首页列表
服务市场列表
分类筛选
链筛选
精选服务展示
```

响应结构：

```json
{
  "version": 1,
  "generated_at": "2026-06-08T03:02:44Z",
  "provider_count": 2,
  "first_party_count": 0,
  "chain_count": 3,
  "base_url": "https://catalog.bankofai.io/api",
  "frontend": {
    "featured_fqns": ["open-meteo-weather"],
    "categories": [
      {
        "id": "data",
        "count": 2
      }
    ],
    "chains": [
      {
        "id": "eip155:97",
        "count": 1
      }
    ]
  },
  "providers": [
    {
      "fqn": "open-meteo-weather",
      "title": "Open-Meteo Weather API",
      "title_zh": "Open-Meteo 天气 API",
      "main_title": "Open-Meteo Weather API",
      "sub_title": "按经纬度查询实时天气",
      "subtitle": "Coordinate-based current weather",
      "description": "Current weather data from the public Open-Meteo API.",
      "use_case": "Use for current weather lookup when latitude and longitude are already known.",
      "i18n": {
        "zh-CN": {
          "title": "Open-Meteo 天气 API",
          "subtitle": "按经纬度查询实时天气",
          "description": "来自公开 Open-Meteo API 的实时天气数据。",
          "useCase": "适合在已知经纬度时查询实时天气。"
        }
      },
      "logo": "https://open-meteo.com/favicon.ico",
      "category": "data",
      "category_meta": {
        "id": "data",
        "label": "Data",
        "label_zh": "数据"
      },
      "chains": ["eip155:97"],
      "chain_kinds": ["bnb"],
      "chains_meta": [
        {
          "id": "eip155:97",
          "kind": "bnb",
          "label": "BNB Smart Chain Testnet",
          "label_zh": "BNB 测试网"
        }
      ],
      "is_first_party": false,
      "is_featured": true,
      "featured_tags": ["weather", "open-data", "no-api-key"],
      "service_url": "https://gateway.bankofai.io/providers/open-meteo-weather",
      "endpoint_count": 1,
      "has_metering": true,
      "has_free_tier": false,
      "min_price_usd": 0.001,
      "max_price_usd": 0.001,
      "sha": "content-hash"
    }
  ]
}
```

顶层字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version` | number | Catalog API 版本 |
| `generated_at` | string | 静态快照生成时间 |
| `provider_count` | number | provider 总数 |
| `first_party_count` | number | 自营 provider 数量 |
| `chain_count` | number | 已使用链数量 |
| `base_url` | string | 生产 Catalog API 地址 |
| `frontend` | object | 前端筛选和精选配置 |
| `providers` | array | provider 列表摘要 |

`frontend` 字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `featured_fqns` | string[] | 精选 provider 的 fqn 列表 |
| `categories` | array | 当前有 provider 的分类 |
| `categories[].id` | string | 分类 ID |
| `categories[].label` | string | 分类英文展示名 |
| `categories[].label_zh` | string | 分类中文展示名 |
| `categories[].count` | number | 分类下 provider 数 |
| `chains` | array | 当前有 provider 的链 |
| `chains[].id` | string | 链 ID |
| `chains[].kind` | string | 链友好类型，例如 `bnb`、`tron` |
| `chains[].label` | string | 链英文展示名 |
| `chains[].label_zh` | string | 链中文展示名 |
| `chains[].count` | number | 链下 provider 数 |

Provider 摘要字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `fqn` | string | provider 唯一标识 |
| `title` | string | 英文标题 |
| `title_zh` | string | 中文服务名，前端头部第一行可直接使用 |
| `main_title` | string | 主标题，前端头部第二行可直接使用 |
| `sub_title` | string | 副标题，前端头部第三行可直接使用 |
| `subtitle` | string | 英文副标题 |
| `description` | string | 英文介绍 |
| `use_case` | string | 英文使用场景 |
| `i18n.zh-CN` | object | 中文标题、副标题、介绍、使用场景 |
| `logo` | string | logo URL |
| `category` | string | 分类 ID |
| `category_meta` | object | 分类展示信息，包含 `label` 和 `label_zh` |
| `chains` | string[] | 支持链列表 |
| `chain_kinds` | string[] | 链友好类型，例如 `bnb`、`tron` |
| `chains_meta` | array | 链展示信息，不需要前端自己解析 CAIP-2 |
| `is_first_party` | boolean | 是否自营 |
| `is_featured` | boolean | 是否精选 |
| `featured_tags` | string[] | 标签 |
| `service_url` | string | gateway provider 根地址 |
| `endpoint_count` | number | endpoint 数量 |
| `has_metering` | boolean | 是否存在计费 endpoint |
| `has_free_tier` | boolean | 是否存在免费 endpoint |
| `min_price_usd` | number | 最低美元价格 |
| `max_price_usd` | number | 最高美元价格 |
| `sha` | string | 内容 hash，用于前端缓存和变更检测 |

## 5. Provider 详情

```http
GET /api/providers/<fqn>.json
```

示例：

```http
GET /api/providers/open-meteo-weather.json
```

用途：

```text
服务详情页
endpoint 列表
支付状态展示
调用入口展示
```

响应结构：

```json
{
  "fqn": "open-meteo-weather",
  "title": "Open-Meteo Weather API",
  "title_zh": "Open-Meteo 天气 API",
  "main_title": "Open-Meteo Weather API",
  "sub_title": "按经纬度查询实时天气",
  "subtitle": "Coordinate-based current weather",
  "description": "Current weather data from the public Open-Meteo API.",
  "use_case": "Use for current weather lookup when latitude and longitude are already known.",
  "i18n": {
    "zh-CN": {
      "title": "Open-Meteo 天气 API",
      "subtitle": "按经纬度查询实时天气",
      "description": "来自公开 Open-Meteo API 的实时天气数据。",
      "useCase": "适合在已知经纬度时查询实时天气。"
    }
  },
  "logo": "https://open-meteo.com/favicon.ico",
  "category": "data",
  "category_meta": {
    "id": "data",
    "label": "Data",
    "label_zh": "数据"
  },
  "chains": ["eip155:97"],
  "chain_kinds": ["bnb"],
  "chains_meta": [
    {
      "id": "eip155:97",
      "kind": "bnb",
      "label": "BNB Smart Chain Testnet",
      "label_zh": "BNB 测试网"
    }
  ],
  "is_first_party": false,
  "is_featured": true,
  "featured_tags": ["weather", "open-data", "no-api-key"],
  "service_url": "https://gateway.bankofai.io/providers/open-meteo-weather",
  "endpoint_count": 1,
  "has_metering": true,
  "has_free_tier": false,
  "min_price_usd": 0.001,
  "max_price_usd": 0.001,
  "sha": "content-hash",
  "status": {
    "catalog": "listed",
    "gateway": "loaded",
    "payment": "verified-testnet",
    "upstream": "verified"
  },
  "endpoints": [
    {
      "method": "GET",
      "path": "/v1/forecast",
      "url": "https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast",
      "title": "Current Weather",
      "subtitle": "Lookup by coordinates",
      "description": "Current weather for latitude and longitude coordinates.",
      "use_case": "Use when an app or agent needs current weather metrics for a known coordinate.",
      "i18n": {
        "zh-CN": {
          "title": "实时天气",
          "subtitle": "按经纬度查询",
          "description": "查询指定经纬度的实时天气数据。",
          "useCase": "适合应用或 Agent 已知坐标并需要实时天气指标时使用。"
        }
      },
      "metered": true,
      "min_price_usd": 0.001,
      "max_price_usd": 0.001
    }
  ]
}
```

详情比列表多两个字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `status` | object | catalog、gateway、payment、upstream 状态 |
| `endpoints` | array | endpoint 详情列表 |

`status` 字段说明：

| 字段 | 示例 | 说明 |
| --- | --- | --- |
| `catalog` | `listed` | 是否已进入 catalog |
| `gateway` | `loaded` | gateway 是否已加载 |
| `payment` | `verified-testnet` | 支付是否已验证 |
| `upstream` | `verified` | 上游服务是否已验证 |

Endpoint 字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `method` | string | HTTP 方法 |
| `path` | string | provider 内部 endpoint path |
| `url` | string | 可调用的 gateway 完整 URL |
| `title` | string | endpoint 英文标题 |
| `subtitle` | string | endpoint 英文副标题 |
| `description` | string | endpoint 英文介绍 |
| `use_case` | string | endpoint 英文使用场景 |
| `i18n.zh-CN` | object | endpoint 中文文案 |
| `metered` | boolean | 是否计费 |
| `min_price_usd` | number | 最低美元价格 |
| `max_price_usd` | number | 最高美元价格 |

## 6. Pay JSON

```http
GET /api/pay/<fqn>.json
```

示例：

```http
GET /api/pay/open-meteo-weather.json
```

用途：

```text
Agent 读取可调用 API
CLI 读取支付调用摘要
前端提供“复制调用配置”
```

响应结构：

```json
{
  "version": 1,
  "fqn": "open-meteo-weather",
  "title": "Open-Meteo Weather API",
  "title_zh": "Open-Meteo 天气 API",
  "main_title": "Open-Meteo Weather API",
  "sub_title": "按经纬度查询实时天气",
  "subtitle": "Coordinate-based current weather",
  "description": "Current weather data from the public Open-Meteo API.",
  "use_case": "Use for current weather lookup when latitude and longitude are already known.",
  "i18n": {
    "zh-CN": {
      "title": "Open-Meteo 天气 API",
      "subtitle": "按经纬度查询实时天气",
      "description": "来自公开 Open-Meteo API 的实时天气数据。",
      "useCase": "适合在已知经纬度时查询实时天气。"
    }
  },
  "service_url": "https://gateway.bankofai.io/providers/open-meteo-weather",
  "chains": ["eip155:97"],
  "chain_kinds": ["bnb"],
  "chains_meta": [
    {
      "id": "eip155:97",
      "kind": "bnb",
      "label": "BNB Smart Chain Testnet",
      "label_zh": "BNB 测试网"
    }
  ],
  "sha": "content-hash",
  "endpoints": [
    {
      "method": "GET",
      "path": "/v1/forecast",
      "url": "https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast",
      "description": "Current weather for latitude and longitude coordinates.",
      "metered": true,
      "min_price_usd": 0.001,
      "max_price_usd": 0.001
    }
  ]
}
```

前端注意：

```text
pay-json 不包含详细展示字段，例如 logo、status、endpoint title。
详情页展示用 /api/providers/<fqn>.json。
Agent/CLI 调用摘要用 /api/pay/<fqn>.json。
```

## 7. Pay Markdown

```http
GET /api/pay/<fqn>.md
```

示例：

```http
GET /api/pay/open-meteo-weather.md
```

用途：

```text
给人阅读的调用说明
文档页展示
Agent 上下文补充
```

响应类型：

```text
text/markdown
```

## 8. 分类

```http
GET /api/categories.json
```

响应示例：

```json
[
  {
    "id": "data",
    "label": "Data",
    "label_zh": "数据",
    "count": 2
  }
]
```

说明：

```text
categories.json 是 catalog.json 里 frontend.categories 的直接导出。
如果前端已经请求了 catalog.json，可以直接使用 catalog.frontend.categories，不需要重复请求。
前端展示文案优先使用 label_zh，不需要自己把 category ID 转中文。
```

## 9. 搜索索引

```http
GET /api/search-index.json
```

用途：

```text
前端本地搜索
轻量关键词匹配
离线搜索缓存
```

响应结构：

```json
{
  "version": 1,
  "generated_at": "2026-06-08T03:02:44Z",
  "documents": [
    {
      "fqn": "open-meteo-weather",
      "title": "Open-Meteo Weather API",
      "subtitle": "Coordinate-based current weather",
      "description": "Current weather data from the public Open-Meteo API.",
      "use_case": "Use for current weather lookup when latitude and longitude are already known.",
      "category": "data",
      "chains": ["eip155:97"],
      "featured_tags": ["weather", "open-data", "no-api-key"],
      "service_url": "https://gateway.bankofai.io/providers/open-meteo-weather",
      "endpoints": [
        {
          "method": "GET",
          "path": "/v1/forecast",
          "title": "Current Weather",
          "description": "Current weather for latitude and longitude coordinates."
        }
      ]
    }
  ]
}
```

搜索建议：

```text
优先匹配 fqn、title、featured_tags、category。
其次匹配 description、use_case、endpoints[].title、endpoints[].path。
搜索结果点击后跳转到 /providers/<fqn> 对应的详情页。
```

## 10. 前端渲染建议

头部三行标题建议直接使用：

```text
第一行：provider.title_zh
第二行：provider.main_title
第三行：provider.sub_title
```

中文页面：

```ts
const zh = provider.i18n?.["zh-CN"];
const title = provider.title_zh ?? zh?.title ?? provider.title;
const mainTitle = provider.main_title ?? provider.title;
const subTitle = provider.sub_title ?? zh?.subtitle ?? provider.subtitle;
const description = zh?.description ?? provider.description;
const useCase = zh?.useCase ?? provider.use_case;
```

列表页建议展示：

```text
logo
title / 中文 title
subtitle / 中文 subtitle
description / 中文 description
category
chains
category_meta.label_zh
chains_meta[].label_zh
featured_tags
min_price_usd / max_price_usd
endpoint_count
has_metering
has_free_tier
```

精选展示建议：

```text
卡片是否显示精选 badge：直接看 provider.is_featured。
精选分组或首页精选排序：用 catalog.frontend.featured_fqns。
```

统计字段使用建议：

```text
provider_count 可以用于顶部统计。
first_party_count 和 chain_count 是统计信息，前端可以展示，但不建议用它们驱动业务逻辑。
分类、链筛选项请用 catalog.frontend.categories 和 catalog.frontend.chains。
不要在前端写死分类和链列表，最多只把兜底展示文案写死。
```

详情页建议展示：

```text
provider 基本信息
status
endpoints
每个 endpoint 的 method、path、url、价格、中文说明
复制 endpoint url
查看 pay-json
查看 pay.md
```

调用 API 时：

```text
Catalog API 只负责发现和展示。
真正调用 provider API 时，请使用 endpoint.url，也就是 gateway URL。
如果 endpoint 是 paid，未携带 x402 payment header 时 gateway 会返回 402 Payment Required。
```

链展示建议：

```text
一期不建议做顶部全局链切换。
原因是 Catalog 的 endpoint.url 对 BNB Chain 和 TRON 是同一类 gateway URL，调用代码不需要把链写进 URL。
链信息主要用于展示 provider 支持范围，以及支付时筛选 payment requirements。
```

前端建议保留：

```text
provider 卡片上的 chains badge
详情页的支持链说明
可选的列表筛选条件
```

前端建议去掉：

```text
顶部全局链切换
依赖顶部链切换改变 endpoint.url 的逻辑
```

CLI 调用代码默认不需要指定链：

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast?latitude=31.2304&longitude=121.4737&current=temperature_2m&timezone=auto'
```

如果用户明确要限制某条链，可以展示为高级用法：

```bash
x402-cli pay \
  --network eip155:97 \
  'https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast?latitude=31.2304&longitude=121.4737&current=temperature_2m&timezone=auto'
```

`--network` 使用 CAIP-2 ID，例如：

```text
eip155:56    BNB Chain
eip155:97    BNB Smart Chain Testnet
tron:mainnet TRON Mainnet
tron:nile    TRON Nile Testnet
tron:shasta  TRON Shasta Testnet
```

前端不需要通过字符串前缀判断链类型。直接使用：

```text
provider.chain_kinds
provider.chains_meta[].kind
provider.chains_meta[].label_zh
catalog.frontend.chains[].kind
catalog.frontend.chains[].label_zh
```

注意：

```text
BNB Chain 和 TRON 在前端展示层可以按同一种 provider 模型处理。
但它们在支付底层不完全一致：network ID、钱包签名机制、facilitator settle 逻辑、gas 承担方式都可能不同。
这些差异由 gateway、x402-cli 和 402 payment requirements 处理，不应该强行放到前端顶部全局切换里。
```

## 11. TypeScript 类型参考

```ts
export type CatalogResponse = {
  version: number;
  generated_at: string;
  provider_count: number;
  first_party_count: number;
  chain_count: number;
  base_url: string;
  frontend: {
    featured_fqns: string[];
    categories: Array<CategoryMeta & { count: number }>;
    chains: Array<ChainMeta & { count: number }>;
  };
  providers: ProviderSummary[];
};

export type LocalizedCopy = {
  title: string;
  subtitle: string;
  description: string;
  useCase: string;
};

export type CategoryMeta = {
  id: string;
  label: string;
  label_zh: string;
};

export type ChainMeta = {
  id: string;
  kind: "bnb" | "tron" | "evm" | "other";
  label: string;
  label_zh: string;
};

export type ProviderSummary = {
  fqn: string;
  title: string;
  title_zh: string;
  main_title: string;
  sub_title: string;
  subtitle: string;
  description: string;
  use_case: string;
  i18n: {
    "zh-CN"?: LocalizedCopy;
  };
  logo: string;
  category: string;
  category_meta: CategoryMeta;
  chains: string[];
  chain_kinds: string[];
  chains_meta: ChainMeta[];
  is_first_party: boolean;
  is_featured: boolean;
  featured_tags: string[];
  service_url: string;
  endpoint_count: number;
  has_metering: boolean;
  has_free_tier: boolean;
  min_price_usd: number;
  max_price_usd: number;
  sha: string;
};

export type ProviderDetail = ProviderSummary & {
  status: {
    catalog: string;
    gateway: string;
    payment: string;
    upstream: string;
  };
  endpoints: ProviderEndpoint[];
};

export type ProviderEndpoint = {
  method: string;
  path: string;
  url: string;
  title: string;
  subtitle: string;
  description: string;
  use_case: string;
  i18n: {
    "zh-CN"?: LocalizedCopy;
  };
  metered: boolean;
  min_price_usd: number;
  max_price_usd: number;
};

export type PayJson = {
  version: number;
  fqn: string;
  title: string;
  title_zh: string;
  main_title: string;
  sub_title: string;
  subtitle: string;
  description: string;
  use_case: string;
  i18n: {
    "zh-CN"?: LocalizedCopy;
  };
  service_url: string;
  chains: string[];
  chain_kinds: string[];
  chains_meta: ChainMeta[];
  sha: string;
  endpoints: Array<{
    method: string;
    path: string;
    url: string;
    description: string;
    metered: boolean;
    min_price_usd: number;
    max_price_usd: number;
  }>;
};
```

## 12. 错误和兼容性

Catalog 是静态文件服务：

```text
文件存在时返回 200。
文件不存在时返回 404。
接口不需要鉴权。
不支持写操作。
不支持服务端分页。
不支持服务端搜索参数。
```

前端建议：

```text
请求失败时展示空状态和重试按钮。
详情页 404 时提示 provider 不存在或尚未发布。
列表页优先使用 /api/catalog.json。
搜索可以使用 /api/search-index.json 在前端本地完成。
```

## 13. 缓存建议

可以按静态资源缓存处理：

```text
catalog.json、search-index.json 建议短缓存。
providers/<fqn>.json、pay/<fqn>.json 可以按 sha 做变更检测。
前端如果发现 sha 变化，需要刷新详情和 pay-json。
```

一期没有数据库，生产发布时应由 CI/CD 生成新的 `dist/` 快照并发布到 Catalog Server 或 CDN。
