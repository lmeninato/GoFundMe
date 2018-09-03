#' Data about 1242 GoFundMe pages.
#'
#' A dataset containing various features and attributes of 1242 GoFundMe pages.
#'
#' @format A data frame with 1242 rows and 14 variables:
#' \describe{
#'   \item{url}{url of GoFundMe page}
#'   \item{Category}{category of the GoFundMe page}
#'   \item{Position}{row position of GoFundMe page on the category url, 0 being the highest position.}
#'   \item{Title}{title of the GoFundMe page}
#'   \item{Location}{location of the creator of the GoFundMe}
#'   \item{Amount_Raised}{amount raised by the GoFundMe page at the time of web scraping}
#'   \item{Goal}{goal amount of the GoFundMe page}
#'   \item{Number_of_Donators}{number of unique donors to the GoFundMe page}
#'   \item{Length_of_Fundraising}{approximate number of days the GoFundMe page has been active}
#'   \item{FB_Shares}{number of Facebook shares of the GoFundMe page}
#'   \item{text}{summary of the GoFundMe page text}
#'   \item{Latitude}{approximate latitude of the GoFundMe page}
#'   \item{Longitude}{approximate longitude of the GoFundMe page} 
#' }
#' @source \url{http://www.gofundme.com}
"gfm_df"
