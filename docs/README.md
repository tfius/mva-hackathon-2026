# docs

Survey of the LIGAND-AI programme, the data it publishes, and what of it runs on this machine.

| Document | Covers |
|---|---|
| [`ligand-ai-inventory.md`](ligand-ai-inventory.md) | ligand-ai.org and AIRCHECK — 22 DEL datasets, 92 E-ASMS screens, measured file sizes, column dictionary, access mechanics |
| [`folding-and-models.md`](folding-and-models.md) | AlphaFold 2/3/DB, open co-folding models, the NVIDIA BioNeMo stack, external datasets, storage planning |
| [`architecture.md`](architecture.md) | Design note — the nomination engine and its closed verification loop; what to build vs. what to consume |
| `ligand-ai-inventory.html` | Both of the above as one published page — [artifact](https://claude.ai/code/artifact/e572f6d0-952b-41b0-b513-8068851096b6) |

## Target machine

| | |
|---|---|
| GPU | 2 × NVIDIA RTX PRO 6000 Blackwell, 96 GB each (compute capability 12.0) |
| CPU | AMD Ryzen Threadripper 7960X, 24C / 48T |
| RAM | 123 GB |
| CUDA | 13.3 toolkit installed |
| Storage | 8T `folding-and-models.md` |

## The short version

- **ligand-ai.org hosts no data.** It is the IHI programme page (grant 101252959, Pfizer + SGC). Everything downloadable lives at [aircheck.ai](https://aircheck.ai).
- **~8 GB** gets you every open AIRCHECK DEL dataset. **~20 GB** gets three co-folding models running with no local MSA database.
- **AlphaFold 3 weights are request-gated**; AF2 and the AlphaFold DB are not. For protein-ligand work, Boltz-2 is the better starting point than either.
- The largest thing worth mirroring is **SAIR at 811 GB** — 5.2 M co-folded protein-ligand structures with experimental potency labels, CC BY 4.0.

Compiled 26 August 2026.
