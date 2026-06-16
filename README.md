# AIRecommendSystem — 系統說明文件

---

## 專案結構

```
AIRecommendSystem/
├── webServer/
│   ├── main.py
│   ├── __init__.py
│   ├── controller/
│   │   ├── __init__.py
│   │   ├── condition.py
│   │   ├── exercise.py
│   │   ├── metric.py
│   │   ├── operator.py
│   │   └── rule.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── condition.py
│   │   ├── exercise.py
│   │   ├── metric.py
│   │   ├── operator.py
│   │   ├── recommend.py
│   │   └── rule.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── condition.py
│   │   ├── exercise.py
│   │   ├── metric.py
│   │   ├── operator.py
│   │   └── rule.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── condition.py
│   │   ├── exercise.py
│   │   ├── metric.py
│   │   ├── operator.py
│   │   └── rule.py
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── condition.py
│   │   ├── exercise.py
│   │   ├── metric.py
│   │   ├── operator.py
│   │   └── rule.py
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       └── httpResponseMethod.py
└── webClient/
    └── www/
        └── template/
            └── rehab_rule_editor.html
```

---

## 資料庫結構說明

本文件說明系統的資料庫 Schema，涵蓋復健動作推薦規則、評估指標、運算子及運動動作定義。

系統透過規則引擎（Rule Engine）依優先順序評估病患的量測數值，並根據條件判斷結果自動推薦或排除對應的復健動作。

`condition` 透過 `rule_id` 與 `rule` 關聯（多對一），並透過 `metric_id`、`operator_id` 分別與 `metric`、`operator` 關聯（多對一）。`condition.exercises` 儲存對應的 `exercise.id` 清單。

---

## 資料表總覽

| 資料表 | 說明 |
|---|---|
| `rule` | 規則定義（含名稱） |
| `condition` | 規則條件，定義指標、運算子、閾值與推薦動作 |
| `metric` | 評估指標定義（e.g., VAS 測試前分數） |
| `operator` | 比較運算子定義（e.g., >, >=, =） |
| `exercise` | 復健動作定義 |

---

## rule

規則定義，以 `name` 識別規則群組，優先順序改由各 `condition.priority` 控制。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 規則名稱 |

---

## condition

規則條件，描述「當某指標滿足某運算子與閾值時，推薦或不推薦哪些動作」。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `rule_id` | int | | 所屬規則（FK → rule） |
| `metric_id` | int | | 評估指標（FK → metric） |
| `operator_id` | int | | 比較運算子（FK → operator） |
| `exercises` | list | | 對應動作 ID 清單（FK → exercise） |
| `max_value` | str | | 範圍最大閾值（e.g., `"3"`, `"10.5"`） |
| `min_value` | str | | 範圍最小閾值（e.g., `"3"`, `"10.5"`） |

---

## metric

評估指標定義，供條件設定時選用。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 指標名稱（e.g., VAS 測試前分數、單腳站立（秒）） |

---

## operator

比較運算子定義，供條件設定時選用。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 運算子符號（e.g., `>`, `>=`, `<=`, `<`, `=`） |

---

## exercise

復健動作定義，為條件推薦的基本單元。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 動作名稱（e.g., Isometric quadriceps set） |

---

## patient

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 姓名 |
| `metric_values` | list[str] | | 評估指標值 |
