"""
Add column to metadata to denote 'focal' samples based on supplied region
Rewrite location, division and country for non-focal samples to be region
Rewrite division_exposure and country_exposure for non-focal samples to be region_exposure
"""

import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Add column to metadata to denote 'focal' samples based on supplied region",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--metadata", type = str, required=True, help="metadata")
    parser.add_argument("--region", type=str, required=False, help="focal region")
    parser.add_argument("--country", type=str, required=False, help="focal country")
    parser.add_argument("--division", type=str, required=False, help="focal division")
    parser.add_argument("--location", type=str, required=False, help="focal location")
    parser.add_argument("--composite", type=str, required=False, help="composite sampling")
    parser.add_argument("--output", type=str, required=True, help="adjusted metadata")
    args = parser.parse_args()

    fix_casing = {
        "asia": "Asia",
        "africa": "Africa",
        "europe": "Europe",
        "north-america": "North America",
        "oceania": "Oceania",
        "south-america": "South America"
    }

    metadata = pd.read_csv(args.metadata, delimiter='\t')

    if args.region in fix_casing:
        focal_region = fix_casing[args.region]
    else:
        metadata.to_csv(args.output, index=False, sep="\t")
        exit()

    print("Adjusting metadata for focal region", args.region)


    metadata.insert(12, 'focal', True)

    metadata.loc[metadata.region != focal_region, 'focal'] = False
    metadata.loc[metadata.region != focal_region, 'location'] = ""
    metadata.loc[metadata.region != focal_region, 'division'] = metadata.region
    metadata.loc[metadata.region != focal_region, 'country'] = metadata.region
    metadata.loc[metadata.region != focal_region, 'division_exposure'] = metadata.region_exposure
    metadata.loc[metadata.region != focal_region, 'country_exposure'] = metadata.region_exposure
    metadata.loc[(metadata.region == focal_region) & (metadata.region_exposure != focal_region), 'division_exposure'] = metadata.region_exposure
    metadata.loc[(metadata.region == focal_region) & (metadata.region_exposure != focal_region), 'country_exposure'] = metadata.region_exposure
    metadata.loc[(metadata.region == focal_region) & (metadata.division_exposure.isna()), 'division_exposure'] = metadata.division
    metadata.loc[(metadata.region == focal_region) & (metadata.country_exposure.isna()), 'country_exposure'] = metadata.country

    metadata.to_csv(args.output, index=False, sep="\t")
