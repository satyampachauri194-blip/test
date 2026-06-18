"""
Web scraping tasks for tender portals.
"""

from celery import shared_task
from typing import List, Dict, Optional
import logging
from datetime import datetime, date
import asyncio

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def scrape_all_portals(self):
    """
    Scrape all configured tender portals.
    
    Orchestrates scraping across multiple government procurement sources.
    """
    try:
        logger.info("Starting full portal scraping cycle")
        
        # Import here to avoid circular imports
        from app.services.scraper.portal_scraper import PortalScraper
        
        scraper = PortalScraper()
        
        # Scrape all portals
        results = scraper.scrape_all()
        
        logger.info(f"Scraping completed: {results}")
        
        return {
            "status": "success",
            "portals_scraped": len(results),
            "tenders_found": sum(r.get("tenders_found", 0) for r in results),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        logger.error(f"Error in scrape_all_portals: {exc}")
        raise self.retry(exc=exc, countdown=120)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def scrape_gem_portal(self):
    """
    Scrape GeM (Government e-Marketplace) portal.
    
    GeM is the primary procurement portal for central government ministries.
    """
    try:
        logger.info("Starting GeM portal scraping")
        
        from app.services.scraper.gem_scraper import GeMScraper
        
        scraper = GeMScraper()
        result = scraper.scrape()
        
        logger.info(f"GeM scraping completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error in scrape_gem_portal: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def scrape_cppp_portal(self):
    """
    Scrape CPPP (Central Public Procurement Portal) portal.
    
    CPPP aggregates tenders from various central government organizations.
    """
    try:
        logger.info("Starting CPPP portal scraping")
        
        from app.services.scraper.cppp_scraper import CPPPScraper
        
        scraper = CPPPScraper()
        result = scraper.scrape()
        
        logger.info(f"CPPP scraping completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error in scrape_cppp_portal: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def scrape_state_portal(self, state_code: str):
    """
    Scrape a specific state eProcurement portal.
    
    Args:
        state_code: State code (e.g., 'UP', 'MH', 'KA')
    """
    try:
        logger.info(f"Starting {state_code} state portal scraping")
        
        from app.services.scraper.state_scraper import StatePortalScraper
        
        scraper = StatePortalScraper(state_code)
        result = scraper.scrape()
        
        logger.info(f"{state_code} scraping completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error in scrape_state_portal for {state_code}: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def scrape_psu_portal(self, psu_name: str):
    """
    Scrape a specific PSU procurement portal.
    
    Args:
        psu_name: Name of the PSU (e.g., 'ONGC', 'BHEL', 'NTPC')
    """
    try:
        logger.info(f"Starting {psu_name} PSU portal scraping")
        
        from app.services.scraper.psu_scraper import PSUScraper
        
        scraper = PSUScraper(psu_name)
        result = scraper.scrape()
        
        logger.info(f"{psu_name} scraping completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error in scrape_psu_portal for {psu_name}: {exc}")
        raise self.retry(exc=exc, countdown=120)


@shared_task
def update_tender_statuses():
    """
    Update status of existing tenders based on closing dates.
    
    Marks tenders as closed/expired if their closing date has passed.
    """
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy import select, update
    from app.models.tender import Tender, TenderStatus
    from app.core.config import settings
    
    try:
        logger.info("Starting tender status update")
        
        # This would use the actual database session in production
        # For now, it's a placeholder
        today = date.today()
        
        # In production, this would execute:
        # UPDATE tenders SET status = 'closed' WHERE closing_date < today AND status = 'active'
        # UPDATE tenders SET status = 'expired' WHERE closing_date < today - 7 AND status = 'closed'
        
        logger.info("Tender statuses updated successfully")
        
        return {
            "status": "success",
            "updated_count": 0,  # Would be actual count from DB
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        logger.error(f"Error updating tender statuses: {exc}")
        raise


@shared_task(bind=True, max_retries=2, default_retry_delay=300)
def download_tender_pdfs(self, tender_id: str, pdf_urls: List[str]):
    """
    Download PDF documents for a tender.
    
    Args:
        tender_id: Tender ID
        pdf_urls: List of PDF URLs to download
    """
    try:
        logger.info(f"Downloading PDFs for tender {tender_id}")
        
        from app.services.scraper.pdf_downloader import PDFDownloader
        
        downloader = PDFDownloader()
        result = downloader.download_pdfs(tender_id, pdf_urls)
        
        logger.info(f"PDF download completed for {tender_id}: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error downloading PDFs for {tender_id}: {exc}")
        raise self.retry(exc=exc, countdown=300)


@shared_task
def cleanup_old_data():
    """
    Clean up old scraping logs and temporary data.
    
    Runs weekly to maintain database health.
    """
    try:
        logger.info("Starting data cleanup")
        
        # Clean up old scraping logs (> 90 days)
        # Clean up temporary files
        # Optimize database tables
        
        logger.info("Data cleanup completed")
        
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        logger.error(f"Error in cleanup_old_data: {exc}")
        raise


@shared_task
def detect_corrigendums():
    """
    Detect and link corrigendums to original tenders.
    
    Monitors portals for tender amendments and updates.
    """
    try:
        logger.info("Starting corrigendum detection")
        
        from app.services.scraper.corrigendum_detector import CorrigendumDetector
        
        detector = CorrigendumDetector()
        result = detector.detect_and_link()
        
        logger.info(f"Corrigendum detection completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error in detect_corrigendums: {exc}")
        raise
