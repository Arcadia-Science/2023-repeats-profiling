library(tidyverse)

# combined table results 
combined_results_table <- read_tsv("results/combined-foldseek-results-table.tsv")

# plot comparisons of the protein hit length vs Tm score, color by reference 
combined_results_table %>% 
  ggplot(aes(x=TM_v_query, y=sequence.length)) + 
  geom_point(aes(color=reference))

combined_results_table %>% 
  filter(TM_v_query > 0.3) %>% 
  ggplot(aes(x=TM_v_query, y=sequence.length)) + 
  geom_point(aes(color=reference))

# group by common name to find information of species with most hits across query proteins

combined_results_table %>%
  filter(TM_v_query > 0.3) %>% 
  group_by(organism.commonName) %>% 
  count() %>% 
  arrange(desc(n))

# stringent filtering 
stringent_filtered_table <- combined_table_refined %>% 
  filter(TM_v_query > .85)

stringent_filtered_table %>% 
  group_by(reference) %>% 
  count() %>% 
  arrange(desc(n))

stringent_filtered_table %>% 
  group_by(organism.scientificName) %>% 
  count() %>% 
  arrange(desc(n))

stringent_filtered_table %>% 
  group_by(organism.commonName) %>% 
  count() %>% 
  arrange(desc(n))
