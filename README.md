# How the Stock Photo Agent Works

The Stock Photo Agent uses a **3-stage AI pipeline** to intelligently find and curate stock photos from Pexels.

---

## The Problem

Searching for stock photos is tedious:
- Generic searches return thousands of mediocre results
- Finding photos that match a specific mood or style takes time
- You have to manually review and select the best ones

## The Solution

The agent acts like a creative team:
1. **Interprets** your request
2. **Searches** with optimized queries
3. **Curates** the best matches
4. **Delivers** ready-to-use photos with proper attribution

---

## The 3-Stage Pipeline

### Stage 1: Query Optimization

**Agent:** Search Query Specialist

**What it does:**
- Analyzes your natural language prompt
- Considers mood, style, subject matter, and context
- Generates 2-4 optimized search queries
- Uses synonyms and related concepts to cast a wider net

**Example:**

Input: `"modern coffee shop with cozy atmosphere and natural lighting"`

Generated queries:
```
1. modern cozy coffee shop interior natural light large windows warm wood tones
2. sunlit specialty cafe Scandinavian hygge vibe neutral palette
3. industrial-chic coffee shop exposed brick soft daylight pendant lights
4. boutique cafe morning light barista at counter latte art greenery
```

**Why this matters:** A single search query limits your results. Multiple intelligent queries find diverse, high-quality options.

---

### Stage 2: Photo Curation

**Agent:** Stock Photo Curator

**What it does:**
- Searches Pexels API with each query (10-15 photos per query)
- Reviews 40-60 total photos from all searches
- Selects the TOP 8-12 photos based on four criteria:

| Criteria | Description |
|----------|-------------|
| **Quality** | Resolution, sharpness, professional appearance |
| **Relevance** | How well it matches your original request |
| **Composition** | Framing, balance, visual appeal |
| **Variety** | Mix of angles, styles, and subjects |

**Why this matters:** The AI acts like a professional photo editor reviewing a contact sheet, selecting only the best matches.

---

### Stage 3: Presentation

**Agent:** Results Presenter

**What it does:**
- Organizes the curated selection
- Formats each photo with complete information:
  - Photo ID
  - Download URLs (original, large, medium, small)
  - Photographer name and profile link
  - Image dimensions
  - Pexels page URL
- Includes attribution requirements

**Why this matters:** You get ready-to-use photos with all the information needed for proper usage and attribution.

---

## What You Get

For each search, you receive 8-12 curated photos with:

- ✅ Multiple size options (original, large, medium, small)
- ✅ Direct download URLs
- ✅ Photographer attribution
- ✅ Pexels page links
- ✅ Image dimensions

All photos are free under the Pexels license for commercial use.

---

## The Selection Philosophy

1. **Breadth first, then narrow** — Multiple queries find diverse options, then AI curates down to the best
2. **Context-aware** — Understands that "cozy" means warm tones, soft lighting, inviting spaces
3. **Professional curation** — Mimics how a designer reviews a photo library
4. **Variety with coherence** — Mix of shots that still feel like a cohesive collection
5. **Practical output** — Ready-to-use with proper attribution

---

## What the Agent Does NOT Do

- ❌ Randomly pick photos
- ❌ Return the first results from Pexels
- ❌ Use a single basic search query
- ❌ Modify or fabricate URLs

---

## Technical Details

- **LLM:** GPT-5-mini (configurable)
- **Photo Source:** Pexels API
- **Framework:** CrewAI with 3 specialized agents
- **Output:** 8-12 curated photos per request
- **Processing Time:** 30-60 seconds

---

## Example Use Cases

| Prompt | What You Get |
|--------|--------------|
| "modern tech startup office" | Clean, professional workspace photos with natural light |
| "cozy autumn cafe" | Warm-toned coffee shop interiors with fall vibes |
| "outdoor adventure hiking" | Mountain trails, hikers, scenic nature shots |
| "minimalist product photography background" | Clean, simple backgrounds for product shots |

---

## Attribution Requirements

All photos from Pexels require attribution:

> "Photo by [Photographer Name](photographer-url) from [Pexels](https://www.pexels.com)"

The agent includes all necessary attribution information in the results.

---

## Summary

The Stock Photo Agent transforms a simple description into a professionally curated collection of stock photos. Instead of scrolling through hundreds of mediocre results, you get 8-12 handpicked photos that match your vision—with all the URLs and attribution info ready to use.

**Input:** Natural language description  
**Output:** Curated photo collection with download links

It's like having a creative team that understands your brief and delivers exactly what you need.

