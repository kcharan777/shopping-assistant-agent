from typing import List, Dict, Any

# Curated reference catalogue for offline mode or initial testing
# Clearly identified as sample reference data per user instructions
SAMPLE_CATALOGUE: List[Dict[str, Any]] = [
    {
        "id": "sample_laptop_01",
        "name": "Lenovo IdeaPad Slim 3 12th Gen Intel Core i5",
        "category": "Laptops",
        "brand": "Lenovo",
        "price_inr": 52990.0,
        "original_price_inr": 68990.0,
        "rating": 4.3,
        "reviews_count": 2150,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80",
        "retailer": "Amazon.in",
        "retailer_url": "https://www.amazon.in/dp/B0B56CY8H2",
        "availability": "In Stock",
        "specifications": {
            "Processor": "Intel Core i5-1235U (10 Cores, up to 4.4 GHz)",
            "RAM": "16GB DDR4 3200MHz",
            "Storage": "512GB NVMe M.2 SSD",
            "Display": "15.6-inch FHD (1920x1080) Anti-glare 250 nits",
            "Graphics": "Integrated Intel Iris Xe Graphics",
            "Battery": "45Wh (Up to 7 hours)",
            "Weight": "1.63 kg",
            "OS": "Windows 11 Home + MS Office 2021"
        },
        "features": [
            "16GB RAM out of the box for smooth coding and multitasking",
            "Rapid Charge technology: 2 hours runtime in 15 mins",
            "Physical webcam privacy shutter and Dolby Audio speakers",
            "Lightweight design suitable for daily college commutes"
        ],
        "strengths": [
            "Generous 16GB RAM prevents slowdowns during software compilation",
            "Comfortable full-size keyboard with numeric keypad",
            "Excellent thermal management for sustained workloads"
        ],
        "limitations": [
            "250-nit display is average for outdoor sunny environments",
            "Integrated graphics not suited for heavy 3D gaming"
        ],
        "source": "Sample Catalogue (Offline Reference)"
    },
    {
        "id": "sample_laptop_02",
        "name": "HP 15s 12th Gen Intel Core i5-1235U",
        "category": "Laptops",
        "brand": "HP",
        "price_inr": 54990.0,
        "original_price_inr": 67990.0,
        "rating": 4.2,
        "reviews_count": 1840,
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80",
        "retailer": "Flipkart",
        "retailer_url": "https://www.flipkart.com",
        "availability": "In Stock",
        "specifications": {
            "Processor": "Intel Core i5-1235U 12th Gen",
            "RAM": "16GB DDR4 RAM",
            "Storage": "512GB PCIe NVMe M.2 SSD",
            "Display": "15.6-inch FHD Micro-edge Anti-glare",
            "Graphics": "Intel Iris Xe Graphics",
            "Battery": "41Wh with Fast Charge",
            "Weight": "1.69 kg",
            "OS": "Windows 11 Home"
        },
        "features": [
            "Fast charge: 0 to 50% in approximately 45 minutes",
            "HP True Vision 720p HD camera with dual array microphones",
            "Micro-edge bezel display for immersive viewing experience"
        ],
        "strengths": [
            "Reliable HP nationwide service network and build",
            "Dual-channel 16GB memory for responsive IDE and browser tabs",
            "Crisp anti-glare display for long reading and studying sessions"
        ],
        "limitations": [
            "No keyboard backlighting on this base configuration",
            "Battery backup tops out at 5.5 to 6 hours on medium brightness"
        ],
        "source": "Sample Catalogue (Offline Reference)"
    },
    {
        "id": "sample_laptop_03",
        "name": "ASUS Vivobook 15 AMD Ryzen 7 5800HS",
        "category": "Laptops",
        "brand": "Asus",
        "price_inr": 48990.0,
        "original_price_inr": 72990.0,
        "rating": 4.4,
        "reviews_count": 3410,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80",
        "retailer": "Amazon.in",
        "retailer_url": "https://www.amazon.in",
        "availability": "In Stock",
        "specifications": {
            "Processor": "AMD Ryzen 7 5800HS (8 Cores, 16 Threads, up to 4.4 GHz)",
            "RAM": "16GB DDR4",
            "Storage": "512GB M.2 NVMe PCIe 3.0 SSD",
            "Display": "15.6-inch FHD (1920x1080) 16:9 aspect ratio",
            "Graphics": "AMD Radeon Graphics",
            "Battery": "42Wh (Up to 6 hours)",
            "Weight": "1.70 kg",
            "OS": "Windows 11 Home"
        },
        "features": [
            "8-Core Ryzen 7 processor offers outstanding raw multithreaded compute",
            "180-degree lay-flat ErgoLift hinge for group sharing",
            "ASUS Antibacterial Guard surface treatment"
        ],
        "strengths": [
            "Superb multithreaded CPU performance at under ₹50,000",
            "High value-to-price ratio with 16GB RAM included",
            "Solid hinge durability and typing comfort"
        ],
        "limitations": [
            "Single-band HDMI port limits external 4K@60Hz output",
            "Display color gamut is standard 45% NTSC"
        ],
        "source": "Sample Catalogue (Offline Reference)"
    },
    {
        "id": "sample_laptop_04",
        "name": "Acer Aspire Lite 12th Gen Intel Core i3-1215U",
        "category": "Laptops",
        "brand": "Acer",
        "price_inr": 31990.0,
        "original_price_inr": 49990.0,
        "rating": 4.1,
        "reviews_count": 980,
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&auto=format&fit=crop&q=80",
        "retailer": "Flipkart",
        "retailer_url": "https://www.flipkart.com",
        "availability": "In Stock",
        "specifications": {
            "Processor": "Intel Core i3-1215U (6 Cores, up to 4.4 GHz)",
            "RAM": "8GB DDR4 (Expandable to 32GB)",
            "Storage": "512GB NVMe SSD",
            "Display": "15.6-inch Full HD LED-backlit TFT LCD",
            "Graphics": "Intel UHD Graphics",
            "Battery": "36Wh",
            "Weight": "1.59 kg",
            "OS": "Windows 11 Home"
        },
        "features": [
            "Ultra-budget option with genuine 12th Gen Intel architecture",
            "Thin and light premium steel-gray chassis",
            "Expandable RAM slots for future upgrades"
        ],
        "strengths": [
            "Most affordable entry point under ₹35,000 for everyday coursework",
            "Fast NVMe SSD boot times",
            "Lightweight form factor (1.59 kg)"
        ],
        "limitations": [
            "Only 8GB default RAM (recommended to upgrade for heavy IDEs)",
            "Battery life is around 4.5 hours under active browsing"
        ],
        "source": "Sample Catalogue (Offline Reference)"
    },
    {
        "id": "sample_laptop_05",
        "name": "Dell 15 Thin & Light Laptop Intel Core i5-1235U",
        "category": "Laptops",
        "brand": "Dell",
        "price_inr": 49990.0,
        "original_price_inr": 64990.0,
        "rating": 4.2,
        "reviews_count": 1420,
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600&auto=format&fit=crop&q=80",
        "retailer": "Reliance Digital",
        "retailer_url": "https://www.reliancedigital.in",
        "availability": "In Stock",
        "specifications": {
            "Processor": "Intel Core i5-1235U 12th Gen",
            "RAM": "16GB DDR4",
            "Storage": "512GB SSD",
            "Display": "15.6-inch FHD 120Hz 250 nits Narrow Border",
            "Graphics": "Intel UHD Graphics",
            "Battery": "41Wh (ExpressCharge)",
            "Weight": "1.66 kg",
            "OS": "Windows 11 + Office H&S 2021"
        },
        "features": [
            "Smooth 120Hz refresh rate display rare at this price point",
            "Dell ComfortView low blue light hardware solution",
            "Spill-resistant keyboard and lift-hinge ergonomics"
        ],
        "strengths": [
            "120Hz screen provides noticeably fluid scrolling and UI responsiveness",
            "Dell build quality and customer support reliability",
            "ExpressCharge powers up to 80% in 60 minutes"
        ],
        "limitations": [
            "Chassis is primarily matte plastic",
            "Audio output through downward speakers is modest"
        ],
        "source": "Sample Catalogue (Offline Reference)"
    }
]
