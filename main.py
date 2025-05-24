import numpy as np
import matplotlib.pyplot as plt
from data_fetcher import AstronomicalDataFetcher
from lensing_processor import GravitationalLensingProcessor
from ml_enhancer import MLEnhancer
from datetime import datetime, timedelta
import os

def generate_visualization(time_period, data_fetcher, lensing_processor, ml_enhancer):
    """Generate visualization for a specific time period."""
    print(f"\nGenerating visualization for {time_period}...")
    
    # Fetch and validate data
    m87_data = data_fetcher.fetch_m87_lensing_data()
    earth_data = data_fetcher.fetch_historical_earth_data(time_period)
    
    # Validate data quality
    validation = data_fetcher.validate_data_quality({
        'm87_data': m87_data,
        'earth_data': earth_data
    })
    
    if not validation['is_valid']:
        print(f"Warning: Data validation failed. Missing fields: {validation['missing_fields']}")
        if validation['quality_score'] < 0.5:
            print("Data quality too low to proceed.")
            return None
    
    # Process spectrum through lensing
    processed_spectrum = lensing_processor.process_spectrum(earth_data['spectrum'])
    
    # Create detailed prompt based on atmospheric composition
    atm_comp = earth_data['atmospheric_composition']
    atm_desc = ", ".join([f"{gas}: {pct*100:.1f}%" for gas, pct in atm_comp.items()])
    
    prompt = f"{earth_data['description']} as seen through the gravitational lensing effect of the M87 black hole. "
    prompt += f"Atmospheric composition: {atm_desc}. "
    prompt += "The image should show accurate spectral data and astronomical features, "
    prompt += "with visible atmospheric effects and surface characteristics appropriate for this time period."
    
    # Generate visualization
    initial_image = ml_enhancer.generate_enhanced_visualization(prompt)
    
    # Enhance with spectrographic data
    enhanced_image = ml_enhancer.enhance_image(initial_image, processed_spectrum)
    
    return enhanced_image, earth_data['description']

def main():
    # Create output directory
    os.makedirs('visualizations', exist_ok=True)
    
    # Initialize components
    data_fetcher = AstronomicalDataFetcher()
    ml_enhancer = MLEnhancer()
    
    # Fetch M87 data
    print("Fetching M87 data...")
    m87_data = data_fetcher.fetch_m87_lensing_data()
    lensing_processor = GravitationalLensingProcessor(m87_data)
    
    # Generate visualizations for different time periods
    time_periods = [
        'early_earth',    # 4.5 billion years ago
        'archaean',       # 3.5 billion years ago
        'proterozoic',    # 2 billion years ago
        'cambrian',       # 500 million years ago
        'triassic',       # 200 million years ago
        'cretaceous'      # 65 million years ago
    ]
    
    # Create a figure to display all visualizations
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()
    
    for idx, period in enumerate(time_periods):
        result = generate_visualization(period, data_fetcher, lensing_processor, ml_enhancer)
        if result is not None:
            image, description = result
            # Save individual visualization
            output_path = f'visualizations/m87_lensed_earth_{period}.png'
            plt.figure(figsize=(12, 8))
            plt.imshow(image)
            plt.axis('off')
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            
            # Add to combined visualization
            axes[idx].imshow(image)
            axes[idx].axis('off')
            axes[idx].set_title(description, fontsize=10)
            print(f"Saved visualization to {output_path}")
    
    # Save combined visualization
    plt.tight_layout()
    plt.savefig('visualizations/m87_lensed_earth_evolution.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    print("\nVisualization complete! Check the 'visualizations' directory for results.")
    print("Individual period visualizations and a combined evolution visualization have been created.")

if __name__ == "__main__":
    main() 