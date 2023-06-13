library(tidyverse)

files_path <- "results/foldseek_results_tables"
files <- dir(files_path, pattern="*_aggregated_features_pca_tsne.tsv")

combined_results_table <- data_frame(filename = files) %>% 
  mutate(file_contents = map(filename, ~ read_tsv(file.path(files_path, .)))) %>% 
  unnest(cols=c(file_contents)) %>% 
  mutate(TM_v_query = str_extract(TM_v_query, "\\S+")) %>%
  mutate(reference = str_extract(filename, "(?<=_)[^_]+(?=_)")) %>% 
  select(reference, protid, sequence.length, organism.scientificName, organism.commonName, organism.lineage, TM_v_query)

reference_lengths <- combined_results_table %>% 
  filter(reference == protid) %>% 
  mutate(reference_length = sequence.length) %>% 
  select(reference, reference_length)

combined_table_filtered <- combined_results_table %>% 
  left_join(reference_lengths) %>% 
  filter(TM_v_query > .5) %>% 
  select(reference, reference_length, protid, sequence.length, TM_v_query, organism.scientificName, organism.commonName, organism.lineage)

stringent_filtered_table <- combined_table_filtered %>% 
  mutate(proportion_of_reference = sequence.length / reference_length) %>% 
  filter(TM_v_query > .85) %>% 
  filter(proportion_of_reference > .7)

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

write_tsv(stringent_filtered_table, "results/filtered-protein-hits-table.tsv")
