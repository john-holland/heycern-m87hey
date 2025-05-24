import unittest
import sys
import os
import coverage
import json
from datetime import datetime

def run_tests():
    """Run all tests with coverage reporting."""
    # Start coverage
    cov = coverage.Coverage()
    cov.start()

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    # Generate coverage report
    coverage_data = {
        'summary': cov.report(),
        'missing_lines': cov.get_missing(),
        'covered_lines': cov.get_covered(),
        'total_lines': cov.get_total()
    }
    
    # Save coverage report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'coverage_report_{timestamp}.json'
    with open(report_file, 'w') as f:
        json.dump(coverage_data, f, indent=2)
    
    # Return test results
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'coverage_report': report_file
    }

if __name__ == '__main__':
    results = run_tests()
    
    # Print summary
    print("\nTest Summary:")
    print(f"Tests run: {results['tests_run']}")
    print(f"Failures: {results['failures']}")
    print(f"Errors: {results['errors']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Coverage report saved to: {results['coverage_report']}")
    
    # Exit with appropriate status code
    sys.exit(results['failures'] + results['errors']) 