#!/usr/bin/env python3
"""
Command-line script to ingest lessons into the database
Usage: python ingest_lessons.py --directory ../lessons_500
"""

import argparse
import logging
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, init_db
from app.lesson_ingestion import ingest_all_lessons, save_ingestion_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for lesson ingestion
    """
    parser = argparse.ArgumentParser(
        description='Ingest German lessons into Prize2Pride database'
    )
    parser.add_argument(
        '--directory',
        default='../lessons_500',
        help='Directory containing lesson Markdown files'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database tables before ingestion'
    )
    parser.add_argument(
        '--report',
        default='ingestion_report.json',
        help='Output file for ingestion report'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        logger.error(f"❌ Directory not found: {args.directory}")
        sys.exit(1)
    
    # Initialize database if requested
    if args.init_db:
        logger.info("🔧 Initializing database tables...")
        try:
            init_db()
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing database: {str(e)}")
            sys.exit(1)
    
    # Get database session
    try:
        db = SessionLocal()
        logger.info("✅ Database connection established")
    except Exception as e:
        logger.error(f"❌ Error connecting to database: {str(e)}")
        sys.exit(1)
    
    # Run ingestion
    try:
        logger.info(f"📚 Starting lesson ingestion from {args.directory}...")
        results = ingest_all_lessons(args.directory, db)
        
        # Save report
        save_ingestion_report(results, args.report)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 INGESTION SUMMARY")
        print("="*60)
        print(f"Total Files:        {results['total_files']}")
        print(f"Successful:         {results['successful']}")
        print(f"Failed:             {results['failed']}")
        print(f"Flashcards Created: {results['total_flashcards']}")
        print(f"Exercises Created:  {results['total_exercises']}")
        print(f"Report:             {args.report}")
        print("="*60 + "\n")
        
        # Exit with appropriate code
        sys.exit(0 if results['failed'] == 0 else 1)
    
    except Exception as e:
        logger.error(f"❌ Error during ingestion: {str(e)}")
        sys.exit(1)
    
    finally:
        db.close()

if __name__ == '__main__':
    main()
