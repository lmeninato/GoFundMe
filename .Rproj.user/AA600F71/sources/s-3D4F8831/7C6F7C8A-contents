load("data/clean_gfm_data.RData")

# summary(gfm_df)
# sum(gfm_df$Amount_Raised, na.rm = TRUE)

library(ggmap)

temp_df = na.omit(gfm_df)

map <- get_map(location = 'USA', zoom = 3)

mapPoints <- ggmap(map) +
  geom_point(aes(x = Longitude, y = Latitude, size = log(Amount_Raised)), data = temp_df, alpha = .5)