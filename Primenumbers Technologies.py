#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup

# Specify the URL for scraping
URL = 'https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787'

# Send a GET request to the server
response = requests.get(URL)

if response.status_code == 200:
    # Parse the HTML content returned by the server
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements having class name as posting-item
    items = soup.find_all('div', {'class': 'posting-item'})

    count = 1
    print("First 5 Job Openings:")
    # Iterate through each item found and extract required details
    for item in items[:5]:
        titleElement = item.h3.a

        # Get job title text
        titleText = titleElement.getText()

        # Get href attribute value of anchor tag
        hrefValue = titleElement['href']

        companyNameElement = item.span.nextSibling

        # Skip span element after the company name
        while not isinstance(companyNameElement, str):
            companyNameElement = companyNameElement.nextSibling

        companyNameText = companyNameElement.strip()

        locationElement = item.p

        # Skip p tags before the location field
        while locationElement.string != None or len(locationElement.strings) == 0:
            locationElement = locationElement.nextSibling

        # Get location string
        locationString = ""
        for s in locationElement.stripped_strings:
            locationString += s + ", "

        # Remove the last comma and space characters
        locationString = locationString[:-2]

        datePostedElement = item.time

        # Get the datetime posted string
        dateTimePostedString = datePostedElement["datetime"]

        descriptionElement = item.ul

        # Check whether there are more than one ul child nodes present inside the li node
        if len(descriptionElement) > 0:
            descList = []
            for d in descriptionElement[0].children:
                if isinstance(d, bs4.element.NavigableString):
                    continue
                else:
                    descList.append(d.getText())
            descriptionText = " ".join(descList).replace("\n", " ")
        else:
            descriptionText = "Not provided."

        # Construct the output message using extracted values
        outMessage = "{}. {} - {}\n{}\nDate Posted: {}\n".format(count, titleText, companyNameText, locationString,
                                                                  dateTimePostedString)

        # Write to the console window
        print(outMessage)

        # Increment the counter variable
        count += 1

    # Close the connection
    response.close()

else:
    print("Error:", response.status_code)


# In[ ]:




