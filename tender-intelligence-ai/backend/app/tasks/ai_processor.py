"""
AI-powered PDF extraction and tender analysis tasks.
"""

from celery import shared_task
from typing import List, Dict, Optional, Any
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def extract_tender_pdf(self, tender_id: str, pdf_path: str):
    """
    Extract structured data from a tender PDF document.
    
    Args:
        tender_id: Tender ID
        pdf_path: Path to the PDF file
    """
    try:
        logger.info(f"Starting PDF extraction for tender {tender_id}")
        
        from app.services.ai.pdf_extractor import PDFExtractor
        
        extractor = PDFExtractor()
        result = extractor.extract(pdf_path)
        
        # Update tender with extracted data
        update_tender_with_extraction.delay(tender_id, result)
        
        logger.info(f"PDF extraction completed for {tender_id}")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "extracted_fields": len(result),
        }
        
    except Exception as exc:
        logger.error(f"Error extracting PDF for {tender_id}: {exc}")
        raise self.retry(exc=exc, countdown=120)


@shared_task
def process_pending_pdfs():
    """
    Process all pending PDFs in the queue.
    
    Finds tenders with downloaded but unprocessed PDFs.
    """
    try:
        logger.info("Starting pending PDF processing")
        
        # Query database for pending PDFs
        # For each pending tender, trigger extraction
        # This is a placeholder - actual implementation would query DB
        
        pending_count = 0  # Would be actual count from DB
        
        logger.info(f"Processed {pending_count} pending PDFs")
        
        return {
            "status": "success",
            "processed_count": pending_count,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as exc:
        logger.error(f"Error processing pending PDFs: {exc}")
        raise


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def analyze_tender_content(self, tender_id: str, extracted_data: Dict[str, Any]):
    """
    Analyze tender content using AI to generate insights.
    
    Args:
        tender_id: Tender ID
        extracted_data: Structured data extracted from PDF
    """
    try:
        logger.info(f"Starting AI analysis for tender {tender_id}")
        
        from app.services.ai.tender_analyzer import TenderAnalyzer
        
        analyzer = TenderAnalyzer()
        analysis = analyzer.analyze(extracted_data)
        
        # Update tender with AI analysis
        update_tender_with_analysis.delay(tender_id, analysis)
        
        logger.info(f"AI analysis completed for {tender_id}")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "risk_score": analysis.get("risk_score"),
            "complexity_score": analysis.get("complexity_score"),
        }
        
    except Exception as exc:
        logger.error(f"Error analyzing tender {tender_id}: {exc}")
        raise self.retry(exc=exc, countdown=180)


@shared_task
def update_tender_with_extraction(tender_id: str, extraction_result: Dict[str, Any]):
    """
    Update tender record with PDF extraction results.
    
    Celery task to handle database update asynchronously.
    """
    try:
        # In production, this would update the database
        logger.info(f"Updating tender {tender_id} with extraction results")
        
        return {"status": "success", "tender_id": tender_id}
        
    except Exception as exc:
        logger.error(f"Error updating tender {tender_id}: {exc}")
        raise


@shared_task
def update_tender_with_analysis(tender_id: str, analysis_result: Dict[str, Any]):
    """
    Update tender record with AI analysis results.
    
    Celery task to handle database update asynchronously.
    """
    try:
        # In production, this would update the database
        logger.info(f"Updating tender {tender_id} with analysis results")
        
        return {"status": "success", "tender_id": tender_id}
        
    except Exception as exc:
        logger.error(f"Error updating tender {tender_id}: {exc}")
        raise


@shared_task
def sync_elasticsearch():
    """
    Sync tender data with Elasticsearch for search functionality.
    
    Ensures search index is up-to-date with latest tender information.
    """
    try:
        logger.info("Starting Elasticsearch sync")
        
        from app.services.search.elasticsearch_service import ElasticsearchService
        
        es_service = ElasticsearchService()
        result = es_service.sync_recent_tenders()
        
        logger.info(f"Elasticsearch sync completed: {result}")
        
        return result
        
    except Exception as exc:
        logger.error(f"Error syncing Elasticsearch: {exc}")
        raise


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def extract_boq(self, tender_id: str, pdf_path: str):
    """
    Extract Bill of Quantities (BOQ) from tender PDF.
    
    Args:
        tender_id: Tender ID
        pdf_path: Path to the PDF file
    """
    try:
        logger.info(f"Extracting BOQ for tender {tender_id}")
        
        from app.services.ai.boq_extractor import BOQExtractor
        
        extractor = BOQExtractor()
        boq_data = extractor.extract(pdf_path)
        
        logger.info(f"BOQ extraction completed for {tender_id}")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "boq_items": len(boq_data.get("items", [])),
        }
        
    except Exception as exc:
        logger.error(f"Error extracting BOQ for {tender_id}: {exc}")
        raise self.retry(exc=exc, countdown=120)


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def extract_atc(self, tender_id: str, pdf_path: str):
    """
    Extract Additional Terms and Conditions (ATC) from tender PDF.
    
    Args:
        tender_id: Tender ID
        pdf_path: Path to the PDF file
    """
    try:
        logger.info(f"Extracting ATC for tender {tender_id}")
        
        from app.services.ai.atc_extractor import ATCExtractor
        
        extractor = ATCExtractor()
        atc_data = extractor.extract(pdf_path)
        
        logger.info(f"ATC extraction completed for {tender_id}")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "atc_clauses": len(atc_data.get("clauses", [])),
        }
        
    except Exception as exc:
        logger.error(f"Error extracting ATC for {tender_id}: {exc}")
        raise self.retry(exc=exc, countdown=120)


@shared_task
def detect_red_flags(tender_id: str, extracted_data: Dict[str, Any]):
    """
    Detect potential red flags in tender documents.
    
    Identifies risky clauses, unrealistic requirements, or problematic terms.
    
    Args:
        tender_id: Tender ID
        extracted_data: Structured data from tender
    """
    try:
        logger.info(f"Detecting red flags for tender {tender_id}")
        
        from app.services.ai.red_flag_detector import RedFlagDetector
        
        detector = RedFlagDetector()
        red_flags = detector.detect(extracted_data)
        
        logger.info(f"Red flag detection completed for {tender_id}: {len(red_flags)} flags found")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "red_flags_count": len(red_flags),
            "red_flags": red_flags,
        }
        
    except Exception as exc:
        logger.error(f"Error detecting red flags for {tender_id}: {exc}")
        raise


@shared_task
def calculate_qualification_probability(
    tender_id: str,
    user_profile: Dict[str, Any],
    tender_requirements: Dict[str, Any]
):
    """
    Calculate probability of user qualifying for a tender.
    
    Compares user's profile against tender requirements.
    
    Args:
        tender_id: Tender ID
        user_profile: User's company profile (turnover, experience, etc.)
        tender_requirements: Tender eligibility criteria
    """
    try:
        logger.info(f"Calculating qualification probability for tender {tender_id}")
        
        from app.services.ai.qualification_calculator import QualificationCalculator
        
        calculator = QualificationCalculator()
        probability = calculator.calculate(user_profile, tender_requirements)
        
        logger.info(f"Qualification probability for {tender_id}: {probability:.2%}")
        
        return {
            "status": "success",
            "tender_id": tender_id,
            "probability": probability,
        }
        
    except Exception as exc:
        logger.error(f"Error calculating qualification for {tender_id}: {exc}")
        raise
