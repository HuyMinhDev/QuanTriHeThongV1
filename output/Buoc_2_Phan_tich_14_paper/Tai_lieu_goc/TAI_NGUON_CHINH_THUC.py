"""Download original PDFs/repos when run on a computer with Internet access.

Default: list only. Explicitly pass --download to fetch. Does not install or
execute third-party code; never overwrites an existing paper or repository.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent
SOURCES = json.loads((BASE / "danh_muc_nguon.json").read_text())
PDFS = {
    1: "https://arxiv.org/pdf/2605.01524",
    2: "https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content",
    3: "https://dl.acm.org/doi/pdf/10.1145/3790097",
    4: "https://dl.acm.org/doi/pdf/10.1145/3765624",
    5: "https://arxiv.org/pdf/2510.22681",
    6: "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0341419&type=printable",
    7: "https://arxiv.org/pdf/2512.20896",
    8: "https://arxiv.org/pdf/2401.11506v2",
    9: "https://dl.acm.org/doi/pdf/10.1145/3705328.3748087",
    10: "https://arxiv.org/pdf/2504.14991",
    11: "https://www.hse.ru/data/2025/07/04/1995597406/%D0%90%D0%BD%D0%B0%D0%BD%D1%8C%D0%B5%D0%B2%D0%B0_%D1%81%D1%82%D0%B0%D1%82%D1%8C%D1%8F%2012.pdf",
    12: "https://pure.uva.nl/ws/files/304772377/3726302.3730280.pdf",
    13: "https://arxiv.org/pdf/2502.11921",
    14: "https://proceedings.iclr.cc/paper_files/paper/2025/file/184a03a3ad07e8897c62461c02634b02-Paper-Conference.pdf",
}


def download_pdf(url, target):
    if target.exists():
        return "already exists; retained"
    temporary = target.with_suffix(".part")
    try:
        request = Request(url, headers={"User-Agent": "Academic-source-downloader/1.0"})
        with urlopen(request, timeout=60) as response, temporary.open("wb") as f:
            total = 0
            while chunk := response.read(1024*1024):
                total += len(chunk)
                if total > 200*1024*1024:
                    raise ValueError("Response exceeds 200 MB; use the publisher link manually")
                f.write(chunk)
        with temporary.open("rb") as f:
            if not f.read(5).startswith(b"%PDF"):
                raise ValueError("Response is not a PDF; use author/publisher access")
        temporary.rename(target)
        return "downloaded"
    finally:
        if temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="fetch PDFs and shallow-clone official repositories")
    parser.add_argument("--paper", type=int, choices=range(1, 15), help="only one paper ID; default all 14")
    args = parser.parse_args()
    selected = [s for s in SOURCES if args.paper is None or s["id"] == args.paper]
    if not args.download:
        for s in selected:
            print(f"{s['id']:02d}. {s['title']}\n  PDF: {PDFS[s['id']]}\n  CODE: {s['code']}")
        print("List only; add --download to fetch. Existing files are retained.")
        return
    pdfdir, repodir = BASE / "Tai_lieu_goc" / "PDF", BASE / "Ma_nguon_day_du"
    pdfdir.mkdir(exist_ok=True)
    repodir.mkdir(exist_ok=True)
    results = []
    for s in selected:
        record = {"id":s["id"], "paper_url":PDFS[s["id"]], "repo_url":s["code"]}
        try:
            record["pdf"] = download_pdf(PDFS[s["id"]], pdfdir / f"{s['id']:02d}.pdf")
        except Exception as exc:
            record["pdf"] = f"not downloaded: {type(exc).__name__}: {exc}"
        destination = repodir / f"{s['id']:02d}"
        if destination.exists():
            record["code"] = "already exists; retained"
        elif not shutil.which("git"):
            record["code"] = "git unavailable; use official repository download"
        else:
            try:
                result = subprocess.run(["git", "clone", "--depth", "1", s["code"], str(destination)],
                                        capture_output=True, text=True, timeout=300)
                record["code"] = "cloned" if result.returncode == 0 else "not cloned: "+result.stderr[-600:]
                if result.returncode == 0:
                    record["commit"] = subprocess.check_output(
                        ["git", "-C", str(destination), "rev-parse", "HEAD"], text=True).strip()
            except Exception as exc:
                record["code"] = f"not cloned: {type(exc).__name__}: {exc}"
        results.append(record)
        print(json.dumps(record, ensure_ascii=False))
    (BASE / "Tai_lieu_goc" / "ket_qua_tai.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
