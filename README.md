# GoFundMe

This is an ongoing project to examine what types of GoFundMe projects are successful as well which GoFundMe pages are scams
or undeserving of donations.
GoFundMe does not provide an API for obtaining data from GoFundMe pages; therefore, this project is a web scraper utilizing
selenium and chromedriver to navigate through the GoFundMe website to extract the top GoFundMe urls.
 I then use requests and BeautifulSoup to parse the raw html of each url in a systematic fashion. I can either directly
extract information from the urls using regex and BeautifulSoup, or engineer features for the dataset (such as getting the latitudes and longitudes from the city where the user has created the GoFundMe). 

The dataset can be accessed easily either by downloading raw tab-delimited `GFM_data.csv` or by loading the `clean_GFM_data.RData` file by installing the R package (to include roxygen2 documentation) with the following command:

```{R}
devtools::install_github("lmeninato/GoFundMe")
```
A lot of information can be found on every GoFundMe url. Here is a sample GFM page:
![sample GFM url](/images/gofundme_sample_url.PNG)

From this we can extract several data points, such as the number of "hearts" a page has, how much money was fundraised by how many different people, text summarizing the cause of the fundraising, etc. Here I highlight how this can be done:

![sample scrape of url](/images/gofundme_sample_scrape.png)

As long as the information is in a consistent location for each url (extracted by navigating the GoFundMe website using selenium for each category) I can have various attributes for each observation (each scraped url).




