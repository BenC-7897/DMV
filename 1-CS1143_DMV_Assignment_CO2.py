import pandas as pd


# 1. Define the 10-region mapping


regions10 = {
    # 1) North America (US & Canada only)
    "North America": [
        "United States",
        "Canada",
    ],

    # 2) Latin America & Caribbean
    "Latin America & Caribbean": [
        "Mexico", "Argentina", "Brazil", "Chile", "Colombia", "Peru", "Venezuela",
        "Uruguay", "Paraguay", "Bolivia", "Ecuador",
        "Panama", "Costa Rica", "Nicaragua", "Honduras", "El Salvador", "Guatemala",
        "Cuba", "Dominican Republic", "Haiti",
        "Jamaica", "Bahamas", "Barbados", "Trinidad and Tobago", "Belize",
        "Antigua and Barbuda", "Dominica", "Grenada",
        "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
        "Aruba", "Curacao", "Bonaire Sint Eustatius and Saba",
        "British Virgin Islands", "Bermuda",
        "Guyana", "Suriname",
        "Anguilla", "Montserrat", "Saint Pierre and Miquelon",
        "Sint Maarten (Dutch part)", "Turks and Caicos Islands",
    ],

    # 3) Europe & Russia
    "Europe & Russia": [
        # Western & Northern Europe
        "United Kingdom", "Ireland", "France", "Belgium", "Netherlands",
        "Luxembourg", "Germany", "Austria", "Switzerland",
        "Iceland", "Norway", "Sweden", "Finland", "Denmark",
        "Faroe Islands", "Monaco", "Liechtenstein", "Andorra", "Greenland",
        # Southern/Eastern Europe & Balkans & Baltics
        "Spain", "Portugal", "Italy", "Greece", "Malta", "Cyprus",
        "Poland", "Czechia", "Slovakia", "Hungary", "Romania", "Bulgaria",
        "Slovenia", "Croatia", "Serbia", "Bosnia and Herzegovina",
        "Montenegro", "North Macedonia", "Kosovo",
        "Estonia", "Latvia", "Lithuania", "Moldova", "Belarus", "Ukraine",
        "Albania", "San Marino", "Vatican",
        # Russia & Caucasus
        "Russia", "Armenia", "Azerbaijan", "Georgia",
    ],

    # 4) MENA (Middle East & North Africa)
    "MENA": [
        "Turkey", "Iran", "Iraq", "Israel", "Jordan", "Lebanon", "Palestine",
        "Saudi Arabia", "United Arab Emirates", "Qatar", "Bahrain", "Kuwait",
        "Oman", "Yemen", "Syria",
        "Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "Sudan",
    ],

    # 5) Sub-Saharan Africa
    "Sub-Saharan Africa": [
        "South Africa", "Nigeria", "Ethiopia", "Kenya", "Ghana", "Cameroon",
        "Angola", "Tanzania", "Uganda", "Senegal", "Cote d'Ivoire",
        "Botswana", "Burkina Faso", "Burundi", "Chad", "Central African Republic",
        "Congo", "Democratic Republic of Congo", "Equatorial Guinea", "Eritrea",
        "Eswatini", "Gabon", "Gambia", "Guinea", "Guinea-Bissau", "Lesotho",
        "Liberia", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius",
        "Mozambique", "Namibia", "Niger", "Rwanda", "Sao Tome and Principe",
        "Seychelles", "Sierra Leone", "Somalia", "South Sudan", "Togo", "Zambia",
        "Zimbabwe", "Cape Verde", "Comoros", "Djibouti", "Saint Helena",
        "Benin",
    ],

    # 6) South Asia
    "South Asia": [
        "India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal",
        "Bhutan", "Afghanistan", "Maldives",
    ],

    # 7) Southeast Asia
    "Southeast Asia": [
        "Indonesia", "Malaysia", "Philippines", "Thailand", "Vietnam",
        "Myanmar", "Cambodia", "Laos", "Singapore", "Brunei", "East Timor",
    ],

    # 8) East Asia & China
    "East Asia & China": [
        "China",
        "Japan", "South Korea", "North Korea",
        "Taiwan", "Hong Kong", "Macao",
    ],

    # 9) Central Asia & Mongolia
    "Central Asia & Mongolia": [
        "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan",
        "Uzbekistan", "Mongolia",
    ],

    # 10) Oceania
    "Oceania": [
        "Australia", "New Zealand", "Papua New Guinea",
        "Fiji", "Samoa", "Tonga", "Vanuatu", "Solomon Islands",
        "Kiribati", "Nauru", "Tuvalu", "Palau",
        "Marshall Islands", "Micronesia (country)",
        "New Caledonia", "French Polynesia", "Wallis and Futuna",
        "Cook Islands", "Niue", "Christmas Island",
    ],
}

# Flatten to a country -> region dict
country_to_region = {}
for region, countries in regions10.items():
    for c in countries:
        country_to_region[c] = region


# 2. Load OWID CO2 data


# Path to OWID file


url = "https://owid-public.owid.io/data/co2/owid-co2-data.csv"

co2 = pd.read_csv(url)

# Keep only columns we need
# 'co2' is in million tonnes CO2 (MtCO2) in OWID
keep_cols = ["country", "year", "co2"]
co2 = co2[keep_cols]

# Drop aggregates & non-country rows by using only countries in our mapping
co2 = co2[co2["country"].isin(country_to_region.keys())].copy()

# Restrict to years >= 1945
co2 = co2[co2["year"] >= 1945].copy()

# Drop rows where co2 is NaN
co2 = co2.dropna(subset=["co2"])

# Give CO2 a clearer name (already in MtCO2)
co2["co2_mt"] = co2["co2"]


# 3. Map countries to regions


co2["region"] = co2["country"].map(country_to_region)

# Sanity check: any country not mapped? (should be empty)
missing = co2[co2["region"].isna()]["country"].unique()
print("Missing region mapping:", missing)


# 4. Aggregate to region × year


co2_region_year = (
    co2
    .groupby(["region", "year"], as_index=False)["co2_mt"]
    .sum()
    .rename(columns={"co2_mt": "co2_total"})
)

# Optional: sort
co2_region_year = co2_region_year.sort_values(["region", "year"]).reset_index(drop=True)

print(co2_region_year.head())


# 5. Save to CSV


co2_region_year.to_csv("co2_region_year_10regions.csv", index=False)
print("Saved co2_region_year_10regions.csv")
