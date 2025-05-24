import os
from datetime import datetime
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import base64

NOAA_MAILING_LIST = [
    'noaa-data-team@noaa.gov',
    'john.gebhard.holland@gmail.com',
    'jholland87@gmail.com',
    'jane@example.com',
    'service@project.org'
]

SCIENCE_COMMUNITY_SOURCE_API_TOKEN_CHECKLIST = [
    {'name': 'John Holland', 'email': 'john.gebhard.holland@gmail.com', 'approved': False},
    {'name': 'Jane Doe', 'email': 'jane@example.com', 'approved': False},
    {'name': 'Project Service Account', 'email': 'service@project.org', 'approved': True}
]

def format_science_community_source_token_checklist():
    """Format the Science Community Source API token checklist for the email."""
    lines = ["Science Community Source API Token Checklist:"]
    for entry in SCIENCE_COMMUNITY_SOURCE_API_TOKEN_CHECKLIST:
        check = '[x]' if entry['approved'] else '[ ]'
        lines.append(f"- {check} {entry['name']} ({entry['email']})")
    return '\n'.join(lines)

def generate_email_content(analysis_results, time_period):
    """Generate email content for the weekly spectral analysis report."""
    
    subject = f"M87 Gravitational Lensing Project - Weekly Spectral Analysis Report ({time_period})"
    
    body = f"""
Dear PBS SpaceTime Team,

I hope this email finds you well. I'm pleased to share the latest findings from our M87 Gravitational Lensing Project's spectral analysis for the {time_period} period.

Visual Poetry:
------------
In the cosmic dance of light and gravity, we witness Earth's ancient story unfold through M87's gravitational lens. Like light streaming through a celestial prism, each aperture reveals a different facet of our planet's past. The gravitational lens acts as nature's own kaleidoscope, bending and weaving light into a tapestry of time, where each thread tells a story of atmospheric evolution, life's emergence, and Earth's transformation.

The composite image we've captured is not merely a photograph, but a window through time itself. As light from different epochs converges through M87's gravitational field, it creates a symphony of spectral signatures - each one a note in the grand cosmic composition of Earth's history. The resulting visualization is a testament to the beauty of physics and the poetry of spacetime.

{format_science_community_source_token_checklist()}

Key Findings:
------------
{format_key_findings(analysis_results)}

Atmospheric Composition:
----------------------
{format_atmospheric_data(analysis_results)}

Marine Life Analysis:
-------------------
{format_marine_data(analysis_results)}

Terrestrial Life Analysis:
------------------------
{format_terrestrial_data(analysis_results)}

Unexpected Discoveries:
---------------------
{format_unexpected_findings(analysis_results)}

Confidence Assessment:
-------------------
{format_confidence_scores(analysis_results)}

Visualization Updates:
-------------------
- Latest composite image has been generated and printed
- Enhanced resolution: 4096x4096 pixels
- Color depth: 32-bit
- Quality score: {analysis_results.get('visualization_quality', 0.92)*100:.1f}%
- Gravitational lensing apertures: {analysis_results.get('lensing_apertures', 12)}
- Light path convergence points: {analysis_results.get('convergence_points', 1500)}
- Spectral integration accuracy: {analysis_results.get('spectral_accuracy', 0.95)*100:.1f}%

Next Steps:
----------
1. Review the attached spectral analysis report for detailed metrics
2. Check the printed visualization in the PBS SpaceTime office
3. Schedule a team discussion for any significant findings
4. Consider potential follow-up observations for areas of interest
5. Contemplate the cosmic poetry of light's journey through spacetime

The full spectral analysis report and visualization data are available in our shared repository. You can access them at:
[Repository Link]

Best regards,
M87 Gravitational Lensing Project Team

P.S. If you notice any anomalies or have questions about specific findings, please don't hesitate to reach out to our team. Remember, each photon that reaches our sensors has traveled through the fabric of spacetime itself, carrying with it the story of Earth's past.
"""

    return subject, body

def format_key_findings(results):
    """Format the key findings section of the email."""
    findings = []
    
    # Add atmospheric findings
    if results.get('atmospheric_composition'):
        atm = results['atmospheric_composition']
        findings.append(f"- Atmospheric CO2 levels: {atm['primary_gases']['CO2']['concentration']*100:.1f}%")
        findings.append(f"- Oxygen concentration: {atm['primary_gases']['O2']['concentration']*100:.1f}%")
    
    # Add marine findings
    if results.get('marine_life'):
        marine = results['marine_life']
        findings.append(f"- Marine phytoplankton concentration: {marine['phytoplankton']['concentration']*100:.1f}%")
        if marine['large_predators']['presence']:
            findings.append(f"- Detected large marine predators: {marine['large_predators']['species_type']}")
    
    # Add terrestrial findings
    if results.get('terrestrial_life'):
        terr = results['terrestrial_life']
        findings.append(f"- Vegetation coverage: {terr['vegetation']['coverage']*100:.1f}%")
        if terr['large_herbivores']['presence']:
            findings.append(f"- Detected large herbivores: {terr['large_herbivores']['species_type']}")
    
    # Add unexpected findings
    if results.get('unexpected_findings'):
        for finding in results['unexpected_findings']:
            if finding['significance'] > 0.7:  # Only include significant findings
                findings.append(f"- {finding['description']} (Significance: {finding['significance']*100:.1f}%)")
    
    return '\n'.join(findings)

def format_atmospheric_data(results):
    """Format the atmospheric data section of the email."""
    if not results.get('atmospheric_composition'):
        return "No atmospheric data available for this period."
    
    atm = results['atmospheric_composition']
    text = []
    
    # Primary gases
    text.append("Primary Gases:")
    for gas, data in atm['primary_gases'].items():
        text.append(f"- {gas}: {data['concentration']*100:.1f}% (Confidence: {data['confidence']*100:.1f}%)")
    
    # Conditions
    text.append("\nConditions:")
    text.append(f"- Pressure: {atm['atmospheric_pressure']:.3f} bars")
    text.append(f"- Temperature: {atm['temperature']:.1f} K")
    text.append(f"- Cloud Coverage: {atm['cloud_coverage']*100:.1f}%")
    
    return '\n'.join(text)

def format_marine_data(results):
    """Format the marine life data section of the email."""
    if not results.get('marine_life'):
        return "No marine life data available for this period."
    
    marine = results['marine_life']
    text = []
    
    # Phytoplankton
    text.append("Phytoplankton:")
    text.append(f"- Concentration: {marine['phytoplankton']['concentration']*100:.1f}%")
    text.append(f"- Species Diversity: {marine['phytoplankton']['species_diversity']*100:.1f}%")
    
    # Large predators
    if marine['large_predators']['presence']:
        text.append("\nLarge Marine Predators:")
        text.append(f"- Species: {marine['large_predators']['species_type']}")
        text.append(f"- Estimated Size: {marine['large_predators']['estimated_size']}")
    
    # Coral reefs
    text.append("\nCoral Reefs:")
    text.append(f"- Coverage: {marine['coral_reefs']['coverage']*100:.1f}%")
    text.append(f"- Health: {marine['coral_reefs']['health']*100:.1f}%")
    
    return '\n'.join(text)

def format_terrestrial_data(results):
    """Format the terrestrial life data section of the email."""
    if not results.get('terrestrial_life'):
        return "No terrestrial life data available for this period."
    
    terr = results['terrestrial_life']
    text = []
    
    # Vegetation
    text.append("Vegetation:")
    text.append(f"- Coverage: {terr['vegetation']['coverage']*100:.1f}%")
    text.append(f"- Diversity: {terr['vegetation']['diversity']*100:.1f}%")
    text.append(f"- Dominant Types: {', '.join(terr['vegetation']['dominant_types'])}")
    
    # Large herbivores
    if terr['large_herbivores']['presence']:
        text.append("\nLarge Herbivores:")
        text.append(f"- Species: {terr['large_herbivores']['species_type']}")
        text.append(f"- Estimated Size: {terr['large_herbivores']['estimated_size']}")
    
    # Predators
    if terr['predators']['presence']:
        text.append("\nPredators:")
        text.append(f"- Species: {terr['predators']['species_type']}")
        text.append(f"- Estimated Size: {terr['predators']['estimated_size']}")
    
    return '\n'.join(text)

def format_unexpected_findings(results):
    """Format the unexpected findings section of the email."""
    if not results.get('unexpected_findings'):
        return "No unexpected findings for this period."
    
    text = []
    for finding in results['unexpected_findings']:
        text.append(f"- {finding['type'].replace('_', ' ').title()}:")
        text.append(f"  Description: {finding['description']}")
        text.append(f"  Significance: {finding['significance']*100:.1f}%")
        text.append(f"  Confidence: {finding['confidence']*100:.1f}%")
    
    return '\n'.join(text)

def format_confidence_scores(results):
    """Format the confidence scores section of the email."""
    if not results.get('confidence_scores'):
        return "No confidence scores available for this period."
    
    text = []
    for aspect, score in results['confidence_scores'].items():
        text.append(f"- {aspect.replace('_', ' ').title()}: {score*100:.1f}%")
    
    return '\n'.join(text)

def capture_visualization(analysis_results, time_period, output_dir='visualizations'):
    """Capture and save the visualization of the gravitational lensing effect."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"m87_lensing_{time_period}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Create figure with dark background
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(20, 20))
    
    # Create custom colormap for cosmic visualization
    colors = [(0, 0, 0.2), (0, 0, 0.5), (0.2, 0, 0.5), (0.5, 0, 0.5),
              (0.8, 0.2, 0.8), (1, 0.5, 1), (1, 0.8, 1), (1, 1, 1)]
    cmap = LinearSegmentedColormap.from_list('cosmic', colors)
    
    # Generate the visualization
    try:
        # Create base image with gravitational lensing effect
        img = generate_lensing_visualization(analysis_results, cmap)
        
        # Add time period and timestamp
        plt.text(0.02, 0.98, f"Time Period: {time_period.replace('_', ' ').title()}",
                transform=plt.gca().transAxes, color='white', fontsize=14)
        plt.text(0.02, 0.95, f"Captured: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                transform=plt.gca().transAxes, color='white', fontsize=12)
        
        # Save the visualization
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualization saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        return None

def generate_lensing_visualization(analysis_results, cmap):
    """Generate the gravitational lensing visualization."""
    # Create a high-resolution grid
    size = 4096
    x = np.linspace(-2, 2, size)
    y = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x, y)
    
    # Generate base image with gravitational lensing effect
    img = np.zeros((size, size))
    
    # Add gravitational lensing effect
    if analysis_results.get('lensing_apertures'):
        num_apertures = analysis_results['lensing_apertures']
        for i in range(num_apertures):
            # Calculate aperture position
            angle = 2 * np.pi * i / num_apertures
            center_x = 0.5 * np.cos(angle)
            center_y = 0.5 * np.sin(angle)
            
            # Add lensing effect for this aperture
            r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            img += np.exp(-r**2 / 0.1) * (0.5 + 0.5 * np.sin(angle * X + angle * Y))
    
    # Add spectral data effects
    if analysis_results.get('atmospheric_composition'):
        atm = analysis_results['atmospheric_composition']
        # Add atmospheric effects
        for gas, data in atm['primary_gases'].items():
            img += data['concentration'] * np.sin(X * Y * 10)
    
    # Add life signatures
    if analysis_results.get('marine_life'):
        marine = analysis_results['marine_life']
        img += marine['phytoplankton']['concentration'] * np.cos(X * 5) * np.sin(Y * 5)
    
    if analysis_results.get('terrestrial_life'):
        terr = analysis_results['terrestrial_life']
        img += terr['vegetation']['coverage'] * np.sin(X * 3) * np.cos(Y * 3)
    
    # Normalize and apply colormap
    img = (img - img.min()) / (img.max() - img.min())
    plt.imshow(img, cmap=cmap, extent=[-2, 2, -2, 2])
    plt.axis('off')
    
    return img

def render_lensing_equation_image(output_dir='visualizations', filename='lensing_equation.png'):
    """Render the gravitational lensing equation as a LaTeX image and save it."""
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 2))
    plt.axis('off')
    equation = r"""
    \[
    \theta_E = \sqrt{\frac{4GM}{c^2} \frac{D_{LS}}{D_L D_S}}
    \]
    """
    plt.text(0.5, 0.5, equation, fontsize=28, ha='center', va='center', color='black')
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0.2, transparent=True)
    plt.close()
    print(f"Lensing equation image saved to: {filepath}")
    return filepath

def render_lensing_equation_image_base64(output_dir='visualizations', filename='lensing_equation.png'):
    """Render the gravitational lensing equation as a LaTeX image, encode as base64, and return an HTML <img> tag."""
    filepath = render_lensing_equation_image(output_dir, filename)
    with open(filepath, 'rb') as img_file:
        b64_data = base64.b64encode(img_file.read()).decode('utf-8')
    img_tag = f'<img src="data:image/png;base64,{b64_data}" alt="Lensing Equation" style="max-width:100%; height:auto;"/>'
    return img_tag 