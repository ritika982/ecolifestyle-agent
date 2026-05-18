CITY_SCHEMES = {
    "patna": [
        "PM Surya Ghar - 40 percent solar subsidy via BREDA Bihar",
        "Swachh Bharat Mission Phase 2 - Patna Municipal waste collection",
        "Bihar Jal-Jeevan Hariyali Mission - ponds, trees, solar pumps",
        "FAME II - up to 1.5 lakh on electric two-wheelers",
        "Patna Smart City e-waste collection points near Boring Road",
    ],
    "bihar": [
        "BREDA Bihar Renewable Energy Dev Agency for rooftop solar",
        "Bihar Jal-Jeevan Hariyali Mission - 24000 crore for environment",
        "PM KUSUM solar pumps for farmers 90 percent subsidy",
        "FAME II EV subsidy through Bihar dealers",
    ],
    "delhi": [
        "Delhi EV Policy - 30000 rupees subsidy on electric two-wheelers",
        "Delhi Single Use Plastic Ban strictly enforced",
        "DDA Composting Units in RWA societies",
        "PM Surya Ghar apply via Delhi DISCOM portal",
    ],
    "mumbai": [
        "Maharashtra Plastic Ban - fines 5000 to 25000 rupees",
        "BMC mandatory 3-bin waste segregation",
        "MCGM Free Compost Bin Scheme for housing societies",
        "Maharashtra EV Policy 25000 rupee subsidy on e-bikes",
    ],
    "bangalore": [
        "BBMP 181 Dry Waste Collection Centres across Bengaluru",
        "Karnataka EV Policy 100 percent road tax waiver",
        "KREDL Rooftop Solar Karnataka subsidy plus central scheme",
        "BBMP mandatory 3-bin waste segregation",
    ],
    "kolkata": [
        "KMC door-to-door waste collection most wards",
        "West Bengal Plastic Ban bags below 75 micron prohibited",
        "WBSEDCL Solar Net Metering simpler approval process",
        "Eco Park New Town e-waste drop facility open to public",
    ],
    "chennai": [
        "Tamil Nadu Comprehensive Plastic Ban enforced by TNPCB",
        "GCC mandatory 3-bin segregation every household",
        "TANGEDCO Solar Net Metering simplified process",
        "Tamil Nadu EV Policy 2023 subsidies and road tax waiver",
    ],
    "hyderabad": [
        "GHMC door-to-door garbage collection citywide",
        "Telangana EV Policy 10000 rupee incentive on e-bikes",
        "TSREDCO Telangana solar rooftop approvals",
        "Swachh Hyderabad composting projects",
    ],
}

NATIONAL = [
    "PM Surya Ghar - 40 percent subsidy rooftop solar 300 units free monthly",
    "FAME II - up to 1.5 lakh on electric two-wheelers",
    "PM KUSUM - 90 percent subsidy solar pumps for farmers",
    "Swachh Bharat Mission Phase 2 solid waste management",
    "Plastic Waste Management Rules 2021 single use plastic ban",
    "E-Waste Management Rules 2022 return e-waste to authorised collectors",
]


def get_local_schemes(location):
    loc = location.lower().strip()
    for key, schemes in CITY_SCHEMES.items():
        if key in loc or loc in key:
            result = f"Eco schemes for {location}:\n"
            result += "\n".join(f"- {s}" for s in schemes)
            return result
    result = f"National eco schemes for {location}:\n"
    result += "\n".join(f"- {s}" for s in NATIONAL)
    return result