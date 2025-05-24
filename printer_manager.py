import json
import os
import requests
from datetime import datetime
from typing import Dict, Optional
import logging

class PrinterManager:
    def __init__(self, config_path: str = '.cursor-improvements.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.printer_config = self.config['printing']
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging for printer operations."""
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'printer.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('PrinterManager')
        
    def print_visualization(self, visualization_path: str) -> bool:
        """Print a visualization using the configured printer."""
        try:
            # Check printer status
            if not self._check_printer_status():
                self.logger.error("Printer is not ready")
                return False
            
            # Prepare print job
            job_id = self._create_print_job(visualization_path)
            if not job_id:
                return False
            
            # Send to printer
            success = self._send_to_printer(job_id)
            if success:
                self.logger.info(f"Successfully printed visualization: {visualization_path}")
                self._update_print_history(job_id, visualization_path)
            return success
            
        except Exception as e:
            self.logger.error(f"Error printing visualization: {str(e)}")
            return False
    
    def _check_printer_status(self) -> bool:
        """Check if the printer is ready for printing."""
        try:
            # This would typically check the printer's status
            # For now, return mock data
            return True
        except Exception as e:
            self.logger.error(f"Error checking printer status: {str(e)}")
            return False
    
    def _create_print_job(self, visualization_path: str) -> Optional[str]:
        """Create a print job on the OpenShift job server."""
        try:
            # This would typically create a job on OpenShift
            # For now, return a mock job ID
            return f"print_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        except Exception as e:
            self.logger.error(f"Error creating print job: {str(e)}")
            return None
    
    def _send_to_printer(self, job_id: str) -> bool:
        """Send the print job to the printer."""
        try:
            # This would typically send the job to the printer
            # For now, return mock success
            return True
        except Exception as e:
            self.logger.error(f"Error sending to printer: {str(e)}")
            return False
    
    def _update_print_history(self, job_id: str, visualization_path: str) -> None:
        """Update the print history log."""
        history_file = 'logs/print_history.json'
        
        try:
            # Load existing history
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Add new entry
            history.append({
                'job_id': job_id,
                'visualization': visualization_path,
                'timestamp': datetime.now().isoformat(),
                'printer_config': {
                    'paper_size': self.printer_config['paper_size'],
                    'color_mode': self.printer_config['color_mode'],
                    'resolution': self.printer_config['resolution']
                }
            })
            
            # Save updated history
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error updating print history: {str(e)}")
    
    def check_supplies(self) -> Dict[str, bool]:
        """Check printer supplies and request refill if needed."""
        try:
            # This would typically check actual printer supplies
            # For now, return mock data
            supplies = {
                'paper': True,
                'ink': True,
                'toner': True
            }
            
            # If any supply is low, request refill
            if not all(supplies.values()):
                self._request_supply_refill(supplies)
            
            return supplies
            
        except Exception as e:
            self.logger.error(f"Error checking supplies: {str(e)}")
            return {}
    
    def _request_supply_refill(self, supplies: Dict[str, bool]) -> None:
        """Request supply refill from W.B. Mason."""
        try:
            # This would typically make an API call to W.B. Mason
            # For now, just log the request
            self.logger.info(f"Requesting supply refill for: {supplies}")
            
            # Send notification email
            self._send_refill_notification(supplies)
            
        except Exception as e:
            self.logger.error(f"Error requesting supply refill: {str(e)}")
    
    def _send_refill_notification(self, supplies: Dict[str, bool]) -> None:
        """Send notification about supply refill request."""
        try:
            # This would typically send an email
            # For now, just log the notification
            self.logger.info(f"Sending refill notification to: {self.printer_config['notification_email']}")
            
        except Exception as e:
            self.logger.error(f"Error sending refill notification: {str(e)}")

def main():
    manager = PrinterManager()
    
    # Example usage
    visualization_path = "visualizations/latest.png"
    if manager.print_visualization(visualization_path):
        print("Visualization printed successfully")
    else:
        print("Failed to print visualization")
    
    # Check supplies
    supplies = manager.check_supplies()
    print("\nPrinter supplies status:")
    for supply, status in supplies.items():
        print(f"{supply}: {'OK' if status else 'Needs refill'}")

if __name__ == '__main__':
    main() 