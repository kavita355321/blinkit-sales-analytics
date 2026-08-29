"""Regression tests for the Blinkit cleaning and KPI workflow."""

import unittest

from python.blinkit_analysis import calculate_kpis, load_and_clean_data


class BlinkitAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_and_clean_data()

    def test_expected_row_count(self) -> None:
        self.assertEqual(len(self.data), 8_523)

    def test_fat_content_is_standardised(self) -> None:
        self.assertEqual(
            set(self.data["item_fat_content"].dropna().unique()),
            {"Low Fat", "Regular"},
        )

    def test_sales_has_no_missing_values(self) -> None:
        self.assertFalse(self.data["sales"].isna().any())

    def test_total_sales_regression(self) -> None:
        kpis = calculate_kpis(self.data).set_index("metric")["value"]
        self.assertAlmostEqual(kpis["Total Sales"], 1_201_681.4808, places=4)

    def test_exact_duplicates_are_removed(self) -> None:
        self.assertEqual(int(self.data.duplicated().sum()), 0)


if __name__ == "__main__":
    unittest.main()

