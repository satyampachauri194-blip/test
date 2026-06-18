"""
Celery application configuration and worker setup.
"""

from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery application
celery_app = Celery(
    'tender_intelligence',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        'app.tasks.scraper',
        'app.tasks.ai_processor',
        'app.tasks.notifications',
        'app.tasks.pdf_extractor',
        'app.tasks.alerts',
    ]
)

# Configure Celery
celery_app.conf.update(
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='Asia/Kolkata',
    enable_utc=True,
    
    # Task execution
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    task_soft_time_limit=240,  # 4 minutes soft limit
    
    # Rate limiting
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Broker settings
    broker_heartbeat=608,
    broker_connection_timeout=10,
    broker_pool_limit=10,
    
    # Retry settings
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # Event monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Scheduled tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    # Scrape government portals every hour
    'scrape-all-portals-hourly': {
        'task': 'app.tasks.scraper.scrape_all_portals',
        'schedule': crontab(minute=0),  # Every hour
    },
    
    # Scrape GeM portal every 30 minutes
    'scrape-gem-portal': {
        'task': 'app.tasks.scraper.scrape_gem_portal',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    
    # Scrape CPPP portal every hour
    'scrape-cppp-portal': {
        'task': 'app.tasks.scraper.scrape_cppp_portal',
        'schedule': crontab(minute=15),  # Every hour at minute 15
    },
    
    # Process pending PDFs every 15 minutes
    'process-pending-pdfs': {
        'task': 'app.tasks.pdf_extractor.process_pending_pdfs',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    
    # Send alert digests daily at 9 AM IST
    'send-daily-alert-digest': {
        'task': 'app.tasks.alerts.send_daily_digest',
        'schedule': crontab(hour=9, minute=0),  # 9 AM IST
    },
    
    # Update tender statuses daily at midnight
    'update-tender-statuses': {
        'task': 'app.tasks.scraper.update_tender_statuses',
        'schedule': crontab(hour=0, minute=0),  # Midnight
    },
    
    # Clean up old data weekly
    'cleanup-old-data': {
        'task': 'app.tasks.scraper.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Sunday 2 AM
    },
    
    # Sync Elasticsearch every 30 minutes
    'sync-elasticsearch': {
        'task': 'app.tasks.ai_processor.sync_elasticsearch',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}

# Worker routing
celery_app.conf.task_routes = {
    'app.tasks.scraper.*': {'queue': 'scraper'},
    'app.tasks.pdf_extractor.*': {'queue': 'pdf'},
    'app.tasks.ai_processor.*': {'queue': 'ai'},
    'app.tasks.notifications.*': {'queue': 'notifications'},
    'app.tasks.alerts.*': {'queue': 'alerts'},
}

# Auto-discover tasks
celery_app.autodiscover_tasks(['app'])


@celery_app.on_after_configure.connect
def on_after_configure(sender, **kwargs):
    """Log configuration after setup."""
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Celery configured successfully")
    logger.info(f"Broker: {settings.CELERY_BROKER_URL}")
    logger.info(f"Timezone: {celery_app.conf.timezone}")
