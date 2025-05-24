import numpy as np
from astropy import units as u
from scipy.ndimage import gaussian_filter

class GravitationalLensingProcessor:
    def __init__(self, lensing_data):
        self.lensing_data = lensing_data
        self.einstein_radius = lensing_data['lensing_parameters']['einstein_radius']
        self.shear = lensing_data['lensing_parameters']['shear']
        self.convergence = lensing_data['lensing_parameters']['convergence']

    def calculate_lensing_effect(self, source_position, source_image):
        """
        Calculate the gravitational lensing effect on a source image.
        
        Args:
            source_position: Position of the source relative to the lens
            source_image: 2D array representing the source image
            
        Returns:
            Lensed image
        """
        # Convert source position to angular coordinates
        theta_x, theta_y = source_position
        
        # Calculate deflection angle
        deflection = self._calculate_deflection(theta_x, theta_y)
        
        # Apply lensing transformation
        lensed_image = self._apply_lensing_transform(source_image, deflection)
        
        return lensed_image

    def _calculate_deflection(self, theta_x, theta_y):
        """Calculate the deflection angle for a given source position."""
        # Simple point mass lens model
        theta = np.sqrt(theta_x**2 + theta_y**2)
        deflection_magnitude = self.einstein_radius**2 / theta
        
        # Add shear effect
        deflection_x = deflection_magnitude * theta_x/theta + self.shear * theta_x
        deflection_y = deflection_magnitude * theta_y/theta + self.shear * theta_y
        
        return deflection_x, deflection_y

    def _apply_lensing_transform(self, image, deflection):
        """Apply the lensing transformation to the image."""
        # Create coordinate grids
        y, x = np.indices(image.shape)
        
        # Apply deflection
        x_deflected = x + deflection[0]
        y_deflected = y + deflection[1]
        
        # Interpolate the image at the deflected positions
        from scipy.interpolate import griddata
        points = np.column_stack((x.flatten(), y.flatten()))
        values = image.flatten()
        xi = np.column_stack((x_deflected.flatten(), y_deflected.flatten()))
        
        lensed = griddata(points, values, xi, method='linear', fill_value=0)
        lensed = lensed.reshape(image.shape)
        
        # Apply magnification
        magnification = 1 / (1 - self.convergence)**2
        lensed *= magnification
        
        return lensed

    def process_spectrum(self, spectrum):
        """
        Process spectrographic data through the lensing effect.
        
        Args:
            spectrum: Dictionary containing wavelength and intensity data
            
        Returns:
            Processed spectrum
        """
        wavelengths = spectrum['wavelengths']
        intensity = spectrum['intensity']
        
        # Apply redshift due to gravitational lensing
        z = 0.00436  # M87 redshift
        redshifted_wavelengths = wavelengths * (1 + z)
        
        # Apply gravitational lensing effects to the spectrum
        # This is a simplified model
        processed_intensity = intensity * (1 + self.convergence)
        
        return {
            'wavelengths': redshifted_wavelengths,
            'intensity': processed_intensity
        } 