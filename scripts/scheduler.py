"""
scheduler.py — 주 3회 자동 스케줄러
settings.yaml의 schedule_days & schedule_time 기준 자동 실행
"""

import logging
import os
import sys
from pathlib import Path

import schedule
import time
import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env", override=True)

from scripts.run_agent import run_full_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("scheduler")


def load_config() -> dict:
    with open(ROOT / "config" / "settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def scheduled_job():
    """스케줄 트리거 시 실행되는 작업."""
    logger.info("⏰ 스케줄 트리거 — 파이프라인 시작")
    dry_run = os.environ.get("HUMAN_GATE", "true").lower() == "true"
    # HUMAN_GATE=true면 dry-run 아님 (승인 게이트가 처리)
    run_full_pipeline(dry_run=False)


def setup_schedule(config: dict):
    """settings.yaml 기반으로 스케줄 등록."""
    schedule_days = config["blog"]["schedule_days"]
    schedule_time = config["blog"]["schedule_time"]  # "09:00"

    day_map = {
        "monday": schedule.every().monday,
        "tuesday": schedule.every().tuesday,
        "wednesday": schedule.every().wednesday,
        "thursday": schedule.every().thursday,
        "friday": schedule.every().friday,
        "saturday": schedule.every().saturday,
        "sunday": schedule.every().sunday,
    }

    for day in schedule_days:
        day_lower = day.lower()
        if day_lower in day_map:
            day_map[day_lower].at(schedule_time).do(scheduled_job)
            logger.info(f"  스케줄 등록: 매주 {day} {schedule_time}")
        else:
            logger.warning(f"  알 수 없는 요일: {day} — 스킵")


def main():
    config = load_config()
    logger.info("=" * 50)
    logger.info("Blog Agent Scheduler 시작")
    logger.info(f"발행 주기: 주 {config['blog']['posts_per_week']}회")
    logger.info(f"발행 요일: {config['blog']['schedule_days']}")
    logger.info(f"발행 시간: {config['blog']['schedule_time']}")
    logger.info("=" * 50)

    setup_schedule(config)

    logger.info("스케줄러 대기 중... (종료: Ctrl+C)")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    except KeyboardInterrupt:
        logger.info("스케줄러 종료")


if __name__ == "__main__":
    main()
