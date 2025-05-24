import unittest
import numpy as np
from astropy import units as u
from lensing_processor import GravitationalLensingProcessor

class TestGravitationalLensingProcessor(unittest.TestCase):
    def setUp(self):
        # Create test lensing data
        self.lensing_data = {
            'lensing_parameters': {
                'einstein_radius': 0.1 * u.arcsec,
                'shear': 0.1,
                'convergence': 0.2
            }
        }
        self.processor = GravitationalLensingProcessor(self.lensing_data)

    def test_lensing_effect_calculation(self):
        """Test the calculation of lensing effects on an image."""
        # Create a test image
        test_image = np.ones((100, 100))
        source_position = (0.5, 0.5)  # arcseconds
        
        # Calculate lensing effect
        lensed_image = self.processor.calculate_lensing_effect(source_position, test_image)
        
        # Check output
        self.assertEqual(lensed_image.shape, test_image.shape)
        self.assertTrue(np.all(np.isfinite(lensed_image)))
        self.assertTrue(np.all(lensed_image >= 0))

    def test_deflection_calculation(self):
        """Test the calculation of deflection angles."""
        # Test different source positions
        test_positions = [
            (0.1, 0.1),
            (0.5, 0.5),
            (1.0, 1.0)
        ]
        
        for pos in test_positions:
            deflection = self.processor._calculate_deflection(pos[0], pos[1])
            
            # Check deflection structure
            self.assertEqual(len(deflection), 2)
            self.assertTrue(np.all(np.isfinite(deflection)))
            
            # Check deflection magnitude
            deflection_magnitude = np.sqrt(deflection[0]**2 + deflection[1]**2)
            self.assertGreater(deflection_magnitude, 0)

    def test_spectrum_processing(self):
        """Test the processing of spectrographic data."""
        # Create test spectrum
        test_spectrum = {
            'wavelengths': np.linspace(300, 1000, 1000),
            'intensity': np.ones(1000)
        }
        
        # Process spectrum
        processed_spectrum = self.processor.process_spectrum(test_spectrum)
        
        # Check output structure
        self.assertIn('wavelengths', processed_spectrum)
        self.assertIn('intensity', processed_spectrum)
        
        # Check wavelength shift
        self.assertTrue(np.all(processed_spectrum['wavelengths'] > test_spectrum['wavelengths']))
        
        # Check intensity modification
        self.assertTrue(np.all(processed_spectrum['intensity'] > 0))
        self.assertTrue(np.all(np.isfinite(processed_spectrum['intensity'])))

    def test_lensing_transform(self):
        """Test the lensing transformation application."""
        # Create test image
        test_image = np.ones((100, 100))
        deflection = (0.1, 0.1)
        
        # Apply transformation
        transformed = self.processor._apply_lensing_transform(test_image, deflection)
        
        # Check output
        self.assertEqual(transformed.shape, test_image.shape)
        self.assertTrue(np.all(np.isfinite(transformed)))
        self.assertTrue(np.all(transformed >= 0))

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test zero deflection
        test_image = np.ones((100, 100))
        zero_deflection = (0.0, 0.0)
        transformed = self.processor._apply_lensing_transform(test_image, zero_deflection)
        np.testing.assert_array_almost_equal(transformed, test_image)
        
        # Test large deflection
        large_deflection = (10.0, 10.0)
        transformed = self.processor._apply_lensing_transform(test_image, large_deflection)
        self.assertEqual(transformed.shape, test_image.shape)
        self.assertTrue(np.all(np.isfinite(transformed)))

if __name__ == '__main__':
    unittest.main() 