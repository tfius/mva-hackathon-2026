# Folding, co-folding and the NVIDIA stack

What is downloadable for structure prediction and structure-based ligand work, and what it costs in disk.

Companion to [`ligand-ai-inventory.md`](ligand-ai-inventory.md).

---

## 1. "Download AlphaFold" is three different things

| Artifact | Terms | Access |
|---|---|---|
| **AlphaFold 2** | Apache-2.0 code, CC BY 4.0 weights | **Open**, no gate. Apo only — protein and complexes, no ligands |
| **AlphaFold 3** | CC-BY-NC-SA 4.0, code *and* parameters | **Request-gated.** Code is public at [google-deepmind/alphafold3](https://github.com/google-deepmind/alphafold3); weights are not downloadable. Form to DeepMind, academic affiliation required, non-commercial only, no redistribution, approval discretionary |
| **AlphaFold DB** | CC BY 4.0 | **Open.** 214 M predicted structures. Per-proteome tars on the EBI FTP; full mirror ~23 TiB at `gs://public-datasets-deepmind-alphafold-v4` |

For this programme the AlphaFold *database* matters more than the model. It already covers most of the 92 E-ASMS targets and will cover the incoming 2,000-protein set. Retrieval beats folding when someone has already folded it.

## 2. Co-folding is the relevant capability

WP7 is pose and hit prediction, which needs protein **and** ligand folded together. Every serious open co-folder ships weights with no request step.

| Model | Weights | Size | Why it matters here |
|---|---|---:|---|
| **Boltz-2** | `boltz-community/boltz-2` | 6.2 GB | MIT, `pip install boltz` (2.2.1). Joint structure **and binding affinity** — approaching FEP accuracy at ~1000× the speed. Start here. |
| OpenFold3 | `OpenFold/OpenFold3` | 12.6 GB | Fully open AF3 reproduction, four checkpoints. AF3 behaviour without the licence. |
| Chai-1 | `chaidiscovery/chai-1` | 1.2 GB | Lightest co-folder; good for high-throughput triage passes. |
| Protenix | ByteDance / community | varies | Another AF3 reproduction, several size variants including a mini. |
| ESMFold | `facebook/esmfold_v1` | — | Single-sequence, no MSA, seconds per protein. Apo only, useful for bulk sanity checks. |

Boltz-2 is the obvious start: it is the only one that outputs affinity, which plugs straight into DEL hit triage — score AIRCHECK's enriched compounds against the target structure and cross-check the `ENRICHMENT` column.

### Database footprint

AF3's genetic databases are 252 GB compressed, **630 GB uncompressed**, with ~1 TB recommended and SSD strongly preferred — MSA search is I/O-bound. AF2's `full_dbs` are larger still, dominated by BFD; `reduced_dbs` is far smaller if you do not need maximum accuracy. Boltz and Chai sidestep this entirely by defaulting to a remote MSA server, or can point at local ColabFold/MMseqs2 databases.

**Roughly 20 GB gets all three co-folders running with no local database at all.**

### Hardware fit

| | |
|---|---|
| Compute capability | Blackwell is 12.0; AF3's floor is 8.0 ✓ |
| CUDA | 13.3 toolkit already installed ✓ |
| VRAM | 96 GB/card vs. the A100-80GB the docs assume — noticeably larger complexes than published limits |
| RAM | 123 GB vs. 64 GB recommended for genetic search ✓ |

## 3. NVIDIA BioNeMo

Roughly twenty repos under [NVIDIA-BioNeMo](https://github.com/NVIDIA-BioNeMo), most updated within the past week. Several fill gaps this project would otherwise have to build.

| Model / library | What it does | Fit |
|---|---|---|
| **nvMolKit** | GPU-accelerated cheminformatics — molecular similarity, conformer generation, geometry optimisation | The sleeper hit. DEL-scale fingerprinting and similarity are the CPU bottleneck in every pipeline here |
| **nvDock** | All-atom diffusion docking for a *known* pocket | Pose prediction on targets with a solved or AFDB structure |
| **DiffDock** | Blind docking, no pocket definition needed. NVIDIA's NIM build is retrained on PLINDER + SAIR — 1 M complexes, 5.2 M structures | Upstream is MIT ([gcorso/DiffDock](https://github.com/gcorso/DiffDock)); the retrained NIM is stronger |
| **DualBind** | 3D structure-based binding affinity, dual-loss framework | Second opinion against Boltz-2's affinity head |
| **GenMol** | Masked discrete diffusion, fragment-based generation with scaffold/motif retention. Supersedes MolMIM | Hit expansion — hold the DEL warhead, vary the rest. `nvidia/NV-GenMol-89M-v2`, 1.4 GB |
| **ReaSyn** | Predicts a molecule's synthesis pathway from building blocks. Apache-2.0 | Maps onto WP4 hit expansion — filters generated compounds to ones that can be made |
| **La-Proteina / Proteina / Proteina-Complexa** | Flow-based generative protein design; Complexa does binder design against protein **and small-molecule** targets | `nvidia/NV-La-Proteina-Ucond-v1` 17.1 GB, `-Motif-v1` 15.8 GB |
| **boltz-cp** | Context parallelism for Boltz-2 | Splits a single prediction across both cards — the direct answer to having two GPUs |
| **KERMT** | Pretrained GNN for molecular property prediction. Apache-2.0 | ADMET-style filtering on generated compounds |
| **cuik-molmaker** | Fast molecular featurization | Feeds the GNNs above |
| **megalodon / avgflow** | Conformer generation (SO(3)-averaged flow matching, ICML 2025) | Conformer ensembles ahead of docking |
| **ESM-2 mirrors** | `nvidia/esm2_*`, 8 M → 15 B parameters, MIT | 15 B checkpoint is 121 GB — fits, but 3 B (22.7 GB) is the practical choice |
| RNAPro · CodonFM · JEPA-DNA | RNA 3D folding, codon-resolution LMs, genomic foundation model | Out of scope, worth knowing they exist |

### The blueprint that matters

NVIDIA publishes a [generative virtual screening blueprint](https://github.com/NVIDIA-BioNeMo-blueprints/generative-virtual-screening) chaining **GenMol → DiffDock → Boltz-2**: generate candidates, dock them, score binding affinity. That is a complete hit-expansion loop and exactly the shape of WP4. Swap in a DEL-derived starting scaffold and the AIRCHECK `ENRICHMENT` column becomes ground truth for calibrating it.

> **Licensing.** Terms vary per repo and are not uniform. ReaSyn, KERMT and RNAPro are Apache-2.0; the ESM-2 mirrors are MIT; several others — Proteina, DualBind, nvDock, boltz-cp — carry non-standard or unstated licences on GitHub. Check the per-repo `LICENSE` and the model card before anything leaves research use. NIM containers are a separate distribution channel and need an NGC account and API key.

## 4. External datasets worth mirroring

| Dataset | Contents | Licence | Size |
|---|---|---|---:|
| **SAIR** (SandboxAQ) | 1,048,857 unique protein-ligand pairs, 5.2 M 3D structures, co-folded with Boltz-1x, labelled with ChEMBL/BindingDB potency | CC BY 4.0, commercial OK | **811 GB** |
| **PLINDER** | PDB-derived protein-ligand interaction dataset with published splits | Open | varies |
| **KinDEL** (insitro) | 81 M DEL compounds with docking poses for MAPK14 and DDR1 | Open | large |
| MMELON (IBM) | Multi-view molecular foundation model, graph + image + text, up to 200 M molecules | — | — |
| MPDF | Multimodal pretraining DEL-fusion for denoising non-specific DEL interactions | — | — |

SAIR is the single largest item in either document and the most directly useful: it is the closest thing to labelled ground truth at scale for affinity fine-tuning.

## 5. Storage planning

| Candidate | Footprint | Worth it? |
|---|---:|---|
| All open AIRCHECK DEL parquet | ~8 GB | Yes — mirror everything, it's noise-level |
| DELBERT corpus + 4 checkpoints | 7.9 GB | Yes |
| Boltz-2 + Chai-1 + OpenFold3 | 20 GB | Yes — all three, no local MSA database needed |
| GenMol + La-Proteina + ESM-2 3B | 57 GB | Yes if running the generative loop |
| AF3 genetic databases | 630 GB | Only if committing to AF3 with local MSA search. **SSD.** |
| SAIR | 811 GB | Yes for affinity fine-tuning |
| AlphaFold DB, full mirror | 23 TiB | No. Pull per-proteome tars instead |

SSD matters for the AF3 databases (MSA search is I/O-bound) and for materialized training shards. Everything else is fine on spinning disk.

Suggested layout with the new disks: one volume for immutable raw mirrors (AIRCHECK parquet, HuggingFace cache, SAIR — ~900 GB with headroom for the 2,000-protein E-ASMS release), a separate fast SSD volume for materialized training shards, MSA databases and MLflow artifacts. The second is where real growth happens.

## 6. Where this joins the main plan

Continuing the run sequence from [`ligand-ai-inventory.md`](ligand-ai-inventory.md):

7. **Add structure to the fingerprint models.** Retrieve AFDB structures for the DEL targets, co-fold the top-enriched compounds with Boltz-2, check whether its affinity head agrees with measured `ENRICHMENT`. That correlation gates everything structure-based downstream.
8. **Close the generative loop.** GenMol → nvDock/DiffDock → Boltz-2 on a confirmed DEL hit, filtered through ReaSyn for synthesizability. A WP4 hit-expansion pipeline running end to end locally.
9. **Test generalization externally.** Score against KinDEL (MAPK14, DDR1), fine-tune the Boltz-2 affinity head on SAIR, register for the Target 2035 PGK2 challenge.

## Sources

- [AlphaFold 3 weights terms of use](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md) · [AF3 installation and database setup](https://github.com/google-deepmind/alphafold3/blob/main/docs/installation.md)
- [Nature: AI protein-prediction tool AlphaFold3 is now more open](https://www.nature.com/articles/d41586-024-03708-4)
- [AlphaFold Protein Structure Database in 2024](https://academic.oup.com/nar/article/52/D1/D368/7337620) — *Nucleic Acids Research*
- [Boltz-2](https://boltz.bio/boltz2) · [MIT + Recursion release announcement](https://ir.recursion.com/news-releases/news-release-details/mit-and-recursion-release-boltz-2-next-generation-ai-model)
- [NVIDIA-BioNeMo on GitHub](https://github.com/NVIDIA-BioNeMo) · [generative virtual screening blueprint](https://github.com/NVIDIA-BioNeMo-blueprints/generative-virtual-screening)
- [SAIR on HuggingFace](https://huggingface.co/datasets/SandboxAQ/SAIR) · [SandboxAQ announcement](https://www.sandboxaq.com/press/sandboxaq-unveils-sair-structurally-augmented-ic50-repository-a-novel-open-dataset-of-protein-ligand-structures-labelled-by-binding-affinities)

---

Model sizes and licences were read from the HuggingFace and GitHub APIs on 26 August 2026; database figures are from the projects' own documentation.
