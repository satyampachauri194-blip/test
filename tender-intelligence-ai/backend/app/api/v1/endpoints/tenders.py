"""
Tender endpoints for listing, searching, and viewing tenders.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
import logging
import time

from app.db.session import get_db
from app.models.tender import Tender, TenderStatus, ProcurementType, TenderType
from app.models.user import User
from app.schemas.tender import (
    TenderResponse,
    TenderListResponse,
    TenderFilters,
    TenderStats,
)
from app.security.dependencies import get_current_user, get_optional_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=TenderListResponse)
async def list_tenders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[TenderStatus] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    min_bid_value: Optional[float] = None,
    max_bid_value: Optional[float] = None,
    closing_within_days: Optional[int] = None,
    query: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    List tenders with optional filters.
    
    Supports pagination, sorting, and various filters.
    Free users limited to recent tenders; paid users get full access.
    """
    from datetime import date, timedelta
    
    start_time = time.time()
    
    # Build base query
    stmt = select(Tender).where(Tender.status == TenderStatus.ACTIVE)
    
    # Apply filters
    if status:
        stmt = stmt.where(Tender.status == status)
    
    if state:
        stmt = stmt.where(Tender.state == state)
    
    if category:
        stmt = stmt.where(Tender.category == category)
    
    if department:
        stmt = stmt.where(Tender.department.ilike(f"%{department}%"))
    
    if min_bid_value is not None:
        stmt = stmt.where(Tender.bid_value_min >= min_bid_value)
    
    if max_bid_value is not None:
        stmt = stmt.where(Tender.bid_value_max <= max_bid_value)
    
    if closing_within_days:
        cutoff_date = date.today() + timedelta(days=closing_within_days)
        stmt = stmt.where(Tender.closing_date <= cutoff_date)
    
    if query:
        stmt = stmt.where(
            or_(
                Tender.title.ilike(f"%{query}%"),
                Tender.description.ilike(f"%{query}%"),
                Tender.tender_id.ilike(f"%{query}%"),
            )
        )
    
    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()
    
    # Apply pagination
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size).order_by(Tender.closing_date.asc())
    
    # Execute query
    result = await db.execute(stmt)
    tenders = result.scalars().all()
    
    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size
    
    search_time_ms = int((time.time() - start_time) * 1000)
    
    return TenderListResponse(
        tenders=[
            TenderResponse(
                id=t.id,
                tender_id=t.tender_id,
                tender_number=t.tender_number,
                title=t.title,
                description=t.description,
                department=t.department,
                buyer_name=t.buyer_name,
                authority=t.authority,
                organization_type=t.organization_type,
                state=t.state,
                district=t.district,
                city=t.city,
                pincode=t.pincode,
                category=t.category,
                sub_category=t.sub_category,
                procurement_type=t.procurement_type,
                tender_type=t.tender_type,
                bid_value_min=t.bid_value_min,
                bid_value_max=t.bid_value_max,
                emd_amount=t.emd_amount,
                currency=t.currency,
                publish_date=t.publish_date,
                opening_date=t.opening_date,
                closing_date=t.closing_date,
                corrigendum_date=t.corrigendum_date,
                status=t.status,
                source_url=t.source_url,
                source_portal=t.source_portal,
                pdf_urls=t.pdf_urls,
                document_count=t.document_count,
                eligibility_criteria=t.eligibility_criteria,
                turnover_required=t.turnover_required,
                experience_years=t.experience_years,
                mse_exemption=t.mse_exemption,
                startup_exemption=t.startup_exemption,
                ai_summary=t.ai_summary,
                risk_score=t.risk_score,
                complexity_score=t.complexity_score,
                qualification_probability=t.qualification_probability,
                red_flags=t.red_flags,
                view_count=t.view_count,
                saved_count=t.saved_count,
                is_corrigendum=t.is_corrigendum,
                corrigendum_count=t.corrigendum_count,
                awarded_bidder=t.awarded_bidder,
                awarded_amount=t.awarded_amount,
                created_at=t.created_at,
                updated_at=t.updated_at,
                days_to_close=t.days_to_close,
                is_urgent=t.is_urgent,
            )
            for t in tenders
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        search_time_ms=search_time_ms,
    )


@router.get("/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    Get detailed information about a specific tender.
    
    Includes AI analysis, documents, and related tenders.
    """
    from sqlalchemy import update
    
    # Find tender by external ID
    result = await db.execute(select(Tender).where(Tender.tender_id == tender_id))
    tender = result.scalar_one_or_none()
    
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tender not found",
        )
    
    # Increment view count
    await db.execute(
        update(Tender)
        .where(Tender.id == tender.id)
        .values(view_count=Tender.view_count + 1)
    )
    await db.commit()
    
    return TenderResponse(
        id=tender.id,
        tender_id=tender.tender_id,
        tender_number=tender.tender_number,
        title=tender.title,
        description=tender.description,
        department=tender.department,
        buyer_name=tender.buyer_name,
        authority=tender.authority,
        organization_type=tender.organization_type,
        state=tender.state,
        district=tender.district,
        city=tender.city,
        pincode=tender.pincode,
        category=tender.category,
        sub_category=tender.sub_category,
        procurement_type=tender.procurement_type,
        tender_type=tender.tender_type,
        bid_value_min=tender.bid_value_min,
        bid_value_max=tender.bid_value_max,
        emd_amount=tender.emd_amount,
        currency=tender.currency,
        publish_date=tender.publish_date,
        opening_date=tender.opening_date,
        closing_date=tender.closing_date,
        corrigendum_date=tender.corrigendum_date,
        status=tender.status,
        source_url=tender.source_url,
        source_portal=tender.source_portal,
        pdf_urls=tender.pdf_urls,
        document_count=tender.document_count,
        eligibility_criteria=tender.eligibility_criteria,
        turnover_required=tender.turnover_required,
        experience_years=tender.experience_years,
        mse_exemption=tender.mse_exemption,
        startup_exemption=tender.startup_exemption,
        ai_summary=tender.ai_summary,
        risk_score=tender.risk_score,
        complexity_score=tender.complexity_score,
        qualification_probability=tender.qualification_probability,
        red_flags=tender.red_flags,
        view_count=tender.view_count + 1,
        saved_count=tender.saved_count,
        is_corrigendum=tender.is_corrigendum,
        corrigendum_count=tender.corrigendum_count,
        awarded_bidder=tender.awarded_bidder,
        awarded_amount=tender.awarded_amount,
        created_at=tender.created_at,
        updated_at=tender.updated_at,
        days_to_close=tender.days_to_close,
        is_urgent=tender.is_urgent,
    )


@router.get("/stats", response_model=TenderStats)
async def get_tender_stats(
    db: AsyncSession = Depends(get_db),
):
    """
    Get tender statistics and trends.
    
    Useful for dashboard and analytics.
    """
    from datetime import date, timedelta
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic counts
    active_stmt = select(func.count()).where(Tender.status == TenderStatus.ACTIVE)
    closed_stmt = select(func.count()).where(Tender.status == TenderStatus.CLOSED)
    today_stmt = select(func.count()).where(Tender.publish_date == today)
    week_stmt = select(func.count()).where(Tender.publish_date >= week_ago)
    month_stmt = select(func.count()).where(Tender.publish_date >= month_ago)
    
    # Urgent (closing within 7 days)
    urgent_cutoff = today + timedelta(days=7)
    urgent_stmt = select(func.count()).where(
        and_(
            Tender.status == TenderStatus.ACTIVE,
            Tender.closing_date <= urgent_cutoff,
            Tender.closing_date >= today,
        )
    )
    
    # Corrigendum count
    corrigendum_stmt = select(func.count()).where(Tender.is_corrigendum == True)
    
    # Execute all counts
    active_result = await db.execute(active_stmt)
    closed_result = await db.execute(closed_stmt)
    today_result = await db.execute(today_stmt)
    week_result = await db.execute(week_stmt)
    month_result = await db.execute(month_stmt)
    urgent_result = await db.execute(urgent_stmt)
    corrigendum_result = await db.execute(corrigendum_stmt)
    
    return TenderStats(
        total_active=active_result.scalar() or 0,
        total_closed=closed_result.scalar() or 0,
        total_today=today_result.scalar() or 0,
        total_this_week=week_result.scalar() or 0,
        total_this_month=month_result.scalar() or 0,
        urgent_count=urgent_result.scalar() or 0,
        corrigendum_count=corrigendum_result.scalar() or 0,
        by_procurement_type={},  # TODO: Add aggregation
        by_state={},  # TODO: Add aggregation
        by_department={},  # TODO: Add aggregation
        avg_bid_value=None,  # TODO: Add aggregation
        median_bid_value=None,  # TODO: Add aggregation
        daily_counts=[],  # TODO: Add trend data
    )
