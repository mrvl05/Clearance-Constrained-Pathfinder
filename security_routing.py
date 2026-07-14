# Name: Marvel Jefferson Luke
# Student Number: 24722784

'''Here I still implement the same structure as the provided implementation (which is still incomplete), but I still use the same imports
   as we still need them for this implementation to reach the target complexity. We use the Python modules of enum and heapq, where the enum is to help
   create integer representation of the clearance options, and the heapq to be the heap priority queue that keeps the smallest time to be the priority, as we need
   the smallest time possible, so when it is popped, it is already the smallest time.'''
from enum import IntEnum
from heapq import heappush, heappop

'''The class Clearance is used to initialize the clearance option representation so that we can easily compare them in most of our code, and also to store them and retrieve them 
   like as an index, where we mostly use list data structure. The NONE is assign to 0 (NONE means that there is no clearance needed), RED is 1, BLUE is 2, GREEN is 3.'''
class Clearance(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2
    GREEN = 3

'''This security_route() function is used to find the smallest time needed from a source station to the target station with a specific clearance that is needed, where
   different clearance at the same station can lead to different optimal paths that is available. Thus, the provided implementation is still missing the clearance as part
   of the decision making for determining the shortest path, where in this implementation, I also use clearance as part of the decision making process to find the shortest path. 
   Moreover, this implementation mainly uses the Dijkstra's algorithm to find the shortest path (here in this case is the shortest amount of time from source station
   to the target station). As explained before, we need to keep track of the latest shortest time of from the segments to the target station, as for example in a particular segment with clearance BLUE,
   it means that we require the BLUE clearance to get through that segment (in here we can visualize the segment as like edges in graphs), therefore we need the BLUE clearance in hand before we can proceed through that segment. Thus, if we currently 
   do not have the BLUE clearance in hand, then we need to go to a station where we can change our clearance to BLUE, then proceed. Furthermore, as all the time given is not negative value and changing the clearance
   at certain stations do not need extra cost, then this Dijkstra's algorithm will accurately give the shortest path (time) as needed by the problem. Other than that, we also use priority queue heap
   to keep the smallest time at priority to be popped first, meaning the smallest time will always be processed first, thus giving shortest amount of total time. The detail of the code is as below.'''
def security_route(stations, segments, source, target):

    # Initializing the value 4 to the clearance option, because we have 4 types of clearance, which are none, red, blue, green
    clearance_options = 4

    # Assigning the length of the station list, which is from the argument given of this function
    # We will use this quite often in the later code, as it acts like the N of operations that we need to iterate through to process each station correctly
    station_length = len(stations)

    # Creating a list to store the edges / segments available from a particular station with particular clearance.
    # Here it functions like the adjacency list (which is also covered in the lecture), where the vertex (here like the station and clearance) has the incident edges / segments
    adjacency_lst = []

    # Making for loop to iterate through each station, using the index
    # Note that this operation might seem to be O(n^2) with the nested for loop, but this is actually O(n), as the outer loop is n, and inner loop is 4, so 4n, thus O(n)
    # Initializing with creating all empty lists to later be filled over time
    for x in range(station_length):
        # Creating a list to contain the color clearances
        lst_color_clearance = []
        # Making inner for loop to iterate through clearance options (4), and append empty list to the created list inside the outer loop
        for y in range(clearance_options):
            lst_color_clearance.append([])
        # Appending the inner list to the adjacency list created before, so everything is still empty
        adjacency_lst.append(lst_color_clearance)

    # Creating a for loop to iterate through the given argument segments and assigning each index to the respective variables as below
    # This is done to make the retrieval easier with the already separated variables
    # Note again that this operation might seem to be O(n^2) with the nested for loop, but this is actually O(n), as the outer loop is n, and inner loop is 4, so 4n, thus O(n)
    for each_entry in segments:
        # Separating each index of each entry into separated variables
        start_station = each_entry[0]
        finish_station = each_entry[1]
        time = each_entry[2]
        clearance_needed = each_entry[3]

        # Making an inner for loop to iterate through the clearance options
        for color in range(clearance_options):
            # If at that particular segment the clearance required is NONE or the same with the currently iterated clearance, then append that (time, station, color) tuple to the adjacency list with the start station and the color
            # This means that the segment is available to be used from that particular station with particular clearance
            if clearance_needed == Clearance.NONE or clearance_needed == color:
                adjacency_lst[start_station][color].append((time, finish_station, color))

    # Making the infinity value to be used, as we assume that the shortest time is still infinity, and later will be updated over time if the time is smaller
    # This is according to the research I have done on how to make infinity value
    infinity = float("inf")

    # Creating list that contains all the time needed to get to the particular station with particular clearance
    time_lst = []

    # Making for loop to iterate through the stations, and create a list for each station
    # Note again that the time complexity of this operation is O(n)
    # This is to initialize the list for the time
    for x in range(station_length):
        each_stn = []
        # Using inner for loop and append infinity value (4 times) to the each station list
        for y in range(clearance_options):
            each_stn.append(infinity)
        # Appending the infinity values to the main time list
        time_lst.append(each_stn)

    # Making a list for the heap priority queue, that we use to keep the smallest time processed first, thus ensuring shortest path (time) is given
    heap_pq_lst = []

    # Checking if at the source station the clearance is NONE or not, where if not (reprogram of clearance available at that station) then that means we have the option to keep NONE clearance or change to the particular clearance
    # If it is NONE, then that means we cannot change to any colored clearance, so still be NONE clearance
    if stations[source] != Clearance.NONE:
        # Creating a list that consist of our option to keep or not
        player_option_start = [Clearance.NONE, int(stations[source])]
        # Iterate through the options
        for color in player_option_start:
            # Checking if the clearance of source station is infinity, then we change the time to be 0, because this is the source, then push that into the heap pq
            if time_lst[source][color] == infinity:
                time_lst[source][color] = 0
                # Pushing the (time, station, clearance) tuple to the heap priority queue list
                heappush(heap_pq_lst, (0, source, color))
    else:
        # Cannot change clearance, so just change the time to be 0
        time_lst[source][Clearance.NONE] = 0
        # Pushing the tuple to the heap priority queue list
        heappush(heap_pq_lst, (0, source, Clearance.NONE))

    # Creating a while loop to iterate indefinitely until the heap priority queue list is empty (which is empty when all paths have been popped out)
    # If after the queue list is empty and there has not been found matching station of path to the target, that means the target cannot be reached, so return None
    while heap_pq_lst:
        # Pop the priority path and assign that to a variable
        popped_and_checked = heappop(heap_pq_lst)
        # Separate the tuple data of that currently worked on path into separate variables to make comparison easier
        time_now = popped_and_checked[0]
        station_now = popped_and_checked[1]
        clearance_now = popped_and_checked[2]
        # Checking if the currently worked on station is same as the target, if so then return the current time, as that is the smallest total time to get to the target station
        if station_now == target:
            return time_now
        # Checking if the currently processed time is less than the latest / updated smallest time, if so then continue the rest of code, because that means this currently processed path is slower than the latest known smallest time, so just ignore that
        if time_now > time_lst[station_now][clearance_now]:
            continue
        # Update the clearance with the current station
        clearance_updated = int(stations[station_now])
        # Checking if the updated clearance is not NONE and not the current clearance, that means that station can change clearance and is not the same with the current clearance
        if clearance_updated != Clearance.NONE and clearance_updated != clearance_now:
            # Checking if this is a faster path, by comparing that the current time is less than the updated clearance time
            if time_now < time_lst[station_now][clearance_updated]:
                # If so, then make that time to be the updated time for the updated clearance
                time_lst[station_now][clearance_updated] = time_now
                # Pushing that updated data to the heap priority queue list
                heappush(heap_pq_lst, (time_now, station_now, clearance_updated))
        # Making for loop to iterate through the adjacency list with the currently processed station and clearance
        for each_segment in adjacency_lst[station_now][clearance_now]:
            # Separating the tuple data from each segment into variables
            time_needed_at_one_segment = each_segment[0]
            station_after = each_segment[1]
            clearance_after = each_segment[2]
            # Incrementing the total time to be the currently processed time added with the time at that particular segment leading to the target
            total_time = time_now + time_needed_at_one_segment
            # Checking if the total time is less than the currently processed segment time
            if total_time < time_lst[station_after][clearance_after]:
                # If so, then that means we need to put that total time as the latest time for that segment, because this is the way to get the smallest total time to the target
                time_lst[station_after][clearance_after] = total_time
                # Pushing that tuple data again to the heap priority queue list
                heappush(heap_pq_lst, (total_time, station_after, clearance_after))

    # After exiting the while loop, that means there is no matched station with target, so that means the target station cannot be reached, thus returning None
    return None