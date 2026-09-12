import unittest

from tools.build_source_review_queue import build_queue


def entry(entry_id, zh, *, status="source_attributed", source="tw-judicial", domains=None, kind="unclassified", flags=None):
    return {
        "id": entry_id,
        "forms": {"zh_Hant": zh, "zh_Hans": zh, "en": "Example"},
        "references": [{"source_id": source, "record": "1", "context": "ctx"}],
        "domains": domains or ["unclassified"],
        "domain_basis": "automatic_keyword_rules",
        "kind": kind,
        "kind_basis": "automatic_surface_rules",
        "jurisdictions": [],
        "jurisdiction_basis": "not_assessed",
        "status": status,
        "flags": flags or [],
        "review": {"translation": "source_attributed"},
    }


class SourceReviewQueueTests(unittest.TestCase):
    def test_core_homograph_outranks_source_only_group(self):
        entries = [
            entry("cn-a", "法人", status="evidence_linked", source="oll-cn-core", domains=["civil"], kind="term"),
            entry("tw-a", "法人"),
            entry("tw-b", "上诉", source="tw-judicial"),
            entry("tm-b", "上诉", source="tw-tipo-trademark", domains=["intellectual_property"]),
        ]
        report = build_queue(entries)
        self.assertEqual(report["homograph_review_groups"][0]["zh_Hans"], "法人")
        self.assertIn("homograph_with_reviewed_or_editorial_entry", report["homograph_review_groups"][0]["reasons"])

    def test_unclassified_high_value_single_is_queued(self):
        report = build_queue([entry("tw-law", "某某法", kind="statute")])
        self.assertEqual(report["single_high_value_candidates"][0]["entry"]["id"], "tw-law")
        self.assertEqual(report["single_high_value_candidates_total"], 1)

    def test_low_risk_classified_single_is_not_queued(self):
        report = build_queue([entry("tw-low", "普通词", domains=["civil"], kind="unclassified")])
        self.assertEqual(report["single_high_value_candidates_total"], 0)


if __name__ == "__main__":
    unittest.main()
