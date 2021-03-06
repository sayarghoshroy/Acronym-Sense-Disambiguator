# Acronym Sense Disambiguator

## Identifies acronyms in a text file and disambiguates possible expansions

#### Illustration

##### Input

<p align="justify">
IBM is an American multinational information technology company headquartered in Armonk, New York, United States, with operations in over 170 countries.
</p>

<p align="justify">
IBM manufactures and markets computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is also a major research organization, holding the record for most patents generated by a business (as of 2018) for 25 consecutive years. Inventions by IBM include the automated teller machine, the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL programming language, the UPC barcode, and dynamic random-access memory. The IBM mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s...
</p>

##### System Output

<p align="justify">
IBM(International Business Machines) is an American multinational information technology company headquartered in Armonk, New York, United States, with operations in over 170 countries.
</p>

<p align="justify">
IBM(International Business Machines) manufactures and markets computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM(International Business Machines) is also a major research organization, holding the record for most patents generated by a business (as of 2018) for 25 consecutive years. Inventions by IBM(International Business Machines) include the automated teller machine, the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL(Structured Query Language) programming language, the UPC(Universal Product Code) barcode, and dynamic random-access memory. The IBM(International Business Machines) mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s...
</p>

#### To Run the Acronym Sense Disambiguator System on a Text File:

```bash
python3 main.py
```

> And enter the file name once the prompt appears

#### To Build the Searchable Index from a Raw Wikipedia Dump:

```bash
bash build.sh <path_to_dump> <path_to_index_directory>
```

- ##### A tested out and ready to use searchable index will be shared upon request. Save it in the directory with the source code.

- ##### The Acronym Server API can be found [here](http://acronyms.silmaril.ie/cgi-bin/xaa?).

---

### Introduction

<p align="justify">
Disambiguating acronyms is an important task in Computational Linguistics, occasionally used as a preprocessing step for further downstream tasks. Acronyms are often domain specific and have a high degree of polysemy, with an average of 9.7 possible expansions per acronym. Thus, expansion of acronyms in most situations requires disambiguation. In this project we use the context around the occurrence of an acronym and match it with known contexts for different expansions to estimate the intended full-form. Given some text, we get all possible expansions from an existing mapping function, and for each of the terms, we lookup associated wikipedia articles from an indexed dump to find the known context and then assign scores based on lexical matches. The accuracy of the system increases with larger text (about 100-200 words is sufficient for most cases), although accurate disambiguation has been achieved with just single lines of text.
</p>

### System in Detail

#### Searchable Wiki Index

<p align="justify">
The first step in building the system was creating a searchable index of the Wikipedia dump. The dump in itself is over 50 gigabytes in size and running queries on that would be infeasible. Hence, the indexer uses the porter stemmer to stem the lexical items in the titles of every available Wikipedia article and creates an easy to search-for directory structure. To search for a particular query, each word in the query is stemmed and compared against a document map which points to the particular directory in the created index where the required information can be found.
</p>

<p align="justify">
The indexed data creates a directory structure where each directory of the form n_ m, where n and m are integers between 0 and 26, holds the results for stemmed queries starting with the n-th followed by the m-th English alphabet. 0 represents a blank case. The index takes about 12 hours to build from the main dump and further queries can be run on the indexed dump itself with a lookup into the created document map. For each item in the index, we have the associated tf-idf score based on the number of articles the item appears in and its frequency of appearance in each article. Now, when we search for something in the dump. We can order our results based on these scores and select a specified number of results.
</p>

#### Identifying Acronyms

<p align="justify">
Let’s say, we want to process a particular text file. We require all the lexical items in the text file. For this, we tag each word using the averaged perceptron tagger available in the natural language toolkit. We disallow words having certain tags as they are simply functional. We also remove be-verbs and words falling in a predefined set of stop words. After this, the acronym finder module recognizes acronyms given in the text. We consider a capitalized sequence of alphabets as an acronym. Note that words such as “laser” which was once an acronym now exists in the English vocabulary as a common noun. Hence, these words are out of our scope. Also, note that in order to refine the definition of an acronym, only this particular module has to be modified and the entire system need not be affected. The module gives us a list of all acronyms recognized in the file. Now, suppose an acronym, say ACM, has appeared twice in the text file, we consider it only once. Hence, in one particular file, we make an implicit assumption that a particular acronym which has made multiple appearances shall map to the same expansion.
</p>

#### Acronym Expansion and Disambiguation

<p align="justify">
Now, we pass each acronym into our disambiguator subsystem. The subsystem is further divided into a set of modules. Firstly, one submodule sends a request to an API provided by ‘The Acronym Server’. The API provides us with an XML of the data which we parse using ‘etree’ available in the ‘xml’ package to extract the valid expansions of the acronym. Some error handling conditions such as checking for bracketed clauses and null values have been added here to make the system more robust and fault tolerant.
</p>

<p align="justify">
Thus, we have a list of possible expansions for an acronym and we focus on a particular one which is passed into the module for querying on the indexed dump. The expansion is broken up into word units and stemmed. This collection of units is searched for in the index. The list of descriptions of titles of all Wikipedia pages which contain this collection is returned sorted according to the tf-idf scores. Now, we process the returned list and consider only the lexical items. We stem each lexical item using the Snowball Stemmer available in the Natural Language Toolkit and convert it into a set of comparable units. The lexical items in the text file which is presented by the user are also stemmed in the same manner and a comparable word set is created. We define the confidence score of the expansion as the number of matches in these two sets i.e the cardinality of the set intersection. Note that, in order to modify the parameters for the confidence score, only this module needs to be modified. Hence, if you wish to try out some other heuristics, you can do so easily and the processing which happens following this step need not be altered at all. Clearly, we can calculate the confidence score for every expansion of a particular acronym and choose the one with the highest score. We define a mapping from an acronym to its selected expansion and create a new document in which we introduce the expansions for recognized acronyms and place them in brackets beside the corresponding abbreviations.
</p>

<p align="justify">
This document is made available to the user. The time taken by the system is directly proportional to the number of items whose confidence scores are to be found. We were able to speed up the process by loading the document map into the RAM just once instead of loading it before every query. The document map is about 260 megabytes in size and takes time to load into the RAM. Making this a one-time operation led to a huge increase in the speed of the system.
</p>

#### Future Modifications

<p align="justify">
In addition to trying out other heuristics for the confidence scores, one can consider entire Wikipedia articles for disambiguation as opposed to just the title descriptions. Note that this would be an extremely heavy operation and would require a lot of computing power. To increase the system speed, one can make all operations run in parallel using a pool of threads. We can disambiguate each acronym and compute confidence scores for each expansion in parallel.
</p>

<p align="justify">
The Acronym Server in itself can be made more robust. It mainly has acronyms for day to day conversation used in social media platforms and is primarily restricted to the USA. You may not get expansions for a particular political party in India or something which is very domain specific, say CL mapping to Computational Linguistics. The Acronym Server is evolving and one can help them out by submitting acronyms. Hence, in the near future, this system will have much more base data than it does today.
</p>

---
