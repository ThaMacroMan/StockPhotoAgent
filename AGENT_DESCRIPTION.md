# Stock Photo Search Agent - Informative Description

## Overview

The Stock Photo Search Agent is an AI-powered service that intelligently searches, curates, and delivers high-quality stock photos from Pexels based on natural language descriptions. Users receive a professionally curated collection of 8-12 perfectly matched photos with complete attribution and multiple download options—in 30-60 seconds.

---

## 1. The Problem

Finding the right stock photos is time-consuming and frustrating:

- **Generic searches return overwhelming results** — Thousands of mediocre photos that require extensive manual filtering
- **Matching specific moods is difficult** — Finding photos that capture the exact atmosphere or aesthetic takes significant effort
- **Manual curation drains time** — Reviewing hundreds of photos and tracking attribution info adds unnecessary overhead

---

## 2. The Solution

The Stock Photo Search Agent uses a **3-stage AI pipeline** that works like a professional creative team. When you describe what you need (e.g., "modern coffee shop with cozy atmosphere"), the agent interprets your intent, generates 4 optimized search queries, retrieves 40-60 candidate photos from Pexels, applies professional curation criteria (quality, relevance, composition, variety), and delivers 8-12 expertly selected photos with complete download URLs, photographer attribution, and licensing information—all in 30-60 seconds.

---

## 3. Key Capabilities

**Capability 1: Natural Language Understanding**  
Interprets creative briefs to extract mood, style, subject matter, and context—translating descriptions into actionable search strategies.

**Capability 2: Intelligent Multi-Query Search**  
Generates 2-4 optimized search queries using synonyms and strategic variations to find diverse, high-quality options.

**Capability 3: Professional Photo Curation**  
Reviews 40-60 photos and selects the TOP 8-12 based on quality, relevance, composition, and variety.

**Capability 4: Complete Attribution & Licensing**  
Automatically provides photographer names, profile links, dimensions, and attribution requirements for legal compliance.

---

## 4. How It Works

### User Input

Natural language descriptions including subject matter, style, mood, and context.

**Example inputs:**

- `"modern coffee shop with cozy atmosphere and natural lighting"`
- `"outdoor adventure hiking mountain trail"`
- `"tech startup office with diverse team collaborating"`

### Data Collection

Searches **Pexels API** with 2-4 optimized queries, retrieving 10-15 photos per query (40-60 total candidates).

### Processing

**Stage 1: Query Optimization** — Analyzes prompts using GPT-5-mini and generates 2-4 diverse search queries targeting different aspects of the request.

**Stage 2: Photo Curation** — Executes Pexels API searches, reviews all candidates, and selects TOP 8-12 photos based on professional criteria (quality, relevance, composition, variety).

**Stage 3: Results Formatting** — Organizes curated selection with complete metadata: Photo ID, all download URLs, photographer attribution, dimensions, Pexels page link.

### Output

**Formatted JSON/Markdown document** with 8-12 curated photos, multiple download URLs per photo (original, large, medium, small), complete photographer attribution, image metadata, and licensing information.

---

## 5. Transparency & Data Handling

| Field                     | Details                                                                                                                                                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Processing Location**   | Secure cloud infrastructure (Railway hosting, US-based servers)                                                                                                                                                  |
| **LLMs Used**             | GPT-5-mini (OpenAI) for natural language understanding, query generation, and curation logic                                                                                                                     |
| **Third-Party Tools**     | **A)** Pexels API — Searches and retrieves stock photos with attribution<br>**B)** OpenAI API — Powers LLM agents for analysis and curation<br>**C)** Masumi Payment Network — Handles blockchain-based payments |
| **Data Usage**            | User prompts processed temporarily to generate queries and curate photos; no user data permanently stored                                                                                                        |
| **Data Retention**        | Minimal; prompts and job data held in-memory during processing (~30-60 seconds); no long-term storage                                                                                                            |
| **Data Storage Location** | Data processed in-memory on US-based cloud infrastructure; no persistent database storage                                                                                                                        |
| **Security Measures**     | TLS/HTTPS encryption for API communications; API keys as environment variables; access-restricted hosting; no logging of sensitive data                                                                          |
| **Privacy**               | No personal data collected or stored; only search prompts processed temporarily; fully compliant with Pexels API terms; no user tracking                                                                         |
| **Legal Basis**           | Data processing based on legitimate interest (Art. 6(1)(f) GDPR); only publicly available Pexels photos accessed                                                                                                 |
| **User Rights**           | Users may request information, data correction, or deletion via support; minimal retention ensures automatic data purge after processing                                                                         |
| **Access Logs**           | No personal tracking; minimal operational logging for debugging (job IDs, status); logs contain no PII                                                                                                           |
| **Output Formats**        | Structured JSON with photo metadata, formatted Markdown report with clickable links, 8-12 curated photos, complete attribution info                                                                              |

---

## 6. Real-World Impact

**Time Savings:** Saves 15-30 minutes per search; eliminates manual photo review and attribution tracking

**Quality Improvement:** 90%+ relevance rate through AI-powered curation; professional-grade selection with consistent results

**Faster Workflows:** Enables rapid design iteration; reduces decision fatigue; speeds up client presentations

---

## 7. Who It's For

- **Creative Professionals:** Designers, art directors, and content creators needing photos for client projects and marketing materials
- **Marketing Teams:** Social media managers and brand strategists requiring on-brand visuals for campaigns and content
- **Agencies & Studios:** Design agencies needing efficient photo sourcing for multiple projects
- **Freelancers:** Independent creators and small business owners needing professional photos without time investment
- **Developers:** Product designers and UX professionals needing placeholder or production-ready images

---

## 8. How to Use the Agent

### Input Examples

| Input Field                       | Example                                                        |
| --------------------------------- | -------------------------------------------------------------- |
| **Prompt: Modern Workspace**      | `"modern tech startup office with diverse team collaborating"` |
| **Prompt: Lifestyle/Food**        | `"cozy coffee shop with warm atmosphere and natural lighting"` |
| **Prompt: Nature/Adventure**      | `"outdoor adventure hiking mountain trail with scenic views"`  |
| **Prompt: Minimalist/Design**     | `"minimalist workspace with plants and natural light"`         |
| **Prompt: Business/Professional** | `"professional business meeting in modern conference room"`    |

### Prompt Tips and Limitations

**✅ Best Practices:**

- Be specific about style and mood (e.g., "modern", "cozy", "industrial")
- Mention key elements (e.g., "natural lighting", "diverse team")
- Include context (e.g., "office space", "cafe interior")
- Use adjectives for atmosphere (e.g., "warm", "professional", "dynamic")

**⚠️ Limitations:**

- No custom image editing—finds and curates existing Pexels photos only
- Results depend on Pexels catalog availability
- English language prompts work best
- No real-time/breaking news photos

**🔄 Follow-Up:** Refine prompts with more specific details if results don't match expectations

---

## Real Output Example

**Query:** `"Modern coffee shop with cozy atmosphere and natural lighting"`

**Result Summary:**

| Metric              | Value       |
| ------------------- | ----------- |
| Photos Returned     | 10          |
| Processing Time     | ~45 seconds |
| Search Queries Used | 4           |
| Photo Source        | Pexels      |

**Sample Result:**

```
================================================================================
📸 STOCK PHOTO SEARCH RESULTS
================================================================================

1) Cozy cafe interior with large windows and seating
   - Photo ID: 32745111
   - Original: https://images.pexels.com/photos/32745111/pexels-photo-32745111.jpeg
   - Large: https://images.pexels.com/photos/32745111/...?h=650&w=940
   - Medium: https://images.pexels.com/photos/32745111/...?h=350
   - Small: https://images.pexels.com/photos/32745111/...?h=130
   - Photographer: Sami Abdullah — https://www.pexels.com/@onbab
   - Dimensions: 3944x7008

[... 9 more curated photos with full metadata ...]

================================================================================
Photos provided by Pexels. Attribution required.
================================================================================
```

**What the Agent Did:**

1. Identified key themes: modern, coffee shop, cozy, natural lighting
2. Generated 4 optimized search queries targeting different aspects
3. Retrieved 40-60 candidate photos from Pexels
4. Curated top 10 based on quality, relevance, composition, variety
5. Formatted with complete attribution and download links

---

## Need Help?

**Documentation:** [https://docs.masumi.network](https://docs.masumi.network)  
**Support:** [https://docs.masumi.network/documentation](https://docs.masumi.network/documentation)

---

_Ready for Sokosumi Marketplace — December 2025_
