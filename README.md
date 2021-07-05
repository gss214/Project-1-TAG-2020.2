# Project-1-TAG-2020.2

## Development Information

Project 1 of the theory and application of graphs course at UnB in 2020.2

University of Brasilia, Institute of Exact Sciences,  Computer Science Department

Theory and Application of Graphs - 2020.2

Developed by: Guilherme Silva Souza

Language used: Python

## Description

In 2003, in the article "David Lusseau et al., The bottelenosis dolphin community of Doubful Sound features a large proportion of long-lasting associations, Journal of Behavioral Ecology and Sociobiology 54:4, 396-405 (2003)." a social network of lasting relationships is identified in a community of 62 dolphins and presented as an (undirected) graph for studies. Data are in attached file (soc-dolphins.zip). The project consists of writing a program in which it reads the file (soc-dolphins.mtx, or txt), assembles with this data an undirected, weightless graph, using adjacency lists, and then performs the following:

- It implements two forms of the Bron-Kerbosch algorithm: one with pivoting, the other without pivoting;
- Finds and prints on screen (twice, once for each Bron-Kerbosch implementation) all maximal clicks (indicating the number of vertices and which ones);
- The average agglomeration coefficient of the graph.