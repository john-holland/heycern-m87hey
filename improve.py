import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Any

class ImprovementManager:
    def __init__(self, config_path: str = '.cursor-improvements.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.improvement_areas = self.config['improvement_areas']
        self.improvement_rules = self.config['improvement_rules']
        self.automated_settings = self.config['automated_improvements']
        
    def analyze_test_results(self, coverage_report: str) -> Dict[str, float]:
        """Analyze test coverage and results to identify improvement areas."""
        with open(coverage_report, 'r') as f:
            coverage_data = json.load(f)
            
        improvement_scores = {}
        for area in self.improvement_areas:
            score = self._calculate_area_score(area, coverage_data)
            improvement_scores[area['name']] = score
            
        return improvement_scores
    
    def _calculate_area_score(self, area: Dict[str, Any], coverage_data: Dict[str, Any]) -> float:
        """Calculate improvement score for a specific area."""
        # Calculate coverage for target files
        file_coverage = 0
        for file in area['target_files']:
            if file in coverage_data['files']:
                file_coverage += coverage_data['files'][file]['coverage']
        
        # Calculate metric scores
        metric_scores = []
        for metric in area['metrics']:
            if metric in coverage_data['metrics']:
                metric_scores.append(coverage_data['metrics'][metric])
        
        # Combine scores
        if not metric_scores:
            return 0.0
            
        return (file_coverage + sum(metric_scores)) / (len(area['target_files']) + len(metric_scores))
    
    def generate_improvements(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate improvement suggestions based on scores."""
        improvements = []
        
        for area_name, score in scores.items():
            if score < self.automated_settings['review_threshold']:
                area = next(a for a in self.improvement_areas if a['name'] == area_name)
                improvement = self._create_improvement(area, score)
                if improvement:
                    improvements.append(improvement)
        
        return improvements[:self.automated_settings['max_improvements_per_run']]
    
    def _create_improvement(self, area: Dict[str, Any], score: float) -> Dict[str, Any]:
        """Create a specific improvement suggestion."""
        rules = self.improvement_rules[area['name']]
        
        improvement = {
            'area': area['name'],
            'description': area['description'],
            'target_files': area['target_files'],
            'current_score': score,
            'suggested_changes': []
        }
        
        # Add specific improvements based on rules
        if area['name'] == 'spectral_accuracy':
            improvement['suggested_changes'].extend([
                f"Increase wavelength resolution to {rules['min_wavelength_resolution']} nm",
                f"Add missing absorption features: {', '.join(rules['required_absorption_features'])}",
                f"Extend wavelength range to {rules['wavelength_range']} nm"
            ])
        elif area['name'] == 'lensing_accuracy':
            improvement['suggested_changes'].extend([
                f"Improve deflection angle accuracy to {rules['min_deflection_accuracy']}",
                f"Implement missing effects: {', '.join(rules['required_effects'])}"
            ])
        elif area['name'] == 'visualization_quality':
            improvement['suggested_changes'].extend([
                f"Increase resolution to {rules['min_resolution']}",
                f"Increase color depth to {rules['color_depth']} bits",
                f"Add missing elements: {', '.join(rules['required_elements'])}"
            ])
        
        return improvement
    
    def apply_improvements(self, improvements: List[Dict[str, Any]]) -> None:
        """Apply the suggested improvements."""
        for improvement in improvements:
            commit_message = self.automated_settings['commit_message_template'].format(
                area=improvement['area'],
                description=improvement['description']
            )
            
            # Apply changes to each target file
            for file in improvement['target_files']:
                self._apply_file_improvements(file, improvement)
            
            # Commit changes
            subprocess.run(['git', 'add', *improvement['target_files']])
            subprocess.run(['git', 'commit', '-m', commit_message])
    
    def _apply_file_improvements(self, file: str, improvement: Dict[str, Any]) -> None:
        """Apply improvements to a specific file."""
        # This would be implemented based on the specific improvements needed
        # For now, we'll just log the intended changes
        print(f"Applying improvements to {file}:")
        for change in improvement['suggested_changes']:
            print(f"  - {change}")

def main():
    # Initialize improvement manager
    manager = ImprovementManager()
    
    # Get latest coverage report
    coverage_reports = [f for f in os.listdir('tests') if f.startswith('coverage_')]
    if not coverage_reports:
        print("No coverage reports found")
        return
        
    latest_report = max(coverage_reports)
    coverage_path = os.path.join('tests', latest_report)
    
    # Analyze results and generate improvements
    scores = manager.analyze_test_results(coverage_path)
    improvements = manager.generate_improvements(scores)
    
    # Apply improvements if any
    if improvements:
        print("\nApplying improvements:")
        manager.apply_improvements(improvements)
    else:
        print("\nNo improvements needed at this time")

if __name__ == '__main__':
    main() 