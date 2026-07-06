# Static feature significance vs HAB (per-lake, n=132)

Unit = LAKE (static features are per-lake; lake-week testing = pseudoreplication). Test = **Spearman**(feature, per-lake bloom prevalence) -- rank-based, so robust to the skewed, [0,1]-bounded prevalence. Every lake has ample weeks (min 414, median 521 valid weeks), so prevalence is well-estimated and unweighted Spearman is appropriate (weighting barely moves rho). **Inclusion screen = raw p<0.1** (permissive; select candidates, narrow to top-N later) -- NOT a significance claim. **q(BH)** = Benjamini-Hochberg FDR (honest multiple-comparison context; `*` = survives q<0.05). 

**Feature extent (BasinATLAS):** lakes are assigned to their **max-overlap L12 sub-basin**; attributes mix extents by design -- climate/soil/morphology use the **local sub-basin** (`_s*`), while land-use / anthropogenic **loading** proxies use the **upstream catchment** (`_u*`, the hydrologically correct extent for what reaches the lake). So this is a *containing-L12 + upstream-context* screen, not strictly local. `AUC_lakeweek` is a DESCRIPTIVE between-lake effect size (repeated-week; **<0.5 = inverse association**, per the rho sign) -- not a significance test. **True per-lake depth omitted** (needs HydroLAKES); `lkv_mc_usu` is a crude upstream-lake-volume morphology proxy, not lake depth.

| feature | meaning | n | Spearman rho | p | q(BH) | incl(p<.1) | FDR | AUC(desc) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `inu_pc_umn` | inundation % (min) | 133 | +0.351 | 0.0000 | 0.0011 | YES | * | 0.624 |
| `AREASQKM` | lake surface area | 133 | +0.226 | 0.0090 | 0.0682 | YES |  | 0.581 |
| `lka_pc_use` | lake area % (upstream) | 133 | +0.224 | 0.0097 | 0.0682 | YES |  | 0.644 |
| `cmi_ix_syr` | moisture index | 133 | -0.218 | 0.0117 | 0.0682 | YES |  | 0.374 |
| `ari_ix_sav` | aridity index | 133 | -0.215 | 0.0128 | 0.0682 | YES |  | 0.375 |
| `swc_pc_syr` | soil water % | 133 | -0.215 | 0.0130 | 0.0682 | YES |  | 0.377 |
| `pet_mm_syr` | PET (annual mm) | 133 | +0.206 | 0.0172 | 0.0682 | YES |  | 0.600 |
| `for_pc_use` | forest % (upstream) | 133 | -0.206 | 0.0176 | 0.0682 | YES |  | 0.379 |
| `pre_mm_syr` | precip (annual mm) | 133 | -0.204 | 0.0186 | 0.0682 | YES |  | 0.380 |
| `tmp_dc_syr` | air temp (annual, x10C) | 133 | +0.189 | 0.0290 | 0.0956 | YES |  | 0.597 |
| `snd_pc_uav` | sand % | 133 | -0.173 | 0.0459 | 0.1378 | YES |  | 0.415 |
| `hft_ix_u09` | human footprint 2009 | 133 | +0.170 | 0.0505 | 0.1390 | YES |  | 0.614 |
| `cly_pc_uav` | clay % | 133 | +0.157 | 0.0709 | 0.1800 | YES |  | 0.565 |
| `wet_pc_ug1` | wetland % | 133 | +0.142 | 0.1039 | 0.2449 |  |  | 0.616 |
| `slt_pc_uav` | silt % | 133 | +0.127 | 0.1441 | 0.2934 |  |  | 0.577 |
| `ire_pc_use` | irrigated % (upstream) | 133 | +0.126 | 0.1487 | 0.2934 |  |  | 0.540 |
| `ppd_pk_uav` | pop. density (upstream) | 133 | +0.125 | 0.1512 | 0.2934 |  |  | 0.587 |
| `gwt_cm_sav` | groundwater table depth | 133 | +0.099 | 0.2549 | 0.4309 |  |  | 0.554 |
| `urb_pc_use` | urban % (upstream) | 133 | +0.098 | 0.2634 | 0.4309 |  |  | 0.565 |
| `pop_ct_usu` | population (upstream) | 133 | +0.098 | 0.2635 | 0.4309 |  |  | 0.541 |
| `nli_ix_uav` | night lights | 133 | +0.095 | 0.2742 | 0.4309 |  |  | 0.584 |
| `gdp_ud_usu` | GDP (upstream) | 133 | +0.088 | 0.3153 | 0.4730 |  |  | 0.537 |
| `crp_pc_use` | cropland % (upstream) | 133 | +0.071 | 0.4139 | 0.5862 |  |  | 0.523 |
| `run_mm_syr` | runoff (mm) | 133 | +0.070 | 0.4263 | 0.5862 |  |  | 0.571 |
| `dor_pc_pva` | degree of regulation | 133 | +0.062 | 0.4786 | 0.6318 |  |  | 0.508 |
| `soc_th_uav` | soil organic C | 133 | -0.051 | 0.5619 | 0.7032 |  |  | 0.440 |
| `lkv_mc_usu` | upstream lake volume (depth proxy) | 133 | +0.049 | 0.5753 | 0.7032 |  |  | 0.528 |
| `kar_pc_use` | karst % (upstream) | 133 | +0.036 | 0.6808 | 0.7831 |  |  | 0.516 |
| `pst_pc_use` | pasture % (upstream) | 133 | -0.035 | 0.6882 | 0.7831 |  |  | 0.476 |
| `ero_kh_uav` | soil erosion | 133 | +0.024 | 0.7882 | 0.8670 |  |  | 0.532 |
| `ele_mt_uav` | elevation (m, upstream) | 133 | +0.008 | 0.9251 | 0.9824 |  |  | 0.541 |
| `ria_ha_usu` | river area (ha, upstream) | 133 | +0.004 | 0.9655 | 0.9824 |  |  | 0.461 |
| `slp_dg_uav` | slope (deg, upstream) | 133 | +0.002 | 0.9824 | 0.9824 |  |  | 0.529 |

**13 of 33 static features pass the p<0.1 inclusion screen** (candidate set for modeling); **1 survive FDR q<0.05**. Area (`AREASQKM`): rho=+0.226, p=0.0090 -> included; q=0.068 (does not survive FDR).