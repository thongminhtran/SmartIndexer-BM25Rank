# README for COMP 479/6791 Project 3: Advanced Indexing and Ranking System

## Overview
This project, for COMP 479/6791 Fall 2022, aims to refine your indexing procedure, implement ranking for search returns, and analyze the impact of your design decisions on the system's results.

## Objectives
- Enhance the indexing process from previous projects.
- Implement document ranking using the BM25 formula.
- Conduct tests and analyze outcomes based on design decisions.

## Due Date
**7th November 2021**

## Data
- **Dataset:** Utilize the Reuters21578 collection for testing purposes. Continue improving your text preprocessing skills, although this should be a secondary focus for this project.

## Description
The project is divided into two subprojects, each building upon the other:

### Subproject I: Indexing System Upgrade
- **Objective:** Improve the indexing module from Project 2 to append `docID` directly to the postings list for a term using a hash table.
- **Tasks:**
  1. Compare the timing of this SPIMI-inspired procedure with the naive indexer for 10,000 term-docID pairings.
  2. Compile an inverted index for Reuters21578 without compression techniques, using NEWID values for `docID`.

### Subproject II: Probabilistic Search Engine
- **Objective:** Transform your indexer into a search engine that ranks documents based on the BM25 formula, considering assumptions about term and document independence.
- **Tasks:**
  1. Rank documents your index returns.
  2. Return a ranked list of results for a given query.

### Test Queries
Design four test queries to demonstrate your system:
  1. A single keyword query.
  2. A query with several keywords for BM25.
  3. A multiple keyword query with AND logic.
  4. A multiple keyword query with OR logic.

## Deliverables
1. **Individual Project Submission**
2. **Code:** Well-documented source code.
3. **Sample Runs:** Documented sample runs for specified information needs:
   - Democrats' welfare and healthcare reform policies
   - Drug company bankruptcies
   - George Bush
4. **Additional Materials:** Any testing or aborted design ideas showcasing your project.
5. **Project Report:** A comprehensive report summarizing your approach, design, and learnings. Include an analysis of sample run results.
