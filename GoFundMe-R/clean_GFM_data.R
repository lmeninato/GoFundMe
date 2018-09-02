setwd("~/Github/GoFundMe")

library(tidyverse)

gfm_df = read_tsv("GFM_data.csv")

gfm_df <- gfm_df %>%
  select(-c(1))

donation_goal <- gfm_df %>%
  pull(Goal)

num_donors <- gfm_df %>%
  pull(Number_of_Donators)

length_fundraising <- gfm_df %>%
  pull(Length_of_Fundraising)

fb_shares <- gfm_df %>%
  pull(FB_Shares)

gfm_hearts <- gfm_df %>%
  pull(GFM_hearts)

transform_donation_goal <- function(goal){
  goal = replace_na(goal, "NA")
  goal = str_replace_all(goal, ",", "")
  
  
  if (str_detect(goal, "M")){
    
    goal = str_replace(goal, "M", "")
    return(as.numeric(goal)*1000000)
    
  }
  
  if (str_detect(goal, "k") | str_detect(goal, "K")){
    goal = str_replace(goal, "k", "")
    
    return(as.numeric(goal)*1000)
  }
  
  else {
    
    return(as.numeric(goal))
    
  }
}

donation_goal <- map_dbl(donation_goal, transform_donation_goal)
num_donors <- map_dbl(num_donors, transform_donation_goal)
fb_shares <- map_dbl(fb_shares, transform_donation_goal)
gfm_hearts <- map_dbl(gfm_hearts, transform_donation_goal)



gfm_df = gfm_df %>%
  mutate(Goal = donation_goal) %>%
  mutate(Number_of_Donators = num_donors) %>%
  mutate(FB_Shares = fb_shares) %>%
  mutate(GFM_hearts = gfm_hearts)
