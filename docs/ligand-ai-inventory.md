# LIGAND-AI data inventory

What the IHI LIGAND-AI programme publishes today, what is downloadable without an account, and what runs locally.

**Counts:** 22 DEL datasets · 92 E-ASMS screens · 15 open with no login · ~6 GB of DEL parquet measured · 6.8 GB DELBERT corpus · 4 pretrained checkpoints.

---

## 1. The site is a programme page, not a data portal

Nothing is downloadable from ligand-ai.org itself. Every asset it describes is hosted elsewhere.

LIGAND-AI is an Innovative Health Initiative project (grant 101252959) led by Pfizer and the Structural Genomics Consortium, with partners across nine countries. The public site is a React SPA with seven content routes — `/about`, `/work-packages`, `/partners`, `/resources`, `/protocol`, `/news`, `/contact`. The news feed is empty ("check back soon"); `/resources` is a link board pointing outward.

Programme scope, which tells you what lands over the next few years:

- Ligandability data for **2,000 purified human proteins** by Enantioselective Affinity Selection Mass Spectrometry
- At least 200 newly purified proteins, 500 community-contributed targets
- Two open-source DNA-encoded libraries
- Open benchmarking with CASP, CACHE and DREAM
- All of it committed to release in "AI-ready formats" via AIRCHECK

So the practical question resolves entirely into AIRCHECK plus the code repos around it.

## 2. Where the assets live

| Resource | What it holds | Access |
|---|---|---|
| [aircheck.ai](https://aircheck.ai) | DEL + E-ASMS datasets, trained models, challenge data. **The only bulk data here.** | Mostly open |
| [MAINFRAME](https://aircheck.ai/mainframe) | International ML / cheminformatics network behind the modelling | Community |
| [BEACON](https://conscience.ca/beacon/) | Conscience benchmarking consortium; runs CACHE challenges with wet-lab validation | Challenges |
| [PCN](https://www.thesgc.org/ProteinContributionNetwork) | Submit purified protein, get it screened, receive validated hits back | Contribute |
| [SGC protocols](https://public.thesgc.org/protocol/) | Expression and purification protocols for LIGAND-AI proteins | Open |
| [Target 2035](https://www.target2035.net/) | Parent mission; runs the PGK2 DEL-ML challenge | Community |

## 3. DEL datasets — 22 total, 15 open

Sizes measured directly against the signed-URL service, not estimated. Every open file is a single parquet.

| Target / screen | Partner | Selection | Size | Access |
|---|---|---|---:|---|
| WDR91 | HitGen | 2023-08-28 | 0.91 GB | Open |
| WDR12 | HitGen | 2023-08-28 | 0.33 GB | Open |
| SETDB1 | HitGen | 2023-08-28 | 0.98 GB | Open |
| LRRK2 | HitGen | 2023-08-28 | — | API 500 |
| DCAF7 | HitGen | 2025-03-31 | 0.94 GB | Open |
| Chicken PLCZ1 | HitGen | 2025-03-31 | 0.94 GB | Open |
| Chicken PLCZ1 · vs. known inhibitor | HitGen | 2024-03-31 | 0.63 GB | Open |
| Human PLCZ1 D202R / H170A+H215A | HitGen | 2025-03-31 | 0.13 GB | Open |
| Human PLCZ1 mut · vs. known inhibitor | HitGen | 2025-03-31 | 0.10 GB | Open |
| PLCZ1 chicken-or-human combined | HitGen | 2025-03-31 | — | API 500 |
| PLCZ1 off-target His-PLCD1;2:756 | HitGen | 2025-03-31 | 0.88 GB | Open |
| Nsp2 full-length | UNC | 2024-10-07 | web | Open |
| Nsp2 full-length · vs. known inhibitor | UNC | 2024-10-07 | web | Open |
| Nsp2 protease domain | UNC | 2024-10-07 | web | Open |
| Nsp2 protease domain · vs. known inhibitor | UNC | 2024-10-07 | web | Open |
| SETDB1 | X-Chem | 2023-10-20 | — | Login |
| WDR91 | X-Chem | 2023-10-20 | — | Login |
| RFWD3 | X-Chem | 2023-10-20 | — | Login |
| DNMT3A | X-Chem | 2023-10-20 | — | Login |
| DCAF1 | X-Chem | 2023-10-20 | — | Login |
| AAMP | X-Chem | 2023-10-20 | — | Login |
| THEMIS | X-Chem | TBD | — | Login |

"web" = downloadable from the AIRCHECK datasets page but not exposed through the `aircheckdata` package, which currently indexes HitGen only. The two `API 500` rows resolve in the package's dataset list but the signed-URL service returns 500 — retry, or take those two from the web download button.

Nine measured files total **5.84 GB**. With LRRK2 and the combined PLCZ1 screen, budget ~8 GB for the complete open HitGen set.

Note the experimental design in the PLCZ1 family: paired screens with and without a competing known inhibitor, plus a deliberate off-target counter-screen against PLCD1. That is a ready-made selectivity benchmark, not just five more targets.

## 4. E-ASMS — 92 screens, all open

Every E-ASMS dataset is SGC-contributed with a download button and no login. Names encode `GENE_UNIPROT_start_end`, so construct boundaries are in the identifier.

```
PLCG1_P19174_1_1290          DNMT3A_Q9Y6K1_278_427       PIAS1_O75925_124_490
LRRK2_Q5S007_2141_2527       BIRC3_Q13489_26_103         NSP3Macro_Sars2_206_374
TP53_P04637_94_294           KLHL3_Q9UH77_298_587        LRRK2_Q5S007_1327_1838
FBXW7_Q969H0_349_707         KLHL40_Q2TBA0_313_621       FLN5_NA_NA_NA
PLCZ1_Q86YW0_2_608           HTTQ54_P42858_1-3175        SKP1_P63208_1_163
NEIL3_Q8TAT5_1_301           KHSRP_Q92945_234_497        COPB2_P35606_1_300
WDR48_Q8TAF3_5_677           DDB1_Q16531_1_1140          HUWE1_Q7Z6Z7_1611_1700
ChickV_NSP2_536-1333         PGAM5_Q96HS1_90_289         SLC9C2_Q5TAH2_856_1090
TRIM37_O94972_267_407        AASS_Q9UDR5_455_926         Rab40C_Q96S21_10-224
PATL2_C9JE40_288_543         SEC31A_O94979_1_338         WDR55_Q9H6Y2_21_334
HERC2_O95714_2959_3326       PB2_Q0A2G6_318_483          CORO1A_P31146_1_461
rep_P0DTD1_6453_6798         NEIL2_Q969S2_1_332          USP37_Q86T82_1_979
BRD1A_O95696_555_688         FBX022_Q8NEZ5_13-403        INPP5D_Q92835_2_858
STUB1_Q9UNE7_1_303           TOPBP1_Q92547_1264_1493     HERC2_O95714_3951_4321
WIPI2_Q9Y4P8_13_380          ChikV_NSP2_993-1333         KLHL2_O95198_294_593
TRIM58_Q8NG06_250_466        ChikVNSP3_M9VZ69_1334_1493  DCAF1_Q9Y4B6_1039_1401
DCAF7_P61962_1_342           ZER1_Q7Z7L7_518_766         RFWD3_Q6PCD5_425_774
MAGEA3_P43357_104_294        ASH1L_Q9NR48_2051_2335      DDX1_Q92499_1_740
WDR20_Q8TBZ3_1_569           NOVA1_P51513_49_246         BICC1_Q9H694_47_425
GFP_P44212_1-238             TRIM39_Q9HCM9_323_518       TRIM28_Q13263_619_811
PLCZ1_Q2VRL0_1_637           WDR91_A4D1P6_392_747        THEMIS_Q8N1K5_267_562
DHX58_Q96C10_1_678           SLC9C1_Q4G0N8_859_1013      ABHD14B_Q96IU4_1_210
TBXT_O15178_41_226           KLHL7_Q8IXQ5_290_586        rep_P0DTD1_5325_5925
HERC2_O95714_371_736         SPSB2_Q99619_26_219         TRIM36_Q9NQ86_507_728
TBL1XR1_Q9BZK7_1_514         DUSP29_Q68J44_1_220         YTHDC1_Q96MU7_345_509
TLE4_Q04727_474_773          YTHDF2_Q9Y5A9_408_550       PLCD1_P51178_2_756
AASS_Q9UDR5_23_476           IFIH1_Q9BYX4_306_1025       HAT1_O14929_20_341
HRAS_NA_NA_NA                FAN1_Q9Y2M0_373_1017        MSH6_P52701_89_203
MBPcontrol_NA_NA_NA          ascc3_E1BNG3_400_2201       DENV2_NSP5_1-901
SETDB1_Q15047_197_403        PBK_Q96KB5_1_322            BCAT1_P54687_1_386
TRIM24_O15164_824_1006       PLCG2_P16885_1_1195
```

Structure hiding in that list:

- **GFP and MBP are negative controls** — free non-specific-binder baselines
- **HERC2 appears three times**; LRRK2, AASS and rep (SARS-CoV-2 replicase) twice — different constructs, so within-protein domain comparisons come free
- Seven targets (DNMT3A, LRRK2, DCAF1, DCAF7, RFWD3, SETDB1, THEMIS, WDR91, PLCZ1/PLCD1) overlap with the DEL side — the cross-modality pairs worth building on

## 5. Target 2035 PGK2 challenge data

A separate tab hosts benchmark-shaped data with train/test splits already defined. All three require an account (Baylor College of Medicine as provider):

- `PGK2` — target screen against the BCM OpenDEL screening libraries
- `PGK2_CACHE_Val_Test_Set` — validation and test split for the challenge
- `OpenDEL_libraries` — building-block IDs and SMILES for all 12 OpenDEL libraries

This is the one part of AIRCHECK with a published evaluation protocol and gold labels, so it is where you calibrate against other people's numbers. [Target2035_Aircheck_Utils](https://github.com/StructuralGenomicsConsortium/Target2035_Aircheck_Utils) ships fingerprint extraction, parquet readers, a training notebook and the evaluation scripts.

## 6. Models and code that run locally

### DELBERT — the strongest published baseline

A self-supervised transformer treating molecular fingerprints as a discrete token language, masked-LM pretrained. Designed for exactly AIRCHECK's constraint: screening data released as precomputed fingerprints without structures. ICLR 2026 MLGenX workshop; reported 1.6–2.7× improvement in early-enrichment metrics over XGBoost and LightGBM ensembles on three of four targets under library-based OOD evaluation.

| Artifact | Repo | Size |
|---|---|---:|
| Code | [bowang-lab/DELBERT](https://github.com/bowang-lab/DELBERT) | — |
| Tokenized corpus (WDR12/91, LRRK2, SETDB1, DCAF7) | [wanglab/delbert_data](https://huggingface.co/datasets/wanglab/delbert_data) | 6.77 GB |
| Finetuned · WDR91 | `wanglab/delbert-wdr91` | 284 MB |
| Finetuned · LRRK2 | `wanglab/delbert-lrrk2` | 284 MB |
| Finetuned · SETDB1 | `wanglab/delbert-setdb1` | 284 MB |
| Finetuned · DCAF7 | `wanglab/delbert-dcaf7` | 284 MB |

Inference takes raw AIRCHECK parquet directly — the dense FP columns `ECFP4`, `FCFP6`, `ATOMPAIR`, `TOPTOR` are the model's expected input, so no conversion sits between download and prediction.

### AIRCHECK's own pipelines

| Repo | What it does | Local? |
|---|---|---|
| [AIRCHECK-DEL-ML](https://github.com/StructuralGenomicsConsortium/AIRCHECK-DEL-ML) | Containerized end-to-end DEL screening pipeline — Docker, MLflow, LightGBM/scikit-learn, RDKit, FastAPI serving | Yes — documented fully-local mode; GCP optional |
| [AIRCHECK-data-package](https://github.com/StructuralGenomicsConsortium/AIRCHECK-data-package) | `aircheckdata` — loader with column selection and caching | Yes |
| [Target2035_Aircheck_Utils](https://github.com/StructuralGenomicsConsortium/Target2035_Aircheck_Utils) | Fingerprint extraction, parquet→NumPy, training notebook, eval metrics | Yes |
| [AIRCHECK-negative_sampler](https://github.com/StructuralGenomicsConsortium/AIRCHECK-negative_sampler) | Negative sampling for DEL training sets | Yes |
| [EASMS-data-processing](https://github.com/StructuralGenomicsConsortium/EASMS-data-processing) | E-ASMS processing scripts | Yes |

The models AIRCHECK hosts on its own site are two LightGBM classifiers, `DEL-WDR91` and `DEL-LRRK2`, each with linked experiment results, a prediction view and source. Treat them as the floor to beat, not the state of the art.

## 7. Getting the data

Programmatic access needs no account for the HitGen sets. The package resolves a dataset name to a signed GCS URL through a public endpoint, then streams the parquet.

```bash
# verified working on this machine, Python 3.14, clean venv
pip install aircheckdata

# list what the package indexes (HitGen only, 11 datasets)
python -c "from aircheckdata import list_datasets; print(list_datasets())"

# inspect the schema before pulling a gigabyte
python -c "from aircheckdata import get_columns; print(get_columns('HitGen','WDR91'))"
```

```python
from aircheckdata import load_dataset

# pull only what the model needs — the FP columns are the bulk of the file
df = load_dataset(
    "HitGen", "WDR91",
    columns=["DEL_ID", "SMILES", "ECFP4", "FCFP6", "ATOMPAIR", "TOPTOR",
             "TARGET_VALUE", "NTC_VALUE", "ENRICHMENT", "LABEL"],
    show_progress=True,
)
```

Under the hood it POSTs `{"company_name": ..., "target": ...}` to a Cloud Run signed-URL service and reads the returned URL with PyArrow. That same endpoint gives a plain HTTPS URL you can hand to `curl` or `aria2c`, which is faster for bulk mirroring.

> **Licence.** The HitGen DEL data is covered by the [HitGen EULA](https://www.aircheck.ai/docs/HitGen.pdf). Read it before mirroring anything, and check its redistribution terms before any derived dataset leaves this machine. X-Chem and BCM data additionally require an AIRCHECK account.

E-ASMS datasets are downloaded from the web table rather than the package — the loader currently indexes DEL/HitGen only. 92 individual downloads is worth scripting against the same signed-URL service once you have the provider and target strings.

## 8. What is in a DEL parquet

22 columns. Structures are included for the HitGen sets — the fingerprints-only privacy mode DELBERT was designed around applies to other providers.

| Column | Meaning |
|---|---|
| `SMILES` | Structure of the enumerated DEL compound |
| `DEL_ID` | Unique ID of the fully enumerated DEL compound |
| `LIBRARY_ID` | Vendor and sub-library number |
| `BB1_ID` / `BB2_ID` / `BB3_ID` | Building-block IDs at each cycle — the split for library-based OOD evaluation |
| `TARGET_ID` | Protein target identifier |
| `TARGET_VALUE` | Raw sequence count in the target selection |
| `NTC_VALUE` | Raw count in the no-target control selection |
| `ENRICHMENT` | Ratio of target count to NTC count |
| `LABEL` | Binary enrichment label — 0 not enriched, 1 enriched |
| `MW` / `ALOGP` | Molecular weight (integer), calculated LogP (1 dp) |
| `ECFP4` / `ECFP6` | Extended-connectivity count fingerprints, radius 2 / 3, 2048 bits |
| `FCFP4` / `FCFP6` | Feature-connectivity fingerprints, 2048 bits |
| `ATOMPAIR` | Atom-pair fingerprint, 2048 bits |
| `TOPTOR` | Topological torsion, non-binary, 2048 bits |
| `MACCS` | 166-bit MACCS keys, binary |
| `RDK` | RDKit graph fingerprint, 2048 bits, max path 7, binary |
| `AVALON` | Avalon fingerprint, 2048 bits |

Not every dataset carries all nine fingerprint types; each download is marked with which are present.

> **The one real trap.** The parquet files are compressed sparse fingerprints. Materializing nine dense 2048-wide FP columns as int32 is roughly 70 KB per row — over a multi-million-row screen that expands from under a gigabyte on disk into the terabyte range. Always pass `columns=`, and keep working sets as sparse arrays or memory-mapped shards. This is a working-set discipline, not a download-size problem.

## 9. Suggested first runs

1. **Reproduce a published number.** Pull WDR91 (0.91 GB) and `wanglab/delbert-wdr91`, run inference on raw parquet, confirm the early-enrichment metric against the paper. Validates licence, loader, schema and model input format before anything is trained.
2. **Establish the floor.** Train the LightGBM baseline via AIRCHECK-DEL-ML in fully-local mode on the same target and split.
3. **Train DELBERT from scratch.** Pretrain and finetune on the 6.77 GB corpus using library-based OOD splits on `BB*_ID`. One GPU per run, two concurrently.
4. **Exploit the paired screens.** The PLCZ1 family — with/without competing inhibitor, plus the PLCD1 counter-screen — supports selectivity modelling that single-target datasets cannot. Nothing published uses it yet.
5. **Cross the modalities.** Seven proteins have both DEL and E-ASMS screens. Whether DEL-trained models transfer to E-ASMS hit calling on the same protein is open with the data already in hand.
6. **Add structure.** See [`folding-and-models.md`](folding-and-models.md).

## Sources

Dataset counts, target lists and access states read directly from the AIRCHECK site; file sizes measured against the signed-URL service; package behaviour and column dictionary verified in a clean virtualenv on this machine.

- [ligand-ai.org](https://ligand-ai.org/) — programme site, work packages, resources
- [aircheck.ai/datasets](https://aircheck.ai/datasets) — DEL and E-ASMS catalogue
- [Enabling Open Machine Learning of DEL Selections](https://pubs.acs.org/doi/10.1021/acs.jmedchem.5c01972) — *J. Med. Chem.*
- [AIRCHECK: Powering AI-Driven Drug Discovery with Open Science](https://zenodo.org/records/15330172) — Zenodo
- [SGC Open Data](https://www.thesgc.org/open_data) · [IHI project factsheet](https://www.ihi.europa.eu/projects-results/project-factsheets/ligand-ai)

---

Compiled 26 August 2026. Two dataset endpoints were returning HTTP 500 at time of writing; the AIRCHECK site also carries a banner noting datasets are being re-benchmarked ahead of a release "later this year", so expect this catalogue to grow.
