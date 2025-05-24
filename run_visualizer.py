from email_template import capture_visualization
import json

def main():
    # Sample analysis results for testing
    analysis_results = {
        'lensing_apertures': 12,
        'convergence_points': 1500,
        'spectral_accuracy': 0.95,
        'visualization_quality': 0.92,
        'atmospheric_composition': {
            'primary_gases': {
                'CO2': {'concentration': 0.35, 'confidence': 0.95},
                'O2': {'concentration': 0.21, 'confidence': 0.98},
                'N2': {'concentration': 0.78, 'confidence': 0.99},
                'CH4': {'concentration': 0.001, 'confidence': 0.92}
            }
        },
        'marine_life': {
            'phytoplankton': {
                'concentration': 0.15,
                'confidence': 0.88,
                'species_diversity': 0.75
            }
        },
        'terrestrial_life': {
            'vegetation': {
                'coverage': 0.65,
                'diversity': 0.82,
                'dominant_types': ['gymnosperms', 'ferns']
            }
        }
    }

    # Time periods to visualize
    time_periods = ['early_earth', 'archaean', 'proterozoic', 'cambrian', 'triassic', 'cretaceous']

    print("Starting visualization generation...")
    
    for period in time_periods:
        print(f"\nGenerating visualization for {period}...")
        filepath = capture_visualization(analysis_results, period)
        if filepath:
            print(f"Successfully created visualization: {filepath}")
        else:
            print(f"Failed to create visualization for {period}")

if __name__ == "__main__":
    main() 