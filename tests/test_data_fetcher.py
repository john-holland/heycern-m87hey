import unittest
import numpy as np
from astropy import units as u
from data_fetcher import AstronomicalDataFetcher

class TestAstronomicalDataFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = AstronomicalDataFetcher()

    def test_m87_data_structure(self):
        """Test that M87 data has all required fields and correct units."""
        data = self.fetcher.fetch_m87_lensing_data()
        
        self.assertIsNotNone(data)
        self.assertIn('black_hole_mass', data)
        self.assertIn('distance', data)
        self.assertIn('position', data)
        self.assertIn('lensing_parameters', data)
        
        # Check units
        self.assertTrue(isinstance(data['black_hole_mass'], u.Quantity))
        self.assertTrue(isinstance(data['distance'], u.Quantity))
        
        # Check lensing parameters
        params = data['lensing_parameters']
        self.assertIn('einstein_radius', params)
        self.assertIn('shear', params)
        self.assertIn('convergence', params)
        self.assertIn('accretion_disk_orientation', params)
        self.assertIn('jet_angle', params)

    def test_historical_earth_data(self):
        """Test historical Earth data for different time periods."""
        time_periods = ['early_earth', 'archaean', 'proterozoic', 
                       'cambrian', 'triassic', 'cretaceous']
        
        for period in time_periods:
            data = self.fetcher.fetch_historical_earth_data(period)
            
            self.assertIsNotNone(data)
            self.assertIn('spectrum', data)
            self.assertIn('description', data)
            self.assertIn('position', data)
            self.assertIn('atmospheric_composition', data)
            
            # Check spectrum data
            spectrum = data['spectrum']
            self.assertIn('wavelengths', spectrum)
            self.assertIn('intensity', spectrum)
            self.assertEqual(len(spectrum['wavelengths']), len(spectrum['intensity']))
            
            # Check atmospheric composition
            atm_comp = data['atmospheric_composition']
            self.assertIsInstance(atm_comp, dict)
            total = sum(atm_comp.values())
            self.assertAlmostEqual(total, 1.0, places=2)

    def test_spectrum_generation(self):
        """Test spectrum generation for different time periods."""
        # Test early Earth spectrum
        early_spectrum = self.fetcher._generate_early_earth_spectrum()
        self._validate_spectrum(early_spectrum)
        self.assertTrue(np.any(early_spectrum['intensity'] > 1.5))  # Check for thermal emission
        
        # Test Cretaceous spectrum
        cretaceous_spectrum = self.fetcher._generate_cretaceous_spectrum()
        self._validate_spectrum(cretaceous_spectrum)
        self.assertTrue(np.any(cretaceous_spectrum['intensity'] > 1.3))  # Check for vegetation

    def _validate_spectrum(self, spectrum):
        """Helper method to validate spectrum structure."""
        self.assertIn('wavelengths', spectrum)
        self.assertIn('intensity', spectrum)
        self.assertEqual(len(spectrum['wavelengths']), len(spectrum['intensity']))
        self.assertTrue(np.all(spectrum['intensity'] >= 0))
        self.assertTrue(np.all(np.isfinite(spectrum['intensity'])))

    def test_data_quality_validation(self):
        """Test data quality validation."""
        test_data = {
            'm87_data': self.fetcher.fetch_m87_lensing_data(),
            'earth_data': self.fetcher.fetch_historical_earth_data('cretaceous')
        }
        
        validation = self.fetcher.validate_data_quality(test_data)
        
        self.assertIn('is_valid', validation)
        self.assertIn('missing_fields', validation)
        self.assertIn('quality_score', validation)
        self.assertTrue(validation['is_valid'])
        self.assertGreater(validation['quality_score'], 0.5)

if __name__ == '__main__':
    unittest.main() 