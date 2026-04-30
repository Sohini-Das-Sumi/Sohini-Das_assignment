"""
Batch Processing Example Script for Trinethra

This script demonstrates how to use the TrinethraBatchProcessor to:
1. Process multiple feedbacks from a list
2. Process feedbacks from a CSV file
3. Generate comprehensive batch reports
4. Export results to JSON
"""

import json
from trinethra import TrinethraBatchProcessor


def example_1_list_processing():
    """Example 1: Process a list of feedback transcripts"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Batch Processing from Python List")
    print("="*70)

    batch_processor = TrinethraBatchProcessor()

    feedbacks = [
        "He is very reliable and gets things done on time. Always follows instructions perfectly.",
        "She built an excellent tracking system for production and identified key bottlenecks. Team uses her tools daily.",
        "He does what I ask but doesn't take initiative. No systems thinking evident.",
        "She noticed quality issues and created a dashboard that reduced defects by 20%. Outstanding work.",
        "He helps with coordination but everything stops when he's not there. No lasting systems."
    ]

    result = batch_processor.process_batch_feedbacks(feedbacks)

    if 'error' in result:
        print(f"Error: {result['error']}")
        return

    print_batch_summary(result)


def example_2_csv_processing():
    """Example 2: Process feedbacks from a CSV file"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Batch Processing from CSV File")
    print("="*70)

    batch_processor = TrinethraBatchProcessor()

    # Process the test CSV file
    result = batch_processor.process_csv_file(
        'test_feedbacks.csv',
        feedback_column='feedback'
    )

    if 'error' in result:
        print(f"Error: {result['error']}")
        return

    print_batch_summary(result)


def example_3_export_results():
    """Example 3: Export batch results to JSON file"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Exporting Batch Results to JSON")
    print("="*70)

    batch_processor = TrinethraBatchProcessor()

    result = batch_processor.process_csv_file('test_feedbacks.csv', feedback_column='feedback')

    if 'error' in result:
        print(f"Error: {result['error']}")
        return

    # Save to JSON file
    output_file = 'batch_processing_results.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ Results exported to {output_file}")
    print(f"  Total entries: {result['summary']['total_entries']}")
    print(f"  Average score: {result['summary']['average_score']}/10")


def print_batch_summary(result):
    """Helper function to print batch processing results"""
    summary = result['summary']

    print(f"\n📊 BATCH SUMMARY")
    print("-" * 70)
    print(f"Total entries: {summary['total_entries']}")
    print(f"Successfully processed: {summary['processed_entries']}")
    print(f"Errors: {result['total_errors']}")
    print(f"Error rate: {summary['error_rate']}%")

    print(f"\n📈 PERFORMANCE METRICS")
    print("-" * 70)
    print(f"Average score: {summary['average_score']}/10")
    print(f"Min score: {summary['min_score']}")
    print(f"Max score: {summary['max_score']}")

    print(f"\n📊 SCORE DISTRIBUTION")
    print("-" * 70)
    print("1-3 (Need Attention):  ", summary['score_distribution']['1-3'], "Fellows")
    print("4-6 (Productivity):    ", summary['score_distribution']['4-6'], "Fellows")
    print("7-10 (Performance):    ", summary['score_distribution']['7-10'], "Fellows")

    print(f"\n🎯 BAND DISTRIBUTION")
    print("-" * 70)
    for band, count in summary['band_distribution'].items():
        print(f"{band:.<40} {count} Fellows")

    print(f"\n🔝 TOP KPIs (Most Common)")
    print("-" * 70)
    if summary['common_kpis']:
        for kpi, count in summary['common_kpis'].items():
            print(f"{kpi:.<40} {count} mentions")
    else:
        print("No KPIs identified")

    print(f"\n⚠️  COMMON GAPS")
    print("-" * 70)
    if summary['common_gaps']:
        for gap, count in summary['common_gaps'].items():
            print(f"{gap:.<40} {count} instances")
    else:
        print("No gaps identified")

    print(f"\n🏗️  LAYER DISTRIBUTION")
    print("-" * 70)
    print(f"Execution only:        {summary['layer_distribution']['execution_only']} Fellows")
    print(f"Systems building:      {summary['layer_distribution']['systems_building']} Fellows")
    print(f"Mixed:                 {summary['layer_distribution']['mixed']} Fellows")

    print(f"\n📋 INDIVIDUAL RESULTS")
    print("-" * 70)
    for res in result['results']:
        status = "✓" if not res['errors'] else "⚠"
        print(f"{status} Entry {res['index']:2d}: Score {res['score']:2d} - {res['label']:.<30} ({res['band']})")
        if res['kpis']:
            print(f"        KPIs: {', '.join(res['kpis'])}")
        if res['errors']:
            for error in res['errors']:
                print(f"        Error: {error}")


def create_custom_csv():
    """Helper function to create a custom CSV file"""
    print("\n" + "="*70)
    print("HELPER: Creating Sample CSV File")
    print("="*70)

    import csv

    sample_data = [
        {
            'fellow_name': 'Rajesh Kumar',
            'feedback': 'Very productive. Completes all assigned tasks on time. However, lacks initiative in identifying new problems.',
            'company': 'Manufacturing Inc',
            'tenure': '3 months'
        },
        {
            'fellow_name': 'Sarah Chen',
            'feedback': 'Built a comprehensive dashboard for sales tracking. Identified key bottlenecks in the pipeline. Created SOP that the team now uses daily.',
            'company': 'Tech Startups',
            'tenure': '4 months'
        }
    ]

    filename = 'custom_feedbacks.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['fellow_name', 'feedback', 'company', 'tenure'])
        writer.writeheader()
        writer.writerows(sample_data)

    print(f"✓ Created {filename}")


if __name__ == "__main__":
    print("TRINETHRA BATCH PROCESSING EXAMPLES")
    print("="*70)

    # Run examples
    example_1_list_processing()
    example_2_csv_processing()
    example_3_export_results()

    # Optional: Create and process a custom CSV
    print("\n" + "="*70)
    print("BONUS: Creating and Processing Custom CSV")
    print("="*70)
    create_custom_csv()

    batch_processor = TrinethraBatchProcessor()
    result = batch_processor.process_csv_file('custom_feedbacks.csv', feedback_column='feedback')

    if 'error' not in result:
        print(f"✓ Custom CSV processed: {result['summary']['processed_entries']} entries")
        print(f"  Average score: {result['summary']['average_score']}/10")

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
