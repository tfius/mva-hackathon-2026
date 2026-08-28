# Architecture: a nomination engine with a closed verification loop

Design note. Companion to [`ligand-ai-inventory.md`](ligand-ai-inventory.md) and [`folding-and-models.md`](folding-and-models.md).

**Thesis.** The valuable, unbuilt piece is not the prediction pipeline — those components are downloaded and working. It is *deciding which protein to work on*, coupled to a loop that can prove the decision wrong.

---

## 1. Why this is buildable

The feedback edge already exists physically, owned by other people:

- **SGC Protein Contribution Network** accepts a purified protein, screens it for small-molecule binders, returns validated hits
- **AIRCHECK** publishes the resulting data openly
- **LIGAND-AI** commits to 2,000 proteins over the programme, and is currently *crowdsourcing* which ones

So the wet lab, the screening capacity and the publication channel are all provided. What is missing is the prior — which protein, and why — and the bookkeeping that turns a guess into a measurement.

That gap is the product.

## 2. The loop

```
   BRENDA / Rhea / UniProt                    AFDB pocket geometry
   pathway position, essentiality,            + AIRCHECK hit/no-hit history
   disease link, chokepoint
            │ CONSEQUENCE                              │ LIGANDABILITY
            └──────────────┬───────────────────────────┘
                           ▼
                     NOMINATE  ──► pre-registered call, timestamped,
                           │        written before the answer exists
                           ▼
       PREDICT   DELBERT rank │ GenMol→ReaSyn │ nvDock/DiffDock │ Boltz-2
                           │
        ┌──────────────────┼──────────────────┬─────────────────┐
        ▼                  ▼                  ▼                 ▼
   retrospective       SAIR / PGK2        literature      PCN SUBMISSION
   held-out target     gold labels                        (physical)
   ~hours              ~weeks                             ~months
                                                               │
                                                    E-ASMS / DEL screen
                                                               │
                                              AIRCHECK publishes it ──┐
                           ◄───────────────────────────────────────────┘
                              new ligandability labels, incl. negatives
```

## 3. Nomination = ligandability × consequence

Neither axis alone is sufficient. Scoring on ligandability alone reproduces the field's existing bias toward kinases — highly ligandable, heavily crowded, low marginal value. Scoring on consequence alone nominates proteins that cannot be drugged.

### Consequence — from the enzyme/pathway side

| Source | Terms | Use |
|---|---|---|
| **BRENDA** | **CC BY 4.0**, free download after accepting licence. 112,288 enzymes, 15,335 organisms, 5.8 M data points, 278,840 ligands | Enzyme function, kinetics, known substrate/inhibitor ligands |
| **Rhea** (EBI) | Open | Reaction-level network; the open substitute for KEGG |
| **UniProt** | CC BY 4.0 | Sequence, annotation, disease association — the join key for everything |
| **ChEBI** | Open | Ligand ontology |
| ~~KEGG~~ | REST API free **academic only**, 3 req/s; **bulk FTP is a paid subscription**, commercial needs a licence from Pathway Solutions | **Do not architect on bulk KEGG.** Lookups only, if at all |

Signals: pathway chokepoint position, essentiality, disease linkage, degree in the reaction network, whether the family already has chemical tools.

### Ligandability — measurable, not just estimated

Everyone else estimates this. Here it can be read off experiments:

- **92 E-ASMS screens** and **22 DEL screens** in AIRCHECK are ligandability experiments with published outcomes
- **AFDB** supplies structure for pocket detection on essentially every candidate
- Pocket geometry + screen outcome is a supervised problem with real labels

### The negatives nobody uses

Screens that returned nothing. DEL runs with no enrichment. `GFP_P44212_1-238` and `MBPcontrol_NA_NA_NA` sitting in the E-ASMS list as deliberate non-binders.

Published ligandability models train on positives plus *assumed* negatives — usually "not yet found" treated as "cannot bind". This project has genuine experimental negatives, and gains more with every AIRCHECK release. That is the strongest single reason a nomination model built here would outperform what exists, and it costs nothing extra to exploit.

## 4. Pre-registration is what makes it a system

**Every nomination is logged before the screen runs.** Append-only, timestamped, containing the ranked call, the predicted binders, and a stated confidence.

Without it the project degenerates into retrospective scoring: the model looks excellent on data it has already seen and transfers to nothing. With it, every AIRCHECK release is an automatic, unarguable grading event.

It is a `jsonl` file. It is also the difference between a demo and a measurement instrument.

```jsonl
{"ts":"2026-08-26T19:00:00Z","protein":"UniProt:Q9H6Y2","construct":"21-334",
 "rank":3,"p_ligandable":0.71,"basis":["afdb_pocket","rhea_chokepoint","brenda_family"],
 "predicted_binders":["DEL_ID:...","DEL_ID:..."],"model":"nom-v0.1","screen_status":"pending"}
```

## 5. Verification at three timescales

| Loop | Latency | Question it answers | Can it refute you? |
|---|---|---|---|
| **Retrospective** | hours | Hold out an AIRCHECK target — does the nominator rank it correctly, does the pipeline recover its known binders? | Weakly — same data distribution |
| **Prospective in-silico** | weeks | Do calls hold against SAIR, PGK2 gold labels, published literature? | Partly |
| **Physical** | months | Submit to PCN. Does the screen find binders? | **Yes. This is the real one** |

Only the third can genuinely falsify a nomination. The first two exist to avoid wasting the third.

## 6. What actually gets built

Three components. The pipeline is downloaded, the wet lab belongs to SGC.

1. **Scorer** — joins BRENDA/Rhea/UniProt → AFDB pockets → AIRCHECK screen outcomes; emits a ranked protein list with a ligandability probability and a consequence score
2. **Registry** — append-only nomination log, written before any screen
3. **Grader** — replays the registry against each new AIRCHECK release; reports calibration, hit rate, and drift

The prediction stack (DELBERT, GenMol, ReaSyn, nvDock/DiffDock, Boltz-2) is consumed as-is. See [`folding-and-models.md`](folding-and-models.md).

## 7. Open decision

**Domain**: human drug targets (LIGAND-AI's shape — kinases, E3 ligases, readers, the dark proteome) or enzymes and biocatalysis (BRENDA's shape).

This changes the *weights* in the scorer and who consumes the output. It does not change the architecture, the loop, or any component choice. Not blocking — resolve it when the scorer needs tuning.

## 8. Second-order opportunity

BRENDA's 278,840 ligands carry measured Km/kcat against specific enzymes. That is an affinity-label source with entirely different physics from DEL enrichment counts.

Training or validating a single model across both — binding enrichment *and* enzyme kinetics — is not something the published work attempts. Worth a look once the primary loop runs.

---

Compiled 26 August 2026.
