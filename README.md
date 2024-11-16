Théo Charlot, Nicolas Gouget, Rémi Ilango
M2 ATAL

# distributed_data

# Top 5 Score Pagerank 


## DF no URL partioner (2 and 4 nodes)

| Link                                                                                       | PageRank Score     |
|--------------------------------------------------------------------------------------------|--------------------|
| [Boksa_%28disambiguation%29](http://dbpedia.org/resource/Boksa_%28disambiguation%29)       | 534.3935469409988  |
| [Sid_%28disambiguation%29](http://dbpedia.org/resource/Sid_%28disambiguation%29)           | 429.1328876877597  |
| [Obornjaca](http://dbpedia.org/resource/Obornjaca)                                         | 333.2843275163721  |
| [Bogaras](http://dbpedia.org/resource/Bogaras)                                             | 319.34832872672814 |
| [Blazov](http://dbpedia.org/resource/Blazov)                                               | 283.6398303443939  |


## RDD With URL partioner (2 and 4 nodes)

| Link                                                                                                      | PageRank Score       |
|-----------------------------------------------------------------------------------------------------------|----------------------|
| [Living_people](http://dbpedia.org/resource/Living_people)                                                | 36794.33146754514    |
| [United_States](http://dbpedia.org/resource/United_States)                                                | 13201.340151981216   |
| [Race_and_ethnicity_in_the_United_States_Census](http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census) | 10371.162005541357   |
| [List_of_sovereign_states](http://dbpedia.org/resource/List_of_sovereign_states)                          | 5195.347361862181    |
| [United_Kingdom](http://dbpedia.org/resource/United_Kingdom)                                              | 4923.82130931521     |

## cluster-df-partition-2w

| Link                                                                                                   | PageRank Score    |
|--------------------------------------------------------------------------------------------------------|-------------------|  
| [Boksa_%28disambiguation%29](http://dbpedia.org/resource/Boksa_%28disambiguation%29)                   | 534.3935469409988 |
| [Sid_%28disambiguation%29](http://dbpedia.org/resource/Sid_%28disambiguation%29)                       | 429.1328876877597 |
| [Obornjaca](http://dbpedia.org/resource/Obornjaca)                                                     | 333.2843275163721 |
| [Bogaras](http://dbpedia.org/resource/Bogaras)                                                         | 319.34832872672814 |
| [Blazov](http://dbpedia.org/resource/Blazov)                                                           | 283.6398303443939 |

## cluster-notype-partition-0w
| Link                                                                                                   | PageRank Score    |
|--------------------------------------------------------------------------------------------------------|-------------------|  
| [Living_people](http://dbpedia.org/resource/Living_people)                                             | 36794.33146754523 |
| [United_States](http://dbpedia.org/resource/United_States)                                             | 13201.340151981214 |
| [Race_and_ethnicity_in_the_United_States_Census](http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census)  | 10371.162005541351 |
| [List_of_sovereign_states](http://dbpedia.org/resource/List_of_sovereign_states)                       | 5195.347361862185 |
| [United_Kingdom](http://dbpedia.org/resource/United_Kingdom)                                           | 4923.821309315204 |

# All the cluster rdd with no partition give the same exact results
## cluster-notype-no-partition
| Link                                                                                                   | PageRank Score    |
|--------------------------------------------------------------------------------------------------------|-------------------|  
| [Living_people](http://dbpedia.org/resource/Living_people)                                             | 36794.33146754487 |
| [United_States](http://dbpedia.org/resource/United_States)                                             | 13201.340151981194 |
| [Race_and_ethnicity_in_the_United_States_Census](http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census)  | 10371.162005541348 |
| [List_of_sovereign_states](http://dbpedia.org/resource/List_of_sovereign_states)                       | 5195.347361862185 |
| [United_Kingdom](http://dbpedia.org/resource/United_Kingdom)                                           | 4923.821309315207 |

# All the cluster df with partition give the same exact results
## cluster-df-partition-0w
| Link                                                                                       | PageRank Score     |
|--------------------------------------------------------------------------------------------|--------------------|
| [Boksa_%28disambiguation%29](http://dbpedia.org/resource/Boksa_%28disambiguation%29)       | 534.3935469409988  |
| [Sid_%28disambiguation%29](http://dbpedia.org/resource/Sid_%28disambiguation%29)           | 429.1328876877597  |
| [Obornjaca](http://dbpedia.org/resource/Obornjaca)                                         | 333.2843275163721  |
| [Bogaras](http://dbpedia.org/resource/Bogaras)                                             | 319.34832872672814 |
| [Blazov](http://dbpedia.org/resource/Blazov)                                               | 283.6398303443939  |



# Analysis of the different approaches

![cpu](https://github.com/user-attachments/assets/a8c7754b-80e8-49f7-95b4-2c17f77116b4)
![cpu2](https://github.com/user-attachments/assets/0cdb3665-d404-4657-81cd-6635efd3ff51)


| Approach                                                                                     | Time   |
|--------------------------------------------------------------------------------------------|--------------------|
|   rdd-partition-0w     | 52mins |
|  rdd-partition-2w      | 55mins
|  rdd-partition-4w      | 47mins |
|--------------------------------------------------------------------------------------------|--------------------|
|   rdd-no-partition-0w     | 45mins |
|   rdd-no-partition-2w     | 49mins |
|   rdd-no-partition-4w     | 30mins |
|--------------------------------------------------------------------------------------------|--------------------|
|   df-partition-0w     | 63mins |
|   df-partition-2w     | 57mins |
|   df-partition-4w     | 33mins |
|--------------------------------------------------------------------------------------------|--------------------|
|   df-no-partition-0w     | 58mins |
|  df-no-partition-2w      | 54mins |
|  df-no-partition-4w      | 45mins |


# Analyse Réseau et disque
### Comme on peut le voir ci-dessous, le partitionnement des données entraîne une utilisation accrue du réseau pour l'échange d'informations entre noeuds avec peu d'utilisation du disque. Tandis qu'en RDD et sans partition on a de grands échanges sur le disque
Réseau: 
![network](https://github.com/user-attachments/assets/e1d11e5e-eb1e-4d1b-a555-ab7199778573)
Disque: 
![disk](https://github.com/user-attachments/assets/19ece3d8-12e5-4078-aedf-e75fb842696e)




