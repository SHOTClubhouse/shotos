import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRM = ROOT / "packs" / "win-the-work" / "crm"


def columns(name):
    with (CRM / name).open(encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    return rows


class CrmTemplateTests(unittest.TestCase):
    def test_templates_are_empty_headers_with_unique_fields(self):
        for name in (
            "qualification-sheet.csv",
            "hubspot-deals.csv",
            "salesforce-leads.csv",
            "salesforce-opportunities.csv",
        ):
            with self.subTest(name=name):
                rows = columns(name)
                self.assertEqual(len(rows), 1)
                self.assertTrue(all(field.strip() for field in rows[0]))
                self.assertEqual(len(rows[0]), len(set(rows[0])))

    def test_vendor_required_fields_and_method_fields_are_present(self):
        sheet = set(columns("qualification-sheet.csv")[0])
        hubspot = set(columns("hubspot-deals.csv")[0])
        leads = set(columns("salesforce-leads.csv")[0])
        opportunities = set(columns("salesforce-opportunities.csv")[0])
        self.assertTrue({"LEAP stage", "NUDGE decision", "Proposal ready", "Evidence URL"} <= sheet)
        self.assertTrue({"Deal name", "Pipeline", "Deal stage", "SHOTos LEAP stage", "SHOTos NUDGE decision"} <= hubspot)
        self.assertTrue({"Company", "Last Name", "Lead Status", "SHOTos_LEAP_Stage__c"} <= leads)
        self.assertTrue({"Name", "CloseDate", "StageName", "AccountId", "SHOTos_NUDGE_Decision__c"} <= opportunities)
        self.assertEqual({x for x in leads if x.startswith("SHOTos_")},
                         {x for x in opportunities if x.startswith("SHOTos_")})


if __name__ == "__main__":
    unittest.main()
