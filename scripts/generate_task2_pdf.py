"""Generate Task2_Values_Audit.pdf — academic document format."""
from __future__ import annotations
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ── Output path ──────────────────────────────────────────────────────────────
OUT = Path(__file__).resolve().parents[2] / "NTULearn_Submission_Clean" / "Task2_Values_Audit.pdf"

# ── Layout constants ─────────────────────────────────────────────────────────
L, R = 0.11, 0.89
TOP, BOT = 0.930, 0.072
LH = 0.0215
LH_S = 0.024
FS_DOC = 14
FS_SEC = 11
FS_BOD = 10.2
FS_FTR = 8.5
WRAP = 90

C_DARK = "#111827"
C_BODY = "#374151"
C_FTR  = "#9ca3af"
AUTHOR = "Huang Sining | G2505429H | SINING001@e.ntu.edu.sg"


# ── Renderer ─────────────────────────────────────────────────────────────────
class Doc:
    def __init__(self, path):
        self._pdf    = PdfPages(path)
        self._fig    = None
        self._ax     = None
        self._y      = TOP
        self._pageno = 0
        self._first  = True

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
            self._ax.text(L, self._y, "Task 2: Values Audit",
                          fontsize=FS_DOC, fontweight="bold", color=C_DARK, va="top")
            self._y -= LH_S + 0.004
            self._ax.plot([L, R], [self._y, self._y], color="#6b7280", lw=0.7)
            self._y -= 0.018

    def _footer(self):
        self._ax.text(L, BOT - 0.010,
                      f"Task 2 | {AUTHOR} | Page {self._pageno}",
                      fontsize=FS_FTR, color=C_FTR, va="bottom")

    def _need(self, lines: int, extra: float = 0.0):
        if self._y - (lines * LH + extra + 0.006) < BOT:
            self._new_page()

    def section(self, text: str):
        self._need(3, LH_S)
        self._ax.text(L, self._y, text, fontsize=FS_SEC, fontweight="bold",
                      color=C_DARK, va="top")
        self._y -= LH_S + 0.006

    def sub(self, text: str):
        lines = textwrap.wrap(text, WRAP)
        self._need(len(lines) + 1)
        self._ax.text(L, self._y, lines[0], fontsize=FS_BOD + 0.3,
                      fontweight="bold", color=C_DARK, va="top")
        self._y -= LH
        for ln in lines[1:]:
            self._ax.text(L, self._y, ln, fontsize=FS_BOD + 0.3,
                          fontweight="bold", color=C_DARK, va="top")
            self._y -= LH
        self._y -= 0.004

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

    # ── Q1 Mission Statement ──────────────────────────────────────────────────
    doc.section("1.  Mission Statement and Company Profile")
    doc.body(
        "The hypothetical company, referred to as FairLens RegTech, is a growth-stage specialist "
        "compliance software provider focused exclusively on AI-driven consumer credit. Its mission "
        "is to operationalise legally relevant fairness across jurisdictions — giving regulated "
        "lenders the monitoring, explanation, and governance evidence they need to satisfy both US "
        "fair lending obligations and UK FCA Consumer Duty requirements, without requiring them to "
        "build that capability in-house."
    )
    doc.gap(0.006)
    doc.body(
        "Core values: regulatory defensibility (every finding in the tool must trace to a "
        "documented regulatory source), fairness (the tool must surface real risk, not label-wash "
        "it), transparency (the rule logic, thresholds, and provenance are visible and versioned), "
        "and efficiency (the tool must reduce compliance cost, not add to it). These values are "
        "in genuine tension: tighter monitoring can reduce credit volume, increase manual review "
        "cost, and surface model weaknesses that the client would prefer not to document. The "
        "company accepts this tension as the cost of building a tool that measures substance "
        "rather than performing compliance."
    )
    doc.gap(0.006)
    doc.body(
        "The company is at Series A stage, approximately four years old. Current headcount is "
        "45 FTE, distributed across credit analytics (12), compliance engineering (14), model "
        "governance and legal advisory (8), and sales and customer success (11). The company "
        "currently serves 12 pilot clients across the United States and United Kingdom."
    )
    doc.gap(0.006)

    doc.sub("Revenue aspirations:")
    doc.body(
        "Target ARR of USD 6-8 million within three years, derived from 50-70 mid-market "
        "lenders at an average annual contract value of USD 100,000-150,000, inclusive of "
        "implementation and ongoing support. Current ARR is approximately USD 900,000 from "
        "pilot engagements. The pricing model is subscription-based with a usage component "
        "tied to monthly active applicant volumes, creating revenue upside as clients scale."
    )
    doc.gap(0.006)

    doc.sub("Cost structure:")
    doc.body(
        "Engineering and analytics talent accounts for approximately 60% of operating "
        "expenditure. Legal and regulatory advisory retainers account for 18%, reflecting the "
        "cost of keeping rule configurations current as regulations evolve. Sales, marketing, "
        "and customer success account for 15%. Infrastructure, data, and licensing account for "
        "the remainder. Target gross margin at scale is 68-72%, consistent with comparable B2B "
        "SaaS compliance platforms. Customer acquisition cost is currently high (12-18 month "
        "payback) because enterprise compliance sales cycles are long; the target is to reduce "
        "this to 9 months by year three through partnerships with credit bureau data providers."
    )
    doc.gap(0.006)

    doc.sub("Geographical coverage:")
    doc.body(
        "The current go-to-market focus is the United States and United Kingdom. Both markets "
        "have active AI-lending sectors, established regulatory expectations, and large enough "
        "compliance teams to represent paying clients. The product roadmap targets EU expansion "
        "no earlier than 2027, aligned with the AI Act's enforcement timeline for high-risk AI "
        "systems in financial services. Singapore is a secondary priority given MAS model risk "
        "management guidance, but requires a separate sales and regulatory localisation effort."
    )

    # ── Q2 Whose Perspective ──────────────────────────────────────────────────
    doc.section("2.  Whose Perspective the Tool Serves")
    doc.body(
        "The primary paying client is the Chief Compliance Officer (CCO) and senior management "
        "of a regulated mid-market lender. The most materially affected stakeholder is the "
        "rejected credit applicant, who has no contractual relationship with the RegTech "
        "provider and no direct voice in tool design. The regulator is a secondary audience: "
        "it does not purchase the tool but its expectations define what the tool must evidence."
    )
    doc.gap(0.006)
    doc.body(
        "Stakeholder tensions are real. The CCO wants defensible automation and manageable "
        "compliance cost. The lender's risk management function wants predictive performance, "
        "which sometimes conflicts with fairness objectives — a model with high predictive "
        "accuracy may produce larger group disparities than a constrained fair model. Consumers "
        "want access to credit and clear explanations when they are declined. The regulator wants "
        "evidence of fair treatment and good customer outcomes, which requires the lender to "
        "document uncomfortable findings, not just clear ones. These tensions are not resolvable "
        "by tool design alone; they are political choices that the RegTech provider inherits."
    )
    doc.gap(0.006)

    doc.sub("Why the CCO, and have we sized the market?")
    doc.body(
        "The design choice to serve the CCO primarily is driven by two factors: demonstrated "
        "ability to pay and team competence. On ability to pay: Grand View Research estimated "
        "global RegTech market size at USD 21.7 billion in 2023, growing at approximately 22% "
        "compound annual growth rate, of which credit-compliance tooling is a fast-growing "
        "sub-segment. Within the US, FDIC 2024 data identifies approximately 1,200 FDIC-insured "
        "commercial banks and credit unions in the mid-market segment — defined here as "
        "institutions with USD 500 million to USD 10 billion in assets — that use automated "
        "credit scoring. Estimated annual compliance spend per institution in this segment "
        "ranges from USD 800,000 to USD 2.5 million. AI fairness and model governance tooling "
        "is an emerging but growing sub-category within that spend."
    )
    doc.gap(0.006)
    doc.body(
        "Ability to pay is further evidenced by regulatory fine exposure. US ECOA enforcement "
        "actions have resulted in settlements ranging from USD 1 million to over USD 100 million "
        "(the BancorpSouth settlement in 2016 and the Trident Mortgage settlement in 2021 are "
        "notable examples). A USD 100,000-150,000 annual compliance tool is a rational insurance "
        "purchase against that exposure. In the UK, FCA Consumer Duty enforcement is at an early "
        "stage but the FCA has made clear that board-level evidence of outcome monitoring is a "
        "prerequisite for ongoing authorisation in consumer credit. The addressable UK mid-market "
        "segment numbers approximately 120 FCA-authorised consumer credit lenders using "
        "automated scoring. On team competence: the founding team combines credit risk modelling, "
        "regulatory affairs, and software engineering experience, which is the specific combination "
        "required to translate regulatory expectations into operational software."
    )

    # ── Q3 Risk vs Compliance ─────────────────────────────────────────────────
    doc.section("3.  Is the Tool Measuring Genuine Risk or Documenting Compliance?")
    doc.body(
        "The tool is designed to measure genuine risk. One concrete design choice illustrates "
        "this commitment."
    )
    doc.gap(0.006)
    doc.body(
        "Sensitive demographic attributes — nationality, ethnicity, religion, and marital status — "
        "are excluded from the credit model's training features. This is standard practice. "
        "However, they are retained in the dataset and used in post-decision fairness auditing. "
        "This additional step is not legally required for a basic model build. A lender could "
        "claim technical compliance by simply confirming that protected attributes are absent from "
        "the model inputs. The tool goes further by testing whether model outcomes differ across "
        "groups defined by those attributes even when the attributes were not used as direct "
        "inputs. This detects the kind of indirect or proxy-driven disparity — where correlated "
        "socioeconomic variables produce group outcome differences — that would persist invisibly "
        "under a checklist approach. Including this feature costs the client more difficult "
        "conversations; excluding it would be easier to sell. It is included because it "
        "improves genuine risk detection."
    )
    doc.gap(0.006)
    doc.body(
        "A feature deliberately excluded further illustrates the design philosophy. The prototype "
        "does not produce an automated compliance certificate or a single pass/fail score. "
        "Such a feature would be commercially attractive and easy to implement. It would also "
        "serve documentation over substance: a single score encourages clients to treat the output "
        "as an audit pass rather than as evidence requiring human review. The tool instead produces "
        "specific findings linked to specific rule configurations and source references, and "
        "explicitly flags which findings require human judgement rather than automated resolution."
    )

    # ── Q4 Who Bears the Cost ─────────────────────────────────────────────────
    doc.section("4.  Who Bears the Cost if the Tool Gets It Wrong?")
    doc.body(
        "False positives — flagging a compliant portfolio as non-compliant — impose cost on the "
        "lender through unnecessary manual review and investigation. More seriously, a lender "
        "may respond to repeated false positives by tightening credit criteria to clear the "
        "tool's thresholds. This can reduce lending access to the very groups the tool was "
        "designed to protect. The stakeholder who ultimately bears this cost is the consumer "
        "who is denied credit unnecessarily because the RegTech tool overcalibrated."
    )
    doc.gap(0.006)
    doc.body(
        "False negatives — clearing a non-compliant portfolio — are more serious in terms of "
        "harm magnitude and harder to detect. A lender that believes its model has cleared a "
        "fairness review may reduce monitoring frequency and defer remediation. If hidden disparity "
        "persists undetected, affected consumer groups face systematic credit exclusion without "
        "any regulatory response or internal correction. The harm is diffuse, cumulative, and "
        "invisible to the individuals affected. The specific stakeholder who bears this cost is "
        "the consumer applicant in the disadvantaged group."
    )
    doc.gap(0.006)
    doc.body(
        "Performance drift imposes cost on both lenders and consumers when economic conditions "
        "or applicant mix shift without detection. A model that was validated as fair under one "
        "macroeconomic environment may produce materially different disparity ratios two years "
        "later when income distributions or employment patterns change. Without continuous drift "
        "monitoring, neither the lender nor the regulator has visibility into this degradation. "
        "The prototype addresses this with a recession-scenario drift simulation, but real "
        "drift monitoring requires ongoing data ingestion that the prototype does not provide."
    )
    doc.gap(0.006)
    doc.body(
        "Jurisdiction misconfiguration — applying the US rule configuration to a UK-regulated "
        "product, or vice versa — may expose the lender to regulatory action in the incorrectly "
        "configured market. If a UK-regulated entity's product is accidentally evaluated under "
        "the less demanding US configuration, the FCA Consumer Duty evidence requirements will "
        "not be checked, and the board report will not reflect the correct risk picture. The "
        "lender bears this cost in the form of regulatory exposure; the consumer bears it in "
        "the form of reduced protection."
    )
    doc.gap(0.006)
    doc.body(
        "The most dangerous failure is a false sense of compliance: the tool produces "
        "thorough-looking reports and findings while genuine harmful outcomes persist in the "
        "portfolio. This failure is the hardest to detect, because it requires the tool to be "
        "honest about the limits of its own coverage — which is commercially inconvenient. For "
        "this reason, the tool explicitly documents what it does not check, what data it does "
        "not have access to, and where human judgement is required rather than automated. The "
        "boundary is drawn deliberately to prevent the tool from being used as a shield against "
        "regulatory scrutiny rather than as a genuine risk instrument."
    )


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Doc(str(OUT))
    doc._new_page(flush=False)
    build(doc)
    doc.close()
    print(f"Written: {OUT}")


if __name__ == "__main__":
    main()
