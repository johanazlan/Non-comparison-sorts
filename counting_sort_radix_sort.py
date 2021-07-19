# Question 1 
# best_interval function

def best_interval(transactions, t):
    """ 
    Given an input list transactions and t where t is the length of the interval. best_interval will output a 2 element tuple
    (best_t, max_count) where best_t is the best start time for the interval and max_count is the number of elements in the 
    inteval which is in the transactions list. trans_sorted stores the sorted list after doing radix sort. 

    Complexity: O(nk) where n is the number of elements in the transactions and k is the greatest number 
                of digits in max_item.
    Auxiliary space: O(n) where n is the number of elements in transactions to create a count array of size n.

    """


    #Sort the transactions list that is given
    trans_sorted = sort_radix(transactions)

    i = 0 #Pointer for upper bound in an interval
    j = 0 #Pointer for lower bound in an interval
    count = 0
    max_count = 0
    best_t = 0
    
    #Loop through the sorted list
    for i in range(len(trans_sorted)): 

        # Check if the next element after i is within the interval length and to prevent index out of bounds. 
        # If yes the increment i until it reaches the upper bound of the interval.
        if i != (len(trans_sorted) - 1) and trans_sorted[i+1] <= (trans_sorted[j] + t): 
            i = i + 1

        # will only enter if i reaches the upper bound of an interval.
        else:
            count = (i+1) - j # get the count of elements between the interval inclusive of lower and upper bound.

            if count > max_count: # update max_count if there is a greater count 
                max_count = count 
                best_t = trans_sorted[i] - t # get best_t of the interval by taking the last element of the interval minus t

                if best_t < 0: #since best_t cant be negative, its minimum is 0
                    best_t = 0

            # increment lower bound to check new interval 
            j = j + 1

    return (best_t, max_count)


#  Max column for radix sort
import math

def sort_radix(new_list):
    """
    Given an input list transactions, find the maximum item of that list. Using the max_item, get the maximum number of columns 
    for the transactions list. Loop through each column, call the function sort_counting and do a counting sort on that column and 
    increment column.

    Complexity: O(nk) where n is the number of elements in the transactions to find the max_item and k is the greatest number 
                of digits in max_item.
    Auxiliary space: O(n) where n is the number of elements in transactions to create a count array of size n. 

    """

    #find max 
    #O(N) time
    if new_list == []: 
        return []

    else:
        max_item = new_list[0] #initialize max as first item
        for item in new_list:
            if item > max_item: #check if need to update max_item. 
                max_item = item


    #find max no. of columns
    #O(log k) time
    column = 0

    #This is to ensure that an input of 0 will still be able to be sorted. 
    if max_item == 0:
        column = 0
        sort_counting(new_list, column)

    else:
        #To get the maximum no. of columns to do counting sort. For each column, it will call sort_counting and perform 
        # a counting sort. Once every column is sorted, the list is sorted. 
        while column <= math.ceil(math.log(max_item,10)): #get no. of columns 
            sort_counting(new_list, column)
            column = column + 1
        
    return new_list 


# Counting sort

def sort_counting(new_list, column):
    """
    Given an unsorted list of non-negative integers and column, this function sorts the input list by column using counting sort
    to produce a sorted list. 

    Complexity: O(nk) where n is the number of elements in the transactions and k is the greatest number of digits
                in max_item in transactions
    Auxiliary space: O(n) where n is the number of elements in transactions. 

    """

    base = 10

    # find the maximum digit for a particular column. The first item is initialized as max_item and max_digit is initialized as 
    # as the maximum digit in a column. Loop through the elements in the list and update max_digit.
    max_item = new_list[0] #initialize max as first item
    max_digit = (max_item // (base ** column)) % base 
    for item in new_list:
        item_digit = (item // (base ** column)) % base 
        if item_digit > max_digit: #update max_digit 
            max_digit = item_digit


    # initialize count array with None's. Then at each position of None, initialize an empty list 
    count_array = [None] * (max_digit + 1) #(max item + 1) because start from 0
    for i in range(len(count_array)):
        count_array[i] = [] #At each position of count_array, initialize an empty list
    

    # update count array by looping through the input list. At each iteration, get the item digit of a column and append the item 
    # to the position of the digit into their buckets in the count array.
    for item in new_list:
        item_digit = (item // (base ** column)) % base 
        count_array[item_digit].append(item) #Append the item at position of its digit depending on the column
    

    # update input array once all items are in their buckets in the count array. Loop through the count array to obtain each
    # bucket. Then loop through each bucket and place the items into the input array.
    index = 0
    for i in range(len(count_array)): #Loop through count array
        bucket = count_array[i] #keep track of each bucket 
        for j in range(len(bucket)): #Loop through the bucket
            new_list[index] = bucket[j] #updating input array
            index = index + 1

    # new_list will be sorted  
    return new_list


#Question 2
# Anagrams

def words_with_anagrams(list1, list2):
    """
    This function takes input of 2 lists which are list1 and list2. This function is used to find all the words in the first list
    which have anagrams in the second list. The output of this function is a list of strings from list1 which have at least
    one anagram in list2.

    Complexity: O(L1M1 + L2M2) where L1 is the number of elements in list1 and L2 is the number of elements in list2. 
    Auziliary Space: O(N) where N is all the additional lists that are used. 
  
    """

    #tup1 and tup2 is a 2 element tuple. The first element contains the sorted list and the second element 
    # contains the count_array sorted in order of length and sorted by radix sort.
    tup1 = counting_sort_word(list1) #(sorted_alpha, count_array)
    sorted_alpha1 = tup1[0]
    count_array1 = tup1[1]

    tup2 = counting_sort_word(list2)
    sorted_alpha2 = tup2[0]


    # We want to compare the words in sorted_alpha1 and sorted_alpha2. Then if word in 
    # sorted_alpha1 == sorted_alpha2, take the index of the word in sorted_alpha1 and output count_array1[index]
    # into a new list.

    #Loop through sorted_alpha1
    i = 0
    j = 0
    k = 0
    output = []

    for i in range(len(sorted_alpha1)):

        if i > len(sorted_alpha1) - 1 or i > len(sorted_alpha2) - 1:
            break

        bucket1 = sorted_alpha1[i]
        bucket2 = sorted_alpha2[i]
        
    
        for j in range(len(bucket1)):
           
            #Checks if bucket1 and bucket2 are both not empty.
            #if empty, go to next bucket
            if len(bucket1) != 0 and len(bucket2) != 0:
                word1 = bucket1[j]
                word2 = bucket2[k]

                #elif len(bucket2) != 0: 
                if word1 == word2:
                    output.append(count_array1[i][j])
                    j = j + 1
                    if k < len(bucket2)-1:
                        k = k + 1

                    #bucket 2
                    #if the next word is the same as the current word, skip the next word
                    if k < len(bucket2) - 2 and bucket2[k+1] == word2: 
                        k = k + 2
                        
                    #bucket1
                    #if the next word is the same as the current word, add to output list 
                    # and skip that word
                    elif j < len(bucket1) - 2 and bucket1[j+1] == word1:
                        output.append(count_array1[i][j+1])
                        j = j + 2

                #if word1 is smaller than word2 then increment pointer j
                elif word1 < word2:
                    j = j + 1

                #if word1 is larger than word2 and word2 is not the last element then increment 
                # pointer k  
                elif word1 > word2 and k < len(bucket2) - 1:
                    k = k + 1

        k = 0
    
    return output
               


#  Counting Sort for alphabets

#sort the list by increasing length
def counting_sort_word(new_list):
    """
    This function is the first function that will be called from words_with_anagrams. This function takes input of the new_list
    which can be list1 or list2. This function starts by sorting the words from the new_list by increasing length. The output
    of sorting the words in increasing length will be a linked list where the words in each nested list are grouped by their
    length. The index of the nested lists represents the length of all the words grouped inside that nested list. 
    Once the words are grouped by their length in increasing order, sorted_alpha is created to ensure that the list containing
    the words that are grouped by their length stays untouched. Each word in each bucket of sorted_alpha is first sorted by 
    counting sort then each bucket of the same length does radix sort. To make sure that we remember the original word, 
    original_index, original_index2 and sorted_index are created. original_index is used to store the index of elements in the
    bucket before sorting with radix sort and also before sorting the words in alpabetical order. original_index2 is used to
    store the index of the words after sorting in alpabetical order. sorted_index is used to store the new index of the words 
    in the bucket after doing radix sort.  The output of this function is a 2 element tuple where the first element is the 
    count_array containing all the original words and sorted_alpha containing all the sorted words.

    Complexity: O(N + M) where N is the size of the input_list and all the additional lists created to store the index of the words.
                M is the number of characters in the longest word. 
    Auxiliary Space: O(n) where n is the size of original_index, original_index2, sorted_index

    """

    ### Sort the words by increasing length ###

    #initialize max_item and max_length
    max_item = new_list[0] #initalize first word as max_item 
    max_length = len(max_item) #initalize first word as item with max_length
    
    #Update the max_length
    for item in new_list:
        if len(item) > max_length: #update max_item if there is an item with greater length
            max_item = item
            max_length = len(item) #get the maximum length of the item
    #print(max_item)

    # initialize count array of size max length
    count_array = [None] * (max_length + 1) #(max item + 1) because start from 0. Use max_length to initialize size of count_array
    #print(count_array) 

    for i in range(len(count_array)):
        count_array[i] = [] #At each position of count_array, initialize an empty list
    #print(count_array)

    # update count array
    # This count_array contains the original word.
    for item in new_list:
        count_array[len(item)].append(item) #Use the item's length as an index for the item in count array since sorting by increasing length
    #print(count_array)


#Do counting sort for each word in each bucket by using count_array as reference but the output is stored in sorted_alpha.

    #initialize sorted_alpha to the size of the max length of an item and fill each position with empty list.
    sorted_alpha = [None] * (max_length + 1)
    for i in range(len(sorted_alpha)):
        sorted_alpha[i] = []

    #Do Radix Sort for each bucket that has an item
    for i in range(len(count_array)):
        bucket = count_array[i] #keep track of each bucket 

        if len(bucket) != 0: #Only do Radix sort if there are at least 2 elements in a bucket
        
            original_index = [] #a list to keep track of index of words in each bucket before changing the original word
            original_index2 = [] #a list to keep track of index of words after sorting alphabetically
            for j in range(len(bucket)): #loop through each bucket
                #counting_sort_sorted_alpha sorts the word at bucket[j] and stores the word in sorted_alpha. 
                counting_sort_sorted_alpha(bucket[j], sorted_alpha)
                tup = (bucket[j], j) #create a tuple for original_index to store the word and index together
                original_index.append(tup)
                tup2 = (sorted_alpha[i][j], j) #create a tuple for original_index2 to store the sorted word and index together
                original_index2.append(tup2)

            #Do radix sort for each bucket once all words in the bucket are sorted alphabetically.
            #returns the sorted bucket.
            sorted_alpha[i] = radix_sort_alpha(sorted_alpha[i], i) 

            #to change the position of the words in each bucket of count_array when there is a change in position of index 
            sorted_index = [] 
            for index in range(len(sorted_alpha[i])): #Loop through the bucket
                word = sorted_alpha[i][index] #get the word in bucket
                for k in range(len(original_index2)): #Loop through original_index2
                    if original_index2[k][1] not in sorted_index: #check if the index is already in sorted_order
                        if word == original_index2[k][0]: #compare if the word and the word of index k and tuple element 0 is the same or not
                            sorted_index.append(original_index2[k][1]) #Append the index of the word in sorted_order.
                            break

            index = 0
            i = 0
            for i in range (len(sorted_index)): #Loop through sorted_index
                bucket[index] = original_index[sorted_index[i]][0] #change element at bucket[index] to the word at index of sorted_index[i][0]
                index = index + 1
         
    return sorted_alpha, count_array
    
   


#  Find max no. of columns of longest word

#make sure break loop once there is no alphabet for that column for smaller words
#call radix sort

def radix_sort_alpha(new_list, word_length):
    """
    This function takes as input a new_list which is a bucket from sorted_alpha that the words wants to be sorted using 
    radix_sort. The second input is the word_length. word_length is the length of the words. word_length also indicates 
    which bucket were using to sort as the buckets are sorted according to length. The length of the buckets is the index.
    This function is used to get the number of columns by just taking the index of item in count_array. Then loop through 
    no. of columns from back to front. Lastly, call counting_sort_alpha for each column. The output of this function is the 
    bucket that is given in the input but in sorted order after sorting all the columns of the word. 

    Complexity: O(nk) where n is the number of words in the bucket and k is the number of columns that the words have. 
    Auxiliary Space: O(1) because all the operations in this function is done in-place and no extra storage is required.

    """

    #Get first column from the back and call radix sort. Then decrement column. Repeat
    column = -1 

    #if column is greater or equal to negative word length, do radix sort for that column and decrement column.
    #Exit loop when column equals to negative word length 
    while column >= - word_length: 
        counting_sort_alpha(new_list, column)
        column = column - 1
    
    return new_list


#  Radix sort to sort the characters of words with same length

#implementation of counting sort for 1 column
#sorting the word from left to right
def counting_sort_alpha(new_list, column):
    """
    This function takes an input new_list which is the bucket that wants to be sorted by radix sort. Another input is 
    the column. Column is the column of the word starting from the back of the word or column = - 1. This function does 
    a normal radix sort on the bucket that is passed to this function. The output of counting_sort_alpha is the same bucket 
    containing all the same words but the words are in sorted position according to which column is in the input.
    This method is stable. 

    Complexity: O(N+M) where N is the number of words in the bucket and M is the alphabets in the word and is the base. 
                M is used to build the count_array. 
    Auxiliary space: O(1) because all the operations in this function is done in-place and no extra storage is required.

    """

    base = 26

    #find max item and get the max_alpha in column
    max_item = new_list[0] #initialize max as first item
    max_alpha = ord(max_item[column]) - 97 #initialize last column as max alphabet

    for item in new_list:
        item_alpha = ord(item[column]) - 97 #get last column for item
        if item_alpha > max_alpha: #compare the last column to check which alphabet is bigger 
            max_alpha = item_alpha #update max_alpha to be the largest alphabet

    #initialize count array with None's. Then at each position of None, initialize an empty list 
    count_array = [None] * (base + 1) 
    for i in range(len(count_array)):
        count_array[i] = [] #At each position of count_array, initialize an empty list

    # update count array by looping through the input list
    for item in new_list:
        item_alpha = ord(item[column]) - 97 #get the alphabet of the column and change it to ascii form
        count_array[item_alpha].append(item) #We put in the word into position of the alphabet's ascii form.

    index = 0
    for i in range(len(count_array)):
        bucket = count_array[i] #Keep track of the bucket
        for j in range(len(bucket)): 
            new_list[index] = bucket[j] #updating input array
            index = index + 1
          
    return new_list



#  Counting sort alpha 

#Sort individual words to make the order of the word in alphabetical order.
def counting_sort_sorted_alpha(word, sorted_alpha):
    """
    This function takes as input word by word from each bucket and sorted_alpha which is a linked list which has the 
    same elements as the original input list. sorted_alpha is used for sorting the individual words in alphabetical
    order in this function. The approach to sort each word in alphabetical order is by doing counting sort. 
    The output for this function will be sorted_alpha containing the same words but are sorted in alphabetical 
    order.

    Complexity: O(N+M) where N is the length of the count array and M is the size of the word.
    Auxiliary Space: O(M) where M is the size of the word. 
   
    """


    base = 26

    # initialize count array with None's. Then at each position of None, initialize an empty list 
    count_array = [None] * (base + 1) 
    for i in range(len(count_array)):
        count_array[i] = []

    #update count array by looping through the length of the word
    for i in range(len(word)):
        item = ord(word[i]) - 97 #get the alphabet from the word starting at i = 0
        count_array[item].append(item) #Append the alphabet into the count array at index of the alphabet


    index = 0
    word_list = [] #create an empty list to store the alphabets of the word temporarily.
    for i in range(len(count_array)): #Loop through count_array

        #Check if the word_list is < than len(word). word_list will store the alphabets of the word. 
        # So the length should be the same if all alphabets of the word is in word_list
        if len(word_list) < len(word): 
            item = i
            bucket = count_array[i] 

            if len(bucket) != 0: #so we dont check for empty list
                #j is the index of the alphabet in the bucket. Loop through bucket to get the alphabet. 
                for j in range(len(bucket)): 
                    item = chr(bucket[j] + 97) #get the alphabet and store in item
                    word_list.append(item) #Append the alphabet to word_list.

        else:
            break 

    sorted_word = "".join(word_list) #join all the alphabets in word_list to become a sorted word. 
    index = len(sorted_word) #index of the sorted word is the same as its length
    sorted_alpha[index].append(sorted_word) #Append the sorted word at sorted_alpha[index]
    
    #return the sorted_alpha list.
    #sorted_alpha list will contain all the words in sorted order.
    return sorted_alpha


