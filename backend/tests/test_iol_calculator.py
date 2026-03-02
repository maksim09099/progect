import unittest

from backend.iol_calculator import EyeBiometry, LensConstants, recommended_iol_power


class IOLCalculatorTests(unittest.TestCase):
    def test_recommended_output_structure(self):
        bio = EyeBiometry(k1=43.5, k2=44.1, acd=3.2, axial_length=23.9)
        result = recommended_iol_power(bio)

        self.assertIn("srk_t_like", result)
        self.assertIn("haigis_like", result)
        self.assertIn("recommended", result)

    def test_deterministic_result(self):
        bio = EyeBiometry(k1=42.0, k2=43.0, acd=3.0, axial_length=24.0)
        r1 = recommended_iol_power(bio)
        r2 = recommended_iol_power(bio)

        self.assertEqual(r1, r2)

    def test_custom_lens_constants_affect_result(self):
        bio = EyeBiometry(k1=43.0, k2=44.0, acd=3.1, axial_length=23.5)
        default_result = recommended_iol_power(bio)

        custom_lens = LensConstants(a_const=118.0, haigis_a0=1.2, haigis_a1=0.35, haigis_a2=0.12)
        custom_result = recommended_iol_power(bio, custom_lens)

        self.assertNotEqual(default_result["recommended"], custom_result["recommended"])


if __name__ == "__main__":
    unittest.main()
