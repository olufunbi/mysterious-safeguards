#!/usr/bin/python3

# You need to install bitarray library first by using
# !pip install bitarray
import sys
from bitarray import bitarray

# 0 : t0 - t1, 1 : t1 - t2, so on...
guard_avail_t = 1000000000 * bitarray('0')
redundant_avail_t = 1000000000 * bitarray('0')

def prepare_data(lines):

    global redundant_avail_t
    global guard_avail_t
    temp_buf = 1000000000 * bitarray('0')
    count = 1
    
    for line in lines:
        t_slot = line.strip().split(' ')
        start = int(t_slot[0])
        end = int(t_slot[1])
   
        #print ("start %d end %d" %(start, end))
        # Mark availability
        temp_buf[:] = 0
        temp_buf[start:end] = 1

        # check duplicate and maintain redundant time slots
        redundant_avail_t = redundant_avail_t | (guard_avail_t & temp_buf)

        # Update cumulative guard available slots
        guard_avail_t = guard_avail_t | temp_buf

        #print("guard num %d" %count)
        count += 1



def func(lines):
    global redundant_avail_t
    global guard_avail_t
    min_impact = sys.maxsize
    min_imp_guard_id = 0
    guard_id = 0

    for line in lines:
        t_slot = line.strip().split(' ')
        start = int(t_slot[0])
        end = int(t_slot[1])
        impact = 0 
        # check for impact if removed
        impact = redundant_avail_t[start:end].count(0)

        if impact < min_impact:
            min_impact = impact
            min_imp_guard_id = guard_id

        guard_id += 1

    print ("\nLifeguard number %d could be removed with less impact on coverage" %(min_imp_guard_id+1))

    # remove min impact guard id time coverage
    t_slot = lines[min_imp_guard_id].strip().split(' ')
    start = int(t_slot[0])
    end = int(t_slot[1])

    guard_avail_t[start:end] = guard_avail_t[start:end] & redundant_avail_t[start:end]

    # calculate time coverage after firing min impactful lifeguard
    return guard_avail_t.count(1)


def main():
    # main driver function
    # replace path below with path to each of your input files
    with open('path_to_input_file') as my_file:
        lines = my_file.readlines()

    guard_count = lines[0]
    lines.pop(0)

    # process realtime input and prepare compute easy data
    prepare_data(lines)

    # identify the guard with least impact on time coverage on firing.
    result = func(lines)
    print ("Maximum time coverage after removing one lifeguard : %d\n" % result)

    # replace the integer 10 below with the appropriate value
    f = open("10.out", "a")
    f.write(str(result))
    f.close()


if __name__ == "__main__":
    main()
