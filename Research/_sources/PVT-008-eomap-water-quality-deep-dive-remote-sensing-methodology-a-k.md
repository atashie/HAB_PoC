---
key: PVT-008
title: EOMAP Water Quality Deep Dive (Remote Sensing Methodology) — a.k.a. "Water Quality – Technical Deep Dive"
authors_or_org: EOMAP GmbH (no individual authors identified; company technical/marketing document)
year: 2025
url: https://eomap.com/wp-content/uploads/2025/05/WQ_deep_dive_S.pdf (the file actually served by the start-download landing URL; internal metadata / indexed title shows "Version: May 2025")
access_date: 2026-07-01
tier: PVT
source_type: Company technical whitepaper (PDF) plus corroborating company website pages — commercial vendor content, not independently peer-reviewed
categories: [remote-sensing]
relevance: Medium
full_text_access: blocked
fetch_status: partial
review_severity: clean
review_overall: pass
---

# EOMAP Water Quality Deep Dive (Remote Sensing Methodology) — a.k.a. "Water Quality – Technical Deep Dive"

> Note: provisional URL was resolved to a primary source. Original: https://eomap.com/start-download/water-quality-deep-dive

**What it is.** A commercial technical whitepaper ("Water Quality – Technical Deep Dive," dated May 2025) in which EOMAP GmbH, a satellite Earth-observation service provider, describes its proprietary remote-sensing methodology for deriving inland- and coastal-water quality parameters (chlorophyll, turbidity, Secchi depth, CDOM, surface temperature, a cyanobacteria/HAB proxy indicator, and trophic-state classification) from multi-satellite optical imagery. The PDF itself is an image/vector-heavy InDesign export that could not be extracted as text by the fetch tool, so this dossier relies on EOMAP's own companion web pages describing the same methodology, with confirmed verbatim overlap on several sentences.

## Key claims
*(each tagged with its blind-review verdict)*

- **[✓ verified]** EOMAP defines Chlorophyll (CHL) as a pigment in phytoplankton cells used as a proxy for algae abundance, with stated concentrations spanning about four orders of magnitude: roughly 0.01–10 µg/l in marine waters/clear lakes versus up to 100 µg/l (or more) in eutrophic lakes.
  - *evidence:* Definition and concentration ranges appear identically on EOMAP's directly-fetched water-quality service page and were independently corroborated by a word-for-word identical sentence surfaced via search-engine indexing of the actual Deep Dive PDF, indicating the same text exists in both. (eomap.com/services/water-quality/ (Chlorophyll section); identical phrase also indexed from within WQ_deep_dive_S.pdf per search results)
  - *quote:* "Chlorophyll values vary over 4 magnitudes... between 0.01 and 10 µg/l... for eutrophic lakes concentrations can reach 100 µg/l"
- **[✓ verified]** Turbidity (TUR) is retrieved from backward light scattering measured in the 450–800 nm spectral range.
  - *evidence:* Stated directly as the measurement method for satellite-based turbidity retrieval on EOMAP's water-quality service page. (eomap.com/services/water-quality/ (Turbidity/TSM section))
  - *quote:* "Satellite-based turbidity is determined by backward scattering of light in a range of 450 to 800 nm."
- **[✓ verified]** EOMAP's Harmful Algal Bloom (HAB) indicator is explicitly a qualitative proxy for cyanobacteria, not a calibrated concentration, derived from the reflectance/absorption discrepancy between the 550 nm and 650 nm bands and sensitive to phycocyanin/phycoerythrin pigments.
  - *evidence:* Stated directly in the HAB section of the water-quality service page; the same 'proxy for cyanobacteria' phrasing also appears in search-indexed text attributed to the Deep Dive PDF. (eomap.com/services/water-quality/ (HAB section))
  - *quote:* "a proxy for cyanobacteria"
- **[✓ verified]** Secchi Disk Depth (SDD) is not measured directly but calculated from the water's optical attenuation coefficient, ranging from under 1 metre in very turbid water to over 20 metres in very clear water.
  - *evidence:* Given as the definition/derivation method and typical range on the water-quality service page. (eomap.com/services/water-quality/ (SDD section))
  - *quote:* "less than a metre in very turbid waters to over 20 metres"
- **[✓ verified]** EOMAP states its satellite water-quality products can be delivered at revisit frequencies of 1–8 days, within 3–12 hours of image acquisition or archive availability, and can draw on satellite archives extending back up to 40 years.
  - *evidence:* Stated as the temporal-coverage capability of the service on the water-quality service page. (eomap.com/services/water-quality/ (temporal coverage section))
  - *quote:* "revisit times ranging from 1 – 8 days"
- **[✓ verified]** A minimum water-body size is required for retrieval, tied to sensor resolution: at least 5×5 water pixels, e.g. at least 50×50 metres when using 10 m resolution Sentinel-2 imagery, with a 1–2 pixel shoreline buffer excluded from analysis.
  - *evidence:* Given as the spatial-resolution / minimum-mapping-unit constraint on the water-quality service page. (eomap.com/services/water-quality/ (spatial resolution section))
  - *quote:* "at least 50×50 metres in extent"
- **[✓ verified]** The methodology explicitly reduces available scenes due to clouds, cloud shadow, atmospheric aerosols and sun glint, and separately flags out floating-vegetation (macrophyte) pixels rather than quantifying them; shallow-water bottom reflectance can also disturb the retrieved signal.
  - *evidence:* Stated as limitations/caveats in the same service page section describing data-quality handling. (eomap.com/services/water-quality/ (limitations section))
  - *quote:* "Clouds, cloud shadows, atmospheric aerosols and sunlight reflections at the water surface can reduce the number of available scenes"
- **[✓ verified]** Retrieved parameter values represent a depth-integrated quantity from the surface down to the light-penetration depth (approximately 1.5 times the visible/Secchi depth, i.e., the euphotic zone), not a single surface-point sample.
  - *evidence:* Stated explicitly as the measurement-depth convention on the water-quality service page. (eomap.com/services/water-quality/ (measurement depth section))
  - *quote:* "approximately 1.5x visible depths"
- **[✓ verified]** In an applied case study (WasMon-CT, for German state agency LUBW in Baden-Württemberg), EOMAP combined Landsat 7, Landsat 8 and Sentinel-2 (high resolution) with Sentinel-3 and MODIS Aqua/Terra (medium resolution, for Lake Constance) to derive turbidity, Secchi disc depth, total/organic absorption, chlorophyll-a and harmful algae blooms for more than 20 lakes over roughly 2011–2017, in a state EOMAP describes as having 'no fewer than 1300 lakes bigger than 1 hectare.'
  - *evidence:* Given as a real deployment example on EOMAP's WasMon-CT case-study page, directly fetched. (eomap.com/usecases/wasmon-ct/)
  - *quote:* "more than 20 lakes within the federal state boundaries over a period of 17 years to 2017"
- **[✓ verified]** EOMAP groups waterbodies into three trophic-state categories: oligotrophic (nutrient-poor), mesotrophic (moderately productive), and eutrophic (nutrient-rich and highly productive).
  - *evidence:* Given as the trophic-state classification scheme on the water-quality service page. (eomap.com/services/water-quality/ (trophic state classification section))
  - *quote:* "oligotrophic (nutrient-poor), mesotrophic (moderately productive), and eutrophic (nutrient-rich and highly productive)"

## Data / numbers
- Chlorophyll (CHL): ~0.01–10 µg/l typical for marine waters/clear lakes; up to 100 µg/l or more in eutrophic lakes (spans ~4 orders of magnitude)
- Turbidity (TUR) retrieval spectral window: 450–800 nm (backward light scattering)
- HAB/cyanobacteria proxy indicator spectral bands compared: 550 nm vs. 650 nm
- Secchi Disk Depth (SDD) range: <1 m (very turbid) to >20 m (very clear)
- Effective measurement/integration depth ≈ 1.5 × visible (Secchi) depth (approx. euphotic zone)
- Revisit frequency: 1–8 days
- Product delivery latency: 3–12 hours after acquisition or archive availability
- Historical satellite archive depth referenced: up to 40 years
- Minimum mappable water body: ≥5×5 water pixels; e.g., ≥50×50 m when using 10 m resolution Sentinel-2 imagery
- Shoreline exclusion buffer: 1–2 pixels
- Sentinel-2 resolution cited: 10 m
- Document version date: May 2025 (per indexed PDF title 'Version: May 2025')
- Case study (WasMon-CT, Baden-Württemberg/LUBW): >20 lakes monitored; monitoring period ~2011–2017 ('17 years to 2017'); state described as having ≥1300 lakes larger than 1 hectare
- No independently verifiable accuracy/validation statistic (R², RMSE, bias, or uncertainty interval) for CHL/TUR/SDD retrieval was locatable in the accessible material

## Methods
Multi-sensor optical remote sensing (Landsat 7, Landsat 8, Sentinel-2 at high spatial resolution; Sentinel-3 and MODIS Aqua/Terra at medium resolution for higher temporal frequency) feeding parameter-specific retrieval algorithms: (1) Chlorophyll (CHL) via a physics-based approach using pigment-specific in-water absorption/spectral characteristics of chlorophyll-a and phaeophytin; (2) Turbidity (TUR)/Total Suspended Matter via backward light-scattering in the 450–800 nm range; (3) a Harmful Algal Bloom (HAB) indicator, explicitly called "qualitative," from the reflectance/absorption discrepancy between 550 nm and 650 nm bands, sensitive to phycocyanin/phycoerythrin; (4) Secchi Disk Depth (SDD), not measured directly but calculated from the water's attenuation coefficient (in-water scattering + absorption); (5) Surface Water Temperature from thermal bands; (6) CDOM from blue-wavelength absorption. Outputs are described as depth-integrated from the surface to the light-penetration (euphotic) depth, ~1.5× the visible/Secchi depth, not single-point surface samples. The method is said to work across "coastal waters to lakes to river sections," with historical satellite archives reaching back up to 40 years, revisit frequencies of 1–8 days, and delivery within 3–12 hours of acquisition/archive availability. It requires a minimum mappable water-body size tied to sensor resolution (≥5×5 water pixels, e.g. ≥50×50 m for 10 m Sentinel-2) with a 1–2 pixel shoreline buffer excluded, and includes automated masking of clouds/cloud shadow/aerosols/sun glint and flagging of floating-vegetation (macrophyte) pixels. Demonstrated in an applied case study (WasMon-CT, for the German state agency LUBW in Baden-Württemberg) covering more than 20 lakes over roughly 2011–2017.

## Stated limitations
The source's own companion materials state: (1) clouds, cloud shadows, atmospheric aerosols, and sun-glint "reduce the number of available scenes," i.e., reduce temporal coverage rather than being corrected away; (2) floating vegetation/macrophyte-covered pixels are detected and "flagged out," i.e., excluded from retrieval rather than quantified; (3) "reflections from the water body ground zones" (bottom reflectance in shallow/optically-shallow water) "can disturb the signal," i.e., degrade retrieval accuracy in shallow areas; (4) there is a hard minimum-mappable-water-body-size constraint set by sensor pixel resolution, meaning small ponds/narrow channels below that threshold cannot be resolved by a given sensor; (5) the HAB indicator is explicitly framed as a "qualitative" proxy for cyanobacteria (a band-difference index), not a calibrated toxin or cell-count concentration. No independently verifiable accuracy/validation statistic (e.g., R², RMSE, bias, or a stated uncertainty/confidence interval) for CHL, TUR, or SDD retrieval could be located in the accessible material — the services page only asserts generically that "extensive validation reports" and "peer-reviewed papers" exist as evidence, without giving the figures themselves.

## Tensions with other findings
This is vendor/commercial marketing-technical content, not an independently peer-reviewed study; as accessed, it asserts validation exists but does not itself supply a baseline or an uncertainty figure for any retrieved parameter, which is a direct tension with this project's own claim-gate requirement (every number needs a baseline + uncertainty) — this source cannot itself satisfy that gate for CHL/TUR/SDD/HAB accuracy claims. Its HAB indicator is explicitly a qualitative proxy for cyanobacteria (a two-band reflectance/absorption difference), not a calibrated cyanobacterial biomass or toxin concentration — a caution against treating "HAB indicator present" as equivalent to a quantified bloom-severity or toxin measurement in any downstream analysis. Separately, chlorophyll and the HAB index are both explicitly labeled "proxy" measures for algae/cyanobacteria rather than direct biomass measurements, reinforcing that any driver/risk claim built on them is correlational (optical proxy ↔ organism abundance) and should not be read as a direct causal or compositional measurement. Methodologically, this dossier entry itself carries a traceability caveat worth flagging in the broader literature review: the primary document's literal text could not be read directly (image-based PDF), so claims here rest on corroborating first-party company pages plus confirmed verbatim snippet overlap, not a clean direct read of the named PDF.

## Blind adversarial review
- **Overall:** pass
- **Unsupported claims:** 0

## Provenance
- Canonical URL: https://eomap.com/wp-content/uploads/2025/05/WQ_deep_dive_S.pdf (the file actually served by the start-download landing URL; internal metadata / indexed title shows "Version: May 2025")
- Access date: 2026-07-01
- Full-text access: blocked | Fetch status: partial
- Fetch notes: Two direct WebFetch attempts on the actual target (the start-download landing URL, and its resolved file https://eomap.com/wp-content/uploads/2025/05/WQ_deep_dive_S.pdf) both returned only raw PDF object/stream data — the document is built largely from JPXDecode-compressed images (InDesign export) with "minimal extractable plain text," so no substantive prose could be pulled from it directly; this counts as a failed direct fetch of the primary artifact per the task's own criteria. Per the task's fallback instruction, I then used WebSearch to locate an accessible version of the same content: search results repeatedly surfaced short excerpts that search engines had indexed from inside the actual PDF (e.g., the exact "Chlorophyll values vary over 4 magnitudes..." and "HAB... proxy for cyanobacteria" sentences), and these excerpts are word-for-word identical to text on EOMAP's own companion web page https://www.eomap.com/services/water-quality/, which I then fetched directly and successfully (clean HTML). I also directly fetched a related EOMAP case-study page (https://eomap.com/usecases/wasmon-ct/) for a concrete, numbers-bearing deployment example of the same methodology family. I deliberately excluded from this dossier any content that WebSearch surfaced from EOMAP pages about unrelated product lines (e.g., a bathymetry accuracy figure of "0.5 m LE90 / RMSE 0.3 m" found on eomap.com/services/bathymetry/) since that describes a different EOMAP service (seafloor depth mapping), not water quality, and attributing it here would be a misattribution. I was unable to find, anywhere in the accessible material, a specific independently-checkable accuracy/validation statistic (R², RMSE, bias, uncertainty interval) for the water-quality parameters themselves — the service page only makes a general, unsupported assertion that validation reports and peer-reviewed papers exist. Because the dossier is built from corroborating company pages rather than a clean direct read of the named PDF, full_text_access is recorded as "blocked" (the specific named document was not itself text-readable) even though fetch_status is "partial" (substantial, well-corroborated substitute content was obtained). Relevance is kept at the provisional "Medium": the content is topically on point (satellite HAB/cyanobacteria proxy methodology, parameter definitions, real multi-lake deployment) but is vendor marketing material without independently verifiable accuracy numbers, so it is best used as context on operational/commercial state-of-the-art rather than as a citable, defensible accuracy claim.
