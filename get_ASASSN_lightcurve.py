#!/usr/bin/env python
"""
Get ASASSN lightcurves from RA and DEC (and radius in arcmin, default 1 arcmin)
by web scraping the Variable Stars Database (https://asas-sn.osu.edu/variables) and Photometry Database (https://asas-sn.osu.edu/photometry)

Example:
python3 get_ASASSN_lightcurve.py ra dec radius(arcmin)
python3 get_ASASSN_lightcurve.py 0.0317 34.67396 0.5
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import re
import pprint

# Helper function to parse the ASASSN results table and return the closest source
def parse_results_for_the_closest_source(url):
    print("Request URL: ", url)
    variable_stars_database_page = requests.get(url)
    soup = BeautifulSoup(variable_stars_database_page.content, "html.parser")
    
    # ASASSN results
    results_table = soup.find_all("table", class_="table-striped")[0]
    table_body = results_table.find_all("tbody")[0]
    table_head = results_table.find_all("thead")[0]
    
    # Parse the results table and download the lightcurve of the closest source
    if (len(table_body.find_all("tr"))>0):
        th = table_head.find_all("th")
        td = table_body.find_all("td")
        first_row = {
            th[0].text: td[0].find_all("a")[0].text,
            'href': "https://asas-sn.osu.edu"+td[0].find_all("a")[0].get("href"),
            th[1].text: td[1].text,
            th[2].text: td[2].text,
            th[3].text: td[3].text,
            th[4].text: td[4].text,
            th[5].text: td[5].text,
            th[6].text: td[6].text,
            th[7].text: td[7].text,
            th[8].text: td[8].text
        }
        # Print the details of the closest source
        pp = pprint.PrettyPrinter(indent=0)
        pp.pprint(first_row)
        return first_row
    else:
        return 0

# Helper function to download a file
def download_file(url, file_name):
    # Send GET request
    response = requests.get(url)
    # Save file
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
            print(file_name, " downloaded\n")
    else:
        print(response.status_code)

# Download the lightcurve of the closest source in ASASSN Variable Stars Database
def query_ASASSN_variable_stars_database(ra, dec, radius=1, save_lightcurve_csv=True):
    # Request ASASSN lightcurve
    URL = "https://asas-sn.osu.edu/variables?ra="+str(ra)+"&dec="+str(dec)+"&radius="+str(radius)+"&vmag_min=&vmag_max=&amplitude_min=&amplitude_max=&period_min=&period_max=&lksl_min=&lksl_max=&class_prob_min=&class_prob_max=&parallax_over_err_min=&parallax_over_err_max=&name=&sort_by=raj2000&sort_order=asc&show_non_periodic=true&show_without_class=true&asassn_discov_only=false&"
    closest_source = parse_results_for_the_closest_source(URL)

    if closest_source:
        # Get the Gaia EDR3 ID of the source
        ## This section can be skipped and the lightcurve can be saved with the ASASSN name
        lightcurve_URL = closest_source['href']
        lightcurve_page = requests.get(lightcurve_URL)
        lightcurve_soup = BeautifulSoup(lightcurve_page.content, "html.parser")
        gaia_edr3_id = lightcurve_soup(text = re.compile('EDR3_ID'))[0].parent.parent.parent.find_all("span", class_="star-data__value")[0].text
        gaia_edr3_id = gaia_edr3_id.replace('\n','')
        print("Gaia EDR3 ID: ", gaia_edr3_id)
        
        # Download the lightcurve of the closest source
        if save_lightcurve_csv:
            folder_name = "variable_stars_database/"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            download_file(closest_source['href']+".csv", folder_name+"EDR3_"+gaia_edr3_id+".csv")
    else:
        print("\nNo corresponding source found in the ASASSN Variable Stars Database\nRequest: ", URL)

# Download the lightcurve of the closest source in ASASSN Photometry Database
def query_ASASSN_photometry_database(ra, dec, radius=1, save_lightcurve_csv=True):
    # Request ASASSN lightcurve
    URL = "https://asas-sn.osu.edu/photometry?utf8=%E2%9C%93&ra="+str(ra)+"&dec="+str(dec)+"&radius="+str(radius)+"&vmag_min=&vmag_max=&epochs_min=&epochs_max=&rms_min=&rms_max=&sort_by=raj2000"
    closest_source = parse_results_for_the_closest_source(URL)

    if closest_source:
        # Download the lightcurve of the closest source
        if save_lightcurve_csv:
            folder_name = "photometry_database/"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            download_file(closest_source['href']+".csv", folder_name+"RA"+str(ra)+"_DEC"+str(dec)+"_Distance"+str(closest_source['Distance (arcsec)'])+"arcsec.csv")
    else:
        print("\nNo corresponding source found in the ASASSN Photometry Database\nRequest: ", URL)

if __name__ == "__main__":
    ra = sys.argv[1]      # deg
    dec = sys.argv[2]     # deg
    radius = sys.argv[3]  # arcmin
    # query_ASASSN_photometry_database(ra, dec, radius)
    query_ASASSN_variable_stars_database(ra, dec, radius)