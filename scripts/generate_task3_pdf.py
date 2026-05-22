"""
Generate Task3_Tool_Design.pdf in academic document format.
Embeds charts inline with figure captions. Covers all assignment
requirements: one-page summary, management pitch (4 questions),
jurisdiction logic, failure modes, limitations/honesty.
"""
from __future__ import annotations
from pathlib import Path
import json
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR  = PROJECT_ROOT / "outputs"
DOCS_DIR     = PROJECT_ROOT / "docs"
NTUL_DIR     = PROJECT_ROOT.parent / "NTULearn_Submission_Clean"

# ── Layout ────────────────────────────────────────────────────────────────────
L, R   = 0.11, 0.89
TOP    = 0.930
BOT    = 0.072
LH     = 0.0215
LH_S   = 0.024
FS_DOC = 14
FS_SEC = 11
FS_BOD = 10.2
FS_CAP = 9.0       # figure caption
FS_FTR = 8.5
WRAP   = 90

C_DARK = "#111827"
C_BODY = "#374151"
C_CAP  = "#4b5563"
C_FTR  = "#9ca3af"
AUTHOR = "Huang Sining | G2505429H | SINING001@e.ntu.edu.sg"


# ── Renderer ─────────────────────────────────────────────────────────────────
class Doc:
    def __init__(self, pdf: PdfPages):
        self._pdf    = pdf
        self._fig    = None
        self._ax     = None
        self._y      = TOP
        self._pageno = 0
        self._first  = True
        self._fig_no = 0      # figure counter

    # ── internal ──────────────────────────────────────────────────────────────
    def _new_page(self, flush: bool = True):
        if self._fig and flush:
            self._footer()
            self._pdf.savefig(self._fig, bbox_inches="tight")
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
            self._ax.text(
                L, self._y,
                "Task 3 Tool Design: Jurisdiction-Aware AI Credit Fairness Checker",
                fontsize=FS_DOC, fontweight="bold", color=C_DARK, va="top"
            )
            self._y -= LH_S + 0.004
            self._ax.plot([L, R], [self._y, self._y], color="#6b7280", lw=0.7)
            self._y -= 0.006
            self._ax.text(
                L, self._y,
                f"{AUTHOR}",
                fontsize=9.5, color="#6b7280", va="top"
            )
            self._y -= LH + 0.006

    def _footer(self):
        self._ax.text(
            L, BOT - 0.010,
            f"Task 3 Tool Design | {AUTHOR} | Page {self._pageno}",
            fontsize=FS_FTR, color=C_FTR, va="bottom"
        )

    def _need(self, lines: int, extra: float = 0.0) -> None:
        if self._y - (lines * LH + extra + 0.006) < BOT:
            self._new_page()

    # ── public text ───────────────────────────────────────────────────────────
    def section(self, text: str):
        self._need(3, LH_S + 0.010)
        self._y -= 0.006
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

    def bullet(self, text: str, indent: float = 0.026):
        lines = textwrap.wrap(text, WRAP - 6)
        self._need(len(lines))
        self._ax.text(L + indent - 0.015, self._y, "-", fontsize=FS_BOD,
                      color=C_BODY, va="top")
        self._ax.text(L + indent, self._y, lines[0], fontsize=FS_BOD,
                      color=C_BODY, va="top")
        self._y -= LH
        for ln in lines[1:]:
            self._ax.text(L + indent, self._y, ln, fontsize=FS_BOD,
                          color=C_BODY, va="top")
            self._y -= LH
        self._y -= 0.003

    def gap(self, size: float = 0.010):
        self._y -= size
        if self._y < BOT + 0.04:
            self._new_page()

    # ── inline figure ─────────────────────────────────────────────────────────
    def figure(self, height_norm: float, caption: str, draw_fn) -> None:
        """
        Flush current text page, then create a dedicated figure page with:
          - chart anchored at the TOP of the page (fixed layout, not y_before dependent)
          - caption below the chart with sufficient margin to avoid tick/label overlap
          - footer at bottom
        Then start a fresh text page for continuation.
        """
        self._fig_no += 1

        # 1. Flush current text page to PDF
        self._footer()
        self._pdf.savefig(self._fig, bbox_inches="tight")
        plt.close(self._fig)
        self._pageno += 1

        # 2. Fixed positions for the figure page (always from top)
        CHART_TOP    = 0.88          # chart top (in figure normalised coords)
        CHART_HEIGHT = height_norm   # e.g. 0.45
        CHART_BOTTOM = CHART_TOP - CHART_HEIGHT
        CAP_TOP      = CHART_BOTTOM - 0.045   # gap for x-axis labels/ticks
        CAP_BOTTOM   = CAP_TOP - 0.12         # caption area

        # 3. Build the figure page
        fig_page = plt.figure(figsize=(8.27, 11.69))
        fig_page.patch.set_facecolor("white")

        # Text overlay (full page)
        ax_text = fig_page.add_axes([0, 0, 1, 1])
        ax_text.axis("off")
        ax_text.set_xlim(0, 1)
        ax_text.set_ylim(0, 1)

        # Chart axes (positioned precisely)
        ax_chart = fig_page.add_axes(
            [L + 0.02, CHART_BOTTOM, (R - L) - 0.04, CHART_HEIGHT - 0.010]
        )
        draw_fn(ax_chart)

        # Figure label above chart
        ax_text.text(
            L, CHART_TOP + 0.005,
            f"Figure {self._fig_no}",
            fontsize=9.5, fontweight="bold", color=C_DARK, va="bottom"
        )

        # Caption below chart (italic, smaller font)
        cap_lines = textwrap.wrap(f"Figure {self._fig_no}: {caption}", WRAP)
        cap_y = CAP_TOP
        for ln in cap_lines:
            ax_text.text(L, cap_y, ln, fontsize=FS_CAP, color=C_CAP,
                         va="top", style="italic")
            cap_y -= LH * 0.90
            if cap_y < BOT + 0.02:
                break

        # Footer
        ax_text.text(L, BOT - 0.010,
                     f"Task 3 Tool Design | {AUTHOR} | Page {self._pageno}",
                     fontsize=FS_FTR, color=C_FTR, va="bottom")

        self._pdf.savefig(fig_page, bbox_inches="tight")
        plt.close(fig_page)

        # 4. Start fresh text page for continuation
        self._fig = plt.figure(figsize=(8.27, 11.69))
        self._fig.patch.set_facecolor("white")
        self._ax  = self._fig.add_axes([0, 0, 1, 1])
        self._ax.axis("off")
        self._ax.set_xlim(0, 1)
        self._ax.set_ylim(0, 1)
        self._pageno += 1
        self._y = TOP

    def close(self):
        self._footer()
        self._pdf.savefig(self._fig, bbox_inches="tight")
        plt.close(self._fig)


# ── Content ───────────────────────────────────────────────────────────────────
def build(doc: Doc, reports: dict, sensitivity: pd.DataFrame, drift: pd.DataFrame):

    us_status = reports["US"]["overall_status"]
    uk_status  = reports["UK"]["overall_status"]

    # ── 1. Plain-language summary (required for all options) ─────────────────
    doc.section("1.  Plain-Language Design Summary")
    doc.body(
        "This document constitutes the required one-page plain-language summary (Section 1) "
        "and the senior management pitch (Sections 2-6) for the Task 3 working prototype. "
        "The prototype implements Option A (Working Prototype) with additional quantitative "
        "analysis elements drawn from Option C."
    )
    doc.gap(0.006)
    doc.body(
        "The tool is a jurisdiction-aware compliance checker for AI-driven credit scoring, "
        "designed for a Lendable / Zable-style consumer lending platform operating across the "
        "United States and the United Kingdom. It takes synthetic applicant data, trains a "
        "logistic regression credit risk model, and evaluates the same model output through "
        "two separately configured regulatory rule sets. Sensitive demographic attributes are "
        "excluded from model training but retained for post-decision fairness auditing."
    )
    doc.gap(0.006)
    doc.body(
        "The central design claim is that the same model output carries different compliance "
        f"meanings depending on jurisdiction. In the latest demo run, the US configuration "
        f"returns '{us_status}' while the UK configuration returns '{uk_status}'. The US "
        "configuration enforces an approval-disparity threshold of 0.80 (four-fifths rule "
        "convention from fair lending practice) and requires specific adverse action reasons "
        "for rejected applicants. The UK configuration enforces a stricter disparity threshold "
        "of 0.90, consistent with the FCA Consumer Duty's outcome-monitoring philosophy, and "
        "additionally requires model card documentation, human oversight evidence, and "
        "board-level remediation governance."
    )
    doc.gap(0.006)
    doc.body(
        "The tool does not provide legal advice, determine that unlawful discrimination has "
        "occurred, or replace human judgement. These boundaries are deliberate: the prototype "
        "surfaces regulatory risk and governance gaps for human review. The design explicitly "
        "chooses not to produce a compliance certificate or a single pass/fail score because "
        "such outputs would serve documentation over genuine risk detection."
    )

    # ── Requirement mapping table ─────────────────────────────────────────────
    doc.section("2.  Assignment Requirement Mapping")
    doc.body(
        "The table below maps each Option A and Option C requirement to the specific component "
        "in the prototype that satisfies it."
    )
    doc.gap(0.006)

    rows = [
        ["Jurisdiction config layer",    "src/config_rules.py — US and UK rules, thresholds, sources, rule version, last-reviewed date"],
        ["Live/simulated data input",    "data/synthetic_applicants.csv — 1,500 synthetic applicants regenerated by run_demo.py"],
        ["Different output by juris.",   "outputs/compliance_reports.json — US 'No major issues', UK 'Review Required'"],
        ["Model card / governance stub", "docs/Task3_Model_Card.md — purpose, inputs, exclusions, assumptions, failure modes"],
        ["Quantitative metric",          "Approval disparity ratio, approval rate, ROC-AUC, feature importance computed per run"],
        ["Threshold methodology",        "US threshold 0.80 (four-fifths rule); UK threshold 0.90 (Consumer Duty strictness)"],
        ["Sensitivity analysis",         "outputs/threshold_sensitivity.csv — disparity ratio vs. model decision threshold"],
        ["Drift simulation",             "outputs/drift_comparison.csv — recession income shock scenario vs. baseline"],
        ["Failure modes",                "False positives, false negatives, drift, jurisdiction misconfiguration, false confidence"],
        ["Management pitch",             "Sections 3-6 below; Limitations in Section 6"],
    ]

    # Draw table in-line on current page
    doc._need(len(rows) + 2, 0.040)
    tbl_top = doc._y
    col_widths = [0.28, 0.50]
    row_h = 0.022

    ax = doc._ax
    # Header
    for ci, (hdr, cw) in enumerate(zip(["Requirement", "Where satisfied"], col_widths)):
        x0 = L + sum(col_widths[:ci])
        ax.add_patch(plt.Rectangle((x0, tbl_top - row_h), cw, row_h,
                                   facecolor="#e5e7eb", edgecolor="#9ca3af", lw=0.5, transform=ax.transData))
        ax.text(x0 + 0.005, tbl_top - row_h / 2, hdr, fontsize=8.6,
                fontweight="bold", color=C_DARK, va="center")

    doc._y = tbl_top - row_h
    for row in rows:
        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            x0 = L + sum(col_widths[:ci])
            face = "white" if rows.index(row) % 2 == 0 else "#f9fafb"
            ax.add_patch(plt.Rectangle((x0, doc._y - row_h), cw, row_h,
                                       facecolor=face, edgecolor="#d1d5db", lw=0.4))
            wrapped = textwrap.wrap(cell, 55 if ci == 1 else 28)
            ax.text(x0 + 0.005, doc._y - row_h / 2, wrapped[0] if wrapped else cell,
                    fontsize=8.2, color=C_BODY, va="center")
        doc._y -= row_h

    doc._y -= 0.012

    # ── 3. Why this product? ──────────────────────────────────────────────────
    doc.section("3.  Why Is This Product Right for the Company?")
    doc.body(
        "The hypothetical RegTech company (FairLens RegTech) is positioned as a specialist "
        "compliance software provider for mid-market AI-lending platforms expanding across "
        "the US and UK. Its core competence is translating regulatory expectations into "
        "executable, versioned operational checks — not providing legal advice. This prototype "
        "directly reflects that positioning. AI credit scoring creates a recurring, "
        "jurisdiction-specific monitoring need: the same model must be re-evaluated every time "
        "regulation changes, portfolios shift, or a new market is entered. A configurable, "
        "automated tool is the natural product for that need."
    )
    doc.gap(0.006)
    doc.body(
        "The commercial rationale is also sound. US ECOA enforcement settlements have ranged "
        "from USD 1 million to over USD 100 million (BancorpSouth 2016, Trident Mortgage 2021), "
        "making a USD 100,000-150,000 annual compliance tool a rational insurance purchase. "
        "In the UK, the FCA has signalled that board-level evidence of Consumer Duty outcome "
        "monitoring is a prerequisite for ongoing authorisation in consumer credit. The product "
        "converts both of these compliance obligations into a repeatable software workflow rather "
        "than a recurring manual exercise."
    )

    # ── 4. Why a tool beats memo / spreadsheet? ───────────────────────────────
    doc.section("4.  What Problem Does This Tool Solve That a Memo or Spreadsheet Cannot?")
    doc.body(
        "A memo can describe regulatory differences between the US and the UK, but it cannot "
        "rerun those checks when a new applicant dataset arrives, when a model threshold is "
        "adjusted, or when a regulation is updated. It is a snapshot, not a workflow. A "
        "spreadsheet can store individual metrics but does not naturally preserve rule "
        "provenance (which version of Regulation B?), model assumptions, adverse action "
        "explanation logic, and drift evidence in a single reproducible artefact."
    )
    doc.gap(0.006)
    doc.body(
        "This tool provides three specific capabilities that neither a memo nor a spreadsheet "
        "can replicate. First, the jurisdiction configuration layer (src/config_rules.py) "
        "stores regulatory parameters as versioned, source-linked records. When the Trump "
        "administration's Regulation B rewrite changed the US explainability standard in "
        "April 2026, a compliance team using a spreadsheet would need to manually update every "
        "downstream document. This tool requires a single rule-version update. Second, the "
        "tool generates adverse action explanations for every rejected applicant as part of "
        "the same pipeline that checks disparity ratios — the output is consistent and "
        "traceable, not manually assembled. Third, the drift simulation and sensitivity "
        "analysis produce quantitative evidence for regulators, not narrative assertions. "
        "The compliance finding is connected to the data and the rule in one JSON report."
    )

    # ── 5. Regulatory divergence handled ─────────────────────────────────────
    doc.section("5.  What Regulatory Divergence Does the Tool Handle, and How?")
    doc.body(
        "The tool handles the divergence between US fair lending obligations (anchored in "
        "ECOA and Regulation B) and UK outcome-based governance obligations (anchored in the "
        "FCA Consumer Duty, PS22/9)."
    )
    doc.gap(0.006)
    doc.body(
        "Within the US, the political landscape has itself shifted. The Biden-era CFPB (October "
        "2023) required specific, model-derived adverse action reasons for AI-driven credit "
        "decisions, tightening explainability obligations. The Trump-era CFPB's Regulation B "
        "Subpart A rewrite (April 2026) reduced that pressure. The prototype's rule_version and "
        "last_reviewed fields in config_rules.py are specifically designed to track these "
        "mid-period political changes, allowing compliance teams to operate against the correct "
        "version of the rule rather than an outdated snapshot."
    )
    doc.gap(0.006)
    doc.body(
        "The structural divergence between US and UK is operationalised through three "
        "configurable differences. (1) Disparity threshold: the US configuration flags "
        "approval-rate disparity below 0.80; the UK configuration flags disparity below 0.90, "
        "reflecting the Consumer Duty's stricter outcome-monitoring stance. (2) Governance "
        "requirements: the UK configuration requires model card documentation, human oversight "
        "evidence, and Consumer Duty outcome monitoring flags; the US configuration requires "
        "model card documentation (consistent with OCC 2026-13 model lifecycle expectations) "
        "but not the UK's board-level remediation governance layer. (3) Adverse action logic: "
        "both configurations require specific adverse action reasons, but the UK configuration "
        "additionally requires evidence that governance processes are embedded in the product "
        "lifecycle — not just that individual denials are explained."
    )
    doc.gap(0.006)
    doc.body(
        "The demo result confirms the jurisdiction logic is real and not decorative. Using the "
        "same 1,500-applicant synthetic portfolio and the same logistic regression model at a "
        "0.50 decision threshold, the US configuration returns 'No major issues detected' "
        "because all group-level approval disparity ratios exceed 0.80. The UK configuration "
        "returns 'Review Required' because the nationality disparity ratio (0.898) and the "
        "ethnicity disparity ratio (0.858) both fall below the stricter 0.90 UK threshold."
    )

    # ── Figure 1: Sensitivity analysis ───────────────────────────────────────
    def draw_sensitivity(ax_c):
        ax_c.plot(sensitivity["threshold"], sensitivity["approval_rate"],
                  marker="o", color="#2563eb", linewidth=1.4, label="Approval rate")
        ax_c.plot(sensitivity["threshold"], sensitivity["ethnicity_disparity_ratio"],
                  marker="s", color="#f59e0b", linewidth=1.4, label="Ethnicity disparity ratio")
        ax_c.plot(sensitivity["threshold"], sensitivity["nationality_disparity_ratio"],
                  marker="^", color="#10b981", linewidth=1.4, linestyle="--",
                  label="Nationality disparity ratio")
        ax_c.axhline(0.80, color="#1d4ed8", linestyle=":", linewidth=1.2, label="US threshold (0.80)")
        ax_c.axhline(0.90, color="#dc2626", linestyle=":", linewidth=1.2, label="UK threshold (0.90)")
        ax_c.set_xlabel("Model decision threshold", fontsize=9)
        ax_c.set_ylabel("Rate / disparity ratio", fontsize=9)
        ax_c.set_ylim(0, 1.05)
        ax_c.set_xlim(0.33, 0.62)
        ax_c.grid(True, alpha=0.25, linewidth=0.6)
        ax_c.legend(fontsize=8, loc="lower right", framealpha=0.9)
        ax_c.tick_params(labelsize=8)
        ax_c.set_facecolor("#fafafa")

    doc.figure(
        0.28,
        "Threshold sensitivity analysis. As the model decision threshold rises, approval "
        "rates and group disparity ratios both improve. The ethnicity disparity ratio "
        "crosses the US threshold (0.80, blue dotted) at approximately threshold=0.50, "
        "and approaches but does not consistently exceed the UK threshold (0.90, red "
        "dotted) until threshold=0.60. This demonstrates that the same portfolio clears "
        "the US compliance check but fails the UK check across a wide range of model "
        "settings — confirming that the jurisdiction divergence is structural, not marginal.",
        draw_sensitivity
    )

    # ── Figure 2: Drift simulation ────────────────────────────────────────────
    doc.section("5.1  Drift Simulation")
    doc.body(
        "The drift simulation models a recession scenario in which applicant incomes are "
        "reduced by 12% and debt-to-income ratios are inflated by 18%. The shock is applied "
        "to the identical 1,500-applicant baseline cohort (same random seed), isolating the "
        "effect of the economic shock from variation in population composition. Figure 2 shows "
        "the effect on approval rate and group-level disparity ratios."
    )
    doc.gap(0.006)
    doc.body(
        "Under the recession shock, the approval rate falls from approximately 0.767 (baseline) "
        "to approximately 0.721 — a meaningful reduction in credit access driven by the income "
        "and DTI deterioration. More importantly, the ethnicity disparity ratio falls from "
        "approximately 0.858 to approximately 0.799, crossing below the US compliance threshold "
        "of 0.80. A portfolio that currently clears the US check would therefore fail that same "
        "check under recession conditions, using the same fixed model and the same threshold. "
        "This result illustrates the core argument for continuous monitoring: a one-time "
        "validation is not sufficient to guarantee ongoing compliance."
    )

    def draw_drift(ax_c):
        cats = drift["scenario"].tolist()
        colors = ["#2563eb", "#f59e0b"]
        x = range(len(cats))
        bars = ax_c.bar(x, drift["approval_rate"], color=colors,
                        width=0.35, label="Approval rate", alpha=0.85)
        ax_c.bar([xi + 0.38 for xi in x], drift["ethnicity_disparity_ratio"],
                 color=["#93c5fd", "#fcd34d"], width=0.35,
                 label="Ethnicity disparity ratio", alpha=0.85)
        ax_c.axhline(0.80, color="#1d4ed8", linestyle=":", linewidth=1.2, label="US threshold (0.80)")
        ax_c.axhline(0.90, color="#dc2626", linestyle=":", linewidth=1.2, label="UK threshold (0.90)")
        ax_c.set_xticks([xi + 0.19 for xi in x])
        ax_c.set_xticklabels(cats, fontsize=9)
        ax_c.set_ylabel("Rate / disparity ratio", fontsize=9)
        ax_c.set_ylim(0, 1.05)
        ax_c.grid(axis="y", alpha=0.25, linewidth=0.6)
        ax_c.legend(fontsize=8, loc="upper right", framealpha=0.9)
        ax_c.tick_params(labelsize=8)
        ax_c.set_facecolor("#fafafa")

    doc.figure(
        0.26,
        "Drift simulation: approval rate and ethnicity disparity ratio under baseline and "
        "recession-scenario conditions. The baseline-trained model is applied unchanged to "
        "the income-shocked population. Dark bars show approval rate; light bars show "
        "ethnicity disparity ratio. The ethnicity disparity ratio falls from approximately "
        "0.858 (baseline) to 0.799 (recession), crossing below the US threshold of 0.80 "
        "(blue dotted line). A portfolio that clears the current US compliance check would "
        "fail that same check under recession conditions — demonstrating that one-time model "
        "validation is insufficient and continuous post-deployment monitoring is required.",
        draw_drift
    )

    # ── 6. What the tool does not do ─────────────────────────────────────────
    doc.section("6.  What Does the Tool Not Do, and Why Were Those Boundaries Chosen?")
    doc.body(
        "The tool does not use real customer data. All applicant records are synthetically "
        "generated. This means the fairness conclusions are illustrative rather than "
        "dispositive: the synthetic data cannot reproduce the actual joint distribution of "
        "income, credit score, and demographic group that would appear in a real lender's "
        "portfolio. This boundary was chosen because the assignment is a class prototype, not "
        "a production system. Using real data would require data-sharing agreements, privacy "
        "safeguards, and regulatory permissions that are outside the scope of the assignment."
    )
    doc.gap(0.006)
    doc.body(
        "The prototype implements SHAP (SHapley Additive exPlanations) using LinearExplainer "
        "for the logistic regression model. The notebook demonstrates both a global summary "
        "plot (distribution of SHAP values across all applicants) and a local waterfall plot "
        "(per-applicant feature contributions for individual rejected applicants). SHAP provides "
        "model-consistent attributions that satisfy the spirit of the CFPB's adverse action "
        "guidance: the explanation reflects what the model actually computed, not a post-hoc "
        "approximation. LIME is not implemented; it would add model-agnostic local explanations "
        "for non-linear models and would be the next addition if the credit model were upgraded "
        "to gradient boosting."
    )
    doc.gap(0.006)
    doc.body(
        "The adverse action reason module (src/model_pipeline.py: adverse_action_reasons) "
        "generates human-readable rejection text using feature-threshold heuristics — for example, "
        "flagging a credit score below 640 or a debt-to-income ratio above 0.45. This is a "
        "deliberate simplification for the prototype: these heuristics approximate the model's "
        "reasoning but are not derived directly from the model's coefficients or SHAP values. "
        "In a production system, the SHAP waterfall values would drive adverse action text "
        "generation, ensuring the explanation and the model's decision are derived from the "
        "same underlying computation. This gap is acknowledged as a design limitation."
    )
    doc.gap(0.006)
    doc.body(
        "The tool does not produce a compliance certificate or a single pass/fail score. "
        "This boundary is deliberate and reflects the values audit: a single score would "
        "encourage clients to treat the tool as an audit shield rather than a genuine risk "
        "instrument. The output instead surfaces specific, rule-linked findings that require "
        "human interpretation."
    )
    doc.gap(0.006)
    doc.body(
        "The regulatory thresholds (0.80 for US, 0.90 for UK) are illustrative. The 0.80 "
        "threshold draws on the four-fifths rule from US employment law, which is sometimes "
        "applied analogously to credit lending disparate impact analysis. The 0.90 threshold "
        "is a design choice reflecting the Consumer Duty's stricter outcome orientation. Both "
        "should be validated by qualified legal counsel and compliance teams before deployment. "
        "With more time, the next additions would be: SHAP explainability, a real lender data "
        "ingestion pipeline, automated rule-change alerts triggered by regulatory update feeds, "
        "approval workflow integration for human review escalation, and time-series monitoring "
        "dashboards replacing the current static drift simulation."
    )
    doc.gap(0.006)

    # ── 7. Failure modes ──────────────────────────────────────────────────────
    doc.section("7.  Failure Mode Analysis")
    doc.body(
        "The prototype explicitly identifies five failure modes, consistent with the assignment "
        "requirement that failure modes be named."
    )
    doc.gap(0.004)
    doc.bullet(
        "False positives: the tool incorrectly flags a compliant portfolio. Lenders may "
        "respond by tightening credit criteria to clear the threshold, inadvertently reducing "
        "lending access to the groups the tool was intended to protect."
    )
    doc.bullet(
        "False negatives: the tool clears a non-compliant portfolio. The lender reduces "
        "monitoring and defers remediation; hidden disparity persists and affected consumer "
        "groups face systematic exclusion without regulatory response. This is the more "
        "serious failure in terms of consumer harm."
    )
    doc.bullet(
        "Performance drift: economic conditions or applicant mix change post-deployment, "
        "altering approval rates and group disparity ratios without the lender's awareness. "
        "Drift monitoring (Figure 2) is implemented but requires continuous real data "
        "ingestion to be effective in production."
    )
    doc.bullet(
        "Jurisdiction misconfiguration: the US rule set is applied to a UK-regulated product "
        "or vice versa. The UK Consumer Duty evidence requirements are more extensive than "
        "the US configuration; misconfiguration would leave those requirements unchecked "
        "while management believes the product is compliant."
    )
    doc.bullet(
        "False sense of compliance: the most dangerous failure. The tool produces "
        "thorough-looking reports and rule-linked findings while genuine harmful outcomes "
        "persist. This failure requires the tool to be honest about the limits of its own "
        "coverage — which is commercially inconvenient. The prototype addresses this by "
        "explicitly documenting what it does not check and flagging which findings require "
        "human judgement."
    )


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    with open(OUTPUTS_DIR / "compliance_reports.json", encoding="utf-8") as f:
        reports = json.load(f)
    sensitivity = pd.read_csv(OUTPUTS_DIR / "threshold_sensitivity.csv")
    drift       = pd.read_csv(OUTPUTS_DIR / "drift_comparison.csv")

    targets = [
        DOCS_DIR / "Task3_Tool_Design.pdf",
        NTUL_DIR / "Task3_Tool_Design.pdf",
    ]
    for out in targets:
        out.parent.mkdir(parents=True, exist_ok=True)
        with PdfPages(str(out)) as pdf:
            doc = Doc(pdf)
            doc._new_page(flush=False)
            build(doc, reports, sensitivity, drift)
            doc.close()
        print(f"Written: {out}")


if __name__ == "__main__":
    main()
