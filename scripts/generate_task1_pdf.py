"""Generate Task1_Selection_and_Research.pdf — academic document format."""
from __future__ import annotations
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ── Output path ──────────────────────────────────────────────────────────────
OUT = Path(__file__).resolve().parents[2] / "NTULearn_Submission_Clean" / "Task1_Selection_and_Research.pdf"

# ── Layout constants ─────────────────────────────────────────────────────────
L, R = 0.11, 0.89          # left / right margin (normalised figure coords)
TOP, BOT = 0.930, 0.072    # top / bottom of content area
LH = 0.0215                # body line height
LH_S = 0.024               # section heading line height
FS_DOC = 14                # document title font size
FS_SEC = 11                # section heading font size
FS_BOD = 10.2              # body text font size
FS_FTR = 8.5               # footer font size
WRAP = 90                  # characters per line (body)
WRAP_REF = 82              # chars for reference URLs (smaller)

C_DARK = "#111827"
C_BODY = "#374151"
C_URL  = "#1d4ed8"
C_FTR  = "#9ca3af"
AUTHOR = "Huang Sining | G2505429H | SINING001@e.ntu.edu.sg"


# ── Renderer ─────────────────────────────────────────────────────────────────
class Doc:
    def __init__(self, path):
        self._pdf   = PdfPages(path)
        self._fig   = None
        self._ax    = None
        self._y     = TOP
        self._pageno = 0
        self._first  = True

    # ── page management ───────────────────────────────────────────────────────
    def _new_page(self, flush=True):
        if self._fig and flush:
            self._footer()
            self._pdf.savefig(self._fig)
            plt.close(self._fig)
        self._fig = plt.figure(figsize=(8.27, 11.69))
        self._fig.patch.set_facecolor("white")
        self._ax  = self._fig.add_axes([0, 0, 1, 1])
        self._ax.axis("off")
        self._ax.set_xlim(0, 1)
        self._ax.set_ylim(0, 1)
        self._y = TOP
        self._pageno += 1

        if self._first:
            self._first = False
            self._ax.text(L, self._y, "Task 1: Selection and Research",
                          fontsize=FS_DOC, fontweight="bold", color=C_DARK, va="top")
            self._y -= LH_S + 0.004
            self._ax.plot([L, R], [self._y, self._y], color="#6b7280", lw=0.7)
            self._y -= 0.018

    def _footer(self):
        self._ax.text(L, BOT - 0.010,
                      f"Task 1 | {AUTHOR} | Page {self._pageno}",
                      fontsize=FS_FTR, color=C_FTR, va="bottom")

    def _need(self, lines: int, extra: float = 0.0) -> None:
        needed = lines * LH + extra + 0.006
        if self._y - needed < BOT:
            self._new_page()

    # ── public methods ────────────────────────────────────────────────────────
    def section(self, text: str):
        self._need(3, LH_S)
        self._ax.text(L, self._y, text, fontsize=FS_SEC, fontweight="bold",
                      color=C_DARK, va="top")
        self._y -= LH_S + 0.006

    def body(self, text: str, indent: float = 0.0):
        lines = textwrap.wrap(text, WRAP - int(indent * 70))
        self._need(len(lines))
        x = L + indent
        for ln in lines:
            self._ax.text(x, self._y, ln, fontsize=FS_BOD, color=C_BODY, va="top")
            self._y -= LH
        self._y -= 0.006

    def bullet(self, text: str):
        lines = textwrap.wrap(text, WRAP - 5)
        self._need(len(lines))
        self._ax.text(L + 0.012, self._y, "•", fontsize=FS_BOD, color=C_BODY, va="top")
        self._ax.text(L + 0.026, self._y, lines[0], fontsize=FS_BOD, color=C_BODY, va="top")
        self._y -= LH
        for ln in lines[1:]:
            self._ax.text(L + 0.026, self._y, ln, fontsize=FS_BOD, color=C_BODY, va="top")
            self._y -= LH
        self._y -= 0.003

    def ref(self, num: int, label: str, url: str):
        label_lines = textwrap.wrap(f"[{num}]  {label}", WRAP)
        url_lines   = textwrap.wrap(url, WRAP_REF)
        self._need(len(label_lines) + len(url_lines), 0.004)
        for ln in label_lines:
            self._ax.text(L, self._y, ln, fontsize=FS_BOD, color=C_BODY, va="top")
            self._y -= LH
        for ln in url_lines:
            self._ax.text(L + 0.030, self._y, ln, fontsize=9.6, color=C_URL, va="top")
            self._y -= LH * 0.96
        self._y -= 0.008

    def gap(self, size: float = 0.012):
        self._y -= size
        if self._y < BOT + 0.04:
            self._new_page()

    def close(self):
        self._footer()
        self._pdf.savefig(self._fig)
        plt.close(self._fig)
        self._pdf.close()


# ── Content ───────────────────────────────────────────────────────────────────
def build(doc: Doc):

    # ── Section 1 ─────────────────────────────────────────────────────────────
    doc.section("1.  Selected Entity: Lendable Ltd / Zable")
    doc.body(
        "The selected regulated entity is Lendable Ltd and its consumer-facing brand Zable. "
        "Lendable Ltd is incorporated in England and Wales and is authorised and regulated by "
        "the Financial Conduct Authority under Firm Reference Number 720261. Its corporate "
        "website at lendable.com explicitly describes operations in the United Kingdom and "
        "North American markets. In the United States, Zable operates a credit card and consumer "
        "loan product and publishes state licensing disclosures at zable.com/licenses, placing the "
        "entity under federal fair lending jurisdiction — specifically the Equal Credit Opportunity "
        "Act (ECOA) and Regulation B — as well as applicable state consumer credit statutes. This "
        "single entity is therefore simultaneously subject to US and non-US regulatory obligations, "
        "satisfying the assignment requirement."
    )

    # ── Section 2 ─────────────────────────────────────────────────────────────
    doc.section("2.  Selected Domain: AI Credit Scoring and Algorithmic Fairness")
    doc.body(
        "The chosen domain is AI-driven credit scoring and algorithmic fairness. Automated credit "
        "decisions affect access to borrowing, product pricing, and financial inclusion at scale. "
        "They also represent a textbook RegTech problem: the same underlying predictive model can "
        "be technically identical while being assessed under materially different legal and "
        "supervisory frameworks depending on the jurisdiction in which it is deployed. Lendable "
        "and Zable publicly emphasise automated underwriting and data-driven decision-making, "
        "making this domain directly relevant to the entity's real-world compliance obligations "
        "in both the United States and the United Kingdom."
    )

    # ── Section 3 ─────────────────────────────────────────────────────────────
    doc.section("3.  Rationale for Selection")
    doc.body(
        "Lendable / Zable is an appropriate choice because it operates the same AI-driven credit "
        "product in two jurisdictions with meaningfully different regulatory philosophies. A "
        "compliance officer at such an entity cannot apply a single checklist: the US requires "
        "specific adverse action reasons and fair lending outcome analysis, while the UK requires "
        "evidence of consumer outcome monitoring and board-level accountability under the FCA "
        "Consumer Duty. The entity is also appropriately sized for a hypothetical RegTech tool — "
        "a specialist AI-lending platform rather than a large global bank — making the compliance "
        "problem realistic and tractable without becoming intractable."
    )

    # ── Section 4 ─────────────────────────────────────────────────────────────
    doc.section("4.  Jurisdictional Comparison: United States and United Kingdom")
    doc.body(
        "In the United States, the core compliance logic for AI-driven credit decisions is "
        "anchored in the Equal Credit Opportunity Act (ECOA) and its implementing regulation, "
        "Regulation B. Lenders must not discriminate on the basis of protected characteristics, "
        "must provide specific and meaningful reasons for adverse credit actions, and must be "
        "able to defend the fairness of their model outcomes under regulatory examination. The "
        "Consumer Financial Protection Bureau (CFPB) is the primary federal enforcement authority "
        "for consumer credit fairness."
    )
    doc.gap(0.006)
    doc.body(
        "In the United Kingdom, the Financial Conduct Authority's Consumer Duty (PS22/9, effective "
        "31 July 2023) creates outcome-based obligations that differ structurally from the US model. "
        "Lenders must demonstrate that their credit products produce good outcomes for customers, "
        "that foreseeable harms are identified and mitigated, and that monitoring evidence is "
        "available at board level. The UK framework shifts compliance from explaining individual "
        "decisions toward evidencing systemic product governance over time."
    )

    # ── Section 5 ─────────────────────────────────────────────────────────────
    doc.section("5.  Political and Regulatory Divergence")
    doc.body("5.1  Within-US Political Shift: Biden Era to Trump Era", indent=0.0)
    doc.gap(0.003)
    doc.body(
        "The regulatory stance on AI-driven credit decisions within the United States has itself "
        "shifted with the political administration, which the assignment requires the tool to "
        "acknowledge. In October 2023, the CFPB under the Biden administration issued guidance "
        "explicitly stating that lenders using complex AI or algorithmic models in credit decisions "
        "must still provide specific and meaningful adverse action reasons to rejected applicants. "
        "The guidance rejected the argument that model complexity excuses vague explanations, and "
        "represented a tightening of the explainability standard for AI credit tools."
    )
    doc.gap(0.006)
    doc.body(
        "In April 2026, the CFPB under the Trump administration finalised a rewrite of Regulation B "
        "Subpart A, largely as proposed. This revision reduced the pressure toward AI-specific "
        "explainability that the Biden-era guidance had introduced. This is a deliberate political "
        "choice: the Trump administration has prioritised reducing regulatory burden on lenders over "
        "expanding AI-specific consumer protections. For a RegTech compliance tool, this shift is "
        "consequential. A tool calibrated to Biden-era enforcement expectations — requiring highly "
        "specific, model-derived adverse action reasons — may produce false positive findings under "
        "the revised Trump-era standard, which interprets the same statutory text more permissively. "
        "The jurisdiction configuration layer in the prototype must therefore be capable of "
        "versioning these rule changes, not treating US regulation as static."
    )
    doc.gap(0.010)

    doc.body("5.2  Structural Divergence: US vs UK Regulatory Philosophies", indent=0.0)
    doc.gap(0.003)
    doc.body(
        "The divergence between the United States and the United Kingdom is not merely technical — "
        "it reflects different political theories of what financial regulation is trying to achieve. "
        "The US framework relies on anti-discrimination law and a protected-class model: harm is "
        "defined as disparate treatment or disparate impact on a legally identified group, and "
        "remedy is centred on adverse action explanation at the level of the individual application. "
        "The regulatory assumption is that ex-post individual explanation, combined with statistical "
        "monitoring, is sufficient protection."
    )
    doc.gap(0.006)
    doc.body(
        "The UK Consumer Duty reflects a different political choice. The regulator expects firms to "
        "monitor outcomes across customer segments proactively, to present board-level evidence that "
        "foreseeable harms are addressed, and to demonstrate remediation when poor outcomes are "
        "identified. This shifts compliance from reactive individual explanation to proactive "
        "systemic outcome governance. A RegTech tool that only produces adverse action reasons "
        "satisfies the US philosophy but fails the UK one."
    )
    doc.gap(0.010)

    doc.body("5.3  Model Risk Management: OCC Bulletin 2026-13", indent=0.0)
    doc.gap(0.003)
    doc.body(
        "In 2026, the Office of the Comptroller of the Currency (OCC) issued Bulletin 2026-13, "
        "which updated model risk management guidance for OCC-supervised institutions. The bulletin "
        "is notable for explicitly excluding generative AI from its scope — a political and "
        "regulatory choice to treat GenAI under future separate guidance rather than fold it into "
        "the existing model risk framework. For AI credit scoring using traditional machine learning "
        "(logistic regression, gradient boosting, neural networks), OCC 2026-13 continues to require "
        "documented model validation, ongoing performance monitoring, a defined model lifecycle, and "
        "human accountability for model outcomes. The Task 3 prototype references this bulletin in "
        "its model risk layer: both the US and UK configurations require model card documentation "
        "and drift monitoring, consistent with OCC 2026-13's lifecycle expectations."
    )

    # ── Section 6 ─────────────────────────────────────────────────────────────
    doc.section("6.  Relevance to the Tool Design")
    doc.body(
        "The Task 3 prototype implements a jurisdiction configuration layer that translates the "
        "above political and regulatory differences into executable operational checks. The US "
        "configuration applies ECOA / Regulation B-style fair lending outcome review and adverse "
        "action explanation logic. The UK configuration applies a stricter outcome disparity "
        "threshold and adds FCA Consumer Duty-style outcome monitoring, model card documentation, "
        "human oversight evidence, and remediation governance requirements. The two configurations "
        "produce materially different compliance statuses from the same model output — demonstrating "
        "that RegTech tools are political artefacts, encoding a specific regulatory interpretation "
        "rather than a universal standard. The rule version and last-reviewed date are stored in "
        "the configuration layer precisely to handle the kind of mid-period political shift "
        "described in Section 5.1."
    )

    # ── Section 7 ─────────────────────────────────────────────────────────────
    doc.section("7.  References and URLs")
    doc.ref(1,
            "Lendable official website — UK and North American markets described.",
            "https://www.lendable.com/")
    doc.ref(2,
            "Lendable UK — FCA-authorised and regulated entity, FRN 720261.",
            "https://www.lendable.co.uk/")
    doc.ref(3,
            "Zable US state licensing disclosures — confirms US regulated operations.",
            "https://www.zable.com/licenses")
    doc.ref(4,
            "CFPB (Biden era, October 2023) — Guidance on adverse action notices for "
            "AI-driven credit decisions; requires specific and meaningful explanations.",
            "https://www.consumerfinance.gov/about-us/newsroom/cfpb-issues-guidance-on-"
            "credit-denials-by-lenders-using-artificial-intelligence/")
    doc.ref(5,
            "CFPB (Trump era, April 2026) — Regulation B Subpart A rewrite finalised; "
            "reduces AI-specific explainability obligations.",
            "https://www.consumerfinancialserviceslawmonitor.com/2026/04/cfpb-finalizes-"
            "regulation-b-subpart-a-rule-largely-as-proposed/")
    doc.ref(6,
            "OCC Bulletin 2026-13 — Revised model risk management guidance; "
            "explicitly excludes generative AI from scope.",
            "https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html")
    doc.ref(7,
            "FCA Consumer Duty — Year 2 board reports and outcome monitoring progress.",
            "https://www.fca.org.uk/news/blogs/year-2-consumer-duty-board-reports-"
            "progress-and-what-comes-next")
    doc.ref(8,
            "FCA Consumer Duty — Multi-firm review of implementation plans.",
            "https://www.fca.org.uk/publications/multi-firm-reviews/consumer-duty-"
            "implementation-plans")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Doc(str(OUT))
    doc._new_page(flush=False)
    build(doc)
    doc.close()
    print(f"Written: {OUT}")


if __name__ == "__main__":
    main()
