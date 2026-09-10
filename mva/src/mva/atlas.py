"""Access to the AlphaGenome Atlas precomputed SNV releases.

The Atlas ships three bgzip+tabix TSVs keyed on (CHROM, POS, REF, ALT): the
variant-impact score (AVI, raw and PHRED), the merged splicing score, and the
SHAP feature attributions that decompose the AVI raw score into its inputs.

All three are **SNV-only** despite the "indels" in the feature-importance
filename; verified by scanning for multi-base REF/ALT and for a set
IS_INSERTION / IS_DELETION flag, which finds none. Indels need the
AlphaGenome API.

The AVI score is a linear ensemble whose features include AlphaMissense and
conservation as well as the AlphaGenome tracks, so it is **not independent** of
AlphaMissense for coding variants. `shap_decompose` exists to make that
dependence measurable rather than assumed - see `am_share`.
"""
from __future__ import annotations

import os
import subprocess
from typing import Iterable, Iterator

ATLAS_DIR = os.environ.get("ATLAS_DIR", "/mnt/data/AlphaGenome")
TABIX = os.environ.get(
    "TABIX", "/mnt/data/mva-hackathon-2026/mamba/envs/mva/bin/tabix")

FILES = {
    "avi": "alphagenome_variant_impact_score_snvs.tsv.gz",
    "splicing": "combined_alphagenome_splicing_snvs.tsv.gz",
    "shap": ("combined_ag_cond_linear_ensemble_20260417"
             "_feature_importance_indels_with_am_snvs.tsv.gz"),
}

COLUMNS = {
    "avi": ["raw_score", "PHRED"],
    "splicing": ["alphagenome_splicing"],
}

# SHAP feature order, as in the file header after CHROM/POS/REF/ALT.
SHAP_FEATURES = [
    "MERGED_SPLICING", "MAX_ABS_ATAC", "MAX_ABS_CONTACT_MAPS", "MAX_ABS_DNASE",
    "MAX_ABS_CHIP_TF", "MAX_ABS_CHIP_HISTONE", "MAX_ABS_CAGE", "MAX_ABS_PROCAP",
    "MAX_ABS_RNA_SEQ", "MAX_ABS_POLYADENYLATION", "ALPHAMISSENSE",
    "CACTUS_241_WAY", "PROTEIN_TERMINATION", "START_LOST", "STOP_LOST",
    "PHASTCONS_470_WAY", "IS_INSERTION", "IS_DELETION",
]
# Features that are somebody else's model or an annotation, not AlphaGenome's
# own sequence-to-function prediction.
BORROWED = ["ALPHAMISSENSE", "CACTUS_241_WAY", "PHASTCONS_470_WAY",
            "PROTEIN_TERMINATION", "START_LOST", "STOP_LOST"]
AG_TRACKS = [f for f in SHAP_FEATURES
             if f not in BORROWED and not f.startswith("IS_")]


def path(kind: str) -> str:
    return os.path.join(ATLAS_DIR, FILES[kind])


def _tabix(kind: str, args: list[str]) -> Iterator[list[str]]:
    proc = subprocess.Popen([TABIX] + args, stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        yield line.rstrip("\n").split("\t")
    proc.wait()
    if proc.returncode:
        raise RuntimeError(f"tabix failed on {kind}: {proc.returncode}")


def region(kind: str, chrom: str, start: int, end: int) -> Iterator[list[str]]:
    """Every Atlas row in a 1-based inclusive interval."""
    yield from _tabix(kind, [path(kind), f"{chrom}:{start}-{end}"])


def regions_from_bed(kind: str, bed: str) -> Iterator[list[str]]:
    yield from _tabix(kind, ["-R", bed, path(kind)])


def shap_decompose(fields: list[str]) -> dict[str, float]:
    """SHAP row -> feature name to contribution. Contributions sum to AVI raw."""
    return dict(zip(SHAP_FEATURES, (float(x) for x in fields[4:])))


def am_share(contrib: dict[str, float]) -> float:
    """Fraction of the AVI score that is AlphaMissense re-entering as a feature.

    A high value means the AVI score is not independent evidence alongside an
    AlphaMissense call - it is the same number wearing a different hat.
    """
    total = sum(abs(v) for v in contrib.values())
    return abs(contrib.get("ALPHAMISSENSE", 0.0)) / total if total else 0.0


def ag_share(contrib: dict[str, float]) -> float:
    """Fraction contributed by AlphaGenome's own regulatory/splicing tracks."""
    total = sum(abs(v) for v in contrib.values())
    return sum(abs(contrib[f]) for f in AG_TRACKS) / total if total else 0.0


def write_sites_bed(variants: Iterable[tuple[str, int]], path_out: str) -> str:
    """A BED of unique sites, sorted for tabix -R."""
    sites = sorted({(c, int(p)) for c, p in variants},
                   key=lambda cp: (cp[0], cp[1]))
    with open(path_out, "w") as fh:
        for c, p in sites:
            fh.write(f"{c}\t{p - 1}\t{p}\n")
    return path_out
