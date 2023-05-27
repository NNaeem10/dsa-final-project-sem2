# DSA final project - sorting algorithm visualizer

For my final project, I made a sorting algorithm visualizer using the Pygame library. I referenced the YouTube video by TechWithTim (https://youtu.be/twRidO-_vqQ)

In his video, he designed the user interface and coded the bubble sort as well as the insertion sort. He made use of generators to create a temporary hault in the program so that the bars could be rendered in their appropriate locations. In addition to these algorithms, I have also coded the following:

* Selection sort
* Quicksort
* Merge sort
* Radix sort
* Heap sort
* Shell's sort

The following is the list of keys and actions they perform in the visualizer:
* R - generate random list
* SPACE - start sorting
* A - ascending order
* D - descending order
* I - insertion sort
* B - bubble sort
* S - selection sort
* M - merge sort
* Q - quick sort
* X - radix sort
* H - shell sort
* P - heap sort

These are all mentioned on the program window.

One limitation of this program is that it is quite memory-intensive (due to graphics being involved and the Pygame library being a very abstract library)

Using the tracemalloc library in Python, I found out that the program uses around 7 MB of memory at its peak

                                                References

Along with the YouTube video by TechWithTim (whose link I previously mentioned), these are the other sources I sought:

* Abdul Bari's YouTube channel
* www.programiz.com
* Data Structures and Algorithms in Python by Michael T. Goodrich


While there is no real world application of this project, I can say first-hand that it helped me enforce my knowledge of sorting algorithms as well as teaching me how to use the Pygame library. Also, this program mainly focused on the algorithm aspect of the course, only making use of 2 data structures, namely arrays and heaps.
