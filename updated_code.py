import requests
import pandas as pd
from openpyxl import Workbook
from bs4 import BeautifulSoup








def scrape_election_data(url,data):

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content area

    # arr = list[543][5]
    main_content = soup.find('main', class_='inner-content')
    if not main_content:
        print("No main content found")
        return

    container_fluid = main_content.find('div', class_='container-fluid')
    if not container_fluid:
        print("No container-fluid found inside main")
        return

    box_wraper = container_fluid.find('div', class_='box-wraper box-boarder')
    page_title = container_fluid.find('div', class_= 'page-title')
    if not box_wraper:
        print("No box-wraper box-boarder found inside container-fluid")
        return

    inner_container = box_wraper.find('div', class_='container-fluid')
    # Find the h2 element
    constitutuency = soup.find('h2')
    if not inner_container:
        print("No inner container-fluid found inside box-wraper")
        return

    row = inner_container.find('div', class_='row')

    # Extract the constituency name
    constituency_name = constitutuency.find('span').text.strip()

    # Whole constituency name (including hyphen and space)
    full_constituency_name = constituency_name

    # State name (without parentheses)
    state_name = constituency_name.split("(")[1].split(")")[0]

    if not row:
        print("No row found inside inner container-fluid")
        return

    candidates = row.find_all('div', class_='col-md-4 col-12')
    if not candidates:
        print("No candidate columns found in row")
        return

    for candidate in candidates:
        cand_box = candidate.find('div', class_='cand-box')
        if not cand_box:
            print("No cand-box found in candidate column")
            continue

        cand_info = cand_box.find('div', class_='cand-info')
        if not cand_info:
            print("No cand-info found in cand-box")
            continue

        # Extract status information
        status_div = cand_info.find('div', class_=('status leading', 'status won'))


        if status_div:
            status = status_div.find('div', style='text-transform: capitalize').text.strip() if status_div.find('div',
                                                                                                                style='text-transform: capitalize') else "No Status"
            if  status.lower() == 'won' or status.lower() == 'leading':
                votes = status_div.find('div').text.strip() if status_div.find('div') else "No Votes"
                vote_margin = status_div.find('span').text.strip('(+)') if status_div.find('span') else "0"
                vote_margin = int(vote_margin)



                # Extract candidate name and party
                nme_prty = cand_info.find('div', class_='nme-prty')
                if nme_prty:
                    name = nme_prty.find('h5').text.strip() if nme_prty.find('h5') else "No Name"
                    party = nme_prty.find('h6').text.strip() if nme_prty.find('h6') else "No Party"

                    ################## This is optional
                    print(f"Status: {status}")
                    
                    print(full_constituency_name)  # Output: 16 - Anand Gujarat
                    print(f"Vote Margin: {vote_margin}")
                    print(f"Candidate Name: {name}")
                    print(f"Party: {party}")
                    print('-' * 40)
                  ################## This is optional

                    data.append({
                        "Status": status,
                        # "Votes": votes,
                        "Full Constituency Name": full_constituency_name,
                        "Vote Margin": vote_margin,
                        "Candidate Name": name,
                        "Party": party
                    })




data = []


if __name__ == '__main__':
    base_url = 'https://results.eci.gov.in/PcResultGenJune2024/candidateswise-{id}.htm'

    # Dictionary of state/union territory IDs and number of seats
    state_seat_info = {
        'S24': 80,  # Uttar Pradesh
        'S13': 48,  # Maharashtra
        'S25': 42,  # West Bengal
        'S04': 39,  # Bihar
        'S22': 38,  # Tamil Nadu
        'S12': 29,  # Madhya Pradesh
        'S10': 28,  # Karnataka
        'S06': 26,  # Gujarat
        'S20': 25,  # Rajasthan
        'S01': 24,  # Andhra Pradesh
        'S18': 21,  # Odisha
        'S11': 20,  # Kerala
        'S29': 17,  # Telangana
        'S03': 14,  # Assam
        'S27': 14,  # Jharkhand
        'S19': 13,  # Punjab
        'S26': 11,  # Chhattisgarh
        'S07': 10,  # Haryana
        'S28': 5,  # Uttarakhand
        'S08': 4,  # Himachal Pradesh
        'S02': 2,  # Arunachal Pradesh
        'S05': 2,  # Goa
        'S14': 2,  # Manipur
        'S15': 2,  # Meghalaya
        'S23': 2,  # Tripura
        'S16': 1,  # Mizoram
        'S17': 1,  # Nagaland
        'S21': 1,  # Sikkim
        'U08': 6,  # Jammu and Kashmir
        'U05': 7,  # Delhi
        'U01': 1,  # Andaman & Nicobar Islands
        'U02': 1,  # Chandigarh
        'U03': 1,  # Dadra & Nagar Haveli
        'U03': 1,  # Daman & Diu
        'U06': 1,  # Lakshadweep
        'U07': 1,  # Puducherry
    }



    for state_id, num_seats in state_seat_info.items():
        for seat_num in range(1, num_seats + 1):
            full_id = f"{state_id}{seat_num}"
            url = base_url.format(id=full_id)
            # print(f"Scraping URL: {url}")
            scrape_election_data(url,data)



df = pd.DataFrame(data)




df_sorted = df.sort_values(by='Vote Margin', ascending=True)

# Print the entire DataFrame without compression (full output)
print(df_sorted.to_string(index=False))

df_sorted.to_excel('ElectionSortedResult.xlsx', index=False)  # Replace 'sorted_data.xlsx' with your desired filename


