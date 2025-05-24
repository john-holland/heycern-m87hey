import requests
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body

class AstronomicalDataFetcher:
    def __init__(self):
        self.eht_data_url = "https://eventhorizontelescope.org/data"
        self.jpl_horizons_url = "https://ssd-api.jpl.nasa.gov/horizons.api"
        self.m87_coords = SkyCoord('12h30m49.42338s', '+12d23m28.0439s', frame='icrs')
        
        # Focused time periods from early Earth to dinosaur era
        self.earth_historical_data = {
            'early_earth': {
                'time': -4500000000,  # 4.5 billion years ago
                'spectrum': self._generate_early_earth_spectrum(),
                'description': 'Early Earth, shortly after formation, with intense volcanic activity and no atmosphere',
                'atmospheric_composition': {
                    'CO2': 0.98,
                    'N2': 0.01,
                    'H2O': 0.01
                }
            },
            'archaean': {
                'time': -3500000000,  # 3.5 billion years ago
                'spectrum': self._generate_archaean_spectrum(),
                'description': 'Archaean Earth with first signs of life and reducing atmosphere',
                'atmospheric_composition': {
                    'CO2': 0.70,
                    'N2': 0.20,
                    'CH4': 0.05,
                    'H2O': 0.05
                }
            },
            'proterozoic': {
                'time': -2000000000,  # 2 billion years ago
                'spectrum': self._generate_proterozoic_spectrum(),
                'description': 'Proterozoic Earth with first oxygen-producing organisms',
                'atmospheric_composition': {
                    'CO2': 0.30,
                    'N2': 0.60,
                    'O2': 0.05,
                    'H2O': 0.05
                }
            },
            'cambrian': {
                'time': -500000000,  # 500 million years ago
                'spectrum': self._generate_cambrian_spectrum(),
                'description': 'Cambrian Earth with explosion of complex life',
                'atmospheric_composition': {
                    'CO2': 0.15,
                    'N2': 0.70,
                    'O2': 0.10,
                    'H2O': 0.05
                }
            },
            'triassic': {
                'time': -200000000,  # 200 million years ago
                'spectrum': self._generate_triassic_spectrum(),
                'description': 'Triassic Earth with first dinosaurs and gymnosperms',
                'atmospheric_composition': {
                    'CO2': 0.20,
                    'N2': 0.65,
                    'O2': 0.10,
                    'H2O': 0.05
                }
            },
            'cretaceous': {
                'time': -65000000,  # 65 million years ago
                'spectrum': self._generate_cretaceous_spectrum(),
                'description': 'Late Cretaceous Earth with diverse dinosaurs and flowering plants',
                'atmospheric_composition': {
                    'CO2': 0.15,
                    'N2': 0.70,
                    'O2': 0.10,
                    'H2O': 0.05
                }
            }
        }
        
    def fetch_m87_lensing_data(self):
        """Fetch gravitational lensing data from M87."""
        try:
            print("Fetching M87 gravitational lensing data...")
            # Enhanced simulated data with more precise parameters
            return {
                'black_hole_mass': 6.5e9 * u.M_sun,
                'distance': 53.5e6 * u.lightyear,
                'position': self.m87_coords,
                'lensing_parameters': {
                    'einstein_radius': 0.1 * u.arcsec,
                    'shear': 0.1,
                    'convergence': 0.2,
                    'accretion_disk_orientation': 17 * u.deg,  # Known orientation
                    'jet_angle': 288 * u.deg  # Known jet angle
                }
            }
        except Exception as e:
            print(f"Error fetching M87 data: {e}")
            return None

    def calculate_earth_position(self, time_years_ago=0):
        """Calculate Earth's position relative to M87 at a given time."""
        try:
            # Convert years ago to Julian date
            current_time = Time.now()
            target_time = current_time - time_years_ago * u.year
            
            # Get Earth's position at that time
            with solar_system_ephemeris.set('jpl'):
                earth_pos = get_body('earth', target_time)
            
            # Calculate vector from Earth to M87
            earth_to_m87 = self.m87_coords.cartesian - earth_pos.cartesian
            
            return {
                'position': earth_pos,
                'vector_to_m87': earth_to_m87,
                'distance': earth_to_m87.norm(),
                'time': target_time
            }
        except Exception as e:
            print(f"Error calculating Earth position: {e}")
            return None

    def fetch_historical_earth_data(self, time_period):
        """Fetch Earth data for a specific historical period."""
        if time_period in self.earth_historical_data:
            data = self.earth_historical_data[time_period]
            position_data = self.calculate_earth_position(abs(data['time']))
            return {
                'spectrum': data['spectrum'],
                'description': data['description'],
                'position': position_data,
                'time_period': time_period,
                'atmospheric_composition': data['atmospheric_composition']
            }
        return None

    def _generate_early_earth_spectrum(self):
        """Generate spectrum data for early Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Intense thermal emission from molten surface
        spectrum[wavelengths > 1000] *= 2.0
        # Strong CO2 absorption
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 0.3
        # Volcanic ash absorption
        spectrum[(wavelengths > 600) & (wavelengths < 800)] *= 0.7
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def _generate_archaean_spectrum(self):
        """Generate spectrum data for Archaean Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Methane absorption bands
        spectrum[(wavelengths > 700) & (wavelengths < 800)] *= 0.6
        # CO2 absorption
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 0.5
        # First signs of biological activity
        spectrum[(wavelengths > 500) & (wavelengths < 600)] *= 1.2
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def _generate_proterozoic_spectrum(self):
        """Generate spectrum data for Proterozoic Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Oxygen absorption bands
        spectrum[(wavelengths > 600) & (wavelengths < 700)] *= 0.8
        # Reduced CO2 absorption
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 0.7
        # Increased biological activity
        spectrum[(wavelengths > 500) & (wavelengths < 600)] *= 1.3
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def _generate_cambrian_spectrum(self):
        """Generate spectrum data for Cambrian Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Complex biological signatures
        spectrum[(wavelengths > 500) & (wavelengths < 700)] *= 1.4
        # Oxygen absorption
        spectrum[(wavelengths > 600) & (wavelengths < 700)] *= 0.9
        # Ocean reflection
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 1.2
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def _generate_triassic_spectrum(self):
        """Generate spectrum data for Triassic Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Gymnosperm vegetation signature
        spectrum[(wavelengths > 500) & (wavelengths < 700)] *= 1.3
        # Desert and arid region signatures
        spectrum[(wavelengths > 700) & (wavelengths < 900)] *= 1.2
        # Atmospheric composition
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 0.8
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def _generate_cretaceous_spectrum(self):
        """Generate spectrum data for Cretaceous Earth."""
        wavelengths = np.linspace(200, 2000, 1000)
        spectrum = np.ones_like(wavelengths)
        # Flowering plant signatures
        spectrum[(wavelengths > 500) & (wavelengths < 700)] *= 1.5
        # Tropical forest signatures
        spectrum[(wavelengths > 600) & (wavelengths < 800)] *= 1.3
        # Ocean signatures
        spectrum[(wavelengths > 400) & (wavelengths < 500)] *= 1.2
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def validate_data_quality(self, data):
        """Validate the quality and completeness of the data."""
        required_fields = {
            'm87_data': ['black_hole_mass', 'distance', 'position', 'lensing_parameters'],
            'earth_data': ['spectrum', 'position', 'description'],
            'position_data': ['position', 'vector_to_m87', 'distance', 'time']
        }
        
        validation_results = {
            'is_valid': True,
            'missing_fields': [],
            'quality_score': 0.0
        }
        
        # Check for required fields
        for category, fields in required_fields.items():
            if category in data:
                for field in fields:
                    if field not in data[category]:
                        validation_results['is_valid'] = False
                        validation_results['missing_fields'].append(f"{category}.{field}")
        
        # Calculate quality score based on data completeness and precision
        if validation_results['is_valid']:
            validation_results['quality_score'] = self._calculate_quality_score(data)
        
        return validation_results

    def _calculate_quality_score(self, data):
        """Calculate a quality score for the data."""
        score = 1.0
        
        # Check position precision
        if 'position' in data.get('m87_data', {}):
            score *= 0.9  # M87 position is well-known
        
        # Check spectrum quality
        if 'spectrum' in data.get('earth_data', {}):
            spectrum = data['earth_data']['spectrum']
            if len(spectrum['wavelengths']) > 500:
                score *= 0.95
        
        return score

    def fetch_solar_system_data(self):
        """Fetch current positions and data of Solar System bodies."""
        try:
            # Simulated data for demonstration
            bodies = {
                'Earth': {
                    'position': [1.0, 0.0, 0.0],  # AU
                    'velocity': [0.0, 29.78, 0.0],  # km/s
                    'spectrum': self._generate_earth_spectrum()
                },
                'Sun': {
                    'position': [0.0, 0.0, 0.0],
                    'velocity': [0.0, 0.0, 0.0],
                    'spectrum': self._generate_sun_spectrum()
                }
            }
            return bodies
        except Exception as e:
            print(f"Error fetching Solar System data: {e}")
            return None

    def _generate_sun_spectrum(self):
        """Generate simulated Sun spectrum data."""
        wavelengths = np.linspace(200, 2000, 1000)  # nm
        # Blackbody-like spectrum
        spectrum = 1e4 * np.exp(-wavelengths/500)
        return {'wavelengths': wavelengths, 'intensity': spectrum}

    def fetch_spectrographic_data(self, target, time_range):
        """Fetch spectrographic data for a specific target and time range."""
        try:
            # Simulated spectrographic data
            return {
                'target': target,
                'time_range': time_range,
                'data': self._generate_earth_spectrum()  # Using Earth spectrum as example
            }
        except Exception as e:
            print(f"Error fetching spectrographic data: {e}")
            return None 