# Arabic RAG API - Integration Guide

**Base URL**: `http://203.57.40.119:8001`

---

## API Endpoint

**POST** `/search` - Search Arabic texts

---

## Input Format

```json
{
  "query": "البخاري",
  "top_n": 3,
  "filter_books": ["hadith_sources_cleaned"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✅ Yes | Arabic search text |
| `top_n` | integer | ❌ No | Number of results (1-20). Default: 3 |
| `filter_books` | array | ❌ No | Filter by book category. Leave empty to search all books |

---

## Output Format

```json
[
  {
    "score": 0.383,
    "book_name": "hadith_sources_cleaned",
    "file_path": "manhaj2030_books_cleaned_v1/hadith_sources_cleaned/bukhari.txt",
    "chunk_index": 3,
    "text": "... Arabic text ..."
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `score` | float | Similarity score (lower = more relevant) |
| `book_name` | string | Book category |
| `file_path` | string | Source file path |
| `chunk_index` | integer | Position in source file |
| `text` | string | Arabic text content |

---

## Available Books

### Current (Test Collection)
- `hadith_sources_cleaned` - Sample hadith data (5 chunks)

### Coming Soon (Full Collection)
When full ingestion is complete, these book categories will be available:

**`hadith_sources_cleaned`** - Hadith Collections (16 books):
- abudaud, bukhari, ibnmajah, mujam_kabeer_tabari, musannaf_abdurrazaq
- musannaf_ibn_abi_shaybah, muslim, musnad_ahmad, mustadrak_alhakim
- muwatta, nasai, sahih_ibn_hibban, sahih_ibn_khuzaimah, sunan_darimi
- sunan_kubra_bayhaqi, tirmidhi

**`rijal_sources_cleaned`** - Narrator Biographies (10 books):
- alisabah, alkamal_duafaa, jarh_tadil, lisan_al_mizan, mizan_al_ietidal
- tabaqat_ibn_saad, tadhkirat_alhuffaz, tahdhib_al_kamal, tahdhib_al_tahdhib
- taqrib_al_tahdhib

**`shurooh_sources_cleaned`** - Hadith Commentaries (6 books):
- al_mughni, aun_almawud, fath_albari, nayl_al_awtar, sharh_nawawi
- tuhfat_al_ahwazhi

---

## Examples

### Example 1: Basic Search
```bash
curl -X POST http://203.57.40.119:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "البخاري",
    "top_n": 3
  }'
```

### Example 2: Search with Filter
```bash
curl -X POST http://203.57.40.119:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "الحديث النبوي",
    "top_n": 5,
    "filter_books": ["hadith_sources_cleaned"]
  }'
```

### Example 3: Python
```python
import requests

response = requests.post(
    "http://203.57.40.119:8001/search",
    json={
        "query": "أبو هريرة",
        "top_n": 3,
        "filter_books": ["hadith_sources_cleaned"]
    }
)

results = response.json()
for result in results:
    print(f"Score: {result['score']}")
    print(f"Text: {result['text'][:100]}...")
```

### Example 4: JavaScript
```javascript
const response = await fetch('http://203.57.40.119:8001/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'البخاري',
    top_n: 3,
    filter_books: ['hadith_sources_cleaned']
  })
});

const results = await response.json();
console.log(results);
```

---

## Error Responses

**422 Validation Error** - Invalid input format
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error** - Search failed
```json
{
  "detail": "Error message here"
}
```

---

## Notes

- Text encoding: UTF-8 (for Arabic support)
- Response time: < 500ms (test collection), may vary with full collection
- Filter by multiple categories: `"filter_books": ["hadith_sources_cleaned", "shurooh_sources_cleaned"]`
- No filter = search all books: Omit `filter_books` or pass `null`

---

**API Documentation**: Visit `http://203.57.40.119:8001/docs` for interactive testing
