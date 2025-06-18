import os
import json
import importlib.util
import sys
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@dataclass
class ScraperConfig:
    path: str
    module: str
    function: str
    max_retries: int = 3
    retry_delay: int = 5  # seconds
    timeout: int = 300  # seconds
    enabled: bool = True
    priority: int = 1  # 1 = high, 2 = medium, 3 = low

@dataclass
class ScraperStats:
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    attempts: int = 0
    success: bool = False
    error_message: Optional[str] = None
    data_size: Optional[int] = None

class ScraperOrchestrator:
    def __init__(self, base_path: Optional[str] = None, config_file: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.results: Dict[str, Any] = {}
        self.stats: Dict[str, ScraperStats] = {}
        self.config_file = config_file
        self.scrapers: Dict[str, ScraperConfig] = self._load_scraper_config()
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    def _load_scraper_config(self) -> Dict[str, ScraperConfig]:
        """Load scraper configurations with retry settings."""
        default_config = {
            # Core scrapers with specific function names
            '7-zip': ScraperConfig('7-zip/main.py', 'scraper_7zip', 'scrape_7zip'),
            'anydesk': ScraperConfig('anydesk/main.py', 'scraper_anydesk', 'scrape_and_store_html'),
            'docker': ScraperConfig('docker/main.py', 'docker_scraper', 'scrape_docker'),
            'fontbase': ScraperConfig('fontbase/main.py', 'scraper_fontbase', 'scrape_fontbase'),
            'fortinet': ScraperConfig('fortinet/main.py', 'scraper_fortinet', 'scrape_fortinet'),
            'Foxit_PDF': ScraperConfig('Foxit_PDF/main.py', 'scraper_foxit_pdf', 'scrape_foxit_pdf'),
            'git': ScraperConfig('git/main.py', 'scraper_git', 'scrape_git'),
            'LibreOffice': ScraperConfig('LibreOffice/main.py', 'scraper_libreoffice', 'scrape_libreoffice'),
            'postman': ScraperConfig('postman/main.py', 'scraper_postman', 'scrape_postman'),
            'slack': ScraperConfig('slack/main.py', 'scraper_slack', 'scrape_slack'),
            'teamviwer': ScraperConfig('teamviwer/main.py', 'scraper_teamviwer', 'scrape_teamviwer'),
            'utraviews': ScraperConfig('utraviews/main.py', 'scraper_utraviews', 'scrape_utraviews'),
            'vlc_main': ScraperConfig('vlc_main/main.py', 'scraper_vlc_main', 'scrape_vlc'),
            'vscode': ScraperConfig('vscode/main.py', 'scraper_vscode', 'scrape_vscode'),
            'winscp': ScraperConfig('winscp/main.py', 'scraper_winscp', 'scrape_winscp'),
            'Zoom': ScraperConfig('Zoom/main.py', 'scraper_zoom', 'scrape_zoom'),
            
            # Node.js scrapers (multiple files)
            'nodejs': ScraperConfig('nodejs/latest.py', 'scraper_nodejs', 'scrape_nodejs'),
            'nodejs_lts': ScraperConfig('nodejs/node_LTS.py', 'scraper_nodejs_lts', 'scrape_nodejs_files'),
            
            # Additional scrapers found in folders - updated with correct function names
            'Fiddler': ScraperConfig('Fiddler/main.py', 'scraper_fiddler', 'scrape_fiddler'),
            'wireshark': ScraperConfig('wireshark/main.py', 'scraper_wireshark', 'scrape_wireshark'),
            'MobaXterm': ScraperConfig('MobaXterm/main.py', 'scraper_mobaxterm', 'scrape_mobaxterm'),
            'thunderbird': ScraperConfig('thunderbird/main.py', 'scraper_thunderbird', 'scrape_thunderbird'),
            'gimp': ScraperConfig('gimp/main.py', 'scraper_gimp', 'scrape_gimp'),
            'peazip': ScraperConfig('peazip/main.py', 'scraper_peazip', 'scrape_peazip'),
            'putty': ScraperConfig('putty/main.py', 'scraper_putty', 'scrape_putty')
        }
        
        # Load custom config if provided
        if self.config_file and Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    custom_config = json.load(f)
                for name, config_data in custom_config.items():
                    if name in default_config:
                        default_config[name] = ScraperConfig(**config_data)
            except Exception as e:
                logger.warning(f"Failed to load custom config: {e}")
                
        return default_config

    async def load_scraper(self, scraper_name: str) -> Optional[Dict[str, Any]]:
        """Load a scraper module dynamically with better error handling."""
        if scraper_name not in self.scrapers:
            logger.error(f"Scraper '{scraper_name}' not found in configuration")
            return None

        config = self.scrapers[scraper_name]
        scraper_path = self.base_path / config.path

        if not scraper_path.exists():
            logger.error(f"Scraper file not found: {scraper_path}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(config.module, str(scraper_path))
            if spec is None or spec.loader is None:
                logger.error(f"Failed to create module spec for {scraper_name}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[config.module] = module
            spec.loader.exec_module(module)
            
            # Try to find the scraping function
            scrape_func = None
            
            # First try the configured function name
            if hasattr(module, config.function):
                scrape_func = getattr(module, config.function)
            else:
                # Try common function name patterns
                possible_functions = [
                    config.function,
                    f"scrape_{scraper_name.lower().replace('-', '_').replace('_main', '')}",
                    f"scrape_{scraper_name.lower().replace('-', '_')}",
                    "main",
                    "scrape",
                    "run"
                ]
                
                for func_name in possible_functions:
                    if hasattr(module, func_name):
                        func = getattr(module, func_name)
                        if callable(func):
                            scrape_func = func
                            break
            
            if not scrape_func:
                logger.error(f"Scraping function not found in {scraper_name}. Tried: {config.function}")
                return None
                
            return {
                'module': module,
                'function': scrape_func
            }
        except Exception as e:
            logger.exception(f"Error loading scraper '{scraper_name}': {str(e)}")
            return None

    async def run_scraper(self, scraper_name: str) -> bool:
        """Run a specific scraper with retry mechanism and timeout."""
        logger.info(f"Starting scraper: {scraper_name}")
        
        config = self.scrapers.get(scraper_name)
        if not config:
            logger.error(f"No configuration found for scraper: {scraper_name}")
            return False

        # Initialize stats
        self.stats[scraper_name] = ScraperStats(name=scraper_name)
        stats = self.stats[scraper_name]
        stats.start_time = datetime.now()

        for attempt in range(config.max_retries):
            stats.attempts += 1
            try:
                scraper = await self.load_scraper(scraper_name)
                if not scraper:
                    return False

                # Run with timeout
                if asyncio.iscoroutinefunction(scraper['function']):
                    await asyncio.wait_for(scraper['function'](), timeout=config.timeout)
                else:
                    # Run sync function in thread pool
                    loop = asyncio.get_event_loop()
                    await asyncio.wait_for(
                        loop.run_in_executor(self.executor, scraper['function']),
                        timeout=config.timeout
                    )
                    
                stats.success = True
                stats.end_time = datetime.now()
                stats.duration = (stats.end_time - stats.start_time).total_seconds()
                
                # Calculate data size
                info_file = Path(self.base_path) / f"{scraper_name}_info.json"
                if info_file.exists():
                    stats.data_size = info_file.stat().st_size
                
                logger.info(f"Successfully completed {scraper_name} scraper in {stats.duration:.2f}s")
                return True
                
            except asyncio.TimeoutError:
                error_msg = f"Timeout after {config.timeout}s"
                logger.error(f"Attempt {attempt + 1}/{config.max_retries} failed for {scraper_name}: {error_msg}")
                stats.error_message = error_msg
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Attempt {attempt + 1}/{config.max_retries} failed for {scraper_name}: {error_msg}")
                stats.error_message = error_msg
                
            if attempt < config.max_retries - 1:
                await asyncio.sleep(config.retry_delay)
        
        stats.end_time = datetime.now()
        stats.duration = (stats.end_time - stats.start_time).total_seconds()
        return False

    def list_available_scrapers(self) -> List[str]:
        """List all available scrapers."""
        return [name for name, config in self.scrapers.items() if config.enabled]

    def get_scraper_status(self, scraper_name: str) -> Dict[str, Any]:
        """Get detailed status of a specific scraper."""
        if scraper_name not in self.scrapers:
            return {"error": "Scraper not found"}
            
        config = self.scrapers[scraper_name]
        scraper_path = self.base_path / config.path
        
        status = {
            "name": scraper_name,
            "enabled": config.enabled,
            "priority": config.priority,
            "file_exists": scraper_path.exists(),
            "file_path": str(scraper_path),
            "max_retries": config.max_retries,
            "timeout": config.timeout,
            "function_name": config.function
        }
        
        # Add stats if available
        if scraper_name in self.stats:
            status["stats"] = asdict(self.stats[scraper_name])
            
        return status

    async def run_all_scrapers(self, max_concurrent: int = 3) -> Dict[str, bool]:
        """Run all available scrapers with controlled concurrency."""
        enabled_scrapers = [name for name, config in self.scrapers.items() if config.enabled]
        
        # Sort by priority
        enabled_scrapers.sort(key=lambda x: self.scrapers[x].priority)
        
        logger.info(f"Running {len(enabled_scrapers)} scrapers with max {max_concurrent} concurrent")
        
        # Use semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_semaphore(scraper_name: str) -> tuple[str, bool]:
            async with semaphore:
                success = await self.run_scraper(scraper_name)
                return scraper_name, success
        
        tasks = [run_with_semaphore(name) for name in enabled_scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        final_results = {}
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Task failed with exception: {result}")
                continue
            scraper_name, success = result
            final_results[scraper_name] = success
            
        return final_results

    async def combine_results(self) -> Dict[str, Any]:
        """Combine results from all scrapers into a single JSON file with enhanced metadata."""
        combined_data = {
            "products": [],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_scrapers": len(self.scrapers),
                "enabled_scrapers": len([s for s in self.scrapers.values() if s.enabled]),
                "successful_scrapers": 0,
                "failed_scrapers": 0,
                "total_duration": 0,
                "total_data_size": 0,
                "scraper_stats": {}
            }
        }

        for scraper_name in self.scrapers:
            info_file = Path(self.base_path) / f"{scraper_name}_info.json"
            
            try:
                if info_file.exists():
                    data = json.loads(info_file.read_text(encoding='utf-8'))
                    combined_data["products"].append(data)
                    combined_data["metadata"]["successful_scrapers"] += 1
                    
                    # Add stats if available
                    if scraper_name in self.stats:
                        stats = self.stats[scraper_name]
                        combined_data["metadata"]["scraper_stats"][scraper_name] = asdict(stats)
                        if stats.duration:
                            combined_data["metadata"]["total_duration"] += stats.duration
                        if stats.data_size:
                            combined_data["metadata"]["total_data_size"] += stats.data_size
                else:
                    logger.warning(f"No results file found for {scraper_name}")
                    combined_data["metadata"]["failed_scrapers"] += 1
                    
            except Exception as e:
                logger.error(f"Error processing {scraper_name} results: {str(e)}")
                combined_data["metadata"]["failed_scrapers"] += 1

        # Save combined results
        output_path = Path(self.base_path) / "combined_results.json"
        try:
            output_path.write_text(
                json.dumps(combined_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            logger.info(f"Combined results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving combined results: {str(e)}")

        return combined_data

    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics about scraper runs."""
        if not self.stats:
            return {"message": "No scraper runs recorded yet"}
            
        total_runs = len(self.stats)
        successful_runs = sum(1 for stats in self.stats.values() if stats.success)
        failed_runs = total_runs - successful_runs
        
        total_duration = sum(stats.duration or 0 for stats in self.stats.values())
        total_data_size = sum(stats.data_size or 0 for stats in self.stats.values())
        
        avg_duration = total_duration / total_runs if total_runs > 0 else 0
        
        return {
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "success_rate": (successful_runs / total_runs * 100) if total_runs > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "total_data_size": total_data_size,
            "scraper_details": {
                name: asdict(stats) for name, stats in self.stats.items()
            }
        }

    async def cleanup_old_files(self, days: int = 7) -> int:
        """Clean up old JSON files older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        for scraper_name in self.scrapers:
            info_file = Path(self.base_path) / f"{scraper_name}_info.json"
            if info_file.exists():
                file_time = datetime.fromtimestamp(info_file.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        info_file.unlink()
                        cleaned_count += 1
                        logger.info(f"Cleaned up old file: {info_file}")
                    except Exception as e:
                        logger.error(f"Failed to clean up {info_file}: {e}")
                        
        return cleaned_count

    def validate_scrapers(self) -> Dict[str, Dict[str, Any]]:
        """Validate all scraper configurations and files."""
        validation_results = {}
        
        for scraper_name, config in self.scrapers.items():
            validation = {
                "name": scraper_name,
                "enabled": config.enabled,
                "file_exists": False,
                "function_found": False,
                "errors": []
            }
            
            # Check if file exists
            scraper_path = self.base_path / config.path
            if scraper_path.exists():
                validation["file_exists"] = True
                
                # Try to load the module and check for function
                try:
                    spec = importlib.util.spec_from_file_location(config.module, str(scraper_path))
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Check for function
                        if hasattr(module, config.function):
                            validation["function_found"] = True
                        else:
                            validation["errors"].append(f"Function '{config.function}' not found")
                    else:
                        validation["errors"].append("Failed to create module spec")
                except Exception as e:
                    validation["errors"].append(f"Module loading error: {str(e)}")
            else:
                validation["errors"].append(f"File not found: {scraper_path}")
                
            validation_results[scraper_name] = validation
            
        return validation_results

async def main():
    parser = argparse.ArgumentParser(description='Product Scraper Orchestrator')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--max-concurrent', type=int, default=3, help='Maximum concurrent scrapers')
    parser.add_argument('--cleanup-days', type=int, default=7, help='Clean up files older than N days')
    parser.add_argument('--validate', action='store_true', help='Validate all scraper configurations')
    args = parser.parse_args()
    
    orchestrator = ScraperOrchestrator(config_file=args.config)
    
    while True:
        print("\n=== Product Scraper Orchestrator ===")
        print("1. List available scrapers")
        print("2. Run specific scraper")
        print("3. Run all scrapers")
        print("4. Combine results")
        print("5. Show statistics")
        print("6. Cleanup old files")
        print("7. Validate scrapers")
        print("8. Exit")
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                scrapers = orchestrator.list_available_scrapers()
                print(f"\nAvailable scrapers ({len(scrapers)}):")
                for i, scraper in enumerate(scrapers, 1):
                    config = orchestrator.scrapers[scraper]
                    status = "✅ Enabled" if config.enabled else "❌ Disabled"
                    print(f"{i}. {scraper} ({status}, Priority: {config.priority})")
                    
            elif choice == '2':
                scrapers = orchestrator.list_available_scrapers()
                print("\nAvailable scrapers:")
                for i, scraper in enumerate(scrapers, 1):
                    print(f"{i}. {scraper}")
                
                idx = int(input("\nEnter scraper number: ").strip()) - 1
                if 0 <= idx < len(scrapers):
                    success = await orchestrator.run_scraper(scrapers[idx])
                    status = "✅ Success" if success else "❌ Failed"
                    print(f"\nScraper status: {status}")
                else:
                    logger.error("Invalid scraper number")
                    
            elif choice == '3':
                print(f"\nRunning all scrapers (max {args.max_concurrent} concurrent)...")
                start_time = time.time()
                results = await orchestrator.run_all_scrapers(args.max_concurrent)
                end_time = time.time()
                
                print(f"\nResults (completed in {end_time - start_time:.2f}s):")
                for scraper, success in results.items():
                    status = "✅ Success" if success else "❌ Failed"
                    print(f"{scraper}: {status}")
                    
            elif choice == '4':
                print("\nCombining results from all scrapers...")
                combined_data = await orchestrator.combine_results()
                metadata = combined_data['metadata']
                print(f"\nProcessed {metadata['total_scrapers']} scrapers:")
                print(f"- Successful: {metadata['successful_scrapers']}")
                print(f"- Failed: {metadata['failed_scrapers']}")
                print(f"- Total duration: {metadata['total_duration']:.2f}s")
                print(f"- Total data size: {metadata['total_data_size']} bytes")
                
            elif choice == '5':
                stats = orchestrator.get_statistics()
                if "message" in stats:
                    print(f"\n{stats['message']}")
                else:
                    print(f"\nScraper Statistics:")
                    print(f"- Total runs: {stats['total_runs']}")
                    print(f"- Successful: {stats['successful_runs']}")
                    print(f"- Failed: {stats['failed_runs']}")
                    print(f"- Success rate: {stats['success_rate']:.1f}%")
                    print(f"- Total duration: {stats['total_duration']:.2f}s")
                    print(f"- Average duration: {stats['average_duration']:.2f}s")
                    print(f"- Total data size: {stats['total_data_size']} bytes")
                
            elif choice == '6':
                days = int(input(f"Clean up files older than how many days? (default: {args.cleanup_days}): ") or args.cleanup_days)
                cleaned = await orchestrator.cleanup_old_files(days)
                print(f"Cleaned up {cleaned} old files")
                
            elif choice == '7':
                print("\nValidating scraper configurations...")
                validation_results = orchestrator.validate_scrapers()
                
                print("\nValidation Results:")
                for scraper_name, validation in validation_results.items():
                    status = "✅ Valid" if validation["file_exists"] and validation["function_found"] else "❌ Invalid"
                    print(f"{scraper_name}: {status}")
                    if validation["errors"]:
                        for error in validation["errors"]:
                            print(f"  - {error}")
                
            elif choice == '8':
                print("\nGoodbye!")
                break
                
            else:
                logger.warning("Invalid choice. Please try again.")
                
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 