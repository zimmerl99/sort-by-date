Sample Json Request Contents to get your list of dates sorted:
{
        "message": "Date Sorting Microservice Help",
        "endpoint": "POST /dates",
        "example_request": {
            "dates": [
                "2025-12-31",
                "01/15/2025",
                "January 3, 2025",
                "2025-02-14"
            ],
            "output_format": "%m/%d/%Y"
        },
        "example_response": {
            "sorted_dates": [
                "01/03/2025",
                "01/15/2025",
                "02/14/2025",
                "12/31/2025"
            ],
            "count": 4
        },
        "supported_input_formats": [
            "2025-01-15 (YYYY-MM-DD)",
            "01/15/2025 (MM/DD/YYYY)",
            "15/01/2025 (DD/MM/YYYY)",
            "2025/01/15 (YYYY/MM/DD)",
            "January 15, 2025 (Month DD, YYYY)",
            "Jan 15, 2025 (Mon DD, YYYY)",
            "15-01-2025 (DD-MM-YYYY)",
            "2025.01.15 (YYYY.MM.DD)",
            "20250115 (YYYYMMDD)"
        ],
        "common_output_formats": {
            "%Y-%m-%d": "2025-01-15",
            "%m/%d/%Y": "01/15/2025",
            "%d/%m/%Y": "15/01/2025",
            "%B %d, %Y": "January 15, 2025",
            "%b %d, %Y": "Jan 15, 2025",
            "%Y/%m/%d": "2025/01/15"
        },
        "notes": [
            "The service accepts dates in various formats",
            "If output_format is not specified, defaults to YYYY-MM-DD",
            "Can handle mixed input formats in the same request",
            "No external dependencies required - uses only Python built-ins"
        ]
