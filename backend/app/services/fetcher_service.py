from datetime import datetime
import traceback

from app.database import SessionLocal
from app.models.item import Item
from app.models.fetch_run import FetchRun
from app.fetchers import (
    YouTubeFetcher,
    SubstackFetcher,
    TwitterFetcher,
    ProductsFetcher,
    BusinessFetcher,
    ApplePodcastFetcher,
)
from app.processors.summarizer import Summarizer

# Module configuration
MODULE_CONFIG = {
    "youtube": {
        "fetcher": YouTubeFetcher,
        "type": "video",
    },
    "substack": {
        "fetcher": SubstackFetcher,
        "type": "article",
    },
    "twitter": {
        "fetcher": TwitterFetcher,
        "type": "article",
    },
    "products": {
        "fetcher": ProductsFetcher,
        "type": "product",
    },
    "business": {
        "fetcher": BusinessFetcher,
        "type": "news",
    },
    "apple_podcast": {
        "fetcher": ApplePodcastFetcher,
        "type": "audio",
    },
}


def run_fetch_job(run_id: str):
    """Run the complete fetch job"""
    db = SessionLocal()

    try:
        # Update status to running
        fetch_run = db.query(FetchRun).filter(FetchRun.id == run_id).first()
        if fetch_run:
            fetch_run.status = "running"
            fetch_run.started_at = datetime.now()
            db.commit()

        print(f"[FetchJob] Starting fetch job: {run_id}")

        summarizer = Summarizer()
        modules_processed = {}
        total_items = 0
        errors = []

        for module_name, config in MODULE_CONFIG.items():
            try:
                print(f"\n[FetchJob] Processing module: {module_name}")

                # Initialize and run fetcher
                fetcher = config["fetcher"]()
                items = fetcher.fetch()

                if not items:
                    print(f"[FetchJob] No items found for {module_name}")
                    modules_processed[module_name] = {"count": 0, "hero": None}
                    continue

                # Select hero using AI
                hero = summarizer.select_hero(items, module_name)

                # Process hero with deep summary
                if hero:
                    print(f"[FetchJob] Processing hero for {module_name}: {hero.title[:40]}...")
                    if module_name == "twitter":
                        # Twitter hero 也用推文翻译方法
                        summarizer.translate_tweet(hero)
                    elif module_name == "youtube":
                        # YouTube hero 也用视频翻译方法
                        summarizer.translate_video(hero)
                    elif module_name == "apple_podcast":
                        # Apple Podcast 复用视频翻译方法
                        summarizer.translate_video(hero)
                    else:
                        hero = summarizer.process_hero(hero, config["type"])

                # Batch translate other items
                other_items = [i for i in items if i.id != hero.id] if hero else items
                if module_name == "twitter":
                    # Twitter 使用专门的翻译方法
                    print(f"[FetchJob] Translating {len(other_items[:10])} tweets...")
                    summarizer.batch_translate_tweets(other_items[:10])
                elif module_name == "youtube":
                    # YouTube 使用专门的翻译方法
                    print(f"[FetchJob] Translating {len(other_items[:10])} videos...")
                    summarizer.batch_translate_videos(other_items[:10])
                elif module_name == "apple_podcast":
                    # Apple Podcast 复用视频翻译方法
                    print(f"[FetchJob] Translating {len(other_items[:10])} podcasts...")
                    summarizer.batch_translate_videos(other_items[:10])
                else:
                    summarizer.batch_translate(other_items[:10])

                # Clear old items for this module
                db.query(Item).filter(Item.module == module_name).delete()
                db.commit()  # 必须先提交删除操作，避免主键冲突

                # Save items to database
                for idx, item in enumerate(items[:30]):
                    is_hero = 1 if hero and item.id == hero.id else 0

                    db_item = Item(
                        id=f"{module_name}_{item.id}",
                        module=module_name,
                        title=item.title,
                        title_zh=item.title_zh,
                        summary=item.summary,
                        link=item.link,
                        source=item.source,
                        author=item.author,
                        pub_date=_parse_date(item.pub_date),
                        thumbnail=item.thumbnail,
                        tags=item.tags,
                        fame_score=item.fame_score,
                        extra=item.extra,
                        core_insight=item.extra.get("core_insight", ""),
                        key_points=item.extra.get("key_points", []),
                        is_hero=is_hero,
                        fetch_run_id=run_id,
                    )
                    db.add(db_item)

                db.commit()

                modules_processed[module_name] = {
                    "count": len(items[:30]),
                    "hero": hero.title if hero else None,
                }
                total_items += len(items[:30])

                print(f"[FetchJob] Saved {len(items[:30])} items for {module_name}")

            except Exception as e:
                error_msg = f"{module_name}: {str(e)}"
                errors.append(error_msg)
                print(f"[FetchJob] Error processing {module_name}: {e}")
                traceback.print_exc()

        # Update fetch run status
        fetch_run = db.query(FetchRun).filter(FetchRun.id == run_id).first()
        if fetch_run:
            fetch_run.status = "completed"
            fetch_run.completed_at = datetime.now()
            fetch_run.modules_processed = modules_processed
            fetch_run.total_items = total_items
            fetch_run.errors = errors
            db.commit()

        print(f"\n[FetchJob] Completed! Total items: {total_items}")

    except Exception as e:
        print(f"[FetchJob] Fatal error: {e}")
        traceback.print_exc()

        fetch_run = db.query(FetchRun).filter(FetchRun.id == run_id).first()
        if fetch_run:
            fetch_run.status = "failed"
            fetch_run.completed_at = datetime.now()
            fetch_run.errors = [str(e)]
            db.commit()

    finally:
        db.close()


def _parse_date(date_str: str):
    """Parse date string to datetime"""
    if not date_str:
        return None
    try:
        from dateutil import parser
        return parser.parse(date_str)
    except:
        return None
